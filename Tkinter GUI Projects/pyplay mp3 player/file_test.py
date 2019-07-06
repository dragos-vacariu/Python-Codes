import Tkinter
from Tkinter import StringVar
from ttk import Progressbar, Combobox

#tkinter._test()

import Tkinter as tk

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
play_list = Playlist()

allButtonsFont = skinOptions[2][play_list.skin] #default Font value Consola 10 bold:
#default value of play_list.skin is 0

def load_file(): pass
def load_directory():pass
def play_music():pass
def pause_music():pass
def stop_music(): pass
def next_song(): pass
def previous_song(): pass
def remove_song(): pass
def randomize(): pass
def volume_down(): pass
def volume_up(): pass
def move_down():pass
def move_up():pass
def shuffle(): pass
def save_playlist(): pass
def new_playlist():pass
def view_playlist():pass
def sort_list(): pass
def showCuttingTool(): pass
def searchSongInPlaylist(): pass
def repeat(): pass

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
    #file = open(automaticallyBackupFile, "wb")
    #pickle.dump(play_list, file)
    window.quit()
    sys.exit()

window = tk.Tk() #tk.Tk() return a widget which is window
Project_Title = "_PyPlay MP3 Player in Python_"
window.title(Project_Title)

backgroundFile = skinOptions[0][play_list.skin]

background_image=tk.PhotoImage(file=backgroundFile)
background_label = tk.Label(window, image=background_image)
background_label.pack()
background_label.place(x=0, y=0, relwidth=1, relheight=1)

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

progress = Progressbar(orient=tk.HORIZONTAL, length=470, mode='indeterminate', value=0, maximum = 100, \
                       style="Horizontal.TProgressbar",) #using the same style

window.mainloop() #loop through the window