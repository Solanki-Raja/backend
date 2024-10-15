import requests

def get_location_coordinates(place_name):
    API_KEY = 'AIzaSyCISgKMgd9AYAhgD-1EfO5cn069Rrh5gTg'
    base_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place_name}&key={API_KEY}"
    
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        if len(data['results']) > 0:
            location = data['results'][0]['geometry']['location']
            lat = location['lat']
            lng = location['lng']
            return lat, lng
        else:
            return None, None
    else:
        return None, None
