# import sys
import os
from shutil import rmtree

# import requests
# from bs4 import BeautifulSoup

import urllib.request
from PIL import Image
import json

title = "1巻 ドラえもん - 小学館eコミックストア"
json_path = "data/" + title + ".json"

print("Reading json... ", end="")

with open(json_path) as file:
    file_contents = file.read()
page_urls = json.loads(file_contents)

print("done")

temp_dir = "temp-" + title
os.mkdir(temp_dir)


images = []
length = len(page_urls)

for n in range(1, length + 1):
    print(f"\rRequesting images... {n}/{length}", end="")
    page_location = f"{temp_dir}/{n}.png"
    urllib.request.urlretrieve(page_urls[str(n)], page_location)

    img = Image.open(page_location)
    # img.resize((600, 800))
    images.append(img)

print(f"\rRequesting images... done        ")
print("Saving pdf...", end="")

pdf_path = title + ".pdf"
images[0].save(
    pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
)
print("done")

print("Deleting temp files...", end="")
rmtree(temp_dir)
print("done")
