
# Analytics with Kafka and Knative

## Prerequisites
1. Access to openshift cluster
2. Knative installed on openshift (https://docs.openshift.com/container-platform/4.1/serverless/getting-started-knative-services.html)
3. Knative serving installed (https://redhat-developer-demos.github.io/knative-tutorial/knative-tutorial-serving/index.html)
4. Knative eventing installed (https://redhat-developer-demos.github.io/knative-tutorial/knative-tutorial-eventing/index.html)


Create a new project in openshift

```
oc new-project kafka-analytics
```

To deploy Apache kafka inside our Knative cluster we use this command

```
oc apply -f https://github.com/strimzi/strimzi-kafka-operator/releases/download/0.16.2/strimzi-cluster-operator-0.16.2.yaml -n kafka-analytics
```
Now that the strimzi operator is running, we spin up our Kafka cluster with one node with the entity operator and zookeeper. 
```
oc apply -f https://raw.githubusercontent.com/strimzi/strimzi-kafka-operator/0.16.2/examples/kafka/kafka-persistent-single.yaml -n kafka-analytics
```
You can check the deployment using 
```
oc get pods -n kafka
```
You can see 3 new pods, Kafka broker, Zookeepr and Entity operator

Deploy kafka-source.yaml to apply the Strimzi install files, including ClusterRoles, ClusterRoleBindings and some Custom Resource Definitions (CRDs).
```
oc apply -f kafka-source.yaml
```
Before deploying the http bridge lets first create a eventing deployment (Knative Service) which will spin up when we get data into our Kafka cluster. 

```
oc apply -f eventing-hello-sink.yaml 
```
(In this I have used my own image which runs a script to run 2 python programs. One collects data using the reciever.py file and saves data into events.txt file. Another uses the data from events.txt to predict the next output by using Simple Liner regression. Feel free to change the contents of the analytics.py file if you want to use any other model.)

Now we have to connect our Kafka cluster to the Knative service which we deployed. for this,  we deploy a Kafka-event-source which acts as a connector between the cluster (source) and the Knative service (sink). 
```
oc apply -f kakfa-event-source.yaml
```

To apply the bridge use this, (assuming you havent changed the cluster name, else change the bootstrapserver under spec accordingly)
```
oc apply -f examples/kafka-bridge/kafka-bridge.yaml
```
You will need an Ingress resource to route the external traffic based on rules mentioned in the resource. For this, Ingress controller needs to be working. 
```
oc apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.30.0/deploy/static/provider/cloud-generic.yaml
```
This will create a Ingree controller, now we can add the resource. 
```
oc apply -f ingress-bridge.yaml
```
The Strimzi Kafka Bridge is reachable through the my-bridge.io host, so you can interact with it using different HTTP methods at the address http://my-bridge.io:80/<endpoint> where <endpoint> is one of the REST endpoints exposed by the bridge for sending and receiving messages, subscribing to topics and so on.
 
To check whether the endpoint is working properly from terminal
```bash
curl -v GET http://my-bridge.io/healthy
```
You can see an output like this
```
> GET /healthy HTTP/1.1
> Host: my-bridge.io:80
> User-Agent: curl/7.61.1
> Accept: */*
> 
< HTTP/1.1 200 OK
< content-length: 0
```

Now that we know we can connect to our HTTP endpoint. Lets send in some dummy data

For this run sender.py from your local machine. 

```
python sender.py
```
This program sends random integer data to our kafka bridge http endpoint http://my-bridge.io/topics/my-topic every second. This auto generates a new topic *my-topic*. This will trigger a deployment of the eventing pod (which you can see on the openshift console). 

If you go to the logs of the eventing pod which was recently generated, you can see the data coming in as you are sending it. 


