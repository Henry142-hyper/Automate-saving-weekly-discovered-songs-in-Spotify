import json
import requests
from secret import refresh_token, base_64

class Refresh:
    """
    Refresh the expired auth token
    """
    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64

    def refresh(self):
        
        print("Refreshing token...")

        query = "https://accounts.spotify.com/api/token"

        response = requests.post(query, 
                    data={"grant_type":"refresh_token",
                          "refresh_token":self.refresh_token},
                    headers={"Authorization":f"Basic {self.base_64}"})

        print(response)

        response_json = response.json()
        
        return response_json["access_token"]

a = Refresh()
a.refresh()
