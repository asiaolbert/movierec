
[
  {
    "model": "movierec.rating",
    "pk": 1,
    "fields": {
      "userId": "1",
      "movieId": "1",
      "rating": "4.0",
      "timestamp": "964982703"
    }
  }
]


import csv
import json
import datetime


file_name = 'dane/ratings.csv' # change to the csv file name that you are trying to upload
with open(file_name) as csvfile:
    csvfile = csv.DictReader(csvfile)
    app_name = 'movierec' # change this to your Django app name
    model_name = 'rating' # the name of you Django model
    field_1 = 'userId' # the name of first field
    field_2 = 'movieId' # the name of second field
    field_3 = 'rating'
    field_4 = 'timestamp'
    x = 0
    output = []
    for each in csvfile:
        x += 1
        timestamp = datetime.datetime.fromtimestamp(float(each[field_4])).strftime("%Y-%m-%d %H:%M")
        row = {}
        row = {'model': app_name+'.'+model_name, 'pk': x, 'fields': ({field_1: each[field_1], field_2: each[field_2],field_3: each[field_3],field_4: timestamp})}
        output.append(row)
    json.dump(output, open('fixture.json','w'), indent=4, sort_keys=False)

