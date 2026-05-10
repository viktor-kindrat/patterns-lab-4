import os
import requests

from .sample_data_generator import generate as generate_sample


class DataDownloader:
    def __init__(self, data_config: dict) -> None:
        self._url = data_config["url"]
        self._file_path = data_config["file"]

    def ensure_downloaded(self) -> None:
        if os.path.exists(self._file_path):
            print(f"[Downloader] Dataset already exists at '{self._file_path}', skipping download.")
            return

        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)

        print(f"[Downloader] Attempting to download dataset from:\n  {self._url}")
        try:
            response = requests.get(self._url, stream=True, timeout=60)
            if response.status_code == 403:
                print("[Downloader] Access requires authentication — generating sample dataset instead.")
                generate_sample(self._file_path)
                return
            response.raise_for_status()
            with open(self._file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"[Downloader] Saved to '{self._file_path}'.")
        except requests.RequestException as exc:
            print(f"[Downloader] Download failed ({exc}) — generating sample dataset instead.")
            generate_sample(self._file_path)
