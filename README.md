# shogakukan-scrapper

 Web scrapper for downloading mangas from [shogakukan](https://csbs.shogakukan.co.jp/) in pdf format

## Why ?

***Shogakukan*** is a japanese website for online manga reading.
This is useful for Japanese learners who want to improve their reading in a fun way.  

However this website doesn't allow downloads and has a really strange interface.
The goal is to download those manga.

## Usage

There are two codes:

- A [javascript script](copy-paste.js) to copy and paste in browser.  
This will retrieve the manga's pages urls by browsing each page and then save said urls in a `json` file.

- A [python CLI](main.py) to download the images from the `json` file and combine them into a `pdf`

```txt
Usage: main.py [OPTIONS] path_to_json

Arguments:  
   path_to_json      TEXT  [default: None] [required]

Options:  
   --title                          TEXT  [default: manga]  
   --destination                    TEXT  [default: current directory]  
   --verbose        --no-verbose          [default: verbose]  
   --help                                 Show this message and exit.  
```

## Dependencies

Find the dependencies in [requirements.txt](requirements.txt).  

```bash
pip install -r requirements.txt
```

> ### Attention
>
> You may find an <**Import Error**> within the dependencies.  
> To solve it, change the following line in the `from_dict.py` file:  
>
>```py
>from collections import Mapping
>```
>
> into
>
>```py
>try:
>    from collections.abc import Mapping
>except ImportError:
>    from collections import Mapping
>```
