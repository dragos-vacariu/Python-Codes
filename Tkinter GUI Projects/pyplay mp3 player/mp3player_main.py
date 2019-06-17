import datetime
import pickle
import random
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinter import StringVar
import os
import pygame
import re
from tkinter.ttk import Progressbar, Combobox
import sched, time
import sys
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


class Playlist:
    def __init__(self):
        self.isSongPause = False
        self.isSongStopped = False
        self.VolumeLevel=1.0
        self.dirFilePath = ""
        self.skin=0
        self.SHUFFLE = False
        self.isListOrdered = 0 #0-onrating ; 1-sorted 2-reversed; 3-random;
        self.validFiles = []
        self.currentSongIndex = None
        self.currentSongPosition = 0
        self.REPEAT = 1 # 1 is value for repeat all
        self.RESUMED=False
        self.viewModel = "FULLSCREEN"

class Song:
    def __init__(self, filename, filepath, filesize):
        self.fileName = filename
        self.filePath = filepath
        self.fileSize = filesize
        self.Rating = 0
        audio = MP3(self.filePath)
        self.Length=audio.info.length
        audio = EasyID3(self.filePath)
        self.Genre = audio["genre"]
        self.Genre = self.Genre[0]
        self.startPos = 0
        self.endPos = self.Length

class CuttingTool:
    def __init__(self, parent):
        if play_list.currentSongIndex != None:
            top = self.top = tk.Toplevel(parent)

            InfoLabelText = StringVar()
            InfoLabelText.set("Welcome to MP3 Cutting capability:\n\n"
                               +"Please enter Start and End value and Hit OK.\n"
                                +"This will NOT change the original file.\n\n\n")
            tk.Label(top, textvariable=InfoLabelText).pack()
            tk.Label(top, text="Start Value (0 - " + str(play_list.validFiles[play_list.currentSongIndex].Length) + "):").pack()

            self.startValue = tk.Entry(top)
            self.startValue.pack(padx=5)

            tk.Label(top, text="End Value (0 - " + str(play_list.validFiles[play_list.currentSongIndex].Length) + "):").pack()
            self.endValue = tk.Entry(top)
            self.endValue.pack(padx=5)

            b = tk.Button(top, text="OK", command=self.ok)
            b.pack(pady=5)
            window.wait_window(self.top)

    def ok(self):
        if self.startValue.get()!="":
            try:
                st_value = float(self.startValue.get())
            except: pass
            else:
                if self.endValue.get() != "":
                    try:
                        ed_value = float(self.endValue.get())
                    except: pass
                    else:
                        if st_value > ed_value:
                            #interchange values
                            aux = st_value
                            st_value = ed_value
                            ed_value = aux
                if st_value > 0 and st_value < play_list.validFiles[play_list.currentSongIndex].Length:
                    play_list.validFiles[play_list.currentSongIndex].startPos = st_value
                    startPos = int(play_list.validFiles[play_list.currentSongIndex].startPos)
                    textStartTime.set("Start Time: {:0>8}".format(str(datetime.timedelta(seconds=startPos))))
                #print("Bad Input: start - " + str(self.startValue) + "  end - " + str(self.endValue))
        if self.endValue.get() != "":
            try:
                ed_value = float(self.endValue.get())
            except : pass
            else:
                if self.startValue.get() !="":
                    try:
                        st_value = float(self.startValue.get())
                    except: pass
                    else:
                        if st_value > ed_value:
                            #interchange values
                            aux = st_value
                            st_value = ed_value
                            ed_value = aux
                if ed_value > 0 and ed_value < play_list.validFiles[play_list.currentSongIndex].Length:
                    play_list.validFiles[play_list.currentSongIndex].endPos = ed_value
                    endPos = int(play_list.validFiles[play_list.currentSongIndex].endPos)
                    textEndTime.set("End Time: {:0>8}".format(str(datetime.timedelta(seconds=endPos))))

        self.top.destroy()

class SearchTool:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)

        InfoLabelText = StringVar()
        InfoLabelText.set("Search for song: \n")
        tk.Label(top, textvariable=InfoLabelText).pack()
        tk.Label(top, text="Value: ").pack()

        self.searchValue = tk.Entry(top)
        self.searchValue.pack(padx=5)
        ForwardButton = tk.Button(top, text="Forward", command=self.forward)
        ForwardButton.pack(pady=5)
        BackwardButton = tk.Button(top, text="Backward", command=self.backward)
        BackwardButton.pack(pady=5)
        window.wait_window(self.top)

    def forward(self):
        global listBox_Song_selected_index
        if self.searchValue.get() != "":
            value = len(play_list.validFiles)
            if listBox_Song_selected_index+1 < value:
                listBox_Song_selected_index+=1
            else:
                listBox_Song_selected_index=0
            for x in range(listBox_Song_selected_index, value):
                if self.searchValue.get().lower() in play_list.validFiles[x].fileName.lower():
                    listBox_Song_selected_index = x
                    # Maintain the selection in the listbox
                    listbox.selection_clear(0, tk.END)  # clear existing selection
                    listbox.select_set(listBox_Song_selected_index)
                    #play_list.currentSongIndex = listBox_Song_selected_index
                    play_music()
                    break;
        self.top.destroy()
    def backward(self):
        global listBox_Song_selected_index
        if self.searchValue.get() != "":
            if listBox_Song_selected_index - 1 > 0:
                listBox_Song_selected_index -= 1
            else:
                listBox_Song_selected_index = len (play_list.validFiles)-1
            for x in range(listBox_Song_selected_index, 0, -1):
                if self.searchValue.get().lower() in play_list.validFiles[x].fileName.lower():
                    listBox_Song_selected_index = play_list.validFiles.index(play_list.validFiles[x])
                    # Maintain the selection in the listbox
                    listbox.selection_clear(0, tk.END)  # clear existing selection
                    listbox.select_set(listBox_Song_selected_index)
                    #play_list.currentSongIndex = listBox_Song_selected_index
                    play_music()
                    break;
        self.top.destroy()

automaticallyBackupFile = "backup.pypl"
allButtonsWidth = 14
allButtonsHeight = 1

progressViewRealTime = 0.5
play_list = Playlist()
listBox_Song_selected_index = ""
APPLICATION_EXIT = False
skinOptions = [["default.gif", "minilights.gif", "road.gif", "darkg.gif", "leaves.gif"],\
               ["blue", "red", "gray", "green", "deeppink"],\
               ["Consolas 10 bold", "Rockwell 10 bold", "Arial 10 italic", "Candara 10 bold", "Arial 10 bold"]]

