import requests
from utils.config import api_key, current_latitude, current_longitude

def findNearesRestArea():
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={current_latitude},{current_longitude}"
        "&radius=50000"
        "&type=cafe|gas_station|restaurant|rest_area"
        f"&key={api_key}"
    )

    repsonse = requests.get(url)

    if repsonse.status_code == 200:
        data = repsonse.json()
        if data['results']:
            places = data['results'][:5]
            print(type(places))
            return [{
                'name': place['name'],
                'lat': place['geometry']['location']['lat'],
                'lng': place['geometry']['location']['lng'],
                'maps_link': f"https://www.google.com/maps/dir/?api=1&origin={current_latitude},{current_longitude}&destination={place['geometry']['location']['lat']},{place['geometry']['location']['lng']}"
            } for place in places]
    
    return []