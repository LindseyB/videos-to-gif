Videos to Gif
---

### What does it do?

Given any number of video files and matching subtitle files it will generate gifs for every single line of dialogue

### How do I use it?

install pre-reqs on your machine:
* avconv
* imagemagick or graphicsmagick

install requirements:

```
$ pip install -r requirements.txt
```

setup your **files.yml** file based on the provided **files.sample.yml** file and keep it in the same directory as videos_to_gif.py

run it:

```
$ python videos_to_gif.py
```