allButtonsFont = skinOptions[2][play_list.skin] #default Font value Consola 10 bold:
#default value of play_list.skin is 0

def load_file():
    global play_list
    fileToPlay = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mp3 files","*.mp3"),("pypl files","*.pypl"),("all files","*.*")))
    if fileToPlay:
        fileName = re.split("/",fileToPlay)
        fileName = fileName[len(fileName)-1]
        fileSize = os.path.getsize(fileToPlay)/(1024*1024)
        fileSize = float("{0:.2f}".format(fileSize))
        if ".mp3" in fileToPlay:
            play_list.validFiles.append(Song(fileName, fileToPlay, fileSize))
            play_list.currentSongIndex = 0
            textFilesToPlay.set("Files To Play: " + str(len(play_list.validFiles)))
        elif ".pypl" in fileToPlay:
            loadPlaylistFile(fileToPlay)
        displayElementsOnPlaylist()

def loadPlaylistFile(fileURL):
    global play_list
    file = open(fileURL, "rb")
    content = pickle.load(file)
    if isinstance(content, Playlist):
        play_list = content
        del content
        textFilesToPlay.set("Files To Play: " + str(len(play_list.validFiles)))
        SkinColor.set(skinOptions[1][play_list.skin])
        changeSkin("<Double-Button>")
        displayElementsOnPlaylist()
        textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
        if play_list.currentSongIndex != None and len(play_list.validFiles)>0:
            SongName.set("Currently Paused: " + play_list.validFiles[play_list.currentSongIndex].fileName)
            SongSize.set("Size: " + str(play_list.validFiles[play_list.currentSongIndex].fileSize) + " MB")
            SongDuration.set("Progress: " + str(play_list.currentSongPosition) + " s")
            #Update Length
            songLength = float("{0:.0f}".format(play_list.validFiles[play_list.currentSongIndex].Length))  # no decimals needed
            textLength.set("Length: {:0>8}".format(str(datetime.timedelta(seconds=songLength))))
            textGenre.set("Genre: " + str(play_list.validFiles[play_list.currentSongIndex].Genre))
            startPos = int(play_list.validFiles[play_list.currentSongIndex].startPos)
            textStartTime.set("Start Time: {:0>8}".format(str(datetime.timedelta(seconds=startPos))))
            endPos = int(play_list.validFiles[play_list.currentSongIndex].endPos)
            textEndTime.set("End Time: {:0>8}".format(str(datetime.timedelta(seconds=endPos))))
            updateRadioButtons()
        updateSortButton()
        view_playlist(True)
        if play_list.SHUFFLE:
            ShuffleButtonText.set("Shuffle On")
        if play_list.REPEAT == 0:
            RepeatButtonText.set("Repeat Off")
        elif play_list.REPEAT == 1:
            RepeatButtonText.set("Repeat All")
        else:
            RepeatButtonText.set("Repeat One")
        return True
    else:
        print("Playlist file has been corrupted.")
        return False

def load_directory():
    global play_list
    play_list.dirFilePath = filedialog.askdirectory()
    if play_list.dirFilePath:
        searchFilesInDirectories(play_list.dirFilePath)
        play_list.currentSongIndex = 0
        textFilesToPlay.set("Files To Play: " + str(len(play_list.validFiles)))
        displayElementsOnPlaylist()

