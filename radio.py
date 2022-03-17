import os
import vlc
import tkinter as tk
from tkinter import ttk


class Player(tk.Frame):
    _geometry = ''
    _stopped = False
    media = None

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.parent = parent  # == root
        self.parent.title('Online radio')
        self.parent.resizable(False, False)

        self.big_frame = ttk.Frame(self.parent)
        self.big_frame.pack(fill="both", expand=True)

        theme_file = "sun-valley.tcl"
        if os.path.isfile(theme_file):
            self.parent.tk.call("source", theme_file)
            self.parent.tk.call("set_theme", "dark")

        self.controls_frame = ttk.Frame(self.big_frame)
        self.controls_frame.grid(row=0, column=0)

        icon_file = 'icons/211876_play_play_icon.png'
        if os.path.isfile(icon_file):
            self.play_btn_img = tk.PhotoImage(
                file='icons/211876_play_play_icon.png')
            self.play_button = ttk.Button(
                self.controls_frame, image=self.play_btn_img, command=self.play)
        else:
            self.play_button = ttk.Button(
                self.controls_frame, text='play', command=self.play)

        icon_file = 'icons/211931_stop_stop_icon.png'
        if os.path.isfile(icon_file):
            self.stop_btn_img = tk.PhotoImage(file=icon_file)
            self.stop_button = ttk.Button(
                self.controls_frame, image=self.stop_btn_img, command=self.stop)
        else:
            self.stop_button = ttk.Button(
                self.controls_frame, text='stop', command=self.stop)

        self.play_button.grid(row=0, column=0, padx=10)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.volume_slider = ttk.Scale(self.controls_frame, from_=0, to=100,
                                       orient=tk.HORIZONTAL, value=90, command=self.volume, length=100)
        self.volume_slider.grid(row=0, column=3, padx=30,
                                columnspan=2, sticky=tk.E)

        # playlist
        self.song_box = tk.Listbox(self.big_frame, bg="black", fg="green", width=60,
                                   selectbackground="gray", selectforeground="black")
        self.song_box.grid(row=1, column=0, columnspan=2)
        self.song_box.bind('<Double-1>', self.play)

        self.status_bar = tk.Label(self.parent, text='', bd=1,
                                   relief=tk.GROOVE, anchor=tk.E)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        playlist_file = 'record.m3u'
        if os.path.isfile(playlist_file):
            with open(playlist_file, mode='r') as file:
                lines = file.readlines()
                for url in lines:
                    self.song_box.insert(tk.END, url.strip())
        else:
            url = 'http://radiorecord.hostingradio.ru/liquidfunk96.aacp'
            self.song_box.insert(tk.END, url)

    def play_time(self):

        if self._stopped:
            return

        # song = self.song_box.get(tk.ACTIVE)

        prev = ""
        m = self.media.get_meta(12)  # vlc.Meta 12: 'NowPlaying',
        if m != prev:
            self.status_bar.config(
                text=f'Now playing:  {m}')
            prev = m

        self.status_bar.after(1000, self.play_time)

    def play(self, x=0):

        self._stopped = False

        url = self.song_box.get(tk.ACTIVE)
        self.player.stop()

        self.media = self.instance.media_new(url)

        self.player.set_media(self.media)

        self.player.play()

        self.play_time()

    def stop(self):
        self.status_bar.config(text='')
        self.song_box.selection_clear(tk.ACTIVE)

        self.status_bar.config(text='')
        self.player.stop()

        self._stopped = True

    def volume(self, x):
        vol = int(self.volume_slider.get())
        if self.player:
            self.player.audio_set_volume(vol)


root = tk.Tk()
player = Player(root)
root.mainloop()
