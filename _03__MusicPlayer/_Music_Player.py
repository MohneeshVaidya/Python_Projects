import os
import pygame

from tkinter import *
from tkinter.ttk import Separator, Scale
from tkinter import filedialog
from PIL import ImageTk, Image
from mutagen.mp3 import MP3

pygame.mixer.init()
pygame.mixer.music.set_volume(0.09)

class App(Tk):
    def __init__(self):
        super(App, self).__init__()

        # Important app attributes
        self._playlist_box   = None
        self._playlist_paths = {}
        self._images         = []
        self._is_playing     = False
        self._status         = None
        self._time           = 0
        self._curr_song      = ''
        self._curr_song_len  = 0
        self._slider_prog    = None
        self._last_stop      = 0
        self._after          = ''

        # Configure app
        self._configure_app()

        # Display playlist
        self._display_playlist()

        # Display progress
        self._display_progress()
        
        # Display controll buttons
        self._display_btns()

        # Display menu
        self._display_menu()

        # Display footer (contains song status and volume cotroller)
        self._display_footer()

        # Initialize playlist
        self._initialize_playlist()
        
    def _configure_app(self):
        self.title('Music Player')
        self.geometry('500x370')
    
    def _display_playlist(self):
        f = Frame(self, bg='black')
        f.pack(pady=20)

        self._playlist_box = Listbox(f, bg='black', fg='darkgreen', width=55, selectbackground='green', selectforeground='white')
        self._playlist_box.pack()

    def _display_progress(self):
        f = Frame(self, bg='black')
        f.pack(fill='x', padx=29)

        self._slider_prog = Scale(f, from_=0, command=lambda pos: self._update_progress(pos))
        self._slider_prog.pack(fill='x')

    def _update_progress(self, pos_ = None):
        if(pos_ is None):
            self._slider_prog.configure(to=self._curr_song_len, value=self._time)
            pass
        else:
            self._last_stop = float(pos_).__round__(3)
            pygame.mixer.music.play(loops=1, start=self._last_stop)
            if(not self._is_playing):
                pygame.mixer.music.pause()

    def _display_btns(self):
        f = Frame(self)
        f.pack(pady=15)

        prev_btn  = Button(f, image=self._resized_image('_03__MusicPlayer/Images/prev-button.png'), command=self._prev)
        next_btn  = Button(f, image=self._resized_image('_03__MusicPlayer/Images/next-button.png'),  command=self._next)
        play_btn  = Button(f, image=self._resized_image('_03__MusicPlayer/Images/play-button.png'),  command=self._play)
        pause_btn = Button(f, image=self._resized_image('_03__MusicPlayer/Images/pause-button.png'), command=self._pause)
        stop_btn  = Button(f, image=self._resized_image('_03__MusicPlayer/Images/stop-button.png'),  command=self._stop)

        for widget in f.winfo_children():
            widget.configure(relief='flat')
            widget.pack(side='left', padx=4)
    
    def _prev(self):
        id_tuple = self._playlist_box.curselection()
        if(not id_tuple):
            return
        curr = id_tuple[0]
        if(curr == 0):
            return
        name = self._playlist_box.get(curr-1)
        self._curr_song = self._playlist_paths[name]
        self._playlist_box.selection_clear(0, 'end')
        self._playlist_box.activate(curr-1)
        self._playlist_box.selection_set(curr-1)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(self._curr_song)
        pygame.mixer.music.play(loops=1)
        if(not self._is_playing):
            pygame.mixer.music.pause()
        self._last_stop = 0

        if(self._after): self._status.after_cancel(self._after)

        self._count_time()
        
    def _next(self):
        id_tuple = self._playlist_box.curselection()
        if(not id_tuple):
            return
        curr = id_tuple[0]
        if(curr == len(self._playlist_paths)-1):
            return
        name = self._playlist_box.get(curr+1)
        self._curr_song = self._playlist_paths[name]
        self._playlist_box.selection_clear(0, 'end')
        self._playlist_box.activate(curr + 1)
        self._playlist_box.selection_set(curr + 1)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(self._curr_song)
        pygame.mixer.music.play(loops=1)
        if(not self._is_playing):
            pygame.mixer.music.pause()
        self._last_stop = 0

        if(self._after): self._status.after_cancel(self._after)

        self._count_time()

    def _play(self):
        name = self._playlist_box.get('active')
        if(not self._playlist_box.curselection()):
            return
        elif(not name):
            return
        self._curr_song = self._playlist_paths[name]
        self._is_playing = True
        
        pygame.mixer.music.load(self._curr_song)
        pygame.mixer.music.play(loops=1)
        self._last_stop = 0

        if(self._after): self._status.after_cancel(self._after)

        self._count_time()

    def _stop(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        old_is_playing, self._is_playing = self._is_playing,  False
        self._playlist_box.selection_clear('active')
        self._curr_song = ''
        self._time = 0
        self._status.configure(text='Time Elapsed 0.0 of 0.0')
        self._last_stop = 0
        self._update_progress()
        return old_is_playing

    def _pause(self):
        if(self._is_playing):
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self._is_playing = not self._is_playing
        self._count_time()

    def _resized_image(self, path):
        _image = Image.open(path).resize((45, 45), Image.Resampling.LANCZOS)
        _image = ImageTk.PhotoImage(_image)
        self._images.append(_image)
        return self._images[-1]
    
    def _display_menu(self):
        menubar = Menu(self)
        self.configure(menu=menubar)

        file = Menu(menubar, tearoff=False)
        menubar.add_cascade(label='File', menu=file)

        file.add_command(label='Add Song...', command=self._add_song)
        file.add_command(label='Add Songs...', command=self._add_songs)
        file.add_separator()
        file.add_command(label='Remove Song...', command=self._delete_song)
        file.add_command(label='Empty the playlist', command=self._delete_all)
        file.add_separator()
        file.add_command(label='Exit', command=self.quit)
    
    def _add_song(self):
        path = filedialog.askopenfilename(filetypes=[('MP3 files', '*.mp3')], initialdir='_04__MusicPlayer/Playlist')
        name = os.path.splitext(os.path.basename(path))[0]
        if(name not in self._playlist_paths):    
            self._playlist_paths[name] = path
            self._playlist_box.insert('end', name)
    
    def _add_songs(self):
        paths = filedialog.askopenfilenames(filetypes=[('MP3 files', '*.mp3')], initialdir='_04__MusicPlayer/Playlist')
        for path in paths:
            name = os.path.splitext(os.path.basename(path))[0]
            if(name not in self._playlist_paths):
                self._playlist_paths[name] = path
                self._playlist_box.insert('end', name)
    
    def _delete_song(self):
        id = self._playlist_box.curselection()
        if(not id):
            return
        id = id[0]
        name = self._playlist_box.get(id)
        self._playlist_box.delete(id)
        self._playlist_paths.pop(name)
        self._is_playing = self._stop()
        if(not self._playlist_paths):
            return
        self._playlist_box.activate(id)
        self._playlist_box.selection_set(id)
        self._play_song_with_id(id)
    
    def _play_song_with_id(self, id):
        name = self._playlist_box.get(id)
        if(not name):
            return
        self._curr_song = self._playlist_paths[name]

        pygame.mixer.music.load(self._curr_song)
        pygame.mixer.music.play()
        if(not self._is_playing):
            pygame.mixer.music.pause()
    
    def _delete_all(self):
        if(not self._playlist_paths):
            return
        self._playlist_paths.clear()
        self._playlist_box.delete(0, 'end')
        self._stop()
    
    def _display_footer(self):
        f = Frame(self, bd=0)
        f.pack(fill='x')

        Separator(f).pack(side='top', fill='x')

        self._status = Label(f, text='Time Elapsed 0.0 of 0.0')
        self._status.pack(side='right', padx=3)

        Label(f, text='Volume:').pack(side='left', padx=3)
        
        # Volume Controller
        Scale(f, from_=0, to=100, length=160, value=9, command=lambda vol: pygame.mixer.music.set_volume(float(vol)/100)).pack(side='left', padx=3)
    
    def _count_time(self):
        if(not self._is_playing or not self._curr_song):
            return
        self._time = pygame.mixer.music.get_pos()/1000 + self._last_stop
        curr_time  = int(self._time) if(self._time > -1) else 0
        curr_time  = '{}.{}'.format(curr_time // 60, curr_time % 60)

        song_len = 0
        if(self._curr_song):
            song_mut = MP3(self._curr_song)
            self._curr_song_len = song_len = int(song_mut.info.length)

        song_len = '{}.{}'.format(song_len // 60, song_len % 60)
        self._status.configure(text='Time Elapsed {} of {}'.format(curr_time, song_len))
        
        self._update_progress()
        if(not pygame.mixer.music.get_busy()):
            self._last_stop = 0
            self._next()

        self._after = self._status.after(1000, self._count_time)
    
    def _initialize_playlist(self):
        path = os.getcwd() + '/_03__MusicPlayer/Playlist'
        for file in os.listdir(path):
            name = os.path.splitext(file)[0]
            self._playlist_paths[name] = path + '/' + file
            self._playlist_box.insert('end', name)
        

if __name__ == '__main__':
    app = App()
    app.mainloop()
