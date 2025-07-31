import datetime
import os

import dotenv
import googlemaps


class GMAPS:
    def __init__(self, api_key=None):
        self.enabled = False
        if api_key is None:
            dotenv.load_dotenv()
            api_key = os.getenv("GOOGLE_MAPS_API_KEY")
            self.enabled = bool(api_key)
        else:
            self.enabled = True
        if self.enabled:
            self.gmaps = googlemaps.Client(key=api_key)

    def get_directions(self, origin, destination, mode="walking"):
        directions_result = self.gmaps.directions(
            origin,
            destination,
            mode=mode,
        )
        instructions = []
        for leg in directions_result[0]["legs"]:
            for step in leg["steps"]:
                instructions.append(step["html_instructions"])
        ## get the distance and duration for all legs
        total_distance = sum(
            leg["distance"]["value"] for leg in directions_result[0]["legs"]
        )
        total_duration = sum(
            leg["duration"]["value"] for leg in directions_result[0]["legs"]
        )
        return {
            "instructions": instructions,
            "total_distance_meters": total_distance,
            "total_duration_seconds": total_duration,
        }

    def get_distance(self, origin, destination):
        # Call Google Maps API to get distance
        pass

    def get_nearby_places(self, location, radius):
        # Call Google Maps API to get nearby places
        pass

    def example(self):
        # Geocoding an address
        geocode_result = self.gmaps.geocode(
            "1600 Amphitheatre Parkway, Mountain View, CA"
        )

        # Look up an address with reverse geocoding
        reverse_geocode_result = self.gmaps.reverse_geocode((40.714224, -73.961452))
        print(reverse_geocode_result[0])
        # Request directions via public transit
        now = datetime.datetime.now()
        directions_result = self.get_directions(
            "Festival Theatre, Edinburgh, UK",
            "Edinburgh Waverley Train station",
            mode="walking",
        )
        print(directions_result)


if __name__ == "__main__":
    dotenv.load_dotenv()
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    gmaps = GMAPS(api_key)
    gmaps.example()
