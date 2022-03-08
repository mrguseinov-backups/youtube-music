import json
from datetime import datetime
from typing import Any, Dict, List

from ytmusicapi import YTMusic

from src.track import Track


class Downloader:
    def __init__(self) -> None:
        self._ytmusic = YTMusic("headers.json")

    def save_liked_tracks(self) -> None:
        print("Downloading tracks from the 'Your Likes' playlist...")
        today = datetime.now().strftime("%Y-%m-%d")
        output_file = f"liked-tracks-{today}.json"
        raw_tracks = self._download_liked_tracks()
        tracks = [track.dict() for track in self._parse_raw_tracks(raw_tracks)]
        with open(output_file, "w") as file:
            json.dump(tracks, file, ensure_ascii=False, indent=4)
        print(f"Dumped {len(tracks)} tracks to '{output_file}'.")

    def _download_liked_tracks(self) -> List[Dict[str, Any]]:
        num_liked_tracks = self._get_num_liked_tracks()
        return self._ytmusic.get_liked_songs(limit=num_liked_tracks)["tracks"]

    def _get_num_liked_tracks(self) -> int:
        return self._ytmusic.get_liked_songs(limit=1)["trackCount"]

    @staticmethod
    def _parse_raw_tracks(raw_tracks: List[Dict[str, Any]]) -> List[Track]:
        return [
            Track(
                id=track["videoId"],
                title=track["title"],
                artists=[artist["name"] for artist in track["artists"]],
                album=None if track["album"] is None else track["album"]["name"],
                duration=track["duration_seconds"],
            )
            for track in raw_tracks
        ]
