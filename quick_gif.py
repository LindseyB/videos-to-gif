#!/usr/bin/python

import sys, os, argparse, subprocess, shutil, yaml, pysrt
from PIL import Image, ImageFont, ImageDraw
from slugify import slugify

directory = "screenshots"

def drawText(draw, x, y, text, font):
  # black outline
  draw.text((x-1, y),text,(0,0,0),font=font)
  draw.text((x+1, y),text,(0,0,0),font=font)
  draw.text((x, y-1),text,(0,0,0),font=font)
  draw.text((x, y+1),text,(0,0,0),font=font)

  # white text
  draw.text((x, y),text,(255,255,255),font=font)

def makeGif(video, start, end, string, output):
  if not os.path.exists(directory):
    os.makedirs(directory)

  subprocess.call(['ffmpeg', '-i', video, '-ss', start, '-to', end, os.path.join(directory, 'image-%05d.png')])

  file_names = sorted((fn for fn in os.listdir(directory)))
  images = []
  font = ImageFont.truetype("fonts/DejaVuSansCondensed-BoldOblique.ttf", args.fontsize)

  for f in file_names:
    image = Image.open(os.path.join(directory,f))
    draw = ImageDraw.Draw(image)

    # reddit tells me this patten sucks, but I like it
    try:
      image_size
    except NameError:
      image_size = image.size

    text_size = font.getsize(args.text)
    x = (image_size[0]/2) - (text_size[0]/2)
    y = image_size[1] - text_size[1] - args.padding
    drawText(draw, x, y, args.text, font)
    image.save(os.path.join(directory,f))

  subprocess.call(['convert', '-loop', '0', os.path.join(directory, '*.png'), output])

def main():
  stream = file('files.yml', 'r')
  data = yaml.load(stream)

  for file in data["files"]:
    video_file_path = file["video"]
    sub_file_path = file["subs"]

    subs = pysrt.open(sub_file_path)

    # generate a gif for every line of dialogue
    for sub in subs:
      start = sub.start
      end = sub.end - sub.start
      makeGif(video_file_path, start, end, sub.text, slugify(sub.text))

  shutil.rmtree(directory)

if __name__ == '__main__':
  main()