def searchFilesInDirectories(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if ".mp3" in file:
                fileSize = os.path.getsize(root + "/" + file) / (1024 * 1024)
                fileSize = float("{0:.2f}".format(fileSize))
                play_list.validFiles.append(Song(file, root + "/" + file, fileSize))

def play_music():
    if len(play_list.validFiles) > 0 :
        try:
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.set_volume(play_list.VolumeLevel)
            if listBox_Song_selected_index != "":
                if listBox_Song_selected_index != play_list.currentSongIndex:
                    play_list.currentSongIndex = listBox_Song_selected_index
                    play_list.currentSongPosition = play_list.validFiles[play_list.currentSongIndex].startPos
                    play_list.RESUMED = False
            play_list.isSongPause = False
            pygame.mixer.music.load(play_list.validFiles[play_list.currentSongIndex].filePath)
            pygame.mixer.music.play()
            if play_list.currentSongPosition>0:
                pygame.mixer.music.set_pos(play_list.currentSongPosition)
                play_list.RESUMED = True
            elif play_list.validFiles[play_list.currentSongIndex].startPos > 0:
                start_pos = play_list.validFiles[play_list.currentSongIndex].startPos
                if play_list.currentSongPosition == 0:
                    play_list.currentSongPosition = start_pos
                pygame.mixer.music.set_pos(start_pos)
                play_list.RESUMED = True
        except Exception as e:
            print("Play Music Function " + str(e))
        else:
            SongName.set("Currently Playing: " + play_list.validFiles[play_list.currentSongIndex].fileName)
            SongSize.set("Size: " + str(play_list.validFiles[play_list.currentSongIndex].fileSize) + " MB")
            songLength = float("{0:.0f}".format(play_list.validFiles[play_list.currentSongIndex].Length))  # no decimals needed
            textLength.set("Length: {:0>8}".format(str(datetime.timedelta(seconds=songLength))))
            textGenre.set("Genre: " + str(play_list.validFiles[play_list.currentSongIndex].Genre))
            startPos = int(play_list.validFiles[play_list.currentSongIndex].startPos)
            textStartTime.set("Start Time: {:0>8}" .format(str(datetime.timedelta(seconds=startPos))))
            endPos = int(play_list.validFiles[play_list.currentSongIndex].endPos)
            textEndTime.set("End Time: {:0>8}" .format(str(datetime.timedelta(seconds=endPos))))
            progress["maximum"] = play_list.validFiles[play_list.currentSongIndex].Length
            updateRadioButtons()
            try:
                scheduler.enter(progressViewRealTime, 1, viewProgress)
                scheduler.run()
            except Exception as exp:
                print("Play Music Function - starting scheduler:" + str(exp))

def pause_music():
    global play_list
    if pygame.mixer.get_init():
        try:
            if play_list.isSongPause == False and pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                PausedButtonText.set("Resume")
                play_list.isSongPause = True
                if len(play_list.validFiles) > 0 :
                    SongName.set("Currently Paused: " + play_list.validFiles[play_list.currentSongIndex].fileName)
                else:
                    SongName.set("Currently Paused: ")
            elif play_list.isSongPause == True and pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
                PausedButtonText.set("Pause")
                play_list.isSongPause = False
                if len(play_list.validFiles) > 0:
                    SongName.set("Currently Playing: " + play_list.validFiles[play_list.currentSongIndex].fileName)
                else:
                    SongName.set("Currently Playing: ")
                scheduler.enter(progressViewRealTime, 1, viewProgress)
                scheduler.run()
        except Exception as e:
            print("Pause Music Function: " + str(e))

def stop_music():
    if pygame.mixer.get_init():
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                SongName.set("Currently Playing: ")
                SongDuration.set("Progress: ")
                SongSize.set("Size: ")
                play_list.isSongStopped = True
                play_list.currentSongPosition=0
                play_list.RESUMED = False
        except Exception as e:
            print("Stop Music Function: " +str(e))

def next_song():
    global listBox_Song_selected_index
    if len(play_list.validFiles) > 0 :
        if (play_list.SHUFFLE==False):
            try:
                play_list.currentSongIndex+=1
                if play_list.currentSongIndex >= len(play_list.validFiles):
                    play_list.currentSongIndex = 0
                else:
                    pass
            except Exception as exp:
                print("Next Song Function" + str(exp))
        else:
            shuffling_playlist()
        listBox_Song_selected_index = play_list.currentSongIndex
        # Maintain the selection in the listbox
        listbox.selection_clear(0, tk.END)  # clear existing selection
        listbox.select_set(listBox_Song_selected_index)
        play_list.currentSongPosition=0
        play_music()

def previous_song():
    global listBox_Song_selected_index
    if len(play_list.validFiles) > 0:
        if(play_list.SHUFFLE==False):
            try:
                play_list.currentSongIndex -= 1
                if play_list.currentSongIndex < 0:
                    play_list.currentSongIndex = len(play_list.validFiles)-1
                else:
                    pass
            except Exception as exp:
                print("Previous Song Function: " + str(exp))
        else:
            shuffling_playlist()
        listBox_Song_selected_index = play_list.currentSongIndex
        # Maintain the selection in the listbox
        listbox.selection_clear(0, tk.END)# clear existing selection
        listbox.select_set(listBox_Song_selected_index)
        play_list.currentSongPosition = 0
        play_music()

def viewProgress():
    global play_list
    global progress
    global Project_Title
    if APPLICATION_EXIT == False:
        if pygame.mixer.music.get_busy() and play_list.isSongPause == False:
            Project_Title = fontTransition(Project_Title)
            window.title(Project_Title) #add animation to font when playing music
            if play_list.RESUMED:
                local_position = play_list.currentSongPosition + (pygame.mixer.music.get_pos() / 1000)
                local_position = float("{0:.0f}".format(local_position)) #no decimals needed
                SongDuration.set("Progress: {:0>8}" .format(str(datetime.timedelta(seconds=local_position))))
                progress["value"] = local_position
                if local_position >= play_list.validFiles[play_list.currentSongIndex].endPos:
                    stop_music()
                    play_list.isSongStopped = False #song is not stopped in this circumstances, song has finished

            else:
                play_list.currentSongPosition = (pygame.mixer.music.get_pos()/1000)
                play_list.currentSongPosition = float("{0:.0f}".format(play_list.currentSongPosition))#no decimals needed
                SongDuration.set("Progress: {:0>8}" .format(str(datetime.timedelta(seconds=play_list.currentSongPosition))))
                progress["value"] = play_list.currentSongPosition
                if len(play_list.validFiles) > 0:
                    if play_list.currentSongPosition >= play_list.validFiles[play_list.currentSongIndex].endPos:
                        stop_music()
                        play_list.isSongStopped = False #song is not stopped in this circumstances, song has finished
            try:
                window.update()  # Force an update of the GUI
            except Exception as exp:
                #Enter here when the program is destroyed
                print("Application destroyed in View Progress Function")

                #Make a backup of everything:
                file = open(automaticallyBackupFile, "wb")
                pickle.dump(play_list, file)

                sys.exit()
            else:
                scheduler.enter(progressViewRealTime, 1, viewProgress)
        elif pygame.mixer.music.get_busy() == False and play_list.isSongPause == False and play_list.isSongStopped ==False:
            play_list.RESUMED = False
            if(play_list.REPEAT==1):
                next_song() #this will keep repeating the playlist
            elif play_list.REPEAT==2:
                play_music() #this will repeat the current song


def volume_down():
    global play_list
    if pygame.mixer.get_init():
        play_list.VolumeLevel-=0.1
        if (play_list.VolumeLevel < 0.0):
            play_list.VolumeLevel = 0.0
        pygame.mixer.music.set_volume(play_list.VolumeLevel)
        textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel*100)) + "%")

def volume_up():
    global play_list
    if pygame.mixer.get_init():
        play_list.VolumeLevel+=0.1
        if(play_list.VolumeLevel>1.0):
            play_list.VolumeLevel=1.0
        pygame.mixer.music.set_volume(play_list.VolumeLevel)
        textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")

def shuffle():
    global play_list
    if(play_list.SHUFFLE):
        ShuffleButtonText.set("Shuffle Off")
        play_list.SHUFFLE = False
    else:
        ShuffleButtonText.set("Shuffle On")
        play_list.SHUFFLE = True

def shuffling_playlist():
    global play_list
    if len(play_list.validFiles)>1:
        rand = random.randint(0, len(play_list.validFiles))
        play_list.currentSongIndex = rand

def save_playlist():
    window.filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                 filetypes=(("pypl files", "*.pypl"), ("all files", "*.*")))
    if window.filename:
        if ".pypl" in window.filename:
            file = open(window.filename, "wb")
        else:
            file = open(window.filename + ".pypl", "wb")
        play_list.currentSongPosition += (pygame.mixer.music.get_pos() / 1000)
        pickle.dump(play_list, file)


