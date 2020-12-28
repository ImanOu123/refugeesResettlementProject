import json
import requests

# get OSM data from OSM API

overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
        [out:json];
        area(3600068841) -> .a;
        (
            node["place"="city"](area.a);
            node["place"="neighbourhood"](area.a);
        );
        out;

        """
OSMdata = requests.get(overpass_url, params={'data': overpass_query}).json()

# print(OSMdata)

with open('OSMdata.txt', 'w') as outfile:
    json.dump(OSMdata, outfile)