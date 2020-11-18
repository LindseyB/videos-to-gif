# coding: utf-8

import Tkinter as tk
import ttk as ttk
import tkFileDialog, pysrt, os
import unicodecsv as csv
from slugify import slugify
from videos_to_gif import makeGif, striptags
from unidecode import unidecode

# TODO: right now we're magically toggling this
generate_csv = True

def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def onMousewheel(event):
    # lol doesn't work on linux
    canvas.yview_scroll(-1*(event.delta/120), "units")

def selectAll():
    for button in sub_buttons:
        button.select()

def generateGifs():
    if video_path and subs:
        to_generate_list = []
        for index, item in enumerate(sub_list):
            if (item.get() != 0):
                item.set(0) # uncheck after it's been processed
                to_generate_list.append(index)
    else:
        return

    popup = tk.Toplevel()
    tk.Label(popup, text="GIFs generating").grid(row=0,column=0)
    progress = 0
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
    progress_bar.grid(row=1, column=0)
    popup.pack_slaves() # do what now?

    progress_step = float(100.0/len(to_generate_list))

    if generate_csv: 
        csvfile = open('names.csv', 'w')
        fieldnames = ['index', 'filename', 'dialog']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    i = 0
    for index in to_generate_list:
        texts = []
        starts = []
        ends = []
        filename = ""

        sub = subs[index]
        starts.append(str(sub.start).replace(',', '.'))
        ends.append(str(sub.end - sub.start).replace(',', '.'))
        texts.append(sub.text)
        filename = format(i, '05') + '-' + slugify(unidecode(sub.text))

        append_offset = index
        while True:
            if (merge_list[append_offset].get() != 0):
                sub = subs[append_offset+1]
                starts.append(str(sub.start).replace(',', '.'))
                ends.append(str(sub.end - sub.start).replace(',', '.'))
                texts.append(sub.text)
                filename = filename + "-" + slugify(unidecode(sub.text))
                append_offset += 1
            else:
                break

        gif_filename = os.path.join(filename + ".gif")
        
        if not os.path.exists(gif_filename):
            try:
                makeGif(video_path, starts, ends, texts, gif_filename)
            except UnicodeEncodeError:
                texts = map(lambda t: unidecode(t), texts)
                makeGif(video_path, starts, ends, texts, gif_filename)

        if generate_csv:
            writer.writerow({'index': i, 'filename': gif_filename, 'dialog': sub.text})

        popup.update()
        progress += progress_step
        progress_var.set(progress)
        i+=1

    popup.destroy()

    if generate_csv:
        csvfile.close()


subs = None
video_path = None
subtitle_path = None
root = tk.Tk()
root.title("Videos to Gif Frontend")

file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a subtitle file', filetypes = [("srt file", "*.srt")])
if file != None:
    subs = pysrt.open(file.name)

file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Choose a video file')
if file != None:
    video_path = file.name

if video_path:
    w = tk.Label(root, text="Possible gifs for: " + video_path)
    w.pack()

if subtitle_path:
    w = tk.Label(root, text="Subs for: " + subtitle_path)
    w.pack()

b = tk.Button(root, text="Generate GIFs for Selected Quotes", command=generateGifs, bg="white")
b.pack()

b_all = tk.Button(root, text="Select All", command=selectAll, bg="white")
b_all.pack()

sub_list = []
merge_list = []
sub_buttons = []
index = 0

canvas = tk.Canvas(root, borderwidth=0)
frame = tk.Frame(canvas)
vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4,4), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
canvas.bind_all("<MouseWheel>", onMousewheel)

for sub in subs:
    sub_list.append(tk.IntVar())
    merge_list.append(tk.IntVar())
    check = tk.Checkbutton(frame, text=striptags(sub.text), variable=sub_list[index])
    sub_buttons.append(check)
    check.grid(row=index, sticky=tk.W)
    merge_check = tk.Checkbutton(frame, variable=merge_list[index])
    merge_check.grid(row=index, sticky=tk.E)
    index+=1

root.mainloop()

