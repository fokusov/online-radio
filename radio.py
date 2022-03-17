import os
import vlc
import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title('Online radio')
root.resizable(False, False)

global player
global media


def play_time():

    if stopped:
        return

    song = song_box.get(tk.ACTIVE)

    prev = ""
    m = media.get_meta(12)  # vlc.Meta 12: 'NowPlaying',
    if m != prev:
        status_bar.config(
            text=f'Now playing:  {m}')
        prev = m

    status_bar.after(1000, play_time)


def play(x=0):

    global stopped
    stopped = False

    url = song_box.get(tk.ACTIVE)
    player.stop()

    global media
    media = instance.media_new(url)

    player.set_media(media)

    player.play()

    play_time()


global stopped
stopped = False


def stop():
    status_bar.config(text='')
    song_box.selection_clear(tk.ACTIVE)

    status_bar.config(text='')
    player.stop()

    global stopped
    stopped = True


def volume(x):
    vol = int(volume_slider.get())
    if player:
        player.audio_set_volume(vol)


big_frame = ttk.Frame(root)
big_frame.pack(fill="both", expand=True)

root.tk.call("source", "sun-valley.tcl")
root.tk.call("set_theme", "dark")

# controls
play_btn_img = tk.PhotoImage(file='icons/211876_play_play_icon.png')
stop_btn_img = tk.PhotoImage(file='icons/211931_stop_stop_icon.png')

controls_frame = ttk.Frame(big_frame)
controls_frame.grid(row=0, column=0)

play_button = ttk.Button(controls_frame, image=play_btn_img, command=play)
stop_button = ttk.Button(controls_frame, image=stop_btn_img, command=stop)

play_button.grid(row=0, column=0, padx=10)
stop_button.grid(row=0, column=1, padx=10)

volume_slider = ttk.Scale(controls_frame, from_=0, to=100,
                          orient=tk.HORIZONTAL, value=90, command=volume, length=100)
volume_slider.grid(row=0, column=3, padx=30, columnspan=2, sticky=tk.E)

# playlist
song_box = tk.Listbox(big_frame, bg="black", fg="green", width=60,
                      selectbackground="gray", selectforeground="black")
song_box.grid(row=1, column=0, columnspan=2)
song_box.bind('<Double-1>', play)

status_bar = tk.Label(root, text='', bd=1, relief=tk.GROOVE, anchor=tk.E)
status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)


instance = vlc.Instance()
player = instance.media_player_new()
playlist_file = 'record.m3u'
if os.path.isfile(playlist_file):
    with open(playlist_file, mode='r') as file:
        lines = file.readlines()
        for url in lines:
            song_box.insert(tk.END, url.strip())
else:
    url = 'http://radiorecord.hostingradio.ru/liquidfunk96.aacp'
    song_box.insert(tk.END, url)

root.mainloop()