def new_playlist():
    global play_list
    if pygame.mixer.get_init():
        if pygame.mixer.music.get_busy():
            SongName.set("Currently Paused: " )
            SongSize.set("Size: ")
            SongDuration.set("Progress: ")
            play_list.validFiles.clear()
            play_list.dirFilePath = ""
            play_list.skin = 0
            play_list.SHUFFLE = False
            play_list.RESUMED = False
            play_list.isListOrdered = 0  # 0-onrating ; 1-sorted 2-reversed; 3-random;
            play_list.REPEAT = 1  # 1 is value for repeat all
        else:
            play_list = Playlist()
    else:
        play_list = Playlist()
    displayElementsOnPlaylist()
    textFilesToPlay.set("Files To Play: " + str(len(play_list.validFiles)))
    textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    #Restore default skin
    SkinColor.set(skinOptions[1][play_list.skin])
    changeSkin("<Double-Button>")

def elementPlaylistDoubleClicked(event):
    global play_list
    if listbox.size():
        widget = event.widget
        index = int(widget.curselection()[0])
        #value = widget.get(index)
        play_list.currentSongIndex = index
        play_list.currentSongPosition = 0
        play_music()

def updateSortButton():
    # 0-onrating, 1-sorted, 2-reversed, 3-random
    if play_list.isListOrdered == 0:
        SortButtonText.set("OnRating")
    elif play_list.isListOrdered == 1:
        SortButtonText.set("Sorted")
    elif play_list.isListOrdered == 2:
        SortButtonText.set("Reversed")
    elif play_list.isListOrdered == 3:
        SortButtonText.set("Random")


def displayElementsOnPlaylist():
    global listbox
    listbox.delete(0, tk.END)
    for element in play_list.validFiles:
        listbox.insert(play_list.validFiles.index(element), str(play_list.validFiles.index(element))+". "+element.fileName)

def changeSkin(event):
    global backgroundFile
    global skinOptions
    global background_label
    global play_list
    #changing buttons
    OpenFileButton["bg"]=SkinColor.get()
    OpenDirectoryButton["bg"]=SkinColor.get()
    PlayButton["bg"]=SkinColor.get()
    PauseButton["bg"]=SkinColor.get()
    StopButton["bg"]=SkinColor.get()
    NextButton["bg"]=SkinColor.get()
    PreviousButton["bg"]=SkinColor.get()
    VolumeDownButton["bg"]=SkinColor.get()
    VolumeUpButton["bg"]=SkinColor.get()
    ShuffleButton["bg"]=SkinColor.get()
    SavePlaylistButton["bg"]=SkinColor.get()
    NewPlaylistButton["bg"]=SkinColor.get()
    ViewPlaylistButton["bg"]=SkinColor.get()
    RepeatButton["bg"]=SkinColor.get()
    RendomizeListButton["bg"]=SkinColor.get()
    RemoveSongButton["bg"]=SkinColor.get()
    SortListButton["bg"]=SkinColor.get()
    MoveUpButton["bg"]=SkinColor.get()
    MoveDownButton["bg"]=SkinColor.get()
    CutSelectedButton["bg"]=SkinColor.get()
    SearchButton["bg"]=SkinColor.get()
    #changing labels
    labelPlaying["fg"]=SkinColor.get()
    labelDuration["fg"]=SkinColor.get()
    labelSize["fg"]=SkinColor.get()
    labelVolumeLevel["fg"]=SkinColor.get()
    labelFilesToPlay["fg"]=SkinColor.get()
    labelLength["fg"]=SkinColor.get()
    labelGenre["fg"]=SkinColor.get()
    labelStartTime["fg"]=SkinColor.get()
    labelEndTime["fg"]=SkinColor.get()
    #changing listbox
    listbox["bg"]=SkinColor.get()
    #changing style of progress bar:
    styl.configure("Horizontal.TProgressbar", background = SkinColor.get())
    #changing background
    index = skinOptions[1].index(SkinColor.get())
    backgroundFile = skinOptions[0][index]
    if os.path.exists(backgroundFile):
        if os.path.isfile(backgroundFile):
            background_image = tk.PhotoImage(file=backgroundFile)
            background_label.configure(image=background_image)
            background_label.image = background_image
            play_list.skin = index
    changeFonts() #change the font that comes with the new skin

def view_playlist(loading=False):
    global play_list
    if loading:
        #prepare the loaded info to coincide with the function call:
        if play_list.viewModel == "COMPACT": play_list.viewModel = "FULLSCREEN"
        elif play_list.viewModel == "PLAYLIST": play_list.viewModel = "COMPACT"
        elif play_list.viewModel == "FULLSCREEN": play_list.viewModel = "PLAYLIST"
    if play_list.viewModel == "FULLSCREEN":
        play_list.viewModel = "COMPACT"
        window.wm_attributes("-fullscreen", False)
        window.geometry("500x430+100+100")
        ViewPlaylistButtonText.set("Compact View")
    elif play_list.viewModel == "COMPACT":
        play_list.viewModel = "PLAYLIST"
        window.geometry("1190x600+100+100")
        ViewPlaylistButtonText.set("Playlist View")
    elif play_list.viewModel == "PLAYLIST":
        window.wm_attributes("-fullscreen", True)
        ViewPlaylistButtonText.set("Fullscreen View")
        play_list.viewModel = "FULLSCREEN"

def repeat():
    global play_list
    if (play_list.REPEAT==0):
        RepeatButtonText.set("Repeat All")
        play_list.REPEAT = 1
    elif (play_list.REPEAT==1):
        RepeatButtonText.set("Repeat One")
        play_list.REPEAT = 2
    else:
        RepeatButtonText.set("Repeat Off")
        play_list.REPEAT = 0

def randomize():
    if len(play_list.validFiles) > 0:
        #Changing list to set, the set is automatically randomized, then changing it back again
        random.shuffle(play_list.validFiles)
        # 0-onrating, 1-sorted, 2-reversed, 3-random
        play_list.isListOrdered = 3 #3 - is the value for randomized
        displayElementsOnPlaylist()
        updateSortButton() #put the correct message on the Sort Button

def navigationSound(event):
    if len(play_list.validFiles) > 0:
        e = event.widget
        x = play_list.validFiles[play_list.currentSongIndex].Length / 470
        play_list.currentSongPosition = (event.x * x)
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(play_list.currentSongPosition)
        progress["value"] = play_list.currentSongPosition
        play_list.RESUMED = True
        # print("Length: " + str(play_list.validFiles[play_list.currentSongIndex].Length) + " X: "+ str(event.x * x))

