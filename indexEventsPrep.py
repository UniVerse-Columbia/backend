#Covnert events into a format that can be used for elsatic Indexing

{"index": {"_index": "restaurant", "_id": 1}}
{"RestaurantID": "_7BGw3YFNOTzP1Www3zB7g", "Cuisine": "Indian"}


import pandas as pd
import numpy as np
import json

df = pd.read_csv("shortlisted_events.csv")
base = {"index": {"_index": "events","_id": 1}}

with open("IndexedEvents.json",'a') as f:

    for index,row in df.iterrows():
        base["index"]["_id"] = row["id"]
        json.dump(base,f)

        f.write('\n')

        eventObj = {}

        eventObj["id"] = str(row["id"])
        eventObj["title"] = str(row["title"])
        eventObj["description"] = str(row["description"])
        eventObj["organizerId"] = str(row["organizerId"])
        eventObj["location"] = str(row["address"])
        eventObj["timestamp"] = str(row["timestamp"])
        eventObj["tags"] = []
        eventObj["attendee"] = []

        tagValues =  "".join(row["tags"])

        for tag in tagValues.split(";"):

            eventObj["tags"].append({"tagName":tag})
                
        json.dump(eventObj,f)

        f.write('\n')




    
