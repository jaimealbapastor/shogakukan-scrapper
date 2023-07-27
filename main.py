import typer
from PyInquirer import prompt, print_json, Separator
from rich import print as rprint

import os
from shutil import rmtree
import urllib.request
from PIL import Image
import json

# global variables
VERBOSE = False
DESTINATION = None

TITLE = None
TEMP_DIR = None

URLS_JSON = None
NB_URLS = 0

IMAGES = []


def vprint(txt: str, end: str = "\n"):
    if VERBOSE:
        rprint(txt, end=end)


def path_no_duplicates(parent_path: str, name: str, ext: str = "") -> str:
    if ext and ext[0] != ".":
        ext = "." + ext
    new_path = os.path.join(parent_path, name + ext)
    n = 1
    while os.path.exists(new_path):
        new_path = os.path.join(parent_path, f"{name}-{n}{ext}")
        n += 1
    return new_path


def read_json(json_path: str):
    global URLS_JSON, NB_URLS

    vprint("Reading json... ", end="")

    with open(json_path) as file:
        file_contents = file.read()
    URLS_JSON = json.loads(file_contents)
    NB_URLS = len(URLS_JSON)

    vprint("\t[green]done[green]")


def mkdir_temp():
    global TEMP_DIR
    TEMP_DIR = path_no_duplicates(DESTINATION, "temp-" + TITLE)
    os.mkdir(TEMP_DIR)


def delete_temp():
    if os.path.isdir(TEMP_DIR):
        vprint("Deleting temp files...", end="\t")
        rmtree(TEMP_DIR)
        vprint("[green]done[green]")


def request_images():
    global IMAGES
    for n in range(1, NB_URLS + 1):
        vprint(f"Requesting images... \t{n}/{NB_URLS}", end="\r")
        page_location = f"{TEMP_DIR}/{n}.png"
        urllib.request.urlretrieve(URLS_JSON[str(n)], page_location)

        img = Image.open(page_location)
        # img.resize((600, 800))
        IMAGES.append(img)
    vprint(f"Requesting images... \t[green]done[green]    ")


def save_pdf():
    vprint("Saving pdf...", end="\t\t")
    pdf_path = path_no_duplicates(DESTINATION, TITLE, ".pdf")

    IMAGES[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=IMAGES[1:]
    )
    vprint("[green]done[green]")


def main(
    json_path: str,
    title: str = "manga",
    destination: str = os.getcwd(),
    verbose: bool = True,
):
    global TITLE, DESTINATION, VERBOSE
    TITLE = title
    DESTINATION = destination
    VERBOSE = verbose

    if not os.path.isfile(json_path):
        rprint(f"[red bold]No file named: [/red bold][green]{json_path}[/green]")
        return
    if not os.path.isdir(destination):
        rprint(
            f"[red bold]Not directory named: [/red bold][green]{destination}[/green]"
        )
        return

    read_json(json_path)
    mkdir_temp()
    request_images()
    save_pdf()
    delete_temp()


if __name__ == "__main__":
    typer.run(main)