def on_closing(): #this function is called only when window is canceled
    global APPLICATION_EXIT
    APPLICATION_EXIT = True
    # Make a backup of everything:
    if(len(play_list.validFiles) == 0):
        #if empty set these field so that when next song will be added they won't take effect
        play_list.isSongPause = False
        play_list.isSongStopped = False
        play_list.isListOrdered = 0  # 0-onrating ; 1-sorted 2-reversed; 3-random;
        play_list.currentSongIndex = None
        play_list.currentSongPosition = 0
        play_list.RESUMED = False
    file = open(automaticallyBackupFile, "wb")
    pickle.dump(play_list, file)
    window.quit()
    sys.exit()

def remove_song():
    global listBox_Song_selected_index
    if len(play_list.validFiles)>0:
        if listBox_Song_selected_index!="":
            del play_list.validFiles[listBox_Song_selected_index]
            displayElementsOnPlaylist()
            textFilesToPlay.set("Files To Play: " + str(len(play_list.validFiles)))
            #listBox_Song_selected_index="" #initialize this if u want to remove only onebyone
            # Maintain the selection
            listbox.select_set(listBox_Song_selected_index)

def list_selected_item(event):
    if listbox.size() > 0:
        global listBox_Song_selected_index
        listboxSelectedEvent = event.widget
        index = int(listboxSelectedEvent.curselection()[0])
        listBox_Song_selected_index = index
        #do this if u want to play the selected song in the listbox when hitting PLAY button
        #play_list.currentSongIndex = index # if uncomment this when a song is selected and the playlist and hit PLAY
        #the song will maintain the same currentSongPosition value as the previous one.

def sort_list():
    # 0-onrating, 1-sorted, 2-reversed, 3-random
    if len(play_list.validFiles) > 0:
        Song = play_list.validFiles[play_list.currentSongIndex]
        if play_list.isListOrdered == 0:
            play_list.isListOrdered = 1
            play_list.validFiles.sort(key=lambda Song: Song.fileName)  # sort the list according to fileName
        elif play_list.isListOrdered == 1:
            play_list.isListOrdered = 2
            play_list.validFiles.reverse()
        elif play_list.isListOrdered == 2:
            play_list.isListOrdered = 3
            randomize() #let them be randomized
        else:
            play_list.isListOrdered = 0
            play_list.validFiles.sort(key=lambda Song: Song.Rating, reverse=True)  # sort the list according to Rating
        #the currentSongIndex has changed
        play_list.currentSongIndex = play_list.validFiles.index(Song)
        updateSortButton()
        displayElementsOnPlaylist()

def UpdateSongRating():
    if len(play_list.validFiles) > 0:
        if pygame.mixer.get_init() != None:
            if pygame.mixer.music.get_busy() or play_list.isSongPause:
                play_list.validFiles[play_list.currentSongIndex].Rating = int(songRating.get())
                updateRadioButtons()
                if play_list.isListOrdered==0 and SortButtonText.get() != "Custom": #if playlist is ordered by rating, update it in real time, since rating has changed
                    Song = play_list.validFiles[play_list.currentSongIndex]
                    play_list.validFiles.sort(key=lambda Song: Song.Rating, reverse=True)  # sort the list according to Rating
                    play_list.currentSongIndex=play_list.validFiles.index(Song)
                    displayElementsOnPlaylist()
                    listBox_Song_selected_index = play_list.currentSongIndex
                    # Maintain the selection in the listbox
                    listbox.selection_clear(0, tk.END)  # clear existing selection
                    # Maintain the selection
                    listbox.select_set(listBox_Song_selected_index)

def updateRadioButtons():
    songRating.set(str(play_list.validFiles[play_list.currentSongIndex].Rating))
    if (int(songRating.get()) == 1):
        changeRadioButtonColor("orangered")
    elif (int(songRating.get()) == 2):
        changeRadioButtonColor("deeppink")
    elif (int(songRating.get()) == 3):
        changeRadioButtonColor("lightpink")
    elif (int(songRating.get()) == 4):
        changeRadioButtonColor("greenyellow")
    elif (int(songRating.get()) == 5):
        changeRadioButtonColor("lightgreen")
    else:
        changeRadioButtonColor("lightgray")
    songRating.set(str(play_list.validFiles[play_list.currentSongIndex].Rating))

def changeRadioButtonColor(color):
    R1["bg"] = color
    R2["bg"] = color
    R3["bg"] = color
    R4["bg"] = color
    R5["bg"] = color

def move_up():
    global listBox_Song_selected_index
    if listBox_Song_selected_index != "":
        Song = play_list.validFiles[listBox_Song_selected_index] #this is the auxiliar variable
        if(listBox_Song_selected_index-1 > 0):
            #interchanging values
            play_list.validFiles[listBox_Song_selected_index] = play_list.validFiles[listBox_Song_selected_index-1]
            play_list.validFiles[listBox_Song_selected_index - 1] = Song
            listBox_Song_selected_index -=1
        else:
            last_position = len(play_list.validFiles) - 1
            play_list.validFiles[listBox_Song_selected_index] = play_list.validFiles[last_position]
            play_list.validFiles[last_position] = Song
            listBox_Song_selected_index = last_position
        displayElementsOnPlaylist()
        # listBox_Song_selected_index="" #initialize this if u want to move only onebyone
        #Maintain the selection
        listbox.select_set(listBox_Song_selected_index)
        SortButtonText.set("Custom")
def move_down():
    global listBox_Song_selected_index
    if listBox_Song_selected_index != "":
        Song = play_list.validFiles[listBox_Song_selected_index]  # this is the auxiliar variable
        if (listBox_Song_selected_index + 1 < len(play_list.validFiles)):
            # interchanging values
            play_list.validFiles[listBox_Song_selected_index] = play_list.validFiles[listBox_Song_selected_index + 1]
            play_list.validFiles[listBox_Song_selected_index + 1] = Song
            listBox_Song_selected_index += 1
        else:
            play_list.validFiles[listBox_Song_selected_index] = play_list.validFiles[0]
            play_list.validFiles[0] = Song
            listBox_Song_selected_index = 0
        displayElementsOnPlaylist()
        # listBox_Song_selected_index="" #initialize this if u want to move only onebyone
        # Maintain the selection
        listbox.select_set(listBox_Song_selected_index)
        SortButtonText.set("Custom")

