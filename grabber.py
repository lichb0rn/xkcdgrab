"""A simple script for downloading xkcd comics to seed mocks/tests"""
from urllib.error import URLError, ContentTooShortError
import urllib.request
import json
import sys
import os


def get_comic_url(num: int) -> str:
    """Return a URL for the specific comic number"""
    return f"https://xkcd.com/{num}/info.0.json"


def download_json(url: str) -> dict:
    """Download a comic and return json object"""
    json_object = {}
    try:
        response = urllib.request.urlopen(url)
        if response.status == 200:
            data = response.read()
            encoding = response.info().get_content_charset("utf-8")
            json_object = json.loads(data.decode(encoding))
    except URLError:
        print(f"Could not open a URL {url}", file=sys.stderr)
    except json.JSONDecodeError:
        print(f"Server returned invalid json from url: {url}", file=sys.stderr)

    return json_object
    

def download_comic_picture(url: str, file_name: str):
    """Download comic picture from url and save it to '.'"""
    print(file_name)
    try:
        urllib.request.urlretrieve(url, file_name)
    except ContentTooShortError:
        print(f"TOO SHORT: {url}", file=sys.stderr)
        
def download_comic(index: int = 614) -> None:
    """Donwload comic with index and save it's json and image to file"""
    comic_url = get_comic_url(index)
    print(f"Downloading comic #{index} from {comic_url}")
    json_obj = download_json(comic_url)
    if len(json_obj) > 0:
        image_url = json_obj["img"]
        _, _, image_name = image_url.rpartition("/")
        current_dir = os.getcwd()
        image_path = os.path.join(current_dir, "comics", image_name)
        json_path = os.path.join(current_dir, "comics", f"{index}.json")
        with open(json_path, "w") as file:
            json.dump(json_obj, file)
        
        download_comic_picture(image_url, image_path)
        
    
def main():
    for index in range(614, 634):
        download_comic(index)


if __name__ == "__main__":
    main()