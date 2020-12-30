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

with open('OSMCitydata.txt', 'w') as outfile:
    json.dump(OSMdata, outfile)


overpass_query1 = """
    [out:json];
    area(3600068841) -> .a;
    
    (
    node["amenity"="place_of_worship"](area.a);
    way["amenity"="place_of_worship"](area.a);
    );
    
    out;
"""

OSMdata1 = requests.get(overpass_url, params={'data': overpass_query1}).json()

with open('OSMReligiousInstitdata.txt', 'w') as outfile:
    json.dump(OSMdata1, outfile)