def changeFonts():
    allButtonsFont = skinOptions[2][play_list.skin]
    OpenFileButton["font"] = allButtonsFont
    OpenDirectoryButton["font"] = allButtonsFont
    PlayButton["font"] = allButtonsFont
    PauseButton["font"] = allButtonsFont
    StopButton["font"] = allButtonsFont
    NextButton["font"] = allButtonsFont
    PreviousButton["font"] = allButtonsFont
    VolumeDownButton["font"] = allButtonsFont
    VolumeUpButton["font"] = allButtonsFont
    ShuffleButton["font"] = allButtonsFont
    SavePlaylistButton["font"] = allButtonsFont
    NewPlaylistButton["font"] = allButtonsFont
    ViewPlaylistButton["font"] = allButtonsFont
    RepeatButton["font"] = allButtonsFont
    RendomizeListButton["font"] = allButtonsFont
    RemoveSongButton["font"] = allButtonsFont
    SortListButton["font"] = allButtonsFont
    MoveUpButton["font"] = allButtonsFont
    MoveDownButton["font"] = allButtonsFont
    CutSelectedButton["font"] = allButtonsFont
    SearchButton["font"] = allButtonsFont
    # changing labels
    labelPlaying["font"] = allButtonsFont
    labelDuration["font"] = allButtonsFont
    labelSize["font"] = allButtonsFont
    labelVolumeLevel["font"] = allButtonsFont
    labelFilesToPlay["font"] = allButtonsFont
    labelLength["font"] = allButtonsFont
    labelGenre["font"] = allButtonsFont
    labelStartTime["font"] = allButtonsFont
    labelEndTime["font"] = allButtonsFont
    # changing listbox
    listbox["font"] = allButtonsFont

def packPositionButton():
    # Put the buttons on the window
    OpenFileButton.pack()
    OpenDirectoryButton.pack()
    PlayButton.pack()
    PauseButton.pack()
    StopButton.pack()
    NextButton.pack()
    PreviousButton.pack()
    VolumeDownButton.pack()
    VolumeUpButton.pack()
    ShuffleButton.pack()
    SavePlaylistButton.pack()
    NewPlaylistButton.pack()
    ViewPlaylistButton.pack()
    RepeatButton.pack()
    RendomizeListButton.pack()
    RemoveSongButton.pack()
    SortListButton.pack()
    MoveUpButton.pack()
    MoveDownButton.pack()
    CutSelectedButton.pack()
    SearchButton.pack()

    # Placing the buttons in the widget

    # column1:
    horizontalButtonsColumnStartCoord = 5
    horizontalSpaceBetweenButtonColumns = 168
    verticalButtonsColumnStartCoord = 5

    RepeatButton.place(x=horizontalButtonsColumnStartCoord, y=5)
    ViewPlaylistButton.place(x=horizontalButtonsColumnStartCoord, y=37)
    PreviousButton.place(x=horizontalButtonsColumnStartCoord, y=69)
    VolumeDownButton.place(x=horizontalButtonsColumnStartCoord, y=101)
    ShuffleButton.place(x=horizontalButtonsColumnStartCoord, y=133)

    # column2:
    horizontalButtonsColumnStartCoord += horizontalSpaceBetweenButtonColumns

    OpenFileButton.place(x=horizontalButtonsColumnStartCoord, y=5)
    OpenDirectoryButton.place(x=horizontalButtonsColumnStartCoord, y=37)
    PlayButton.place(x=horizontalButtonsColumnStartCoord, y=69)
    PauseButton.place(x=horizontalButtonsColumnStartCoord, y=101)
    StopButton.place(x=horizontalButtonsColumnStartCoord, y=133)

    # column3:
    horizontalButtonsColumnStartCoord += horizontalSpaceBetweenButtonColumns

    RendomizeListButton.place(x=horizontalButtonsColumnStartCoord, y=5)
    NewPlaylistButton.place(x=horizontalButtonsColumnStartCoord, y=37)
    NextButton.place(x=horizontalButtonsColumnStartCoord, y=69)
    VolumeUpButton.place(x=horizontalButtonsColumnStartCoord, y=101)
    SavePlaylistButton.place(x=horizontalButtonsColumnStartCoord, y=133)

    # under playlist
    RemoveSongButton.place(x=600, y=620)
    SortListButton.place(x=768, y=620)
    MoveUpButton.place(x=936, y=620)
    MoveDownButton.place(x=1104, y=620)

    #under radio rating buttons
    horizontalButtonsColumnStartCoord = 5
    CutSelectedButton.place(x=horizontalButtonsColumnStartCoord, y=490)
    horizontalButtonsColumnStartCoord+=horizontalSpaceBetweenButtonColumns
    SearchButton.place(x=horizontalButtonsColumnStartCoord, y=490)

def packPositionLabels():
    # Put the labels on the screen
    labelPlaying.pack()
    labelDuration.pack()
    labelSize.pack()
    labelVolumeLevel.pack()
    labelFilesToPlay.pack()
    labelLength.pack()
    labelGenre.pack()
    labelStartTime.pack()
    labelEndTime.pack()

    # Placing the labels
    labelDuration.place(x=10, y=210)
    labelSize.place(x=10, y=230)
    labelPlaying.place(x=10, y=250)
    labelVolumeLevel.place(x=10, y=270)
    labelFilesToPlay.place(x=10, y=290)
    labelLength.place(x=10, y=310)
    labelGenre.place(x=10, y=330)
    labelStartTime.place(x=10, y=350)
    labelEndTime.place(x=10, y=370)

def pressedEnter(event):
    play_music()

