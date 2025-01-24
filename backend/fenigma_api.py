import time
start_time = time.time()

import geopy
from geopy.geocoders import Nominatim
from geopy import distance
from geopy.distance import geodesic
import pandas as pd
import numpy as np


def location_to_latlon(location):
    """
    Converts a location (either a tuple or geopy Location object) into a latitude and longitude pair.

    Args:
        location (tuple or geopy.location.Location): A location object or tuple (latitude, longitude).

    Returns:
        tuple: A tuple containing latitude and longitude.
    """
    if isinstance(location, geopy.location.Location):
        return location.latitude, location.longitude
    return location[0], location[1]


def get_google_maps_link(location1, location2=None, append=False):
    """
    Generates a Google Maps link between two locations.

    Args:
        location1 (tuple or geopy.location.Location): The first location (latitude, longitude).
        location2 (tuple or geopy.location.Location, optional): The second location (latitude, longitude). Defaults to None.
        append (bool, optional): Whether to append the first location to an existing URL. Defaults to False.

    Returns:
        str: A Google Maps direction URL.
    """
    base_url = "https://www.google.com/maps/dir"
    lat1, lon1 = location_to_latlon(location1)

    if not append:
        lat2, lon2 = location_to_latlon(location2)

    if append:
        return f"{append}/{lat1},{lon1}"

    return f"{base_url}/{lat1},{lon1}/{lat2},{lon2}"


def calculate_distance(location1, location2):
    """
    Calculates the distance in miles between two geopy Location objects.

    Args:
        location1 (geopy.location.Location): The first location.
        location2 (geopy.location.Location): The second location.

    Returns:
        float: The distance between the two locations in miles.
    """
    lat1, lon1 = location1.latitude, location1.longitude
    lat2, lon2 = location2.latitude, location2.longitude
    return distance.distance((lat1, lon1), (lat2, lon2)).miles


def get_step(val1, val2, num_steps):
    """
    Calculates the step value between two coordinates to generate intermediate points.

    Args:
        val1 (float): The starting value (latitude or longitude).
        val2 (float): The ending value (latitude or longitude).
        num_steps (int): The number of steps to generate.

    Returns:
        float: The step value to increment or decrement.
    """
    step = abs(val1 - val2) / num_steps
    if val1 > val2:
        step = 0 - step
    return step


def get_pointsmap(location1, location2, num_steps, generate_link=True):
    """
    Generates intermediate points between two locations.

    Args:
        location1 (tuple or geopy.location.Location): The first location (latitude, longitude).
        location2 (tuple or geopy.location.Location): The second location (latitude, longitude).
        num_steps (int): The number of intermediate points to generate.
        generate_link (bool, optional): Whether to generate Google Maps links. Defaults to True.

    Returns:
        list: A list of intermediate locations or Google Maps links.
    """
    lat1, lon1 = location_to_latlon(location1)
    lat2, lon2 = location_to_latlon(location2)

    lat_step = get_step(lat1, lat2, num_steps)
    lon_step = get_step(lon1, lon2, num_steps)

    first = True
    points = []

    for i in range(num_steps):
        if first:
            next_lat = lat1 + lat_step
            next_lon = lon1 + lon_step
            if generate_link:
                points = get_google_maps_link(location1, (next_lat, next_lon))
            else:
                points.append((lat1, lon1))
            points.append((next_lat, next_lon))
            first = False
        else:
            next_lat = next_lat + lat_step
            next_lon = next_lon + lon_step
            if generate_link:
                points = get_google_maps_link((next_lat, next_lon), append=points)
            else:
                points.append((next_lat, next_lon))

    return points


def preprocess_csv(csv_file):
    """
    Preprocesses a CSV file containing geolocation data by counting the occurrences of countries.

    Args:
        csv_file (str): Path to the CSV file.

    Returns:
        int: Returns 0 upon successful completion.
    """
    # df = pd.read_csv(csv_file)
    # country_counts = df['country'].value_counts()

    # df = df.dropna(subset=['lat', 'lon'])
    # df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    # df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
    # df = df.dropna(subset=['lat', 'lon'])
    # print(df.head(5))
    # df = df[df['thing_type'] != "Food"]
    # df = df[df['country'] == "United States"]
    # 
    # # df.to_csv('new_atlas.csv', index=False)
    # for country, count in country_counts.items():
    #     print(f"{country}: {count}")

    return 0


def find_destinations_within_radius(csv_file, origin_lat, origin_lon, radius_miles):
    """
    Finds destinations within a specified radius of an origin point.

    Args:
        csv_file (str): Path to the CSV file containing destinations.
        origin_lat (float): Latitude of the origin point.
        origin_lon (float): Longitude of the origin point.
        radius_miles (float): Radius in miles around the origin to search for destinations.

    Returns:
        pandas.DataFrame: DataFrame containing destinations within the radius.
    """
    start_time = time.time()
    df = pd.read_csv(csv_file)


    # Calculate distances
    df['distance_miles'] = df.apply(lambda row:
                                    geodesic((origin_lat, origin_lon), (row['lat'], row['lon'])).miles,
                                    axis=1)

    run_time = time.time() - start_time
    print(f"run time was {run_time:.3f} seconds")

    # Filter destinations within the radius
    destinations_within_radius = df[df['distance_miles'] <= radius_miles]

    print(destinations_within_radius.head(5))

    return destinations_within_radius


csv_file = 'new_atlas.csv'

# load our geolocation
geolocator = Nominatim(user_agent="fenigma")

orlando = geolocator.geocode("Orlando")
miami = geolocator.geocode("Sarasota")

# # print(get_google_maps_link(orlando, miami))

def get_destinations(point1, point2):
    pointsmap = get_pointsmap(point1, point2, 10, generate_link=False)

    print(pointsmap)

    frames = []

    for point in pointsmap[2:-2]:
        frames.append(find_destinations_within_radius('new_atlas.csv', point[0], point[1], 25))

    df = pd.concat(frames)
    df.drop_duplicates(subset='id', inplace=True)

    dataframe_json = df.to_json(orient="records")

    print(dataframe_json)
    
    return dataframe_json



# print(f"final runtime is {time.time() - start_time:.3f} seconds")
