import os
from kncloudevents import CloudeventsServer
import logging
import sys

logging.basicConfig(stream= sys.stdout, level=logging.INFO)


def run_event(event):
    try:
        os.chdir("../app")
        f = open("events.txt","a+")
        logging.info(" Writing to the file")
        f.write(event.Data())
        f.write("\n")
        f.close() 
        logging.info(event.Data())
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

print("Logs of Knative events")
client = CloudeventsServer()
client.start_receiver(run_event)