def pressedKeyShortcut(event):
    if event.char == " ":
         pause_music()
    elif event.char == "m":
        if pygame.mixer.get_init():
            if pygame.mixer.music.get_volume()>0:
                pygame.mixer.music.set_volume(0)
                textVolumeLevel.set("Volume Level: Mute")
            else:
                pygame.mixer.music.set_volume(play_list.VolumeLevel)
                textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    elif event.char == ",":
        volume_up()
    elif event.char == ".":
        volume_down()
    elif event.char == "r":
        repeat()
    elif event.char == "c":
        view_playlist()
    elif event.char == "x":
        next_song()
    elif event.char =="z":
        previous_song()
    elif event.char =="s":
        shuffle()
    elif event.char =="d":
        stop_music()
    elif event.char == "1":
        if pygame.mixer.get_init():
            play_list.VolumeLevel = 0.1
            pygame.mixer.music.set_volume(play_list.VolumeLevel)
            textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    elif event.char == "2":
        if pygame.mixer.get_init():
            play_list.VolumeLevel = 0.2
            pygame.mixer.music.set_volume(play_list.VolumeLevel)
            textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    elif event.char == "3":
        if pygame.mixer.get_init():
            play_list.VolumeLevel = 0.3
            pygame.mixer.music.set_volume(play_list.VolumeLevel)
            textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    elif event.char == "4":
        if pygame.mixer.get_init():
            play_list.VolumeLevel = 0.4
            pygame.mixer.music.set_volume(play_list.VolumeLevel)
            textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    elif event.char == "5":
        if pygame.mixer.get_init():
            play_list.VolumeLevel = 0.5
            pygame.mixer.music.set_volume(play_list.VolumeLevel)
            textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    elif event.char == "6":
        if pygame.mixer.get_init():
            play_list.VolumeLevel = 0.6
            pygame.mixer.music.set_volume(play_list.VolumeLevel)
            textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    elif event.char == "7":
        if pygame.mixer.get_init():
            play_list.VolumeLevel = 0.7
            pygame.mixer.music.set_volume(play_list.VolumeLevel)
            textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    elif event.char == "8":
        if pygame.mixer.get_init():
            play_list.VolumeLevel = 0.8
            pygame.mixer.music.set_volume(play_list.VolumeLevel)
            textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    elif event.char == "8":
        if pygame.mixer.get_init():
            play_list.VolumeLevel = 0.9
            pygame.mixer.music.set_volume(play_list.VolumeLevel)
            textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    elif event.char == "0":
        if pygame.mixer.get_init():
            play_list.VolumeLevel = 1.0
            pygame.mixer.music.set_volume(play_list.VolumeLevel)
            textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    elif event.char == "i":
        messagebox.showinfo("Information", "Congratulation for discovering navigational keys! \n\n"
                + "As you might not know all the keys, here is a full guide:\n\n"
                + "S - is equivalent to Shuffle Button.\n"
                + "D - is equivalent to Stop Button.\n"
                + "R - is equivalent to Repeat Button.\n"
                + "Z - is equivalent to Previous Button.\n"
                + "X - is equivalent to Next Button.\n"
                + "C - is equivalent to View Button.\n"
                + "M - is equivalent to Mute.\n"
                + "Q - is equivalent to Cut Selected Button\n"
                + "J - is equivalent to Search Button\n"
                + "[1-0] - are equivalent to Volume.\n"
                + "SPACE - is equivalent to Pause.\n"
                + "Enter - is equivalent to Play.\n"
                + ", or < key - is equivalent to Volume Up.\n"
                + ". or > key - is equivalent to Volume Down.\n"
                + "Page Up or Up - can be used to navigate the playlist UP.\n"
                + "Page Down or Down - can be used to navigate the playlist DOWN.\n"
                + "i - will show you this message again.")
    elif event.char == "q":
        showCuttingTool()
    elif event.char =="j":
        searchSongInPlaylist()


def rightClickListboxElement(event):
    if listBox_Song_selected_index != "" and listbox.size():
        element = play_list.validFiles[listBox_Song_selected_index]
        messagebox.showinfo("Song Info", "Filename: " + str(element.fileName) + "\n"
                                        + "Path: " + str(element.filePath) + "\n"
                                        + "Length: {:0>8}" .format(str(datetime.timedelta(seconds = int(element.Length))) ) + "\n"
                                        + "Start Time: {:0>8}" .format(str(datetime.timedelta(seconds = int(element.startPos))) ) + "\n"
                                        + "End Time: {:0>8}" .format(str(datetime.timedelta(seconds = int(element.endPos))) ) + "\n"
                                        + "Size: " + str(element.fileSize) + "\n"
                                        + "Rating: " + str(element.Rating) + "\n")
        #print("Element: " + str(element))

def packPositionListScrolOptionProgRadio():
    #Here are set position, events, controls, styling for listbox, progressbar, scrollbar, option, radiobuttons
    listbox.pack()
    listbox.bind('<Double-Button>', elementPlaylistDoubleClicked)
    listbox.bind('<ButtonPress-3>', rightClickListboxElement)
    listbox.bind('<<ListboxSelect>>', list_selected_item)
    listbox.bind("<Return>", pressedEnter)
    listbox.bind("<Key>", pressedKeyShortcut)
    listbox.place(x=600, y=10)
    scroll.place(x=1165, y=10)
    scroll.config(command=listbox.yview)
    option.bind("<<ComboboxSelected>>", changeSkin)
    option.pack()
    option.place(x=350, y=180)
    styl.theme_use('clam')
    styl.configure("Horizontal.TProgressbar", foreground='red', background='blue')
    progress.bind("<Button>", navigationSound)
    progress.pack()
    progress.place(x=10, y=405)
    R1.pack()
    R2.pack()
    R3.pack()
    R4.pack()
    R5.pack()
    radioButtonLineHeight = 445
    R1.place(x=10, y=radioButtonLineHeight)
    R2.place(x=45, y=radioButtonLineHeight)
    R3.place(x=80, y=radioButtonLineHeight)
    R4.place(x=115, y=radioButtonLineHeight)
    R5.place(x=150, y=radioButtonLineHeight)

def showCuttingTool():
    if listbox.size() and listBox_Song_selected_index!= "":
        dialog = CuttingTool(window)
    else:
        messagebox.showinfo("No file selected", "Use the playlist to select a song.")

def fontTransition(Message):
    Message = list(Message)
    for x in range(0, len(Message)):
        if Message[x] == "_":
            if(x+1<len(Message)):
                Message[x] = Message[x+1]
                Message[x+1] = "_"
            else:
                Message[x] = Message[0]
                Message[0] = "_"
    return "".join(Message)

def searchSongInPlaylist():
    SearchTool(window)

window = tk.Tk() #tk.Tk() return a widget which is window
Project_Title = "_PyPlay MP3 Player in Python_"
window.title(Project_Title)

window.geometry("500x430+100+100")# build a window 30x280 on size at position 500 x 300 (almost center of screen)
window.protocol("WM_DELETE_WINDOW", on_closing)

SkinColor = StringVar()
SkinColor.set(skinOptions[1][play_list.skin])
backgroundFile = skinOptions[0][play_list.skin]

background_image=tk.PhotoImage(file=backgroundFile)
background_label = tk.Label(window, image=background_image)
background_label.pack()
background_label.place(x=0, y=0, relwidth=1, relheight=1)

