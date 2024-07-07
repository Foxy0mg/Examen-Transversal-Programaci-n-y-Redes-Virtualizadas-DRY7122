import requests
import urllib.parse

def geocoding(location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    print(f"Geocoding API URL for {location}:\n{url}")
    if json_status == 200 and json_data["hits"]:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
    else:
        lat = "null"
        lng = "null"
        print(f"Error geocoding {location}: {json_data}")
    return json_status, lat, lng

def routing(orig_coords, dest_coords, vehicle, key):
    route_url = "https://graphhopper.com/api/1/route?"
    params = {
        "point": [f"{orig_coords[0]},{orig_coords[1]}", f"{dest_coords[0]},{dest_coords[1]}"],
        "vehicle": vehicle,
        "key": key
    }
    url = route_url + urllib.parse.urlencode(params, doseq=True)
    print(f"Routing API URL:\n{url}")
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    if json_status == 200:
        distance = json_data["paths"][0]["distance"] / 1000  # distance in km
        time = json_data["paths"][0]["time"] / 1000 / 60  # time in minutes
        return json_status, distance, time, json_data["paths"][0]["instructions"]
    else:
        print(f"Error calculating route: {json_data}")
        return json_status, "null", "null", []

def display_instructions(instructions):
    for step in instructions:
        print(step['text'], f"({step['distance'] / 1000:.1f} km / {step['time'] / 1000 / 60:.1f} min)")

def main():
    key = "ff23744f-9541-4fe5-8957-b4d50f039c0b"
    vehicle = "car"  
    orig = "Los Andes, Chile"
    dest = "Mendoza, Argentina"
    
    orig_status, orig_lat, orig_lng = geocoding(orig, key)
    dest_status, dest_lat, dest_lng = geocoding(dest, key)
    
    if orig_status == 200 and dest_status == 200:
        print(f"Origin coordinates: {orig_lat}, {orig_lng}")
        print(f"Destination coordinates: {dest_lat}, {dest_lng}")
        route_status, distance, time, instructions = routing((orig_lat, orig_lng), (dest_lat, dest_lng), vehicle, key)
        if route_status == 200:
            print(f"\nDistancia: {distance:.1f} km / {distance * 0.621371:.1f} millas")
            print(f"Duración: {time:.1f} minutos / {time / 60:.1f} horas\n")
            display_instructions(instructions)
        else:
            print("Error al calcular la ruta.")
    else:
        print("Error al obtener las coordenadas de origen o destino.")

if __name__ == "__main__":
    main()
