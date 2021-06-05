
#!/usr/bin/python3
# expects to be run as:
# $ python3 videos_to_gif_python3.py video.mp4 subtitles.srt

import os, sys, re, subprocess, shutil, pysrt
from PIL import Image, ImageFont, ImageDraw
from slugify import slugify

directory = "screenshots"
gif_dir = "gifs"
font = ImageFont.truetype("font/DejaVuSansCondensed-BoldOblique.ttf", 14)

def striptags(data):
  # I'm a bad person, don't ever do this.
  # Only okay, because of how basic the tags are.
  p = re.compile(r'<.*?>')
  return p.sub('', data)

def drawText(draw, x, y, text, font):
  # black outline
  draw.text((x-1, y),text,(0,0,0),font=font)
  draw.text((x+1, y),text,(0,0,0),font=font)
  draw.text((x, y-1),text,(0,0,0),font=font)
  draw.text((x, y+1),text,(0,0,0),font=font)

  # white text
  draw.text((x, y),text,(255,255,255),font=font)

def makeGif(video, start, end, string, output):
  if not os.path.exists(gif_dir):
    os.makedirs(gif_dir)

  if not os.path.exists(directory):
    os.makedirs(directory)

  text = striptags(string).split("\n")

  subprocess.call(['avconv', '-i', video, '-vf', 'scale=w=400:h=-1', '-r', '15', '-ss', start, '-t', end, os.path.join(directory, 'image-%05d.png')])

  file_names = sorted((fn for fn in os.listdir(directory)))

  for f in file_names:
    print(f)
    image = Image.open(os.path.join(directory,f))
    draw = ImageDraw.Draw(image)

    # reddit tells me this patten sucks, but I like it
    try:
      image_size
    except NameError:
      image_size = image.size

    subs_num = len(text)
    text_size = font.getsize(text[0])
    text_height = text_size[1]
    for i in range(subs_num):
      text_size = font.getsize(text[i])
      x = (image_size[0]/2) - (text_size[0]/2)
      mult = subs_num - i
      y = image_size[1] - (mult*text_height) - 5 # padding
      drawText(draw, x, y, text[i], font)

    image.save(os.path.join(directory,f))

  subprocess.call(["convert", '-loop', '0', os.path.join(directory, '*.png'), output])
  shutil.rmtree(directory)
  

def generateGifs(video_file_path, sub_file_path):
  outpath = "gifs"

  subs = pysrt.open(sub_file_path, encoding="utf-8")

  # generate a gif for every line of dialogue
  for i, sub in enumerate(subs):
    # 00:00:00,000 => 00:00:00.000
    start = str(sub.start).replace(',', '.')
    end = str(sub.end - sub.start).replace(',', '.')

    gif_filename = os.path.join(outpath, f'{i:06}-{slugify(striptags(sub.text))}.gif')
    
    if os.path.isfile(gif_filename):
      next
    else:
      print("generating " + gif_filename + "...")
      makeGif(video_file_path, start, end, sub.text, gif_filename)

if __name__ == '__main__':
  generateGifs(sys.argv[1], sys.argv[2])