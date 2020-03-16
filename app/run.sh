#!/bin/sh

python app/reciever.py &

while :
do
	python app/analytics.py 
    sleep 10
done




