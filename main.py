import json
import requests
from datetime import date
from secret import spotify_id, discover_weekly_id
from refresh import Refresh

class SaveSongs:
    """
    Save weekly discovered songs
    """
    def __init__(self):
        self.spotify_token = ""
        self.spotify_id = spotify_id
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.playlist_id = ""

    def find_songs(self):
        """
        Find weekly discovered playlist
        """

        print("Finding Songs...")
        
        query = f"https://api.spotify.com/v1/playlists/{self.discover_weekly_id}/tracks"

        response = requests.get(query, headers={"Content-Type":"application/json",
                                            "Authorization":f"Bearer {self.spotify_token}"})

        print(response)
        response_json = response.json()

        file = "discover_weekly.json"
        with open(file, "w") as f:
            json.dump(response_json, f, indent=4)

        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]

        self.add_songs()

    def create_playlist(self):
        """
        Create a new playlist to save weekly discovered songs
        """

        print("Creating Playlist...")

        today = date.today()
        today_formatted = today.strftime("%d/%m/%Y")
        query = f"https://api.spotify.com/v1/users/{self.spotify_id}/playlists"

        playlist_body = json.dumps({"name":today_formatted+" Weekly Discovered Playlist", 
                         "description":"This is this week weekly discovered playlist.",
                         "public":True})

        response = requests.post(query, data=playlist_body, 
                                headers={"Content-Type":"application/json",
                                    "Authorization": f"Bearer {self.spotify_token}"})

        response_json = response.json()

        print(response.status_code)
   
        return response_json["id"]

    def add_songs(self):
        """
        Add songs to created playlist
        """
        self.playlist_id = self.create_playlist()

        print("Adding songs...")

        query = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks?uris={self.tracks}"

        response = requests.post(query,
                                headers={"Content-Type":"application/json",
                                        "Authorization":f"Bearer {self.spotify_token}"})
        
        print(response)

    def refresh(self):
        """
        Refresh token whenever u run the code
        """
        refresh = Refresh()
        self.spotify_token = refresh.refresh()

        self.find_songs()


a = SaveSongs()
a.refresh()