OpenFileButton = tk.Button(window,  #the first parameter is the widget
                   text='Open File',  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=load_file, #the width of the button, and the function which get called when clicking it
                   bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

OpenDirectoryButton = tk.Button(window,  #the first parameter is the widget
                   text='Open Directory',  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=load_directory, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

PlayButton = tk.Button(window,  #the first parameter is the widget
                   text='Play',  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=play_music, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

PausedButtonText = StringVar()
PausedButtonText.set("Pause")
PauseButton = tk.Button(window,  #the first parameter is the widget
                   textvariable=PausedButtonText,  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=pause_music, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

StopButton = tk.Button(window,  #the first parameter is the widget
                   text="Stop",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=stop_music, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                    font=allButtonsFont) #this is the font, size and type

NextButton = tk.Button(window,  #the first parameter is the widget
                   text="Next",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=next_song, #the width of the button, and the function which get called when clicking it
                       bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

PreviousButton = tk.Button(window,  #the first parameter is the widget
                   text="Previous",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=previous_song, #the width of the button, and the function which get called when clicking it
                           bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

VolumeDownButton = tk.Button(window,  #the first parameter is the widget
                   text="Volume Down",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=volume_down, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

VolumeUpButton = tk.Button(window,  #the first parameter is the widget
                   text="Volume Up",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=volume_up, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

ShuffleButtonText = StringVar()
ShuffleButtonText.set("Shuffle Off")

ShuffleButton = tk.Button(window,  #the first parameter is the widget
                   textvariable=ShuffleButtonText,  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=shuffle, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

SavePlaylistButton = tk.Button(window,  #the first parameter is the widget
                   text="Save Playlist",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=save_playlist, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

NewPlaylistButton = tk.Button(window,  #the first parameter is the widget
                   text="New Playlist",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=new_playlist, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

ViewPlaylistButtonText = StringVar()
ViewPlaylistButtonText.set("Compact View")

ViewPlaylistButton = tk.Button(window,  #the first parameter is the widget
                   textvariable=ViewPlaylistButtonText,  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=view_playlist, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

RepeatButtonText = StringVar()
RepeatButtonText.set("Repeat All")

RepeatButton = tk.Button(window,  #the first parameter is the widget
                   textvariable=RepeatButtonText,  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=repeat, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

RendomizeListButton = tk.Button(window,  #the first parameter is the widget
                   text="Randomize List",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=randomize, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

RemoveSongButton = tk.Button(window,  #the first parameter is the widget
                   text="Remove Song",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=remove_song, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

SortButtonText = StringVar()
SortButtonText.set("Sorted")

SortListButton = tk.Button(window,  #the first parameter is the widget
                   textvariable=SortButtonText,  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=sort_list, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

MoveUpButton = tk.Button(window,  #the first parameter is the widget
                   text="Move Up",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=move_up, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

MoveDownButton = tk.Button(window,  #the first parameter is the widget
                   text="Move Down",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=move_down, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

CutSelectedButton = tk.Button(window,  #the first parameter is the widget
                   text="Cut Selected",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=showCuttingTool, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

SearchButton = tk.Button(window,  #the first parameter is the widget
                   text="Search File",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=searchSongInPlaylist, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg="white",  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

packPositionButton()

#Building the labels
SongName = StringVar()
SongName.set("Currently Playing: ")

labelPlaying = tk.Label(window, textvariable=SongName, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont)  # creating a label on the window

SongDuration = StringVar()
SongDuration.set("Progress: ")

labelDuration = tk.Label(window, textvariable=SongDuration, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont)  # creating a label on the window

SongSize = StringVar()
SongSize.set("Size: ")

labelSize = tk.Label(window, textvariable=SongSize, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont)  # creating a label on the window
textVolumeLevel = StringVar()
textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel*100)) + "%")
labelVolumeLevel = tk.Label(window, textvariable=textVolumeLevel, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont)  # creating a label on the window

textFilesToPlay = StringVar()
textFilesToPlay.set("Files To Play: " + str(len(play_list.validFiles)))
labelFilesToPlay = tk.Label(window, textvariable=textFilesToPlay, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont)  # creating a label on the window

textLength = StringVar()
textLength.set("Length: ")
labelLength = tk.Label(window, textvariable=textLength, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont)  # creating a label on the window

textGenre = StringVar()
textGenre.set("Genre: ")
labelGenre = tk.Label(window, textvariable=textGenre, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont)  # creating a label on the window

textStartTime = StringVar()
textStartTime.set("Start Time: ")
labelStartTime = tk.Label(window, textvariable=textStartTime, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont)  # creating a label on the window

textEndTime = StringVar()
textEndTime.set("End Time: ")
labelEndTime = tk.Label(window, textvariable=textEndTime, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont)  # creating a label on the window

packPositionLabels()


#Creating a listbox
scroll = tk.Scrollbar(window, orient="vertical")
listbox = tk.Listbox(window, fg="white", font=allButtonsFont, width=80, bg=SkinColor.get(), height=35, \
                     yscrollcommand=scroll.set)

#Creating Combobox
option = Combobox(window, textvariable=SkinColor, values = skinOptions[1])

#Creating style for progressbar
styl = ttk.Style()

#Creating Progress bar
progress = Progressbar(orient=tk.HORIZONTAL, length=470, mode='indeterminate', value=0, maximum = 100, \
                       style="Horizontal.TProgressbar",) #using the same style

#Creating RadioButton
songRating = StringVar()
songRating.set("0") # initialize

R1 = tk.Radiobutton(window, text="1", variable=songRating, value=1, width=3, bg="lightgray", command=UpdateSongRating)
R2 = tk.Radiobutton(window, text="2", variable=songRating, value=2, width=3, bg="lightgray", command=UpdateSongRating)
R3 = tk.Radiobutton(window, text="3", variable=songRating, value=3, width=3, bg="lightgray", command=UpdateSongRating)
R4 = tk.Radiobutton(window, text="4", variable=songRating, value=4, width=3, bg="lightgray", command=UpdateSongRating)
R5 = tk.Radiobutton(window, text="5", variable=songRating, value=5, width=3, bg="lightgray", command=UpdateSongRating)

packPositionListScrolOptionProgRadio()

scheduler = sched.scheduler(time.time, time.sleep)

#Load backup if possible
if os.path.exists(automaticallyBackupFile):
    loadPlaylistFile(automaticallyBackupFile)

window.mainloop() #loop through the window