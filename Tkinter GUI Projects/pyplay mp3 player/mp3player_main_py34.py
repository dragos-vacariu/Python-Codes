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
from PIL import ImageTk, Image
import subprocess
import math
import shutil
import urllib3
from bs4 import BeautifulSoup

class Playlist:
    def __init__(self):
        self.isSongPause = False
        self.isSongStopped = False
        self.VolumeLevel=1.0
        self.useMassFileEditor=False
        self.dirFilePath = None
        self.danthologyMode=False
        self.danthologyDuration=0
        self.danthologyTimer=0
        self.windowOpacity=1.0
        self.progressTime = "Ascending" #possible values: Ascending and Descending
        self.skin=0
        self.SHUFFLE = False
        self.isListOrdered = 0 #0-on songrating ; 1-sorted by name 2-sorted by name reversed; 3-random ....;
        self.validFiles = []
        self.slideImages = []
        self.slideImagesTransitionSeconds = 0;
        self.usePlayerTitleTransition = True
        self.playingFileNameTransition = "separation" # values : separation, typewriting, none
        self.usingSlideShow = False
        self.slideImageIndex = 0
        self.currentSongIndex = None
        self.currentSongPosition = 0
        self.REPEAT = 1 # 1 is value for repeat all
        self.RESUMED=False
        self.viewModel = "FULLSCREEN"
        self.playTime = 0
        self.customFont = None
        self.customElementBackground = None
        self.customLabelBackground = None
        self.customBackgroundPicture = None
        self.customFontColor = None
        self.customChangeBackgroundedLabelsColor = None
        self.userCreatedColors = []
        self.ProgressBarType = "determinate"
        self.LyricsActiveSource = LyricsOnlineSources[0] #default, all sources

class Song:
    def __init__(self, filename, filepath, filesize):
        self.fileName = filename
        self.filePath = filepath
        self.fileSize = filesize
        self.Rating = 0
        self.NumberOfPlays = 0
        audio = MP3(self.filePath)
        self.sample_rate = audio.info.sample_rate
        self.channels = audio.info.channels
        self.Length = audio.info.length
        
        mp3 = MP3(self.filePath) # if the mp3 file has no tags, then the tags will be added to the file.
        if mp3.tags is None:
            mp3.add_tags()
            mp3.save()
        audio = EasyID3(self.filePath)
        try:
            self.Genre = audio["genre"]
        except: #enter here if you can't get the genre
            self.Genre = "Various"
        else:
            self.Genre = self.Genre[0]
        try:
            self.Artist = audio["artist"]
        except:
            self.Artist = "Various"
        else:
            self.Artist = self.Artist[0]
        try:
            self.Title = audio["title"]
        except:
            self.Title = "Various"
        else:
            self.Title = self.Title[0]
        try:
            self.Year = audio["date"]
        except:
            self.Year = "Various"
        else:
            self.Year = self.Year[0]
        try:
            self.Album = audio["album"]
        except:
            self.Album = "Various"
        else:
            self.Album = self.Album[0]
        self.startPos = 0
        self.endPos = self.Length
        self.fadein_duration = 0
        self.fadeout_duration = 0

class CuttingTool:
    def __init__(self, parent):
        global allButtonsFont
        global dialog
        color = OpenFileButton["bg"]  # get the color which the rest of elements is using at the moment
        if play_list.currentSongIndex != None:
            self.top = tk.Toplevel(parent, bg=color)
            self.top.protocol("WM_DELETE_WINDOW", self.destroy)
            Window_Title = "Cutting Tool"
            self.top.title(Window_Title)
            self.top.geometry("380x300+100+100")
            self.top.attributes('-alpha', play_list.windowOpacity)
            allButtonsFont = skinOptions[2][play_list.skin]
            columnOne = 10
            columnTwo = 220
            self.InfoLabelText = StringVar()
            self.InfoLabelText.set("Welcome to MP3 Cutting capability:\n\n"
                               +"Please enter Start and End value and Hit OK.\n"
                                +"This will NOT change the original file.\n\n\n")
            tk.Label(self.top, textvariable=self.InfoLabelText, fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=40, y=10)
            tk.Label(self.top, text="Start Value (0 - " + str(int(play_list.validFiles[play_list.currentSongIndex].Length)) + "):",
                                            fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=columnOne, y=100)

            self.startValue = tk.Entry(self.top)
            self.startValue.place(x=columnOne, y=120)
            self.startValue.bind("<Return>", self.cutItem)

            tk.Label(self.top, text="End Value (0 - " + str(int(play_list.validFiles[play_list.currentSongIndex].Length)) + "):", fg=fontColor.get(),
                                          font=allButtonsFont, bg=color).place(x=columnOne, y=140)
            self.endValue = tk.Entry(self.top)
            self.endValue.place(x=columnOne, y=160)

            self.endValue.bind("<Return>", self.cutItem)
            self.buttonOK = tk.Button(self.top, text="OK", command=self.okButtonPressed, bg=color, fg=fontColor.get(), font=allButtonsFont)
            self.buttonOK.place(x=columnOne, y=190)

            tk.Label(self.top, text="Add FadeIn: ", fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=columnTwo, y=100)
            self.FadeIn = StringVar()
            self.FadeIn.set(str(play_list.validFiles[play_list.currentSongIndex].fadein_duration))
            fadeOptions = ["5","10","15", "20"]
            self.fadeInBox = Combobox(self.top, textvariable=self.FadeIn, values=fadeOptions)
            self.fadeInBox.place(x=columnTwo, y=120)
            self.fadeInBox.bind("<<ComboboxSelected>>", self.addFadeIn)

            tk.Label(self.top, text="Add FadeOut: ", fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=columnTwo, y=140)
            self.FadeOut = StringVar()
            self.FadeOut.set(str(play_list.validFiles[play_list.currentSongIndex].fadeout_duration))
            self.fadeOutBox = Combobox(self.top, textvariable=self.FadeOut, values=fadeOptions)
            self.fadeOutBox.place(x=columnTwo, y=160)
            self.fadeOutBox.bind("<<ComboboxSelected>>", self.addFadeOut)
            self.top.bind("<Escape>", self.destroyEsc)
            self.top.bind("<Tab>", self.focus_Input)
            self.addFadeInOutAll = tk.Button(self.top, text="Add Fading to All", command=self.addFadingOnPlaylist,
                                             bg=color,
                                             fg=fontColor.get(), font=allButtonsFont)
            self.addFadeInOutAll.place(x=columnTwo, y=190)

            self.restoreButton = tk.Button(self.top, text="Restore Defaults for This Song", command=self.restoreCurrentSong, bg=color, fg=fontColor.get(), font=allButtonsFont)
            self.restoreButton.place(x=80, y=230)

            self.restoreForAllButton = tk.Button(self.top, text="Restore Defaults for All Songs",
                                           command=self.restoreAllSongs, bg=color, fg=fontColor.get(),
                                           font=allButtonsFont)
            self.restoreForAllButton.place(x=80, y=260)

            dialog = self #each instance of CuttingTool will be assigned to this variable:

    def addFadingOnPlaylist(self):
        global play_list
        for song in play_list.validFiles:
            song.fadein_duration = int(self.FadeIn.get())
            song.fadeout_duration = int(self.FadeOut.get())

    def restoreCurrentSong(self):
        global Playlist
        play_list.validFiles[play_list.currentSongIndex].fadein_duration = 0
        play_list.validFiles[play_list.currentSongIndex].fadeout_duration = 0
        play_list.validFiles[play_list.currentSongIndex].startPos = 0
        play_list.validFiles[play_list.currentSongIndex].endPos = play_list.validFiles[play_list.currentSongIndex].Length
        self.FadeIn.set(str(play_list.validFiles[play_list.currentSongIndex].fadein_duration))
        self.FadeOut.set(str(play_list.validFiles[play_list.currentSongIndex].fadeout_duration))

    def restoreAllSongs(self):
        global Playlist
        global play_list
        for song in play_list.validFiles:
            song.fadein_duration = 0
            song.fadeout_duration = 0
        self.FadeIn.set(str(play_list.validFiles[play_list.currentSongIndex].fadein_duration))
        self.FadeOut.set(str(play_list.validFiles[play_list.currentSongIndex].fadeout_duration))

    def take_focus(self):
        self.top.wm_attributes("-topmost", 1)
        self.top.grab_set()
        self.startValue.focus_force()

    def focus_Input(self, event):
        if self.startValue.focus_get():
            self.endValue.focus_force()
        else:
            self.startValue.focus_force()

    def destroyEsc(self,event):
        self.destroy()

    def destroy(self):
        global dialog
        self.top.destroy()
        dialog = None

    def addFadeIn(self, event):
        global play_list
        if play_list.currentSongIndex !=None:
            play_list.validFiles[play_list.currentSongIndex].fadein_duration = int(self.FadeIn.get())
            textFadeIn.set("FadeIn: " + str(play_list.validFiles[play_list.currentSongIndex].fadein_duration)+"s")

    def addFadeOut(self, event):
        global play_list
        if play_list.currentSongIndex!= None:
            play_list.validFiles[play_list.currentSongIndex].fadeout_duration = int(self.FadeOut.get())
            textFadeOut.set("FadeOut: " + str(play_list.validFiles[play_list.currentSongIndex].fadeout_duration)+"s")

    def cutItem(self, event):
        self.okButtonPressed()

    def okButtonPressed(self):
        global dialog
        if self.startValue.get()!="" and play_list.currentSongIndex!=None:
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
        if self.endValue.get() != "" and play_list.currentSongIndex!=None:
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

class SearchTool:
    def __init__(self, parent):
        global allButtonsFont
        global dialog
        self.index = None
        color = OpenFileButton["bg"]  # get the color which the rest of elements is using at the moment
        self.top = tk.Toplevel(parent, bg=color)
        Window_Title = "Search Tool"
        self.top.title(Window_Title)
        self.top.geometry("300x180+100+100")
        self.top.protocol("WM_DELETE_WINDOW", self.closeDestroy)
        self.top.attributes('-alpha', play_list.windowOpacity)
        allButtonsFont = skinOptions[2][play_list.skin]
        InfoLabelText = StringVar()
        InfoLabelText.set("Search for song: \n")
        tk.Label(self.top, textvariable=InfoLabelText, fg=fontColor.get(), font=allButtonsFont, bg=color).pack()
        tk.Label(self.top, text="Value: ", fg=fontColor.get(), font=allButtonsFont, bg=color).pack()
        self.searchValue = tk.Entry(self.top)
        #these were used for instant search, but require multi-processing/threading, otherwise is very slow:
        #self.searchValue.bind("<Key>", self.showResults)
        #self.searchValue.bind("<Return>", self.playNextSearch)

        #this is used for normal search
        self.searchValue.bind("<Return>", self.showResults)

        self.top.bind("<Key>", self.focus_Input)
        self.top.bind("<Tab>", self.focus_out)
        self.searchValue.bind("<Escape>", self.destroyEsc)
        self.searchValue.bind("<Shift_R>", self.playPreviousSearch)
        self.top.bind("<Escape>", self.destroyEsc)
        self.searchValue.pack(padx=5)
        ForwardButton = tk.Button(self.top, text="Forward", command= lambda:self.playNextSearch("<Return>"), fg=fontColor.get(), font=allButtonsFont,
                                bg=color)
        ForwardButton.pack(pady=10)
        BackwardButton = tk.Button(self.top, text="Backward", command=lambda:self.playPreviousSearch("<Shift_R>"), fg=fontColor.get(), font=allButtonsFont,
                                bg=color)
        BackwardButton.pack()
        dialog = self

    def focus_Input(self,event):
        self.searchValue.focus_force()

    def focus_out(self, event):
        window.wm_attributes("-topmost", 1)
        window.grab_set()
        window.focus_force()

    def showResults(self, event):
        global listBox_Song_selected_index
        if len(self.searchValue.get()) > 0:
            listbox.delete(0, tk.END)
            value = self.searchValue.get().lower()
            self.index=0
            for element in play_list.validFiles:
                if value in element.fileName.lower():
                    listbox.insert(tk.END, str(play_list.validFiles.index(element)) + ". " + element.fileName)
                    window.update()
        else:
            displayElementsOnPlaylist()
            listBox_Song_selected_index = play_list.currentSongIndex
            listbox.see(listBox_Song_selected_index)  # Makes sure the given list index is visible. You can use an integer index,
            listbox.selection_clear(0, tk.END)  # clear existing selection
            listbox.select_set(listBox_Song_selected_index)

    def destroyEsc(self,event):
        self.closeDestroy()

    def destroy(self):
        global dialog
        self.top.destroy()
        dialog = None

    def playPreviousSearch(self, event):
        global play_list
        global listBox_Song_selected_index
        elements = listbox.get(0, tk.END)
        if self.index == None:
            self.index = len(elements) - 1
        elif self.index - 1 >= 0:
            self.index -= 1
        else:
            self.index = len(elements)-1
        real_index = elements[self.index]
        real_index = real_index.split(". ")
        real_index = real_index[0]
        listBox_Song_selected_index = self.index
        listbox.see(listBox_Song_selected_index)  # Makes sure the given list index is visible. You can use an integer index,
        listbox.selection_clear(0, tk.END)  # clear existing selection
        listbox.select_set(listBox_Song_selected_index)
        play_list.currentSongIndex = int(real_index)
        if play_list.danthologyMode == False:
            play_list.currentSongPosition = 0
        play_music()

    def playNextSearch(self, event):
        global play_list
        global listBox_Song_selected_index
        elements = listbox.get(0,tk.END)
        if self.index == None:
            self.index = 0
        elif self.index + 1 < len(elements):
            self.index += 1
        else:
            self.index = 0
        real_index = elements[self.index]
        real_index = real_index.split(". ")
        real_index = real_index[0]
        listBox_Song_selected_index = self.index
        listbox.see(listBox_Song_selected_index)  # Makes sure the given list index is visible. You can use an integer index,
        listbox.selection_clear(0, tk.END)  # clear existing selection
        listbox.select_set(listBox_Song_selected_index)
        play_list.currentSongIndex = int(real_index)
        if play_list.danthologyMode == False:
            play_list.currentSongPosition = 0
        play_music()

    def closeDestroy(self,):
        global dialog
        global listBox_Song_selected_index
        self.top.destroy()
        dialog = None
        displayElementsOnPlaylist()
        listBox_Song_selected_index = play_list.currentSongIndex
        listbox.see(listBox_Song_selected_index)  # Makes sure the given list index is visible. You can use an integer index,
        listbox.selection_clear(0, tk.END)  # clear existing selection
        listbox.select_set(listBox_Song_selected_index)

    def take_focus(self):
        self.top.wm_attributes("-topmost", 1)
        self.top.grab_set()
        self.searchValue.focus_force()

class Slideshow:
    #static variables
    timer = 0
    seconds = None
    slideshow_image = None
    slideshow = None
    top=None
    Window_Title=None #can be used as a reference to check if window is opened

    def __init__(self):
        global allButtonsFont
        color = OpenFileButton["bg"]  # get the color which the rest of elements is using at the moment
        Slideshow.top = tk.Toplevel(window, bg=color)
        Slideshow.top.protocol("WM_DELETE_WINDOW", self.destroy)
        if type(allButtonsFont) == StringVar:
            allButtonsFont = allButtonsFont.get()
        Slideshow.Window_Title = "Slideshow"
        Slideshow.top.title(Slideshow.Window_Title)
        Slideshow.top.geometry("300x300+10+10")
        Slideshow.top.attributes('-alpha', play_list.windowOpacity)
        Slideshow.seconds = StringVar()
        Slideshow.seconds.set(play_list.slideImagesTransitionSeconds)
        durationOptions = [1,2,3,4,5,10,15,30,60]

        self.infoText = StringVar()
        self.infoText.set("Welcome to Slideshow!\n\n"+
                          "Please setup your slideshow before\n" +
                          "proceed or hit Continue Button\n"+
                          "(if available) to resume.\n\n" +
                          "Number of Seconds on Transition:")

        self.InfoLabel = tk.Label(Slideshow.top, textvariable=self.infoText, fg=fontColor.get(), font=allButtonsFont,
                                  bg=color)
        self.InfoLabel.pack()

        self.imageDuration = Combobox(Slideshow.top, textvariable=Slideshow.seconds, values=durationOptions)
        self.imageDuration.pack(pady=5)
        self.imageDuration.bind("<<ComboboxSelected>>", self.time_set)
        self.loadImagesButton = tk.Button(Slideshow.top, text="Load Images",
                                                 command=self.loadImages, bg=color, fg=fontColor.get(),
                                                 font=allButtonsFont)
        self.loadImagesButton.pack(pady=10)
        self.clearImages = tk.Button(Slideshow.top, text="Clear Slideshow",
                                                 command=self.clearSlideshow, bg=color, fg=fontColor.get(),
                                                 font=allButtonsFont)
        self.clearImages.pack()
        self.startSlideshowButtonText = StringVar()
        if int(self.seconds.get()) > 0 and len(play_list.slideImages) > 0:
            self.startSlideshowButtonText.set("Continue")
        else:
            self.startSlideshowButtonText.set("Start")

        self.startSlideshow = tk.Button(Slideshow.top, textvariable = self.startSlideshowButtonText,
                                                 command=self.start, bg=color, fg=fontColor.get(),
                                                 font=allButtonsFont)
        self.startSlideshow.pack(pady=10)
        self.numberOfImages = StringVar()
        self.numberOfImages.set("Number of Images: " + str(len(play_list.slideImages)))
        self.labelNumberOfImages = tk.Label(Slideshow.top, textvariable=self.numberOfImages, fg=fontColor.get(), font=allButtonsFont,
                                  bg=color)
        self.labelNumberOfImages.pack()
        Slideshow.top.bind("<Escape>", self.destroyEsc)
        Slideshow.top.bind("<Tab>", self.focus_out)

    def loadImages(self):
        global play_list
        slidePictures = filedialog.askopenfilenames(initialdir="/", title="Please select one or more files", filetypes=(
        ("gif files", "*.gif"), ("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"),("all files", "*.*")))
        play_list.slideImages += list(slidePictures)
        if len(play_list.slideImages) == 0:
            messagebox.showinfo("Information", "Slideshow is empty. No valid files were found. Please load only .jpg, .jpeg or .gif files.")
        self.numberOfImages.set("Number of Images: " + str(len(play_list.slideImages)))

    def focus_out(self, event):
        window.wm_attributes("-topmost", 1)
        window.grab_set()
        window.focus_force()

    def destroyEsc(self,event):
        self.destroy()

    def time_set(self,event):
        global play_list
        play_list.slideImagesTransitionSeconds = Slideshow.seconds.get()

    def clearSlideshow(self):
        play_list.slideImages.clear()
        self.numberOfImages.set("Number of Images: " + str(len(play_list.slideImages)))

    def destroy(self):
        global play_list
        self.top.destroy()
        play_list.usingSlideShow = False
        Slideshow.timer = 0
        Slideshow.seconds = None
        Slideshow.slideshow_image = None
        Slideshow.slideshow = None
        Slideshow.top = None
        Slideshow.Window_Title = None

    @staticmethod
    def take_focus():
        Slideshow.top.wm_attributes("-topmost", 1)
        Slideshow.top.grab_set()
        Slideshow.top.focus_force()

    @staticmethod
    def countSeconds():
        global play_list
        if (time.time() - Slideshow.timer) >= int(Slideshow.seconds.get()):
            if play_list.slideImageIndex+1 < len(play_list.slideImages):
                play_list.slideImageIndex+=1
            else:
                play_list.slideImageIndex = 0
            Slideshow.start()

    @staticmethod
    def start():
        global play_list
        Slideshow.timer = time.time()
        play_list.usingSlideShow = True
        if len(play_list.slideImages) > 0:
            Slideshow.slide_image = ImageTk.PhotoImage(Image.open(play_list.slideImages[play_list.slideImageIndex]).resize((300, 300))) # open all kind of images like this
            Slideshow.slideshow = tk.Label(Slideshow.top, image=Slideshow.slide_image)
            Slideshow.slideshow.pack(fill="both")
            Slideshow.slideshow.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            messagebox.showinfo("Information",
                                "Slideshow is empty. No valid files were found. Please load only .jpg, .jpeg or .gif files.")

class SleepingTool:

    def __init__(self, parent):
        global allButtonsFont
        global dialog
        color = OpenFileButton["bg"]  # get the color which the rest of elements is using at the moment
        self.top = tk.Toplevel(parent, bg=color)
        self.top.protocol("WM_DELETE_WINDOW", self.destroy)
        Window_Title = "Sleeping Tool"
        self.top.title(Window_Title)
        self.top.geometry("300x230+100+100")
        self.top.attributes('-alpha', play_list.windowOpacity)
        if type(allButtonsFont) == StringVar:
            allButtonsFont = allButtonsFont.get()
        self.wakeUpScheduler = None
        self.sleepTimer = 0;
        self.sleepTime = 0;
        self.wakeUpTimer = 0;
        self.wakeUpTime = 0;
        self.sleepingScheduler = None

        InfoLabelText = StringVar()
        InfoLabelText.set("Enter the interval (seconds): \n")
        tk.Label(self.top , textvariable=InfoLabelText, fg=fontColor.get(), font=allButtonsFont, bg=color).pack()
        tk.Label(self.top , text="Sleep Value: ", fg=fontColor.get(), font=allButtonsFont, bg=color).pack()

        self.sleepInterval = tk.Entry(self.top )
        self.sleepInterval.pack(padx=5)
        self.sleepInterval.bind("<Return>", self.eventSleeping)
        SleepButton = tk.Button(self.top , text="Sleep", command=self.sleeping, fg=fontColor.get(), font=allButtonsFont, bg=color)
        SleepButton.pack(pady=5)

        tk.Label(self.top, text="WakeUp Value: ", fg=fontColor.get(), font=allButtonsFont, bg=color).pack()
        self.wakeUpInterval = tk.Entry(self.top)
        self.wakeUpInterval.pack(padx=5)
        self.wakeUpInterval.bind("<Return>", self.eventWakeUp)
        wakeUpButton = tk.Button(self.top, text="Wake Up", command=self.wakeUp, fg=fontColor.get(), font=allButtonsFont,
                                bg=color)
        wakeUpButton.pack(pady=5)

        self.top.bind("<Escape>", self.destroyEsc)
        self.top.bind("<Tab>", self.focus_Input)
        dialog = self

    def destroy(self):
        global dialog
        self.top.destroy()
        dialog = None

    def eventWakeUp(self,event):
        self.wakeUp()

    def eventSleeping(self, event):
        self.sleeping()

    def destroyEsc(self, event):
        self.destroy()

    def focus_Input(self, event):
        if self.sleepInterval.focus_get():
            self.wakeUpInterval.focus_force()
        else:
            self.sleepInterval.focus_force()

    def wakeUp(self):
        global dialog
        if self.wakeUpInterval.get() != "":
            try:
                self.wakeUpTime = int(self.wakeUpInterval.get())
            except Exception as e:
                print(e)
            else:
                self.top.destroy()
                dialog = None
                self.sleepTime=0 #if it was supposed to sleep, overwrite that.
                self.sleepingScheduler=None #if it was supposed to sleep, overwrite that.
                textFallAsleep.set("Fall Asleep: Never") #if it was supposed to sleep, overwrite that.
                self.wakeUpTimer = time.time()
                self.wakeUpScheduler = sched.scheduler(time.time, time.sleep)
                self.wakeUpScheduler.enter(1, 1, lambda : self.whenToWakeUp())
                self.wakeUpScheduler.run()
        self.top.destroy()
        dialog = None

    def take_focus(self):
        self.top.wm_attributes("-topmost", 1)
        self.top.grab_set()
        self.sleepInterval.focus_force()

    def sleeping(self):
        global dialog
        if self.sleepInterval.get() != "":
            try:
                self.sleepTime = int(self.sleepInterval.get())
            except Exception as e:
                print(e)
            else:
                self.top.destroy()
                dialog = None
                self.wakeUpTime = 0 #if it was supposed to wake up, overwrite that
                self.wakeUpScheduler=None #if it was supposed to wake up, overwrite that
                textWakeUp.set("Wake Up: Never") #if it was supposed to wake up, overwrite that
                self.sleepTimer = time.time()
                self.sleepingScheduler = sched.scheduler(time.time, time.sleep)
                self.sleepingScheduler.enter(1, 1,  lambda : self.whenToSleep())
                self.sleepingScheduler.run()
        self.top.destroy()
        dialog = None

    def whenToSleep(self):
        secondsLeft = int(self.sleepTime - (time.time() - self.sleepTimer))
        textFallAsleep.set("Fall Asleep: {:0>8}" .format(str(datetime.timedelta(seconds=secondsLeft))))
        if secondsLeft<=0:
            pause_music()
            self.sleepTime=0
            self.sleepingScheduler = None
            textFallAsleep.set("Fall Asleep: Never")
        else:
            window.update()
            self.sleepingScheduler.enter(1, 1, lambda : self.whenToSleep())

    def whenToWakeUp(self):
        global play_list
        secondsLeft = int(self.wakeUpTime - (time.time() - self.wakeUpTimer))
        textWakeUp.set("Wake Up: {:0>8}".format(str(datetime.timedelta(seconds=secondsLeft))))
        if secondsLeft <= 0:
            self.wakeUpTime = 0
            self.wakeUpScheduler=None
            play_list.VolumeLevel = 1.0
            textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
            textWakeUp.set("Wake Up: Never")
            play_music()
        else:
            window.update()
            self.wakeUpScheduler.enter(1, 1, lambda : self.whenToWakeUp())

class Customize:
    def __init__(self, parent):
        global allButtonsFont
        global dialog
        global play_list
        color = OpenFileButton["bg"] # get the color which the rest of elements is using at the moment
        self.top = tk.Toplevel(parent, bg=color)
        self.top.protocol("WM_DELETE_WINDOW", self.destroy)
        Window_Title = "Customize"
        self.top.title(Window_Title)
        self.top.geometry("620x500+100+100")
        self.top.attributes('-alpha', play_list.windowOpacity)
        columnOne = 10
        columnTwo = 220
        columnThree = 430
        if type(allButtonsFont) == StringVar:
            allButtonsFont = allButtonsFont.get()
        self.InfoLabelText = StringVar()
        self.InfoLabelText.set("Welcome to Customize capability:\n\n"
                                +"Here you can customize your player appearance\n"
                                 +"in any way you like.\n")
        tk.Label(self.top, textvariable=self.InfoLabelText, fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=150, y=5)
        
        self.labelFontColor = tk.Label(self.top, text="Button&Label Color: ", fg=fontColor.get(), font=allButtonsFont, bg=color)
        self.labelFontColor.place(x=columnOne, y=80)

        self.colorBox = Combobox(self.top, textvariable=SkinColor, values=custom_color_list)
        self.colorBox.place(x=columnOne, y=100)
        self.colorBox.bind("<<ComboboxSelected>>", changingBackgroundElementColor)

        tk.Label(self.top, text="Font: ", fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=columnOne, y=120)
        
        aux = allButtonsFont
        allButtonsFont = StringVar() #making this string variable.
        allButtonsFont.set(aux)
        self.fontBox = Combobox(self.top, textvariable=allButtonsFont, values=custom_font_list)
        self.fontBox.place(x=columnOne, y=140)
        self.fontBox.bind("<<ComboboxSelected>>", customFontChange)

        tk.Label(self.top, text="Label Background: ", fg=fontColor.get(), font=allButtonsFont.get(), bg=color).place(x=10, y=160)
        self.labelColorBox = Combobox(self.top, textvariable=labelBackground, values=custom_color_list)
        self.labelColorBox.place(x=columnOne, y=180)
        self.labelColorBox.bind("<<ComboboxSelected>>", changingLabelBackgroundColor)

        tk.Label(self.top, text="Font Color: ", fg=fontColor.get(), font=allButtonsFont.get(), bg=color).place(x=columnOne, y=200)
        self.FontMainColorBox = Combobox(self.top, textvariable=fontColor, values=custom_color_list)
        self.FontMainColorBox.place(x=columnOne, y=220)
        self.FontMainColorBox.bind("<<ComboboxSelected>>", changingFontColor)

        tk.Label(self.top, text="Playing Label Transition: ", fg=fontColor.get(), font=allButtonsFont.get(), bg=color).place(x=columnOne, y=240)
        self.FontTransitionText = StringVar()
        self.FontTransitionText.set(play_list.playingFileNameTransition)
        self.FontTransitionBox = Combobox(self.top, textvariable=self.FontTransitionText, values=["none", "separation", "typewriting"])
        self.FontTransitionBox.place(x=columnOne, y=260)
        self.FontTransitionBox.bind("<<ComboboxSelected>>", self.changeFileNameTransition)

        tk.Label(self.top, text="Color Picker Result Usage: ", fg=fontColor.get(), font=allButtonsFont.get(), bg=color).place(x=columnOne, y=280)
        self.textColorPickerUsage = StringVar()
        self.textColorPickerUsage.set("No Usage")
        self.ColorPickerUsage = Combobox(self.top, textvariable=self.textColorPickerUsage,
                                         values=["No Usage", "Button&Label Color", "Label Background", "Font Color"])
        self.ColorPickerUsage.place(x=columnOne, y=300)
        self.ColorPickerUsage.bind("<<ComboboxSelected>>", self.useColorPicked)
        
        tk.Label(self.top, text="ProgressBar Type: ", fg=fontColor.get(), font=allButtonsFont.get(), bg=color).place(x=columnOne, y=320)
        self.textProgressBarType = StringVar()
        self.textProgressBarType.set(play_list.ProgressBarType)
        self.ProgressBarTypeBox = Combobox(self.top, textvariable=self.textProgressBarType,
                                         values=["determinate", "indeterminate"])
        self.ProgressBarTypeBox.place(x=columnOne, y=340)
        self.ProgressBarTypeBox.bind("<<ComboboxSelected>>", self.changeProgressBar)

        self.TitleTransitionButtonText = StringVar()
        if play_list.usePlayerTitleTransition == True:
            self.TitleTransitionButtonText.set("Title Transition ON")
        else:
            self.TitleTransitionButtonText.set("Title Transition OFF")
        self.TitleTransition = tk.Button(self.top, textvariable=self.TitleTransitionButtonText, command=self.changeTitleTransition, bg=color, fg=fontColor.get(),
                                        font=allButtonsFont.get())
        self.TitleTransition.place(x=columnTwo, y=80)

        tk.Label(self.top, text="Color Bg Labels: ", fg=fontColor.get(), font=allButtonsFont.get(), bg=color).place(x=columnTwo, y=110)
        self.colorBgLabels = StringVar()
        self.colorBgLabels.set("False")
        self.RbFalse = tk.Radiobutton(self.top, text="False", variable=self.colorBgLabels, value=False, width=3, bg=color,
                            command=lambda: changingBackgroundedLabelsColor(self.colorBgLabels,0), fg=fontColor.get(), selectcolor="black", font=allButtonsFont.get())
        self.RbTrue = tk.Radiobutton(self.top, text="True", variable=self.colorBgLabels, value=True, width=3, bg=color,
                            command=lambda: changingBackgroundedLabelsColor(self.colorBgLabels,0), fg=fontColor.get(), selectcolor="black", font=allButtonsFont.get())
        self.RbFalse.place(x=columnTwo, y=130)
        self.RbTrue.place(x=columnTwo, y=160)

        self.browseBackgroundPicture = tk.Button(self.top, text="Load Background", command=self.browse_background_picture, bg=color, fg=fontColor.get(),
                                                 font=allButtonsFont.get())
        self.browseBackgroundPicture.place(x=columnTwo, y=190)
        self.startSlideshow = tk.Button(self.top, text="Start Slideshow", command=showSlideshowWindow, bg=color, fg=fontColor.get(), font=allButtonsFont.get())
        self.startSlideshow.place(x=columnTwo, y=220)

        tk.Label(self.top, text="Window Transparency: ", fg=fontColor.get(), font=allButtonsFont.get(),
                 bg=color).place(x=columnTwo, y=250)
        self.WindowOpacityText = StringVar()
        self.WindowOpacityText.set(play_list.windowOpacity)
        self.WindowOpacityBox = Combobox(self.top, textvariable=self.WindowOpacityText,
                                          values=["1.0", "0.9", "0.8", "0.7", "0.6", "0.5"])
        self.WindowOpacityBox.place(x=columnTwo, y=270)
        self.WindowOpacityBox.bind("<<ComboboxSelected>>", self.changeWindowOpacity)

        tk.Label(self.top, text="Progress Time: ", fg=fontColor.get(), font=allButtonsFont.get(),
                 bg=color).place(x=columnTwo, y=290)

        self.ProgressTimeText = StringVar()
        if play_list.progressTime == "Ascending":
            self.ProgressTimeText.set("Playing Time")
        else:
            self.ProgressTimeText.set("Remaining Time")
        self.ProgressTimeBox = Combobox(self.top, textvariable=self.ProgressTimeText,
                                         values=["Playing Time", "Remaining Time"])
        self.ProgressTimeBox.place(x=columnTwo, y=310)
        self.ProgressTimeBox.bind("<<ComboboxSelected>>", self.changeProgressTime)

        tk.Label(self.top, text="Lyrics Active Source: ", fg=fontColor.get(), font=allButtonsFont.get(),
                 bg=color).place(x=columnTwo, y=330)
        self.LyricsSourcesText = StringVar()
        self.LyricsSourcesText.set(play_list.LyricsActiveSource)
        self.LyricsSourcesBox = Combobox(self.top, textvariable=self.LyricsSourcesText,
                                         values=LyricsOnlineSources)
        self.LyricsSourcesBox.place(x=columnTwo, y=350)
        self.LyricsSourcesBox.bind("<<ComboboxSelected>>", self.changeActiveLyricsSource)

        self.textDanthologyMode = StringVar()

        if play_list.danthologyMode == True:
            self.textDanthologyMode.set("Danthology Mode ON")
        else:
            self.textDanthologyMode.set("Danthology Mode OFF")
        self.danthologyMode = tk.Button(self.top, textvariable=self.textDanthologyMode, command=self.changeDanthologyMode, bg=color, fg=fontColor.get(),
                                        font=allButtonsFont.get())
        self.danthologyMode.place(x=columnThree, y=80)
        self.DanthologyInterval = StringVar()
        self.DanthologyInterval.set(play_list.danthologyDuration)
        tk.Label(self.top, text="Danthology Duration: ", fg=fontColor.get(), font=allButtonsFont.get(), bg=color).place(x=columnThree, y=110)
        self.DanthologySetBox = Combobox(self.top, textvariable=self.DanthologyInterval, values=["0", "10", "30", "60", "90"])
        self.DanthologySetBox.place(x=columnThree, y=140)
        self.DanthologySetBox.bind("<<ComboboxSelected>>", self.changeDanthologyDuration)

        tk.Label(self.top, text="Color Picker: ", fg=fontColor.get(), font=allButtonsFont.get(),
                 bg=color).place(x=columnThree, y=160)

        self.ColorPickerValue = allButtonsFont.get()

        self.scaleRed = tk.Scale(self.top, from_=0, to=255, orient=tk.HORIZONTAL, fg=fontColor.get(), font=allButtonsFont.get(), bg=color)
        self.scaleRed.place(x=columnThree, y=180)
        self.scaleRed.bind("<ButtonRelease-1>", self.composeColor)

        self.scaleGreen = tk.Scale(self.top, from_=0, to=255, orient=tk.HORIZONTAL, fg=fontColor.get(),
                            font=allButtonsFont.get(), bg=color)
        self.scaleGreen.place(x=columnThree, y=220)
        self.scaleGreen.bind("<ButtonRelease-1>", self.composeColor)

        self.scaleBlue = tk.Scale(self.top, from_=0, to=255, orient=tk.HORIZONTAL, fg=fontColor.get(),
                            font=allButtonsFont.get(), bg=color)
        self.scaleBlue.place(x=columnThree, y=260)
        self.scaleBlue.bind("<ButtonRelease-1>", self.composeColor)

        self.ColorPickerResult = tk.Label(self.top, text="     Result       ", fg=fontColor.get(), font=self.ColorPickerValue,
                 bg=color)
        self.ColorPickerResult.place(x=columnThree, y=310)
		
        self.MassFileEditorUsage = tk.IntVar()
        self.MassFileEditorUsage.set(play_list.useMassFileEditor)

        tk.Checkbutton(self.top, text="Use mass file editor capabilities.", fg=fontColor.get(), font=allButtonsFont.get(),
                       bg=color, variable=self.MassFileEditorUsage, command=self.enableDisableMassFileEditor,
                       selectcolor="black").place(x=180, y=380)
		
        tk.Label(self.top, text="Danthology refers to resuming the next song \n"+
                                "at the duration the current one has ended.\n" +
                                "This feature enables easier browse among \n"+
                                "unknown songs.", fg=fontColor.get(),
                        font=allButtonsFont.get(), bg=color).place(x=160, y=410)

        self.top.bind("<Escape>", self.destroyEsc)
        self.top.bind("<Tab>", self.focus_Input)
        dialog = self

    def changeActiveLyricsSource(self, event):
        play_list.LyricsActiveSource = self.LyricsSourcesText.get()

    def changeProgressBar(self, event):
        global play_list
        global progress
        play_list.ProgressBarType = self.textProgressBarType.get()
        progress["mode"] = play_list.ProgressBarType
    
    def enableDisableMassFileEditor(self):
        global play_list
        if self.MassFileEditorUsage.get() == 1:
            play_list.useMassFileEditor = True
        else:
            play_list.useMassFileEditor = False
		
    def changeProgressTime(self, event):
        global play_list
        if self.ProgressTimeText.get() == "Playing Time":
            play_list.progressTime = "Ascending"
        else:
            play_list.progressTime = "Descending"

    def useColorPicked(self, event):
        global SkinColor
        global labelBackground
        global fontColor
        if self.ColorPickerValue!="":
            if self.textColorPickerUsage.get() == "Button&Label Color":
                SkinColor.set(self.ColorPickerValue)
                play_list.userCreatedColors.append(self.ColorPickerValue)
                custom_color_list.append(self.ColorPickerValue)
                changingBackgroundElementColor(event)
            elif self.textColorPickerUsage.get() == "Label Background":
                labelBackground.set(self.ColorPickerValue)
                play_list.userCreatedColors.append(self.ColorPickerValue)
                custom_color_list.append(self.ColorPickerValue)
                changingLabelBackgroundColor(event)
            elif self.textColorPickerUsage.get() == "Font Color":
                fontColor.set(self.ColorPickerValue)
                play_list.userCreatedColors.append(self.ColorPickerValue)
                custom_color_list.append(self.ColorPickerValue)
                changingFontColor(event)

    def composeColor(self, event):
        global custom_color_list
        red = ""
        if int(self.scaleRed.get()) >=0 and  int(self.scaleRed.get()<10):
            red = str(hex(self.scaleRed.get()))
            red=red.split("x")
            red= "0" + red[1]
        else:
            red = str(hex(self.scaleRed.get()))
            red = red.split("x")
            red = red[1]

        green = ""
        if int(self.scaleGreen.get()) >= 0 and int(self.scaleGreen.get() < 10):
            green = str(hex(self.scaleGreen.get()))
            green = green.split("x")
            green = "0" + green[1]
        else:
            green = str(hex(self.scaleGreen.get()))
            green = green.split("x")
            green = green[1]

        blue = ""
        if int(self.scaleBlue.get()) >= 0 and int(self.scaleBlue.get() < 10):
            blue = str(hex(self.scaleBlue.get()))
            blue = blue.split("x")
            blue = "0" + blue[1]
        else:
            blue = str(hex(self.scaleBlue.get()))
            blue = blue.split("x")
            blue = blue[1]

        self.ColorPickerValue = "#" + red + green + blue
        self.ColorPickerResult["bg"] = self.ColorPickerValue

    def destroy(self):
        global dialog
        self.top.destroy()
        dialog = None

    def changeDanthologyDuration(self, event):
        global play_list
        play_list.danthologyDuration = int(self.DanthologyInterval.get())
        play_list.danthologyTimer = time.time()

    def changeWindowOpacity(self,event):
        global play_list
        play_list.windowOpacity = float(self.WindowOpacityText.get())
        window.attributes('-alpha', play_list.windowOpacity)
        self.top.attributes('-alpha', play_list.windowOpacity)

    def changeDanthologyMode(self):
        global play_list
        if play_list.danthologyMode == True:
            play_list.danthologyMode = False
            self.textDanthologyMode.set("Danthology Mode OFF")
            textDanthologyMode.set("Danthology Mode: OFF")
        else:
            play_list.danthologyMode = True
            self.textDanthologyMode.set("Danthology Mode ON")
            textDanthologyMode.set("Danthology Mode: ON")

    def destroyEsc(self, event):
        self.destroy()

    def changeTitleTransition(self):
        global play_list
        if play_list.usePlayerTitleTransition == True:
            play_list.usePlayerTitleTransition = False
            self.TitleTransitionButtonText.set("Title Transition OFF")
            window.title("   PyPlay MP3 Player in Python     ")
        else:
            play_list.usePlayerTitleTransition = True
            self.TitleTransitionButtonText.set("Title Transition ON")

    def focus_Input(self, event):
        if self.colorBox.focus_get():
            self.fontBox.focus_force()
        elif self.fontBox.focus_get():
            self.labelColorBox.focus_force()
        elif self.labelColorBox.focus_get():
            self.FontMainColorBox.focus_force()
        elif self.FontMainColorBox.focus_get():
            self.colorBox.focus_force()

    def changeFileNameTransition(self,event):
        global play_list
        global visualSongNameLabel
        play_list.playingFileNameTransition = self.FontTransitionText.get()
        if play_list.playingFileNameTransition == "none":
            visualSongNameLabel = play_list.validFiles[play_list.currentSongIndex].fileName
        elif play_list.playingFileNameTransition == "typewriting":
            visualSongNameLabel = None
        elif play_list.playingFileNameTransition == "separation":
            visualSongNameLabel = "_" + play_list.validFiles[play_list.currentSongIndex].fileName

    def take_focus(self):
        self.top.wm_attributes("-topmost", 1)
        self.top.grab_set()
        self.colorBox.focus_force()

    def browse_background_picture(self):
        global play_list
        background = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(
        ("gif files", "*.gif"), ("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"),("all files", "*.*")))
        if ".gif" in background:
            play_list.customBackgroundPicture = background
            background_image = tk.PhotoImage(file=play_list.customBackgroundPicture)
            background_label.configure(image=background_image)
            background_label.image = background_image
        elif ".jpg" in background or ".jpeg" in background:
            play_list.customBackgroundPicture = background
            img = ImageTk.PhotoImage(Image.open(background))
            background_label.configure(image=img)
            background_label.image = img
        else:
            messagebox.showinfo("Information", "The background picture has to be a valid .gif file.")

class NewPlaylistDialog:
    def __init__(self, parent):
        global allButtonsFont
        global dialog
        color = OpenFileButton["bg"]
        self.top = tk.Toplevel(parent, bg=color)
        self.top.protocol("WM_DELETE_WINDOW", self.destroy)
        Window_Title = "Info"
        self.top.title(Window_Title)
        self.top.geometry("480x200+100+100")
        self.top.attributes('-alpha', play_list.windowOpacity)
        if type(allButtonsFont) == StringVar:
            allButtonsFont = allButtonsFont.get()
        self.labelInfo = tk.Label(self.top, text="One song is currently playing.\n\nDo you wish to stop, or keep it in the playlist?", \
                                  fg=fontColor.get(), font=allButtonsFont, bg=color).pack()
        StopItButton = tk.Button(self.top, text="Stop It", command=self.stopIt , fg=fontColor.get(), font=allButtonsFont, bg=color)
        KeepItButton = tk.Button(self.top, text="Keep It", command=self.keepCurrentSong, fg=fontColor.get(), font=allButtonsFont, bg=color)
        StopItButton.pack(pady=10)
        KeepItButton.pack(pady=10)
        dialog = self
        self.top.bind("<Escape>", self.destroyEsc)

    def stopIt(self):
        global play_list
        play_list = Playlist()
        stop_music()
        self.destroy()
        clearLabels()
        # Restore default skin
        SkinColor.set(skinOptions[1][play_list.skin])
        changeSkin("<Double-Button>")
        displayElementsOnPlaylist()

    def destroyEsc(self):
        self.destroy()

    def takeFocus(self):
        self.top.wm_attributes("-topmost", 1)
        self.top.grab_set()

    def keepCurrentSong(self):
        global play_list
        list = play_list
        play_list = Playlist()
        if list.currentSongIndex!=None:
            play_list.validFiles.append(list.validFiles[list.currentSongIndex])
            play_list.currentSongIndex = 0
        play_list.currentSongPosition = list.currentSongPosition
        play_list.isSongStopped = list.isSongStopped
        play_list.isSongPause = list.isSongPause
        del list
        self.destroy()
        # Restore default skin
        SkinColor.set(skinOptions[1][play_list.skin])
        changeSkin("<Double-Button>")
        displayElementsOnPlaylist()

    def destroy(self):
        global dialog
        self.top.destroy()
        dialog = None

class Mp3TagModifierTool:
    def __init__(self, fileIndex=0):
        global allButtonsFont
        global dialog
        self.undoRenameBackupFile = "RENAMEALLFILES.backup"
        self.undoArtistTitleBackupFile = "ALLARTISTTITLE.backup"
        color = OpenFileButton["bg"]  # get the color which the rest of elements is using at the moment
        self.top = tk.Toplevel(window, bg=color)
        Window_Title = "Mp3TagModifier Tool"
        columnOne=5
        columnTwo = 150
        columnThree = 290
        self.Song = play_list.validFiles[fileIndex]
        self.top.title(Window_Title)
        self.top.geometry("600x350+100+100")
        self.top.protocol("WM_DELETE_WINDOW", self.destroy)
        self.top.attributes('-alpha', play_list.windowOpacity)
        allButtonsFont = skinOptions[2][play_list.skin]
        tk.Label(self.top, text="Name:", fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=columnOne, y=5)
        self.NameTag = tk.Entry(self.top, width=80)
        self.NameTag.insert(0, self.Song.fileName)
        self.NameTag.place(x=columnOne, y=25)
        self.NameTag.bind("<Key>", self.setNAOnName)
        
        tk.Label(self.top, text="Naming Case:", fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=500, y=5)
        textConversionValues=["NA","Capitalize", "SemiCapitalize", "Upper Case", "Lower Case"]
        self.nameTextFormat = StringVar()
        self.nameTextFormat.set("NA")
        self.NameFormatBox = Combobox(self.top, textvariable=self.nameTextFormat, values=textConversionValues, width=10)
        self.NameFormatBox.place(x=500, y=25)
        self.NameFormatBox.bind("<<ComboboxSelected>>", self.changeNameFormat)
        
        tk.Label(self.top, text="Genre:", fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=columnOne, y=45)
        self.GenreTag = tk.Entry(self.top, width=15)
        self.GenreTag.insert(0, self.Song.Genre)
        self.GenreTag.place(x=columnOne, y=65)
        self.GenreTag.bind("<Key>", self.setNAOnTags)
        tk.Label(self.top, text="Tagging Case:", fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=500, y=65)
        self.tagTextFormat = StringVar()
        self.tagTextFormat.set("NA")
        self.TagFormatBox = Combobox(self.top, textvariable=self.tagTextFormat, values=textConversionValues, width=10)
        self.TagFormatBox.place(x=500, y=85)
        self.TagFormatBox.bind("<<ComboboxSelected>>", self.changeTagFormat)
        
        tk.Label(self.top, text="Year:", fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=columnTwo, y=45)
        self.YearTag = tk.Entry(self.top, width=15)
        self.YearTag.insert(0, self.Song.Year)
        self.YearTag.place(x=columnTwo, y=65)
        self.YearTag.bind("<Key>", self.setNAOnTags)
        tk.Label(self.top, text="Album:", fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=columnThree, y=45)
        self.AlbumTag = tk.Entry(self.top, width=30)
        self.AlbumTag.insert(0, self.Song.Album)
        self.AlbumTag.place(x=columnThree, y=65)
        self.AlbumTag.bind("<Key>", self.setNAOnTags)
        tk.Label(self.top, text="Artist:", fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=columnOne, y=85)
        self.ArtistTag = tk.Entry(self.top, width=35)
        self.ArtistTag.insert(0, self.Song.Artist)
        self.ArtistTag.place(x=columnOne, y=105)
        self.ArtistTag.bind("<Key>", self.setNAOnTags)
        tk.Label(self.top, text="Title:", fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=250, y=85)
        self.TitleTag = tk.Entry(self.top, width=35)
        self.TitleTag.insert(0, self.Song.Title)
        self.TitleTag.place(x=250, y=105)
        self.TitleTag.bind("<Key>", self.setNAOnTags)
        SaveChangesButton = tk.Button(self.top, text="Save Changes", command=self.SaveChanges, fg=fontColor.get(), font=allButtonsFont,
                                bg=color)
        SaveChangesButton.place(x=columnOne, y=145)

        ComposeFileNameButton = tk.Button(self.top, text="Compose Filename from 'Artist - Title'", command=self.composeFileName, fg=fontColor.get(), font=allButtonsFont,
                                        bg=color)
        ComposeFileNameButton.place(x=columnTwo, y=145)
        ComposeArtistTitleButton = tk.Button(self.top, text="Compose Artist/Title from Filename", command=self.composeArtistTitle, fg=fontColor.get(), font=allButtonsFont,
                                        bg=color)
        ComposeArtistTitleButton.place(x=columnTwo, y=175)

        self.MassRenameButton = tk.Button(self.top, text="Rename All Files to 'Artist - Title.mp3'", command=self.renameAllFiles, fg=fontColor.get(), font=allButtonsFont,
                                      bg=color)
        self.MassRenameButton.place(x=columnTwo, y=215)
        if play_list.useMassFileEditor:
            self.MassRenameButton.config(state = tk.NORMAL)
        else:
            self.MassRenameButton.config(state = tk.DISABLED)
                
        self.undoMassRenameButton = tk.Button(self.top, text="Restore Previous Names to All Files.", command=self.restorePreviousNames, fg=fontColor.get(), font=allButtonsFont,
                                      bg=color)
        self.undoMassRenameButton.place(x=columnTwo, y=245)
        if os.path.isfile(self.undoRenameBackupFile) and play_list.useMassFileEditor:
            self.undoMassRenameButton.config(state = tk.NORMAL)
        else:
            self.undoMassRenameButton.config(state = tk.DISABLED)
            
        self.MassArtistTitleComposeButton = tk.Button(self.top, text="Compose Artist/Title from FileName to All Files.mp3'", command=self.composeArtistTitleAll, fg=fontColor.get(), font=allButtonsFont,
                                      bg=color)
        self.MassArtistTitleComposeButton.place(x=columnTwo, y=275)
        if play_list.useMassFileEditor:
            self.MassArtistTitleComposeButton.config(state = tk.NORMAL)
        else:
            self.MassArtistTitleComposeButton.config(state = tk.DISABLED)
        
        self.undoMassArtistTitleComposeButton = tk.Button(self.top, text="Restore Previous Artist/Title to All Files", command=self.undoComposeArtistTitleAll, fg=fontColor.get(), font=allButtonsFont,
                                      bg=color)
        self.undoMassArtistTitleComposeButton.place(x=columnTwo, y=305)
        if play_list.useMassFileEditor and os.path.isfile(self.undoArtistTitleBackupFile):
            self.undoMassArtistTitleComposeButton.config(state = tk.NORMAL)
        else:
            self.undoMassArtistTitleComposeButton.config(state = tk.DISABLED)
        self.top.bind("<Tab>", self.focus_out)
        self.top.bind("<Escape>", self.destroyEsc)
        dialog = self

    def tagCapitalizer(self):
        if self.ArtistTag.get()!= "Various":
            newValue=self.ArtistTag.get().split(" ")
            value=""
            for word in newValue:
                value+= word.capitalize() + " "
            self.ArtistTag.delete(0, tk.END) 
            self.ArtistTag.insert(0, value.strip(" ")) 
        if self.GenreTag.get()!= "Various":
            newValue=self.GenreTag.get().split(" ")
            value=""
            for word in newValue:
                value+= word.capitalize() + " "
            self.GenreTag.delete(0, tk.END) 
            self.GenreTag.insert(0, value.strip(" ")) 
        if self.TitleTag.get()!= "Various":
            newValue=self.TitleTag.get().split(" ")
            value=""
            for word in newValue:
                value+= word.capitalize() + " "
            self.TitleTag.delete(0, tk.END) 
            self.TitleTag.insert(0, value.strip(" ")) 
        if self.AlbumTag.get()!= "Various":
            newValue=self.AlbumTag.get().split(" ")
            value=""
            for word in newValue:
                value+= word.capitalize() + " "
            self.AlbumTag.delete(0, tk.END) 
            self.AlbumTag.insert(0, value.strip(" ")) 
        if self.YearTag.get()!= "Various":
            newValue=self.YearTag.get().split(" ")
            value=""
            for word in newValue:
                value+= word.capitalize() + " "
            self.YearTag.delete(0, tk.END) 
            self.YearTag.insert(0, value.strip(" ")) 
    
    def tagSemiCapitalizer(self):
        if self.ArtistTag.get()!= "Various":
            newValue=self.ArtistTag.get().split(" ")
            value=""
            for word in newValue:
                if newValue.index(word) == 0:
                    value+= word.capitalize() + " "
                else:
                    value+= word.lower() + " "
            self.ArtistTag.delete(0, tk.END) 
            self.ArtistTag.insert(0, value.strip(" ")) 
        if self.GenreTag.get()!= "Various":
            newValue=self.GenreTag.get().split(" ")
            value=""
            for word in newValue:
                if newValue.index(word) == 0:
                    value+= word.capitalize() + " "
                else:
                    value+= word.lower() + " "
            self.GenreTag.delete(0, tk.END) 
            self.GenreTag.insert(0, value.strip(" ")) 
        if self.TitleTag.get()!= "Various":
            newValue=self.TitleTag.get().split(" ")
            value=""
            for word in newValue:
                if newValue.index(word) == 0:
                    value+= word.capitalize() + " "
                else:
                    value+= word.lower() + " "
            self.TitleTag.delete(0, tk.END) 
            self.TitleTag.insert(0, value.strip(" ")) 
        if self.AlbumTag.get()!= "Various":
            newValue=self.AlbumTag.get().split(" ")
            value=""
            for word in newValue:
                if newValue.index(word) == 0:
                    value+= word.capitalize() + " "
                else:
                    value+= word.lower() + " "
            self.AlbumTag.delete(0, tk.END) 
            self.AlbumTag.insert(0, value.strip(" ")) 
        if self.YearTag.get()!= "Various":
            newValue=self.YearTag.get().split(" ")
            value=""
            for word in newValue:
                if newValue.index(word) == 0:
                    value+= word.capitalize() + " "
                else:
                    value+= word.lower() + " "
            self.YearTag.delete(0, tk.END) 
            self.YearTag.insert(0, value.strip(" ")) 
    
    def changeTagFormat(self, event):
        if self.tagTextFormat.get() == "Capitalize":
            self.tagCapitalizer()
        elif self.tagTextFormat.get() == "SemiCapitalize":
            self.tagSemiCapitalizer()
        elif self.tagTextFormat.get() == "Upper Case":
            value = self.ArtistTag.get()
            if value!= "Various":
                self.ArtistTag.delete(0, tk.END) 
                self.ArtistTag.insert(0, value.strip(" ").upper()) 
            value = self.GenreTag.get()
            if value!= "Various":
                self.GenreTag.delete(0, tk.END) 
                self.GenreTag.insert(0, value.strip(" ").upper()) 
            value = self.TitleTag.get()
            if value!= "Various":
                self.TitleTag.delete(0, tk.END) 
                self.TitleTag.insert(0, value.strip(" ").upper()) 
            value = self.AlbumTag.get()
            if value!= "Various":
                self.AlbumTag.delete(0, tk.END) 
                self.AlbumTag.insert(0, value.strip(" ").upper()) 
            value = self.YearTag.get()
            if value!= "Various":
                self.YearTag.delete(0, tk.END) 
                self.YearTag.insert(0, value.strip(" ").upper()) 
        elif self.tagTextFormat.get() == "Lower Case":
            value = self.ArtistTag.get()
            if value!= "Various":
                self.ArtistTag.delete(0, tk.END) 
                self.ArtistTag.insert(0, value.strip(" ").lower()) 
            value = self.GenreTag.get()
            if value!= "Various":
                self.GenreTag.delete(0, tk.END) 
                self.GenreTag.insert(0, value.strip(" ").lower()) 
            value = self.TitleTag.get()
            if value!= "Various":
                self.TitleTag.delete(0, tk.END) 
                self.TitleTag.insert(0, value.strip(" ").lower()) 
            value = self.AlbumTag.get()
            if value!= "Various":
                self.AlbumTag.delete(0, tk.END) 
                self.AlbumTag.insert(0, value.strip(" ").lower()) 
            value = self.YearTag.get()
            if value!= "Various":
                self.YearTag.delete(0, tk.END) 
                self.YearTag.insert(0, value.strip(" ").lower()) 

    def setNAOnName(self, event):
        self.nameTextFormat.set("NA")

    def setNAOnTags(self, event):
        self.tagTextFormat.set("NA")
    
    def changeNameFormat(self, event):
        if self.nameTextFormat.get() == "Capitalize":
            self.NameCapitalizer()
        elif self.nameTextFormat.get() == "SemiCapitalize":
            self.NameSemiCapitalizer()
        elif self.nameTextFormat.get() == "Upper Case":
            value = self.NameTag.get()
            self.NameTag.delete(0, tk.END)
            if value.count("-") == 1:
                value = value.split("-")    
                self.NameTag.insert(0, value[0].strip(" ").upper() + " - " + value[1].strip(" ").upper()) 
            else:
                self.NameTag.insert(0, value.strip(" ").upper())
        elif self.nameTextFormat.get() == "Lower Case":
            value = self.NameTag.get()
            self.NameTag.delete(0, tk.END)
            if value.count("-") == 1:
                value = value.split("-")    
                self.NameTag.insert(0, value[0].strip(" ").lower() + " - " + value[1].strip(" ").lower()) 
            else:
                self.NameTag.insert(0, value.strip(" ").lower())
    
    def composeArtistTitleAll(self):# to be fixed
        dictionary={}
        dict_list=[]
        dict_loaded=False
        if os.path.exists(self.undoArtistTitleBackupFile):
            try:
                file = open(self.undoArtistTitleBackupFile, "rb")
                dict_list = pickle.load(file)
            except Exception:
                dict_list = [] #make sure it's empty
                print("Exception when loading File: " + str(self.undoArtistTitleBackupFile))
                print("Since the content has been corrupted, your file will be replaced.")
            else:
                dict_loaded = True
                file.close()
            finally:
                file = open(self.undoArtistTitleBackupFile, "wb")
        else:
            file = open(self.undoArtistTitleBackupFile, "wb")
        for song in play_list.validFiles:
            if song.fileName != "":
                alreadyContained = False
                if dict_loaded:
                    for element in dict_list:
                        if element["newArtist"] == song.Artist and element["newTitle"] == song.Title and element["fileName"] == song.fileName:
                            alreadyContained = True
                            break
                if alreadyContained == False and os.path.exists(song.filePath):
                    mp3file = EasyID3(song.filePath)
                    dictionary['fileName'] = song.fileName
                    if song.Artist!= "Various":
                        dictionary['oldArtist'] = song.Artist
                    else:
                        dictionary['oldArtist'] = ""
                    if song.Title != "Various":
                        dictionary['oldTitle'] = song.Title
                    else:
                        dictionary['oldTitle'] = ""
                    if pygame.mixer.get_init() and play_list.validFiles.index(song) == play_list.currentSongIndex and pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("clear.mp3") #use this file to release the playback
                    if "-" in song.fileName:
                        value = song.fileName.split("-")
                        song.Artist = value[0].strip(" ")
                        value[1] = value[1].strip(" ")
                        song.Title = value[1].rstrip(".mp3 ")
                        mp3file["artist"] = song.Artist
                        mp3file["title"] = song.Title
                        dictionary["newArtist"] = song.Artist
                        dictionary["newTitle"] = song.Title
                    else:
                        song.Artist = value[0].strip(" ").rstrip(".mp3 ")
                        mp3file["artist"] = song.Artist
                        dictionary["newArtist"] = song.Artist
                        dictionary["newTitle"] = ""
                    dict_list.append(dictionary)
                    dictionary = {}
                    mp3file.save(v2_version=3)
            else: #this branch should never be reached
                messagebox.showinfo("Information", "The name should not be empty.")
        self.ArtistTag.delete(0, tk.END)
        self.ArtistTag.insert(0, self.Song.Artist)
        self.TitleTag.delete(0, tk.END)
        self.TitleTag.insert(0, self.Song.Title)
        pickle.dump(dict_list, file)
        file.close()
        if os.path.isfile(self.undoArtistTitleBackupFile) and play_list.useMassFileEditor:
            self.undoMassArtistTitleComposeButton.config(state = tk.NORMAL)
        else:
            self.undoMassArtistTitleComposeButton.config(state = tk.DISABLED)
    
    def undoComposeArtistTitleAll(self):
        dict_list=[]
        try:
            file = open(self.undoArtistTitleBackupFile, "rb")
            dict_list = pickle.load(file)
            file.close()
        except Exception as exp:
            dict_list = [] #make sure it's empty
            print("Backup File Exception: " + str(exp))
            print("File: " + str(self.undoArtistTitleBackupFile)+ " might be corrupted.")
        for song in play_list.validFiles:
            for element in dict_list:
                if element['fileName'] == song.fileName:
                    if pygame.mixer.get_init() and play_list.validFiles.index(song) == play_list.currentSongIndex and pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("clear.mp3") #use this file to release the playback
                    mp3file = EasyID3(song.filePath)
                    song.Artist = element['oldArtist']
                    song.Title = element['oldTitle']
                    mp3file["artist"] = song.Artist
                    mp3file["title"] = song.Title
                    if song.Artist == "":
                        song.Artist = "Various"
                    if song.Title == "":
                        song.Title = "Various"
                    mp3file.save(v2_version=3)
                    del dict_list[dict_list.index(element)]
                    break
        if len(dict_list) > 0 :
            message = ""
            for element in dict_list:
                message += element['fileName'] + "\n"
            messagebox.showinfo("Information", "Some files not found within playlist:\n" + message)
        self.ArtistTag.delete(0, tk.END)
        self.ArtistTag.insert(0, self.Song.Artist)
        self.TitleTag.delete(0, tk.END)
        self.TitleTag.insert(0, self.Song.Title)
        file = open(self.undoArtistTitleBackupFile, "wb")
        pickle.dump(dict_list, file)
        file.close()

    def renameAllFiles(self):  # to be tested
        dictionary = {}
        dict_list = []
        dict_loaded = False
        if os.path.exists(self.undoRenameBackupFile):
            try:
                file = open(self.undoRenameBackupFile, "rb")
                dict_list = pickle.load(file)
            except Exception:
                dict_list = [] #make sure the list is empty now
                print("Exception when reading the content of File: " + str(self.undoRenameBackupFile))
                print("Since the content has been corrupted, your file will be replaced.")
            else:
                dict_loaded = True
                file.close()
            finally:
                file = open(self.undoRenameBackupFile, "wb")
        else:
            file = open(self.undoRenameBackupFile, "wb")
        for song in play_list.validFiles:
            if song.Artist != "Various" and song.Title != "Various":
                newFileName = song.Artist + " - " + song.Title + ".mp3"
                pathToFile = song.filePath.split(song.fileName)
                pathToFile = pathToFile[0]
                alreadyContained = False
                if dict_loaded:
                    for element in dict_list:
                        if element['newName'] == pathToFile + newFileName:
                            alreadyContained = True
                            break
                if alreadyContained == False and os.path.exists(song.filePath):
                    dictionary['oldName'] = song.filePath
                    dictionary['newName'] = pathToFile + newFileName
                    dict_list.append(dictionary)
                    dictionary = {}
                    try:
                        if pygame.mixer.get_init():
                            if play_list.validFiles.index(
                                    song) == play_list.currentSongIndex and pygame.mixer.music.get_busy():  # enter here if the file to be renamed is currently playing
                                play_list.isSongPause = True
                                pygame.mixer.music.stop()
                                shutil.copy(song.filePath,
                                            pathToFile + newFileName)  # make a copy of this file to the project locaiton
                                fileToRemove = song.filePath
                                song.fileName = newFileName  # this will update the play_list with the new song info
                                song.filePath = pathToFile + newFileName
                                pygame.mixer.music.load(
                                    song.filePath)  # load the new file in the player, so that the old one gets released
                                os.remove(fileToRemove)  # remove the old one
                        else:
                            os.rename(song.filePath, pathToFile + newFileName)  # this will rename the file
                            song.fileName = newFileName  # this will update the play_list with the new song info
                            song.filePath = pathToFile + newFileName
                    except Exception as Exp:
                        print("Exception during Mass Rename: " + str(Exp))
        displayElementsOnPlaylist()
        self.NameTag.delete(0, tk.END)
        self.NameTag.insert(0, self.Song.fileName)
        pickle.dump(dict_list, file)
        file.close()
        if os.path.isfile(self.undoRenameBackupFile) and play_list.useMassFileEditor:
            self.undoMassRenameButton.config(state=tk.NORMAL)
        else:
            self.undoMassRenameButton.config(state=tk.DISABLED)

    def restorePreviousNames (self): # to be tested
        global play_list
        dict_list=[]
        message = ""
        try:
            file = open(self.undoRenameBackupFile, "rb")
            dict_list = pickle.load(file)
            file.close()
        except Exception as exp:
            dict_list = [] #make sure it's empty
            print("Backup File Exception: " + exp)
            print("File: " + str(self.undoRenameBackupFile)+ " might be corrupted.")
        for song in play_list.validFiles:
            for element in dict_list:
                if element['newName'] == song.filePath:
                    filePath = element['newName'].split(song.fileName)
                    filePath = filePath[0]
                    FileName = element['oldName'].split(filePath)
                    FileName = FileName[1]
                    try:
                        if pygame.mixer.get_init():
                            if play_list.validFiles.index(song) == play_list.currentSongIndex and pygame.mixer.music.get_busy():  # enter here if the file to be renamed is currently playing
                                play_list.isSongPause = True
                                pygame.mixer.music.stop()
                                shutil.copy(song.filePath, element['oldName'])  # make a copy of this file to the project locaiton
                                fileToRemove = song.filePath
                                song.fileName = FileName  # this will update the play_list with the new song info
                                song.filePath = element['oldName']
                                pygame.mixer.music.load(song.filePath)  # load the new file in the player, so that the old one gets released
                                os.remove(fileToRemove)  # remove the old one
                        else:
                            os.rename(song.filePath, element['oldName'])  # this will rename the file
                            song.fileName = FileName  # this will update the play_list with the new song info
                            song.filePath = element['oldName']
                    except Exception as Exp:
                        print("Exception during Undo Mass Rename: " + str(Exp))
                    del dict_list[dict_list.index(element)]
                    break
                if dict_list.index(element) == len(dict_list)-1 and element['newName'] != song.filePath:
                    message += song.fileName + "\n"
        displayElementsOnPlaylist()
        self.NameTag.delete(0, tk.END)
        self.NameTag.insert(0, self.Song.fileName)
        file = open(self.undoRenameBackupFile, "wb")
        pickle.dump(dict_list, file)
        file.close()
        if message!="":
            messagebox.showinfo("Information","Some file were not renamed: \n" + message)
        
    def NameCapitalizer(self):
        if "-" in self.NameTag.get():
            value = self.NameTag.get()
            value = value.split("-")
            artist = ""
            title = ""
            for word in value[0].split(" "):
                artist += word.capitalize() + " "
            for word in value[1].split(" "):
                if value[1].split(" ").index(word) < len(value[1].split(" "))-1:
                    title += word.capitalize() + " "
                else:
                    title += word.capitalize()
            
            if len(value) > 2:
                title+=" "
                for i in range(2, len(value)):
                    title+= value[i].capitalize() + " "
            title = title.strip(" ")  # remove the last blank space
            artist = artist.strip(" ")
            if ".mp3" in title:
                value = artist + " - " +title
            else:
                value = artist + " - " + title + ".mp3"
            self.NameTag.delete(0, tk.END)
            self.NameTag.insert(0, value)
        else:
            value = self.NameTag.get()
            value = value.split(" ")
            newValue = ""
            for element in value:
                newValue += element.strip(" ").capitalize() + " "
            self.NameTag.delete(0, tk.END)
            self.NameTag.insert(0, newValue.rstrip(" ")) 

    def composeArtistTitle(self):
        if self.NameTag.get() != "":
            if "-" in self.NameTag.get():
                value = self.NameTag.get()
                value = value.split("-")
                self.ArtistTag.delete(0,tk.END)
                self.ArtistTag.insert(0, value[0].strip(" "))
                self.TitleTag.delete(0, tk.END)
                value[1] = value[1].strip(" ") #remove any whitespaces at the beginning, or end
                self.TitleTag.insert(0, value[1].rstrip(".mp3"))
            else:
                self.ArtistTag.delete(0, tk.END)
                self.ArtistTag.insert(0, self.NameTag.get().rstrip(".mp3 "))
        else:
            messagebox.showinfo("Information", "The name should not be empty.")

    def composeFileName(self):
        if self.ArtistTag.get() != "Various" and self.TitleTag.get() != "Various":
            self.NameTag.delete(0,tk.END)
            self.NameTag.insert(0, self.ArtistTag.get() + " - " + self.TitleTag.get())
        else:
            messagebox.showinfo("Information", "The Artist Name nor the Title should be 'Various'.")

    def NameSemiCapitalizer(self):
        if "-" in self.NameTag.get():
            value = self.NameTag.get()
            value = value.split("-")
            artist = ""
            title = ""
            value[0] = value[0].strip(" ")
            for word in value[0].split(" "):
                artist += word.capitalize() + " "
            value[1] = value[1].strip(" ")
            for word in value[1].split(" "):
                if value[1].split(" ").index(word) == 0:
                    title = word.capitalize() + " "
                else:
                    title += word.lower() + " "
            
            if len(value) > 2:
                for i in range(2, len(value)):
                    title+= value[i].lower() + " "
            title = title.strip(" ") #remove the last blank space
            artist = artist.strip(" ")
            if ".mp3" in title:
                value = artist + " - " +title
            else:
                value = artist + " - " + title + ".mp3"
            self.NameTag.delete(0, tk.END)
            self.NameTag.insert(0, value)
        else:
            value = self.NameTag.get()
            value = value.capitalize()
            self.NameTag.delete(0, tk.END)
            self.NameTag.insert(0, value) 

    def SaveChanges(self):
        global play_list
        pathToFile = self.Song.filePath.split(self.Song.fileName)
        pathToFile = pathToFile[0]
        index = play_list.validFiles.index(self.Song)
        if ".mp3" not in self.NameTag.get().lower():
            value = self.NameTag.get()
            self.NameTag = StringVar()
            self.NameTag.set(value + ".mp3")
        try:
            if pygame.mixer.get_init() and index == play_list.currentSongIndex and pygame.mixer.music.get_busy(): # enter here if the file to be renamed is currently playing
                if play_list.RESUMED:
                    play_list.currentSongPosition = math.floor(play_list.currentSongPosition + pygame.mixer.music.get_pos() / 1000)
                else:
                    play_list.currentSongPosition = math.floor(pygame.mixer.music.get_pos()/1000)
                pygame.mixer.music.stop()
                if self.Song.filePath.lower() != (pathToFile+self.NameTag.get()).lower():
                    shutil.copy(self.Song.filePath, pathToFile+self.NameTag.get())
                    fileToRemove = self.Song.filePath
                    self.Song.fileName = self.NameTag.get()  # this will update the play_list with the new song info
                    self.Song.filePath = pathToFile + self.NameTag.get()
                    self.saveMp3Tags()
                    del play_list.validFiles[play_list.currentSongIndex]
                    play_list.validFiles.insert(play_list.currentSongIndex, self.Song)
                    displayElementsOnPlaylist()
                    pygame.mixer.music.load(play_list.validFiles[play_list.currentSongIndex].filePath) #release the old file, to be able to remove it
                    os.remove(fileToRemove)  # remove the old one
                    play_music() #load the new file in the player, so that the old one gets released
                else: #will enter here is used Capitalize Filename Option
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("clear.mp3") #use this file to release the playback
                    if self.Song.filePath != pathToFile + self.NameTag.get():
                        os.rename(self.Song.filePath, pathToFile + self.NameTag.get())  # this will rename the file
                        self.Song.fileName = self.NameTag.get()  # this will update the play_list with the new song info
                        self.Song.filePath = pathToFile + self.NameTag.get()
                    self.saveMp3Tags()
                    pygame.mixer.music.load(self.Song.filePath)
                    displayElementsOnPlaylist()
                    play_music()
            else:
                if self.Song.filePath != (pathToFile + self.NameTag.get()):
                    os.rename(self.Song.filePath, pathToFile + self.NameTag.get()) #this will rename the file
                    self.Song.fileName = self.NameTag.get() # this will update the play_list with the new song info
                    self.Song.filePath = pathToFile + self.NameTag.get()
                self.saveMp3Tags()
                displayElementsOnPlaylist()
        except Exception as Exp:
            print("Exception during File Tag Update: " + str(Exp))

    def destroy(self):
        global dialog
        self.top.destroy()
        dialog = None

    def destroyEsc(self,event):
        self.destroy()

    def focus_out(self, event):
        window.wm_attributes("-topmost", 1)
        window.grab_set()
        window.focus_force()

    def saveMp3Tags(self):
        mp3file = EasyID3(self.Song.filePath)
        if self.GenreTag.get() != "Various":
            mp3file["genre"] = self.GenreTag.get()
            self.Song.Genre = mp3file["genre"]
            self.Song.Genre = self.Song.Genre[0]
        if self.ArtistTag.get() != "Various":
            mp3file["artist"] = self.ArtistTag.get()
            self.Song.Artist = mp3file["artist"]
            self.Song.Artist = self.Song.Artist[0]
        if self.AlbumTag.get() != "Various":
            mp3file["album"] = self.AlbumTag.get()
            self.Song.Album = mp3file["album"]
            self.Song.Album = self.Song.Album[0]
        if self.YearTag.get() != "Various":
            mp3file["date"] = self.YearTag.get()
            self.Song.Year = mp3file["date"]
            self.Song.Year = self.Song.Year[0]
        if self.TitleTag.get() != "Various":
            mp3file["title"] = self.TitleTag.get()
            self.Song.Title = mp3file["title"]
            self.Song.Title = self.Song.Title[0]
        mp3file.save(v2_version=3)

    def take_focus(self):
        self.top.wm_attributes("-topmost", 1)
        self.top.grab_set()
        self.NameTag.focus_force()

class GrabLyricsTool:
    def __init__(self, index="empty"):
        global allButtonsFont
        global dialog
        self.LyricsDownloads = "LyricsDownloads.lyl"
        if index=="empty":
            index = play_list.currentSongIndex # do not forget that currentSongIndex can be None
        self.songIndex = index
        if self.songIndex != None: # make sure there is a song to search lyrics for.
            color = OpenFileButton["bg"]  # get the color which the rest of elements is using at the moment
            self.top = tk.Toplevel(window, bg=color)
            Window_Title = "Grab Lyrics Tool"
            self.top.title(Window_Title)
            self.top.geometry("540x550+100+100")
            self.top.protocol("WM_DELETE_WINDOW", self.destroy)
            self.top.attributes('-alpha', play_list.windowOpacity)
            allButtonsFont = skinOptions[2][play_list.skin]
            self.welcomeMessage = StringVar()
            self.welcomeMessage.set("Welcome to Grab Lyrics Tool!\n\nThe lyrics are grabbed from various online sources,\n" \
                                +"the results are provided according to your internet connection speed.\n" \
                                +"The Search is based on Artist - Title tags, if these tags are not set\n" \
                                +"accordingly, the lyrics will never be found.")
            tk.Label(self.top, textvariable=self.welcomeMessage, fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=5, y=5)
            self.Lyrics = StringVar()
            self.Lyrics.set("Lyrics")
            tk.Label(self.top, textvariable=self.Lyrics, fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=5, y=115)
            self.frame = tk.Frame(self.top, width=100, height=30, bg=color, borderwidth=1)
            self.frame.place(x=10, y=135)
            self.scrlbar = tk.Scrollbar(self.frame, orient="vertical", width=10)
            self.listboxLyrics = tk.Listbox(self.frame, fg=fontColor.get(), font=allButtonsFont, width=65, bg=color, height=20, \
                         yscrollcommand=self.scrlbar.set)
            self.listboxLyrics.pack(padx=10, pady=10,side = tk.LEFT, fill=tk.X)
            self.scrlbar.config(command=self.listboxLyrics.yview)
            self.scrlbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.SaveLyrics = tk.Button(self.top, text="Save Lyrics",command=self.saveLyrics, fg=fontColor.get(), font=allButtonsFont,
                                              bg=color, state=tk.DISABLED)
            self.SaveLyrics.place(x=10,y=500)

            self.RemoveLyrics = tk.Button(self.top, text="Remove Lyrics", command=self.removeLyrics, fg=fontColor.get(),
                                        font=allButtonsFont,
                                        bg=color, state=tk.DISABLED)
            self.RemoveLyrics.place(x=120, y=500)

            self.DownloadLyricsAll = tk.Button(self.top, text="Download All Lyrics", command=self.downloadAllLyrics, fg=fontColor.get(),
                                          font=allButtonsFont,
                                          bg=color)
            self.DownloadLyricsAll.place(x=260, y=500)
            self.top.bind("<Tab>", self.focus_out)
            self.top.bind("<Escape>", self.destroyEsc)
            if os.path.exists(self.LyricsDownloads):
                try:
                    file = open(self.LyricsDownloads, "rb")
                    lyricsList = pickle.load(file)
                    file.close()
                    for element in lyricsList:
                        if element["fileName"] == play_list.validFiles[self.songIndex].fileName:
                            for line in element["lyrics_list"]:
                                self.listboxLyrics.insert(tk.END, line)
                            self.Lyrics.set("Lyrics for '" + play_list.validFiles[self.songIndex].Artist + " - " \
                                            + play_list.validFiles[self.songIndex].Title + "' -> were found locally:")
                            self.RemoveLyrics.config(state=tk.NORMAL)
                            break
                    if self.listboxLyrics.size() == 0: #lyrics not found.
                        self.LyricsDisplay()
                except Exception:
                    print("Could not load the file: " + self.LyricsDownloads)
                    print("I will search for lyrics online.")
                    self.LyricsDisplay()
            else:
                self.LyricsDisplay()
            dialog = self

    def downloadAllLyrics(self):
        for i in range(0, len(play_list.validFiles)):
            self.songIndex = i
            text_list, source = self.accessPage()
            if len(text_list) > 0 and source != "":
                self.saveLyrics(text_list)
            else:
                print("Lyrics not found for: " + play_list.validFiles[self.songIndex].fileName)

    def removeLyrics(self):
        filename = play_list.validFiles[self.songIndex].fileName
        lyrics_dictionary = {}
        lyricsList = []
        if os.path.exists(self.LyricsDownloads):
            try:
                file = open(self.LyricsDownloads, "rb")
                lyricsList = pickle.load(file)
                file.close()
            except Exception:
                print("Could not load the file: " + self.LyricsDownloads)
        if len(lyricsList) > 0:
            for element in lyricsList:
                if element["fileName"] == filename:
                    del lyricsList[lyricsList.index(element)]
                    messagebox.showinfo("Info", "The lyrics for this song were removed.")
                    break
            try:
                file = open(self.LyricsDownloads, "wb")
                pickle.dump(lyricsList, file)
                file.close()
                self.RemoveLyrics.config(state=tk.DISABLED)
                self.SaveLyrics.config(state=tk.NORMAL)
            except Exception:
                print("Could not remove Lyrics for: " + filename)

    def saveLyrics(self, list_text=None):
        filename = play_list.validFiles[self.songIndex].fileName
        lyrics_dictionary = {}
        lyricsList = []
        if os.path.exists(self.LyricsDownloads):
            try:
                file = open(self.LyricsDownloads, "rb")
                lyricsList = pickle.load(file)
                file.close()
            except Exception:
                print("Could not load the file: " + self.LyricsDownloads)
        alreadyContained = False
        if len(lyricsList) > 0:
            for element in lyricsList:
                if element["fileName"] == filename:
                    alreadyContained = True
                    messagebox.showinfo("Info", "This lyrics are already stored in your local computer.")
                    break
        if alreadyContained == False:
            lyrics_dictionary["fileName"] = filename
            if list_text == None:
                lyrics_dictionary["lyrics_list"] = list(self.listboxLyrics.get(0,tk.END))
            else:
                lyrics_dictionary["lyrics_list"] = list_text
            lyricsList.append(lyrics_dictionary)
            lyrics_dictionary={}
            del lyrics_dictionary
            try:
                file = open(self.LyricsDownloads, "wb")
                pickle.dump(lyricsList, file)
                file.close()
                self.RemoveLyrics.config(state=tk.NORMAL)
            except Exception:
                print("Could not save Lyrics for: " + filename)

    def accessPage(self):
        urllib3.disable_warnings()
        text_list = []
        source = ""
        if play_list.validFiles[self.songIndex].Artist != "Various" and play_list.validFiles[
            self.songIndex].Title != "Various":
            artist = play_list.validFiles[self.songIndex].Artist
            artist = artist.replace(" ", "-")
            title = play_list.validFiles[self.songIndex].Title
            title = title.replace(" ", "-")
            if play_list.LyricsActiveSource == "all":
                url = "http://www.lyrics.my/artists/" + artist + "/lyrics/" + title  # this is possible to change with time. Let's hope it doesn't
                http = urllib3.PoolManager()
                response = http.request('GET', url)
                if response.status == 200:
                    text_list = self.filterTextFromLyricsMy(response.data)
                    source = "lyrics.my"
                else:
                    url = "https://genius.com/" + artist + "-" + title + "-lyrics"  # this is possible to change with time. Let's hope it doesn't
                    # The URL system for genius.com is structured like this at the moment.
                    http = urllib3.PoolManager()
                    response = http.request('GET', url)
                    if response.status == 200:
                        text_list = self.filterTextFromGeniusCom(response.data)
                        source = "genius.com"
            elif play_list.LyricsActiveSource == "lyrics.my":
                url = "http://www.lyrics.my/artists/" + artist + "/lyrics/" + title  # this is possible to change with time. Let's hope it doesn't
                http = urllib3.PoolManager()
                response = http.request('GET', url)
                if response.status == 200:
                    text_list = self.filterTextFromLyricsMy(response.data)
                    source = "lyrics.my"
            elif play_list.LyricsActiveSource == "genius.com":
                url = "https://genius.com/" + artist + "-" + title + "-lyrics"  # this is possible to change with time. Let's hope it doesn't
                # The URL system for genius.com is structured like this at the moment.
                http = urllib3.PoolManager()
                response = http.request('GET', url)
                if response.status == 200:
                    text_list = self.filterTextFromGeniusCom(response.data)
                    source = "genius.com"
        return text_list, source

    def filterTextFromGeniusCom(self, data):
        text = BeautifulSoup(data, "html.parser")
        text = text.decode("utf-8")
        # Start filtering the html content of the webpage
        text = text.split('<div class="lyrics">')
        text = text[1].split('</div>')
        text = text[0]
        text = text.replace("   ", "")
        text = text.replace("\n ", "\n")

        text = text.replace("<p>", "")
        text = text.replace("<b>", "")
        text = text.replace("</b>", "")
        text = text.replace("<i>", "")
        text = text.replace("</i>", "")
        text = text.replace("<!--sse-->", "")
        text = text.replace("<!--/sse-->", "")
        text = text.replace("</p>", "")
        text = text.replace("<br>", "")
        text = text.replace("<br/>", "")
        text = text.replace("[", "")
        text = text.replace("]", "")

        if "<a annotation-fragment" in text:  # if there are any adds between these lyrics, lets remove them.
            text = text.split("<a annotation-fragment=")
            aux = []
            for element in text:
                if 'prevent-default-click="">' in element:
                    element = element.split('prevent-default-click="">')
                    aux.append(element[1])
                else:
                    aux.append(element)
            text = "".join(aux)
            text = text.replace("</a>", "")

        newText = ""
        list_text = []
        for i in range(0, len(text)):
            if (text[i] >= "A" and text[i] <= "Z") or (text[i] >= "a" and text[i] <= "z") or (
                    text[i] >= "0" and text[i] <= "9"):
                newText += text[i]
            elif text[i] == "\n":
                if newText != "":
                    list_text.append("    " + newText)
                    newText = ""
                if text[i - 1] == "\n" and text[i] == "\n" and text[i - 2] == "\n" and i > 3:
                    list_text.append("")
            elif i > 0:
                if (text[i - 1] >= "A" and text[i - 1] <= "Z") or (text[i - 1] >= "a" and text[i - 1] <= "z") \
                        or text[i - 1] == "," or text[i - 1] == ".":  # this is for word spacing.
                    newText += text[i]
        return list_text

    def filterTextFromLyricsMy(self, data):
        text = BeautifulSoup(data, "html.parser")
        text = text.decode("utf-8")
        # Start filtering the html content of the webpage
        text = text.split('<div class="show_lyric">')
        text = text[1].split('</div>')
        text = text[0]
        text = text.replace("   ", "")
        text = text.replace("\n ", "\n")

        text = text.replace("<p>", "")
        text = text.replace("<b>", "")
        text = text.replace("</b>", "")
        text = text.replace("<i>", "")
        text = text.replace("</i>", "")
        text = text.replace("</p>", "")
        text = text.replace("<br>", "")
        text = text.replace("</br>", "")
        text = text.replace("<br/>", "")
        text = text.replace("[", "(")
        text = text.replace("]", ")")
        newText = ""
        list_text = []
        for i in range(0, len(text)):
            if (text[i] >= "A" and text[i] <= "Z") or (text[i] >= "a" and text[i] <= "z") or (
                    text[i] >= "0" and text[i] <= "9") or text[i] == "(" or text[i] == ")":
                newText += text[i]
            elif text[i] == "\n":
                if newText != "":
                    list_text.append("    " + newText)
                    newText = ""
                if newText =="" and len(list_text)>1 and list_text[(len(list_text)-1)]!="" and list_text[(len(list_text)-2)]!="":
                    list_text.append("")
            elif i > 0:
                if (text[i - 1] >= "A" and text[i - 1] <= "Z") or (text[i - 1] >= "a" and text[i - 1] <= "z") \
                        or text[i - 1] == "," or text[i - 1] == "." or text[i - 1] == "?" or text[i - 1] == "!":  # this is for word spacing.
                    newText += text[i]
        return list_text

    def LyricsDisplay(self): #to be continued
        text_list, source = self.accessPage()
        if len(text_list) > 0:
            self.Lyrics.set("Lyrics for '" + play_list.validFiles[self.songIndex].Artist + " - " \
                            + play_list.validFiles[self.songIndex].Title + "' -> were found on " + source + ":")
            for element in text_list:
                self.listboxLyrics.insert(tk.END, element)
            self.SaveLyrics.config(state=tk.NORMAL)
        else:
            self.Lyrics.set("Lyrics for '" + play_list.validFiles[self.songIndex].Artist + " - " \
                            + play_list.validFiles[self.songIndex].Title + "' -> were NOT found!\n" +
                            "Make sure you have Artist and Title Tags completed properly.")
    
    def destroy(self):
        global dialog
        self.top.destroy()
        dialog = None

    def destroyEsc(self,event):
        self.destroy()

    def take_focus(self):
        self.top.wm_attributes("-topmost", 1)
        self.top.grab_set()
    
    def focus_out(self, event):
        window.wm_attributes("-topmost", 1)
        window.grab_set()
        window.focus_force()

class GrabArtistBio():
    def __init__(self, index="empty"):
        global allButtonsFont
        global dialog
        self.LyricsDownloads = "LyricsDownloads.lyl"
        if index == "empty":
            index = play_list.currentSongIndex  # do not forget that currentSongIndex can be None
        self.songIndex = index
        if self.songIndex != None:  # make sure there is a song to search lyrics for.
            color = OpenFileButton["bg"]  # get the color which the rest of elements is using at the moment
            self.top = tk.Toplevel(window, bg=color)
            Window_Title = "Artist Bio"
            self.top.title(Window_Title)
            self.top.geometry("440x350+100+100")
            self.top.protocol("WM_DELETE_WINDOW", self.destroy)
            self.top.attributes('-alpha', play_list.windowOpacity)
            allButtonsFont = skinOptions[2][play_list.skin]
            self.Message = StringVar()
            self.Message.set(
                "According to LastFM:\n\n")
            tk.Label(self.top, textvariable=self.Message, fg=fontColor.get(), font=allButtonsFont,
                     bg=color).place(x=5, y=5)
            self.BioText = StringVar()
            self.BioText.set("Artist Bio:")
            tk.Label(self.top, textvariable=self.BioText, fg=fontColor.get(), font=allButtonsFont, bg=color).place(x=15, y=45)
            self.frame = tk.Frame(self.top, width=100, height=30, bg=color, borderwidth=1)
            self.frame.place(x=5, y=65)
            self.scrlbar = tk.Scrollbar(self.frame, orient="vertical", width=10)
            self.listboxLyrics = tk.Listbox(self.frame, fg=fontColor.get(), font=allButtonsFont, width=55, bg=color,
                                            height=15, \
                                            yscrollcommand=self.scrlbar.set)
            self.listboxLyrics.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.X)
            self.scrlbar.config(command=self.listboxLyrics.yview)
            self.scrlbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.ArtistBioDisplay()
            self.top.bind("<Tab>", self.focus_out)
            self.top.bind("<Escape>", self.destroyEsc)
            dialog = self

    def accessPage(self):
        urllib3.disable_warnings()
        text_list = []
        if play_list.validFiles[self.songIndex].Artist != "Various":
            artist = play_list.validFiles[self.songIndex].Artist
            artist = artist.replace(" ", "_")
            if play_list.LyricsActiveSource == "all":
                url = "https://www.last.fm/music/" + artist + "/+wiki" # this is possible to change with time. Let's hope it doesn't
                http = urllib3.PoolManager()
                response = http.request('GET', url)
                if response.status == 200:
                    text_list = self.filterTextFromWikipedia(response.data)
        return text_list

    def filterTextFromWikipedia(self, data):
        text = BeautifulSoup(data, "html.parser")
        text = text.decode("utf-8")
        # Start filtering the html content of the webpage
        text = text.split('<div class="wiki-content" itemprop="description">')
        text = text[1].split('</div>')
        text = text[0]
        text = text.replace("   ", "")

        text = text.replace("<a>", "")
        text = text.replace("</a>", "")
        text = text.replace("<b>", "")
        text = text.replace("</b>", "")
        text = text.replace("<p>", "")
        text = text.replace("</p>", "")
        text = text.replace("<strong>", "")
        text = text.replace("</strong>", "")
        text = text.replace("<em>", "")
        text = text.replace("</em>", "")
        text = text.replace("<i>", "")
        text = text.replace("</i>", "")
        if "<a " in text:  # if there are any adds between these lyrics, lets remove them.
            text = text.split("<a ")
            aux = []
            for element in text:
                if '">' in element:
                    element = element.split('">')
                    aux.append(element[1] + " ")
                else:
                    aux.append(element)
            text = "".join(aux)
            text = text.replace("</a>", "")
        if "<sup " in text:  # if there are any adds between these lyrics, lets remove them.
            text = text.split("<sup ")
            aux = []
            for element in text:
                if '</sup>' in element:
                    element = element.split('</sup>')
                    aux.append(element[1])
                else:
                    aux.append(element)
            text = "".join(aux)
            text = text.replace("</a>", "")
        newText = ""
        list_text = []
        for i in range(0, len(text)):
            if text[i] != "\n":
                newText += text[i]
            if text[i] == "." and len(list_text)%5==0: #make a new paragraph after each 5 sentences.
                list_text.append(newText)
                newText = ""
                list_text.append("") #add an empty line
            elif len(newText)>=45 and (text[i]==" " or text[i] =="-"):
                list_text.append(newText)
                newText=""
        return list_text

    def ArtistBioDisplay(self): #to be continued
        text_list = self.accessPage()
        if len(text_list) > 0:
            for element in text_list:
                self.listboxLyrics.insert(tk.END, element)
        else:
            self.listboxLyrics.insert(tk.END, "No information found")

    def destroy(self):
        global dialog
        self.top.destroy()
        dialog = None

    def destroyEsc(self, event):
        self.destroy()

    def take_focus(self):
        self.top.wm_attributes("-topmost", 1)
        self.top.grab_set()

    def focus_out(self, event):
        window.wm_attributes("-topmost", 1)
        window.grab_set()
        window.focus_force()
        
automaticallyBackupFile = "PlayListBackup.pypl"
allButtonsWidth = 14
allButtonsHeight = 1

LyricsOnlineSources = ["all", "genius.com", "lyrics.my"]

custom_color_list = ["green", "yellow", "purple", "black", "brown", "sienna", "cyan", "magenta", "pink", "blue", "darkblue", "darkgreen", "deeppink", "red", \
                                            "orange", "gold", "silver", "indigo"]

radioButtonsDefaultColor = "lightgray"

custom_font_list = ["Arial 10", "Consolas 10", "Courier 9", "Verdana 9", "Georgia 9", "Tahoma 9", "Rockwell 10", "Fixedsys 11", "Candara 10", "Impact 9", \
                                    "Calibri 10 italic", "Modern 10 bold", "Harrington 10 bold", "Stencil 10 italic"]
progressViewRealTime = 1 #1 - for 1 second
play_list = Playlist()

listBox_Song_selected_index = None
APPLICATION_EXIT = False
skinOptions = [["default.gif", "minilights.gif", "road.gif", "darkg.gif", "leaves.gif", "darkblue.gif", "map.gif", "space.gif", "universe.gif"],\
               ["blue", "red", "gray", "green", "deeppink", "darkblue", "sienna", "indigo", "black", "custom"],\
               ["Consolas 10 bold", "Rockwell 10 bold", "Arial 10 italic", "Candara 10 bold", "Arial 10 bold", "Calibri 10 bold", "Harrington 10 bold", "Fixedsys 11", "Stencil 10"]]

progressBarMargin = 10

visualSongNameLabel = None

allButtonsFont = skinOptions[2][play_list.skin] #default Font value Consola 10 bold:
#default value of play_list.skin is 0
dialog = None

def load_file():
    global play_list
    fileToPlay = filedialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("mp3 files","*.mp3"),("pypl files","*.pypl"),("all files","*.*")))
    if fileToPlay:
        fileToPlay = list(fileToPlay)
        for file in fileToPlay:
            if ".mp3" in file.lower():
                fileName = re.split("/", file)
                fileName = fileName[len(fileName) - 1]
                fileSize = os.path.getsize(file) / (1024 * 1024)
                fileSize = float("{0:.2f}".format(fileSize))
                play_list.validFiles.append(Song(fileName, file, fileSize))
                play_list.currentSongIndex = 0
                textFilesToPlay.set("Files: " + str(len(play_list.validFiles)))
                play_list.playTime += play_list.validFiles[play_list.currentSongIndex].Length
            elif ".pypl" in file:
                loadPlaylistFile(file)
                break
        displayElementsOnPlaylist()

def loadPlaylistFile(fileURL):
    global play_list
    global allButtonsFont
    global fontColor
    global custom_color_list
    global listBox_Song_selected_index
    try:
        file = open(fileURL, "rb")
        content = pickle.load(file)
        file.close()
    except Exception as exp:
        print("Load Playlist File Exception: " + exp)
        print("File: " + str(fileURL)+ " might be corrupted.")
    else:
        if isinstance(content, Playlist):
            play_list = content
            del content
            textFilesToPlay.set("Files: " + str(len(play_list.validFiles)))
            custom_color_list += play_list.userCreatedColors
            #the following lines will help keeping the predefined values of last skin used in case not all fields were customized
            allButtonsFont = skinOptions[2][play_list.skin]
            changeFonts()  # change the font that comes with the new skin
            updateRadioButtons()
            labelBackground.set("lightgray")  # default value
            fontColor.set("white")  # default value
            changingFontColor("<<ComboboxSelected>>")
            changingLabelBackgroundColor("<<ComboboxSelected>>")
            SkinColor.set(skinOptions[1][play_list.skin])
            changingBackgroundElementColor("<<ComboboxSelected>>")

            # checking if the skin was customized:
            if play_list.customElementBackground != None:
                SkinColor.set(custom_color_list[play_list.customElementBackground])
                changingBackgroundElementColor("<<ComboboxSelected>>")
            if play_list.customLabelBackground!= None:
                labelBackground.set(custom_color_list[play_list.customLabelBackground])
                changingLabelBackgroundColor("<<ComboboxSelected>>")
            if play_list.customFont != None:
                allButtonsFont = custom_font_list[play_list.customFont]
                changeFonts()
            if play_list.customFontColor != None:
                fontColor.set(custom_color_list[play_list.customFontColor])
                changingFontColor("<<ComboboxSelected>>")
            if play_list.customChangeBackgroundedLabelsColor != None:
                changingBackgroundedLabelsColor("not important") #the parameter will not be used in this context
            if play_list.customBackgroundPicture!=None: #this will load the custom background
                if ".gif" in play_list.customBackgroundPicture:
                    background_image = tk.PhotoImage(file=play_list.customBackgroundPicture)
                    background_label.configure(image=background_image)
                    background_label.image = background_image
                elif ".jpg" in play_list.customBackgroundPicture or ".jpeg" in play_list.customBackgroundPicture:
                    img = ImageTk.PhotoImage(Image.open(play_list.customBackgroundPicture))
                    background_label.configure(image=img)
                    background_label.image = img
            #Enter here if the skin was not customized, and put the predefined skin.
            if play_list.customElementBackground == None and play_list.customLabelBackground == None and play_list.customFont == None \
                    and play_list.customBackgroundPicture==None and play_list.customChangeBackgroundedLabelsColor == None and \
                            play_list.customFontColor == None:
                SkinColor.set(skinOptions[1][play_list.skin])
                changeSkin("<Double-Button>")
            displayElementsOnPlaylist()
            textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
            if play_list.currentSongIndex != None and len(play_list.validFiles) > 0:
                SongName.set("Paused: " + play_list.validFiles[play_list.currentSongIndex].fileName)
                SongSize.set("Size: " + str(play_list.validFiles[play_list.currentSongIndex].fileSize) + " MB")
                if play_list.progressTime == "Ascending":
                    SongDuration.set("Time Elapsed: {:0>8}".format(str(datetime.timedelta(seconds=play_list.currentSongPosition))))
                else:
                    SongLength = int(play_list.validFiles[play_list.currentSongIndex].Length - play_list.currentSongPosition)
                    SongDuration.set("Time Left: {:0>8}".format(str(datetime.timedelta(seconds=SongLength))))
                #Update Length
                songLength = float("{0:.0f}".format(play_list.validFiles[play_list.currentSongIndex].Length))  # no decimals needed
                textLength.set("Length: {:0>8}".format(str(datetime.timedelta(seconds=songLength))))
                textGenre.set("Genre: " + str(play_list.validFiles[play_list.currentSongIndex].Genre))
                textArtist.set("Artist: " + str(play_list.validFiles[play_list.currentSongIndex].Artist))
                textAlbum.set("Album: " + str(play_list.validFiles[play_list.currentSongIndex].Album))
                textTitle.set("Title: " + str(play_list.validFiles[play_list.currentSongIndex].Title))
                textYear.set("Year: " + str(play_list.validFiles[play_list.currentSongIndex].Year))
                startPos = int(play_list.validFiles[play_list.currentSongIndex].startPos)
                textStartTime.set("Start Time: {:0>8}".format(str(datetime.timedelta(seconds=startPos))))
                endPos = int(play_list.validFiles[play_list.currentSongIndex].endPos)
                textEndTime.set("End Time: {:0>8}".format(str(datetime.timedelta(seconds=endPos))))
                textFadeIn.set("FadeIn: " + str(play_list.validFiles[play_list.currentSongIndex].fadein_duration)+"s")
                textFadeOut.set("FadeOut: " + str(play_list.validFiles[play_list.currentSongIndex].fadeout_duration) +"s")
                mode = "Stereo" if play_list.validFiles[play_list.currentSongIndex].channels == 2 else "Mono"
                textMonoStereoMode.set("Mode: " + mode)
                textNofPlays.set("No. of Plays: " + str(play_list.validFiles[play_list.currentSongIndex].NumberOfPlays))
                textSampleRate.set("Sample Rate: " + str(play_list.validFiles[play_list.currentSongIndex].sample_rate))
                textTotalPlayTime.set("Total PlayTime: {:0>8}" .format(str(datetime.timedelta(seconds=int(play_list.playTime)))))
                danMode = "ON" if play_list.danthologyMode == True else "OFF"
                textDanthologyMode.set("Danthology Mode: " + danMode)
                #Select current song, and make it visible
                listbox.selection_clear(0, tk.END)
                listbox.select_set(play_list.currentSongIndex)
                listbox.see(play_list.currentSongIndex)
                listBox_Song_selected_index = play_list.currentSongIndex
                updateRadioButtons()
            updateSortButton()
            progress["mode"] = play_list.ProgressBarType
            window.attributes('-alpha', play_list.windowOpacity) #set the opacity
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
    global listBox_Song_selected_index
    play_list.dirFilePath = filedialog.askdirectory()
    if play_list.dirFilePath:
        searchFilesInDirectories(play_list.dirFilePath)
        play_list.currentSongIndex = 0
        play_list.currentSongPosition = 0
        listbox.selection_clear(0, tk.END)
        listbox.select_set(play_list.currentSongIndex)
        listbox.see(play_list.currentSongIndex)
        listBox_Song_selected_index = play_list.currentSongIndex
        textFilesToPlay.set("Files: " + str(len(play_list.validFiles)))
        displayElementsOnPlaylist()

def searchFilesInDirectories(dir):
    global play_list
    for root, dirs, files in os.walk(dir):
        for file in files:
            if ".mp3" in file.lower():
                fileSize = os.path.getsize(root + "/" + file) / (1024 * 1024)
                fileSize = float("{0:.2f}".format(fileSize))
                song = Song(file, root + "/" + file, fileSize)
                play_list.validFiles.append(song)
                play_list.playTime += song.Length

def play_music():
    global play_list
    global visualSongNameLabel
    if len(play_list.validFiles) > 0 and play_list.currentSongIndex!=None:
        try:
            s_rate = play_list.validFiles[play_list.currentSongIndex].sample_rate
            channels = play_list.validFiles[play_list.currentSongIndex].channels
            if pygame.mixer.get_init():
                pygame.mixer.quit() # quit it, to make sure it is reinintialized
                pygame.mixer.pre_init(frequency=s_rate, size=-16, channels=channels, buffer=4096)
            else:
                pygame.mixer.pre_init(frequency=s_rate, size=-16, channels=channels, buffer=4096)
            pygame.mixer.init()
            if play_list.validFiles[play_list.currentSongIndex].fadein_duration == 0:
                pygame.mixer.music.set_volume(play_list.VolumeLevel)
            else: # enter here if song uses fadein
                pygame.mixer.music.set_volume(0.0)
            if listBox_Song_selected_index != None and type(dialog) != SearchTool:
                if listBox_Song_selected_index != play_list.currentSongIndex:
                    play_list.currentSongIndex = listBox_Song_selected_index
                    play_list.currentSongPosition = play_list.validFiles[play_list.currentSongIndex].startPos
                    play_list.RESUMED = False
                listbox.see(play_list.currentSongIndex)  # Makes sure the given list index is visible. You can use an integer index,
                listbox.selection_clear(0, tk.END)  # clear existing selection
                listbox.select_set(play_list.currentSongIndex)
            elif listBox_Song_selected_index == play_list.currentSongIndex and type(dialog) == SearchTool:
                if play_list.danthologyMode == False:
                    play_list.currentSongPosition=0
                #otheriwse keep the currentSongPosition from the previous one.
            pygame.mixer.music.load(play_list.validFiles[play_list.currentSongIndex].filePath)
            pygame.mixer.music.play()
            PausedButtonText.set("Pause")
            play_list.isSongPause = False
            if play_list.currentSongPosition > 0:
                pygame.mixer.music.set_pos(play_list.currentSongPosition)
                play_list.RESUMED = True
            elif play_list.validFiles[play_list.currentSongIndex].startPos > 0:
                start_pos = play_list.validFiles[play_list.currentSongIndex].startPos
                if play_list.currentSongPosition == 0:
                    if play_list.danthologyMode == False:
                        play_list.currentSongPosition = start_pos
                    # otheriwse keep the currentSongPosition from the previous one.
                pygame.mixer.music.set_pos(start_pos)
                play_list.RESUMED = True
            if play_list.danthologyDuration > 0 and play_list.danthologyMode:
                play_list.danthologyTimer = time.time()
        except Exception as e:
            print("Play Music Function: " + str(e))
        else:
            SongName.set("Playing: " + play_list.validFiles[play_list.currentSongIndex].fileName)
            SongSize.set("Size: " + str(play_list.validFiles[play_list.currentSongIndex].fileSize) + " MB")
            songLength = float("{0:.0f}".format(play_list.validFiles[play_list.currentSongIndex].Length))  # no decimals needed
            textLength.set("Length: {:0>8}".format(str(datetime.timedelta(seconds=songLength))))
            textGenre.set("Genre: " + str(play_list.validFiles[play_list.currentSongIndex].Genre))
            textArtist.set("Artist: " + str(play_list.validFiles[play_list.currentSongIndex].Artist))
            textAlbum.set("Album: " + str(play_list.validFiles[play_list.currentSongIndex].Album))
            textTitle.set("Title: " + str(play_list.validFiles[play_list.currentSongIndex].Title))
            textYear.set("Year: " + str(play_list.validFiles[play_list.currentSongIndex].Year))
            startPos = int(play_list.validFiles[play_list.currentSongIndex].startPos)
            textStartTime.set("Start Time: {:0>8}" .format(str(datetime.timedelta(seconds=startPos))))
            endPos = int(play_list.validFiles[play_list.currentSongIndex].endPos)
            textEndTime.set("End Time: {:0>8}" .format(str(datetime.timedelta(seconds=endPos))))
            textFadeIn.set("FadeIn: " + str(play_list.validFiles[play_list.currentSongIndex].fadein_duration)+"s")
            textFadeOut.set("FadeOut: " + str(play_list.validFiles[play_list.currentSongIndex].fadeout_duration) +"s")
            mode = "Stereo" if play_list.validFiles[play_list.currentSongIndex].channels == 2 else "Mono"
            textMonoStereoMode.set("Mode: " + mode)
            textSampleRate.set("Sample Rate: " + str(play_list.validFiles[play_list.currentSongIndex].sample_rate))
            progress["maximum"] = play_list.validFiles[play_list.currentSongIndex].Length
            songRating.set(str(play_list.validFiles[play_list.currentSongIndex].Rating))
            if play_list.playingFileNameTransition == "none":
                visualSongNameLabel = play_list.validFiles[play_list.currentSongIndex].fileName
            elif play_list.playingFileNameTransition == "typewriting":
                visualSongNameLabel = None
            elif play_list.playingFileNameTransition == "separation":
                visualSongNameLabel = "_" + play_list.validFiles[play_list.currentSongIndex].fileName
            updateRadioButtons()
            play_list.validFiles[play_list.currentSongIndex].NumberOfPlays+=1
            textNofPlays.set("No. of Plays: " + str(play_list.validFiles[play_list.currentSongIndex].NumberOfPlays))
            try:
                scheduler.enter(progressViewRealTime, 1, viewProgress)
                scheduler.run()
            except Exception as exp:
                print("Play Music Function - starting scheduler: " + str(exp))

def pause_music():
    global play_list
    if pygame.mixer.get_init():
        try:
            if play_list.isSongPause == False and pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                PausedButtonText.set("Resume")
                play_list.isSongPause = True
                if len(play_list.validFiles) > 0 :
                    SongName.set("Paused: " + play_list.validFiles[play_list.currentSongIndex].fileName)
                else:
                    SongName.set("Paused: ")
            elif play_list.isSongPause == True and pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()
                PausedButtonText.set("Pause")
                play_list.isSongPause = False
                if len(play_list.validFiles) > 0:
                    SongName.set("Playing: " + play_list.validFiles[play_list.currentSongIndex].fileName)
                else:
                    SongName.set("Playing: ")
                scheduler.enter(progressViewRealTime, 1, viewProgress)
                scheduler.run()
        except Exception as e:
            print("Pause Music Function: " + str(e))

def stop_music():
    global play_list
    if pygame.mixer.get_init():
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                SongName.set("Playing: ")
                if play_list.progressTime == "Ascending":
                    SongDuration.set("Time Elapsed: ")
                else:
                    SongDuration.set("Time Left: ")
                SongSize.set("Size: ")
                play_list.isSongStopped = True
                if play_list.danthologyMode == False:
                    play_list.currentSongPosition=0
                play_list.RESUMED = False
                PausedButtonText.set("Pause")
                play_list.isSongPause = False
        except Exception as e:
            print("Stop Music Function: " +str(e))

def handleDanthology():
    global play_list
    if play_list.currentSongPosition >= play_list.validFiles[play_list.currentSongIndex].Length:
        play_list.currentSongPosition =0
    else:
        if play_list.RESUMED:
            play_list.currentSongPosition = math.floor(play_list.currentSongPosition + pygame.mixer.music.get_pos() / 1000)
        else:
            play_list.RESUMED = True

def next_song():
    global listBox_Song_selected_index
    global play_list
    if len(play_list.validFiles) > 0 and play_list.currentSongIndex!=None:
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
        if play_list.danthologyMode == False:
            play_list.currentSongPosition=0
        else:
            handleDanthology()
        play_music()

def previous_song():
    global listBox_Song_selected_index
    global play_list
    if len(play_list.validFiles) > 0 and play_list.currentSongIndex!=None:
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
        if play_list.danthologyMode == False:
            play_list.currentSongPosition = 0
        else:
            handleDanthology()
        play_music()

def addFontTransitions():
    global visualSongNameLabel
    global Project_Title
    if play_list.usePlayerTitleTransition:
        Project_Title = fontTitleTransition(Project_Title)
        window.title(Project_Title)  # add animation to font when playing music
    if play_list.playingFileNameTransition == "typewriting":
        fontTypeWritingTransition()
    elif play_list.playingFileNameTransition == "separation":
        visualSongNameLabel = fontSeparatedTransition(visualSongNameLabel)
    SongName.set("Playing: " + visualSongNameLabel)

def viewProgress():
    global play_list
    global progress
    if play_list.usingSlideShow == True:
        Slideshow.countSeconds()
    if APPLICATION_EXIT == False:
        if pygame.mixer.music.get_busy() and play_list.isSongPause == False:
            addFontTransitions()
            if play_list.RESUMED:
                local_position = math.floor(play_list.currentSongPosition + pygame.mixer.music.get_pos() / 1000)
                if play_list.progressTime == "Ascending":
                    SongDuration.set("Time Elapsed: {:0>8}".format(str(datetime.timedelta(seconds=local_position))))
                else:
                    SongLength = int(play_list.validFiles[play_list.currentSongIndex].Length - local_position)
                    SongDuration.set("Time Left: {:0>8}".format(str(datetime.timedelta(seconds=SongLength))))
                progress["value"] = local_position
                if play_list.validFiles[play_list.currentSongIndex].fadein_duration > 0:
                    fadein(local_position - play_list.validFiles[play_list.currentSongIndex].startPos)
                if play_list.validFiles[play_list.currentSongIndex].fadeout_duration > 0:
                    fadeout(play_list.validFiles[play_list.currentSongIndex].endPos - local_position)
                if play_list.danthologyMode and play_list.danthologyDuration>0:
                    if time.time() - play_list.danthologyTimer >  play_list.danthologyDuration:
                        #Danthology
                        next_song()
                if local_position >= math.floor(play_list.validFiles[play_list.currentSongIndex].endPos):
                    stop_music()
                    play_list.isSongPause = False
                    play_list.isSongStopped = False #song is not stopped in this circumstances, song has finished

            else:
                play_list.currentSongPosition = math.floor(pygame.mixer.music.get_pos()/1000)
                if play_list.progressTime == "Ascending":
                    SongDuration.set("Time Elapsed: {:0>8}".format(str(datetime.timedelta(seconds=play_list.currentSongPosition))))
                else:
                    SongLength = int(play_list.validFiles[play_list.currentSongIndex].Length - play_list.currentSongPosition)
                    SongDuration.set("Time Left: {:0>8}".format(str(datetime.timedelta(seconds=SongLength))))
                progress["value"] = play_list.currentSongPosition
                if play_list.validFiles[play_list.currentSongIndex].fadein_duration > 0:
                    fadein(play_list.currentSongPosition - play_list.validFiles[play_list.currentSongIndex].startPos)
                if play_list.validFiles[play_list.currentSongIndex].fadeout_duration > 0:
                    fadeout(play_list.validFiles[play_list.currentSongIndex].endPos - play_list.currentSongPosition)
                if play_list.danthologyMode and play_list.danthologyDuration > 0:
                    if time.time() - play_list.danthologyTimer >  play_list.danthologyDuration:
                        #Danthology
                        next_song()
                if len(play_list.validFiles) > 0:
                    if play_list.currentSongPosition >= math.floor(play_list.validFiles[play_list.currentSongIndex].endPos):
                        stop_music()
                        play_list.isSongPause = False
                        play_list.isSongStopped = False #song is not stopped in this circumstances, song has finished
            try:
                window.update()  # Force an update of the GUI
            except Exception as exp:
                #Enter here when the program is destroyed
                print("Application destroyed in View Progress Function")

                #Make a backup of everything:
                file = open(automaticallyBackupFile, "wb")
                pickle.dump(play_list, file)
                file.close()
                sys.exit()
            else:
                scheduler.enter(progressViewRealTime, 1, viewProgress)
        elif pygame.mixer.music.get_busy() == False and play_list.isSongPause == False and play_list.isSongStopped == False:
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
        if play_list.currentSongPosition - play_list.validFiles[play_list.currentSongIndex].startPos > \
                play_list.validFiles[play_list.currentSongIndex].fadein_duration and play_list.currentSongPosition < \
                play_list.validFiles[play_list.currentSongIndex].endPos - play_list.validFiles[play_list.currentSongIndex].fadeout_duration:
            pygame.mixer.music.set_volume(play_list.VolumeLevel)
        textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel*100)) + "%")

def volume_up():
    global play_list
    if pygame.mixer.get_init():
        play_list.VolumeLevel+=0.1
        if(play_list.VolumeLevel>1.0):
            play_list.VolumeLevel=1.0
        if play_list.currentSongPosition - play_list.validFiles[play_list.currentSongIndex].startPos > \
            play_list.validFiles[play_list.currentSongIndex].fadein_duration and play_list.currentSongPosition < \
                play_list.validFiles[play_list.currentSongIndex].endPos - play_list.validFiles[play_list.currentSongIndex].fadeout_duration:
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
        rand = random.randint(0, len(play_list.validFiles)-1) #endpoints included
        play_list.currentSongIndex = rand

def save_playlist():
    global play_list
    window.filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                 filetypes=(("pypl files", "*.pypl"), ("all files", "*.*")))
    if window.filename:
        if ".pypl" in window.filename:
            file = open(window.filename, "wb")
        else:
            file = open(window.filename + ".pypl", "wb")
        play_list.currentSongPosition += (pygame.mixer.music.get_pos() / 1000)
        pickle.dump(play_list, file)
        file.close()

def clearLabels():
    textFilesToPlay.set("Files: " + str(len(play_list.validFiles)))
    textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    textGenre.set("Genre: ")
    textArtist.set("Artist: ")
    textAlbum.set("Album: ")
    textTitle.set("Title: ")
    textYear.set("Year: ")
    textFadeIn.set("FadeIn: ")
    textMonoStereoMode.set("Mode: ")
    textNofPlays.set("No. of Plays: ")
    danMode = "OFF" if play_list.danthologyMode==False else "ON"
    textDanthologyMode.set("Danthology Mode: " + danMode)
    textSampleRate.set("Sample Rate: ")
    textEndTime.set("End Time: ")
    textStartTime.set("Start Time")
    textLength.set("Length: ")
    if play_list.progressTime == "Ascending":
        SongDuration.set("Time Elapsed: ")
    else:
        SongDuration.set("Time Left: ")

def new_playlist():
    global play_list
    if dialog != None:
        dialog.destroy()
    if pygame.mixer.get_init():
        if pygame.mixer.music.get_busy():
            NewPlaylistDialog(window)
        else:
            play_list = Playlist()
            clearLabels()
            displayElementsOnPlaylist()
            # Restore default skin
            SkinColor.set(skinOptions[1][play_list.skin])
            changeSkin("<Double-Button>")
    else:
        play_list = Playlist()
        clearLabels()
        displayElementsOnPlaylist()
        # Restore default skin
        SkinColor.set(skinOptions[1][play_list.skin])
        changeSkin("<Double-Button>")

def elementPlaylistDoubleClicked(event):
    global play_list
    if listbox.size():
        if type(dialog) != SearchTool:
            widget = event.widget
            index = int(widget.curselection()[0])
            #value = widget.get(index)
            play_list.currentSongIndex = index
            play_list.currentSongPosition = 0
            play_music()
        else:
            widget = event.widget
            index = int(widget.curselection()[0])
            value = widget.get(index)
            value=value.split(". ")
            play_list.currentSongIndex = int(value[0])
            play_music()

def updateSortButton():
    # 0-onrating, 1-sorted, 2-reversed, 3-random
    if play_list.isListOrdered == 0:
        SortButtonText.set("By Rating")
    elif play_list.isListOrdered == 1:
        SortButtonText.set("By Name")
    elif play_list.isListOrdered == 2:
        SortButtonText.set("Name Reversed")
    elif play_list.isListOrdered == 3:
        SortButtonText.set("Random")
    elif play_list.isListOrdered == 4:
        SortButtonText.set("Rating Reversed")
    elif play_list.isListOrdered == 5:
        SortButtonText.set("By Length")
    elif play_list.isListOrdered == 6:
        SortButtonText.set("Length Reversed")
    elif play_list.isListOrdered == 7:
        SortButtonText.set("By Genre")
    elif play_list.isListOrdered == 8:
        SortButtonText.set("Genre Reversed")
    elif play_list.isListOrdered == 9:
        SortButtonText.set("By Plays")
    elif play_list.isListOrdered == 10:
        SortButtonText.set("Plays Reversed")
    elif play_list.isListOrdered == 11:
        SortButtonText.set("By Year")
    elif play_list.isListOrdered == 12:
        SortButtonText.set("Year Reversed")
    elif play_list.isListOrdered == 13:
        SortButtonText.set("By Album")
    elif play_list.isListOrdered == 14:
        SortButtonText.set("Album Reversed")
    elif play_list.isListOrdered == 15:
        SortButtonText.set("By Title")
    elif play_list.isListOrdered == 16:
        SortButtonText.set("Title Reversed")

def displayElementsOnPlaylist():
    global listbox
    listbox.delete(0, tk.END)
    for element in play_list.validFiles:
        listbox.insert(play_list.validFiles.index(element), str(play_list.validFiles.index(element))+". "+element.fileName)
    textTotalPlayTime.set("Total PlayTime: {:0>8}" .format(str(datetime.timedelta(seconds=int(play_list.playTime)))))

def changingBackgroundElementColor(event):
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
    SleepButton["bg"]=SkinColor.get()
    #changing listbox
    listbox["bg"]=SkinColor.get()
    #changing radiobutton:
    updateRadioButtons()
    #changing style of progress bar:
    styl.configure("Horizontal.TProgressbar", background = SkinColor.get())	
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
    labelTotalPlayTime["fg"]=SkinColor.get()
    labelFallAsleep["fg"]=SkinColor.get()
    labelWakeUp["fg"]=SkinColor.get()
    labelFadeIn["fg"]=SkinColor.get()
    labelFadeOut["fg"]=SkinColor.get()
    labelMonoStereoMode["fg"]=SkinColor.get()
    labelSampleRate["fg"]=SkinColor.get()
    labelNofPlays["fg"]=SkinColor.get()
    labelDanthologyMode["fg"]=SkinColor.get()
    labelArtist["fg"]=SkinColor.get()
    labelAlbum["fg"]=SkinColor.get()
    labelTitle["fg"]=SkinColor.get()
    labelYear["fg"]=SkinColor.get()
    if type(dialog) == Customize: #if entered here means setting a custom color
        play_list.customElementBackground = custom_color_list.index(SkinColor.get())
        dialog.destroy()
        Customize(window)

def customFontChange(event):
    global dialog
    global allButtonsFont
    global play_list
    allButtonsFont = allButtonsFont.get()
    play_list.customFont = custom_font_list.index(allButtonsFont)
    changeFonts()
    dialog.destroy()
    Customize(window)

def changeSkin(event):
    global backgroundFile
    global skinOptions
    global background_label
    global dialog
    global play_list
    global allButtonsFont
    global labelBackground
    if SkinColor.get() == "custom":
        showCustomizeWindow()
    else:
        changingBackgroundElementColor(event)
        #changing background
        play_list.customElementBackground = None
        play_list.customLabelBackground = None
        play_list.customChangeBackgroundedLabelsColor = None
        play_list.customFontColor=None
        play_list.customBackgroundPicture = None
        play_list.customFont = None
        if SkinColor.get() in skinOptions[1]: # if using predefined skins, with predifined backgrounds.
            index = skinOptions[1].index(SkinColor.get())
            backgroundFile = skinOptions[0][index]
            if os.path.exists(backgroundFile):
                if os.path.isfile(backgroundFile):
                    play_list.customBackgroundPicture = backgroundFile
                    background_image = tk.PhotoImage(file=backgroundFile)
                    background_label.configure(image=background_image)
                    background_label.image = background_image
                    play_list.skin = index
        allButtonsFont = skinOptions[2][play_list.skin]
        changeFonts() #change the font that comes with the new skin
        labelBackground.set("lightgray") #default value
        fontColor.set("white") #default value
        changingFontColor(event)
        changingLabelBackgroundColor(event)
        if(dialog != None):
            if type(dialog) == CuttingTool:
                dialog.destroy()
                CuttingTool(window)
            elif type(dialog) == SearchTool:
                dialog.destroy()
                SearchTool(window)
            elif type(dialog) == SleepingTool:
                dialog.destroy()
                SleepingTool(window)
            elif type(dialog) == Customize:
                    dialog.destroy()
                    Customize(window)
            elif type(dialog) == NewPlaylistDialog:
                    dialog.destroy()
                    NewPlaylistDialog(window)
            elif type(dialog) == Mp3TagModifierTool:
                    dialog.destroy()
                    Mp3TagModifierTool()
            elif type(dialog) == GrabLyricsTool:
                    index = dialog.songIndex # store the index of the song for which the lyrics are shown
                    dialog.destroy()
                    GrabLyricsTool(index)
            elif type(dialog) == GrabArtistBio:
                    index = dialog.songIndex # store the index of the song for which the lyrics are shown
                    dialog.destroy()
                    GrabArtistBio(index)
        elif Slideshow.top != None:
            #destroy it
            Slideshow.top.destroy()
            #rebuild it
            Slideshow()

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
        window.geometry("1240x650+100+100")
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
    global play_list
    if len(play_list.validFiles) > 0 and play_list.currentSongIndex!= None:
        e = event.widget
        x = play_list.validFiles[play_list.currentSongIndex].Length / 470
        play_list.currentSongPosition = ((event.x - progressBarMargin) * x)
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(play_list.currentSongPosition)
        progress["value"] = play_list.currentSongPosition
        play_list.RESUMED = True

def on_closing(): #this function is called only when window is canceled
    global APPLICATION_EXIT
    global play_list
    APPLICATION_EXIT = True
    # Make a backup of everything:
    if(len(play_list.validFiles) == 0):
        #if empty set these field so that when next song will be added they won't take effect
        play_list.isSongPause = False
        play_list.isSongStopped = False
        play_list.isListOrdered = 0  # 0-onrating ; 1-sorted 2-reversed; 3-random;
        play_list.currentSongIndex = None
        if play_list.danthologyMode == False:
            play_list.currentSongPosition = 0
        play_list.RESUMED = False
    file = open(automaticallyBackupFile, "wb")
    pickle.dump(play_list, file)
    file.close()
    window.quit()
    sys.exit()

def remove_song():
    global listBox_Song_selected_index
    if listBox_Song_selected_index!=None:
        if listBox_Song_selected_index < len(play_list.validFiles):
            del play_list.validFiles[listBox_Song_selected_index]
            displayElementsOnPlaylist()
            textFilesToPlay.set("Files: " + str(len(play_list.validFiles)))
            #listBox_Song_selected_index=None #initialize this if u want to remove only onebyone
            # Maintain the selection
            listbox.select_set(listBox_Song_selected_index)

def list_selected_item(event):
    if listbox.size() > 0:
        global listBox_Song_selected_index
        if type(dialog) != SearchTool:
            listboxSelectedEvent = event.widget
            index = int(listboxSelectedEvent.curselection()[0])
            value = listbox.get(index)
            value = value.split(". ")
            listBox_Song_selected_index = int(value[0])
        else:
            listboxSelectedEvent = event.widget
            index = int(listboxSelectedEvent.curselection()[0])
            value = listbox.get(index)
            value = value.split(". ")
            listBox_Song_selected_index = int(value[0])
            play_list.currentSongIndex = int(value[0])
            listBox_Song_selected_index = play_list.currentSongIndex
        #do this if u want to play the selected song in the listbox when hitting PLAY button
        #play_list.currentSongIndex = index # if uncomment this when a song is selected and the playlist and hit PLAY
        #the song will maintain the same currentSongPosition value as the previous one.

def sortByFileName():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 1
    play_list.validFiles.sort(key=lambda Song: Song.fileName)  # sort the list according to fileName
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByFileNameReversed():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 2
    play_list.validFiles.sort(key=lambda Song: Song.fileName)  # sort the list according to fileName
    play_list.validFiles.reverse()
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortRandomized():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 3
    randomize() #let them be randomized
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByRating():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 0
    play_list.validFiles.sort(key=lambda Song: Song.Rating, reverse=True)  # sort the list according to Rating
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByRatingReversed():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 4
    play_list.validFiles.sort(key=lambda Song: Song.Rating, reverse=True)  # sort the list according to Rating
    play_list.validFiles.reverse()
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByLength():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 5
    play_list.validFiles.sort(key=lambda Song: Song.Length)  # sort the list according to fileName
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByLengthReversed():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 6
    play_list.validFiles.sort(key=lambda Song: Song.Length)  # sort the list according to fileName
    play_list.validFiles.reverse()
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByGenre():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 7
    play_list.validFiles.sort(key=lambda Song: Song.Genre)  # sort the list according to fileName
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByGenreReversed():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 8
    play_list.validFiles.sort(key=lambda Song: Song.Genre)  # sort the list according to fileName
    play_list.validFiles.reverse()
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByNoOfPlays():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 9
    play_list.validFiles.sort(key=lambda Song: Song.NumberOfPlays)  # sort the list according to fileName
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByNoOfPlaysReversed():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 10
    play_list.validFiles.sort(key=lambda Song: Song.NumberOfPlays)  # sort the list according to fileName
    play_list.validFiles.reverse()
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByYear():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 11
    play_list.validFiles.sort(key=lambda Song: Song.Year)  # sort the list according to fileName
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByYearReversed():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 12
    play_list.validFiles.sort(key=lambda Song: Song.Year)  # sort the list according to fileName
    play_list.validFiles.reverse()
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByAlbum():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 13
    play_list.validFiles.sort(key=lambda Song: Song.Album)  # sort the list according to fileName
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByAlbumReversed():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 14
    play_list.validFiles.sort(key=lambda Song: Song.Album)  # sort the list according to fileName
    play_list.validFiles.reverse()
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByTitle():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 15
    play_list.validFiles.sort(key=lambda Song: Song.Title)  # sort the list according to fileName
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sortByTitleReversed():
    global play_list
    Song = play_list.validFiles[play_list.currentSongIndex]
    play_list.isListOrdered = 16
    play_list.validFiles.sort(key=lambda Song: Song.Title)  # sort the list according to fileName
    play_list.validFiles.reverse()
    play_list.currentSongIndex = play_list.validFiles.index(Song)
    displayElementsOnPlaylist()
    updateSortButton()

def sort_list():
    # 0-onrating, 1-sorted, 2-reversed, 3-random
    global play_list
    aMenu = tk.Menu(window, tearoff=0)
    aMenu.add_command(label='Sort By Name', command=sortByFileName)
    aMenu.add_command(label='Sort By Name Reversed', command=sortByFileNameReversed)
    aMenu.add_command(label='Sort Randomize', command=sortRandomized)
    aMenu.add_command(label='Sort By Rating', command=sortByRating)
    aMenu.add_command(label='Sort By Rating Reversed', command=sortByRatingReversed)
    aMenu.add_command(label='Sort By Length', command=sortByLength)
    aMenu.add_command(label='Sort By Length Reversed', command=sortByLengthReversed)
    aMenu.add_command(label='Sort By Genre', command=sortByGenre)
    aMenu.add_command(label='Sort By Genre Reversed', command=sortByGenreReversed)
    aMenu.add_command(label='Sort By No. Of Plays', command=sortByNoOfPlays)
    aMenu.add_command(label='Sort By No. Of Plays Reversed', command=sortByNoOfPlaysReversed)
    aMenu.add_command(label='Sort By Year', command=sortByYear)
    aMenu.add_command(label='Sort By Year Reversed', command=sortByYearReversed)
    aMenu.add_command(label='Sort By Album', command=sortByAlbum)
    aMenu.add_command(label='Sort By Album Reversed', command=sortByAlbumReversed)
    aMenu.add_command(label='Sort By Title', command=sortByTitle)
    aMenu.add_command(label='Sort By Title Reversed', command=sortByTitleReversed)
    x = 770
    y = 650
    aMenu.post(x, y)

def UpdateSongRating():
    global play_list
    if len(play_list.validFiles) > 0 and play_list.currentSongIndex:
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
    color = OpenFileButton["bg"]  # get the same color as every element
    if (int(songRating.get()) == 1):
        R1["bg"] = color
        R1["fg"] = fontColor.get()
        R2["bg"] = radioButtonsDefaultColor
        R2["fg"] = color
        R3["bg"] = radioButtonsDefaultColor
        R3["fg"] = color
        R4["bg"] = radioButtonsDefaultColor
        R4["fg"] = color
        R5["bg"] = radioButtonsDefaultColor
        R5["fg"] = color
    elif (int(songRating.get()) == 2):
        R1["bg"] = color
        R1["fg"] = fontColor.get()
        R2["bg"] = color
        R2["fg"] = fontColor.get()
        R3["bg"] = radioButtonsDefaultColor
        R3["fg"] = color
        R4["bg"] = radioButtonsDefaultColor
        R4["fg"] = color
        R5["bg"] = radioButtonsDefaultColor
        R5["fg"] = color
    elif (int(songRating.get()) == 3):
        R1["bg"] = color
        R1["fg"] = fontColor.get()
        R2["bg"] = color
        R2["fg"] = fontColor.get()
        R3["bg"] = color
        R3["fg"] = fontColor.get()
        R4["bg"] = radioButtonsDefaultColor
        R4["fg"] = color
        R5["bg"] = radioButtonsDefaultColor
        R5["fg"] = color
    elif (int(songRating.get()) == 4):
        R1["bg"] = color
        R1["fg"] = fontColor.get()
        R2["bg"] = color
        R2["fg"] = fontColor.get()
        R3["bg"] = color
        R3["fg"] = fontColor.get()
        R4["bg"] = color
        R4["fg"] = fontColor.get()
        R5["bg"] = radioButtonsDefaultColor
        R5["fg"] = color
    elif (int(songRating.get()) == 5):
        R1["bg"] = color
        R1["fg"] = fontColor.get()
        R2["bg"] = color
        R2["fg"] = fontColor.get()
        R3["bg"] = color
        R3["fg"] = fontColor.get()
        R4["bg"] = color
        R4["fg"] = fontColor.get()
        R5["bg"] = color
        R5["fg"] = fontColor.get()
    else: #put the default color
        R1["bg"] = radioButtonsDefaultColor
        R1["fg"] = color
        R2["bg"] = radioButtonsDefaultColor
        R2["fg"] = color
        R3["bg"] = radioButtonsDefaultColor
        R3["fg"] = color
        R4["bg"] = radioButtonsDefaultColor
        R4["fg"] = color
        R5["bg"] = radioButtonsDefaultColor
        R5["fg"] = color
    if len(play_list.validFiles) > 0 and play_list.currentSongIndex!=None:
        songRating.set(str(play_list.validFiles[play_list.currentSongIndex].Rating))

def changingFontColor(event):
    global play_list
    OpenFileButton["fg"] = fontColor.get()
    OpenDirectoryButton["fg"] = fontColor.get()
    PlayButton["fg"] = fontColor.get()
    PauseButton["fg"] = fontColor.get()
    StopButton["fg"] = fontColor.get()
    NextButton["fg"] = fontColor.get()
    PreviousButton["fg"] = fontColor.get()
    VolumeDownButton["fg"] = fontColor.get()
    VolumeUpButton["fg"] = fontColor.get()
    ShuffleButton["fg"] = fontColor.get()
    SavePlaylistButton["fg"] = fontColor.get()
    NewPlaylistButton["fg"] = fontColor.get()
    ViewPlaylistButton["fg"] = fontColor.get()
    RepeatButton["fg"] = fontColor.get()
    RendomizeListButton["fg"] = fontColor.get()
    RemoveSongButton["fg"] = fontColor.get()
    SortListButton["fg"] = fontColor.get()
    MoveUpButton["fg"] = fontColor.get()
    MoveDownButton["fg"] = fontColor.get()
    CutSelectedButton["fg"] = fontColor.get()
    SearchButton["fg"] = fontColor.get()
    SleepButton["fg"] = fontColor.get()
    # changing listbox
    listbox["fg"] = fontColor.get()
    if fontColor.get() != "white": #white is the default value which cannot be customized
        play_list.customFontColor = custom_color_list.index(fontColor.get())
    #destroy and rebuild the window so the the colors will also change on the customizer
    if type(dialog) == Customize: # this condition is true only when Customize window is opened
        dialog.destroy()
        Customize(window)

def changingLabelBackgroundColor(event):
    global play_list;
    # changing labels
    labelPlaying["background"] = labelBackground.get()
    labelDuration["background"] = labelBackground.get()
    labelSize["background"] = labelBackground.get()
    labelVolumeLevel["background"] = labelBackground.get()
    labelFilesToPlay["background"] = labelBackground.get()
    labelLength["background"] = labelBackground.get()
    labelGenre["background"] = labelBackground.get()
    labelStartTime["background"] = labelBackground.get()
    labelEndTime["background"] = labelBackground.get()
    labelTotalPlayTime["background"] = labelBackground.get()
    labelFallAsleep["background"] = labelBackground.get()
    labelWakeUp["background"] = labelBackground.get()
    labelFadeIn["background"] = labelBackground.get()
    labelFadeOut["background"] = labelBackground.get()
    labelMonoStereoMode["background"] = labelBackground.get()
    labelSampleRate["background"] = labelBackground.get()
    labelNofPlays["background"] = labelBackground.get()
    labelDanthologyMode["background"] = labelBackground.get()
    labelArtist["background"] = labelBackground.get()
    labelAlbum["background"] = labelBackground.get()
    labelTitle["background"] = labelBackground.get()
    labelYear["background"] = labelBackground.get()
    if labelBackground.get() != "lightgray": #lightgray is the default color, if condition is true, means user cutomized it
        play_list.customLabelBackground = custom_color_list.index(labelBackground.get())

def changingBackgroundedLabelsColor(value, loading=1):
    global play_list
    if loading!=1:
        play_list.customChangeBackgroundedLabelsColor = int(value.get())
    if play_list.customChangeBackgroundedLabelsColor == True:
        labelPlaying["fg"] = fontColor.get()
        labelDuration["fg"] = fontColor.get()
        labelSize["fg"] = fontColor.get()
        labelVolumeLevel["fg"] = fontColor.get()
        labelFilesToPlay["fg"] = fontColor.get()
        labelLength["fg"] = fontColor.get()
        labelGenre["fg"] = fontColor.get()
        labelStartTime["fg"] = fontColor.get()
        labelEndTime["fg"] = fontColor.get()
        labelTotalPlayTime["fg"] = fontColor.get()
        labelFallAsleep["fg"] = fontColor.get()
        labelWakeUp["fg"] = fontColor.get()
        labelFadeOut["fg"] = fontColor.get()
        labelFadeIn["fg"] = fontColor.get()
        labelMonoStereoMode["fg"] = fontColor.get()
        labelSampleRate["fg"] = fontColor.get()
        labelNofPlays["fg"] = fontColor.get()
        labelDanthologyMode["fg"] = fontColor.get()
        labelArtist["fg"] = fontColor.get()
        labelAlbum["fg"] = fontColor.get()
        labelTitle["fg"] = fontColor.get()
        labelYear["fg"] = fontColor.get()
    else:
        color = OpenFileButton["bg"] #put the same color as button background
        labelPlaying["fg"] = color
        labelDuration["fg"] = color
        labelSize["fg"] = color
        labelVolumeLevel["fg"] = color
        labelFilesToPlay["fg"] = color
        labelLength["fg"] = color
        labelGenre["fg"] = color
        labelStartTime["fg"] = color
        labelEndTime["fg"] = color
        labelTotalPlayTime["fg"] = color
        labelFallAsleep["fg"] = color
        labelWakeUp["fg"] = color
        labelFadeOut["fg"] = color
        labelFadeIn["fg"] = color
        labelMonoStereoMode["fg"] = color
        labelSampleRate["fg"] = color
        labelNofPlays["fg"] = color
        labelDanthologyMode["fg"] = color
        labelArtist["fg"] = color
        labelAlbum["fg"] = color
        labelTitle["fg"] = color
        labelYear["fg"] = color

def move_up():
    global listBox_Song_selected_index
    if listBox_Song_selected_index != None:
        Song = play_list.validFiles[listBox_Song_selected_index] #this is the auxiliar variable
        if(listBox_Song_selected_index-1 >= 0):
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
        # listBox_Song_selected_index=None #initialize this if u want to move only onebyone
        #Maintain the selection
        listbox.select_set(listBox_Song_selected_index)
        listbox.see(listBox_Song_selected_index)
        SortButtonText.set("Custom")

def move_down():
    global listBox_Song_selected_index
    if listBox_Song_selected_index != None:
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
        # listBox_Song_selected_index=None #initialize this if u want to move only onebyone
        # Maintain the selection
        listbox.select_set(listBox_Song_selected_index)
        listbox.see(listBox_Song_selected_index)
        SortButtonText.set("Custom")

def changeFonts():
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
    SleepButton["font"] = allButtonsFont
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
    labelTotalPlayTime["font"] = allButtonsFont
    labelFallAsleep["font"] = allButtonsFont
    labelWakeUp["font"] = allButtonsFont
    labelFadeOut["font"] = allButtonsFont
    labelFadeIn["font"] = allButtonsFont
    labelMonoStereoMode["font"] = allButtonsFont
    labelSampleRate["font"] = allButtonsFont
    labelNofPlays["font"] = allButtonsFont
    labelDanthologyMode["font"] = allButtonsFont
    labelArtist["font"] = allButtonsFont
    labelAlbum["font"] = allButtonsFont
    labelTitle["font"] = allButtonsFont
    labelYear["font"] = allButtonsFont
    # changing listbox
    listbox["font"] = allButtonsFont
    #changing radiobuttons:
    R1["font"] = allButtonsFont
    R2["font"] = allButtonsFont
    R3["font"] = allButtonsFont
    R4["font"] = allButtonsFont
    R5["font"] = allButtonsFont

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
    horizontalButtonsColumnStartCoord+=horizontalSpaceBetweenButtonColumns
    SleepButton.place(x=horizontalButtonsColumnStartCoord, y=490)

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
    labelTotalPlayTime.pack()
    labelFadeIn.pack()
    labelFadeOut.pack()
    labelMonoStereoMode.pack()
    labelSampleRate.pack()
    labelNofPlays.pack()
    labelDanthologyMode.pack()
    labelArtist.pack()
    labelAlbum.pack()
    labelTitle.pack()
    labelYear.pack()

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
    labelNofPlays.place(x=300, y=290)
    labelSampleRate.place(x=300, y=310)
    labelFadeIn.place(x=300, y=330)
    labelFadeOut.place(x=300, y=350)
    labelMonoStereoMode.place(x=300, y=370)

    labelTotalPlayTime.place(x=10, y=550)
    labelDanthologyMode.place(x=10, y=570)
    labelFallAsleep.place(x=10, y=590)
    labelWakeUp.place(x=10, y=610)
    
    labelArtist.place(x=300, y=550)
    labelAlbum.place(x=300, y=570)
    labelTitle.place(x=300, y=590)
    labelYear.place(x=300, y=610)

def pressedEnter(event):
    play_music()

def pressedTab(event):
    if dialog != None:
        #it means there is another window opened:
        dialog.take_focus()
    elif Slideshow.top!=None:
        Slideshow.take_focus()

def pressedShiftRight(event):
    move_up()

def pressedCtrlRight(event):
    move_down()

def pressedDelete(event):
    remove_song()

def pressedKeyShortcut(event):
    if event.char == " ":
        pause_music()
    elif event.char == "m" or event.char == "M":
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
    elif event.char == "r" or event.char == "R":
        repeat()
    elif event.char == "c" or event.char == "C":
        view_playlist()
    elif event.char == "x" or event.char == "X":
        next_song()
    elif event.char =="z" or event.char =="Z":
        previous_song()
    elif event.char =="s" or event.char =="S":
        shuffle()
    elif event.char =="d" or event.char =="D":
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
    elif event.char == "a" or event.char == "A":
        if Slideshow.top==None:
            Slideshow()
    elif event.char == "p" or event.char == "P":
        Customize(window)
    elif event.char == "i" or event.char == "I":
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
                + "T - is equivalent to Sleep\Wake Button\n"
                + "L - is equivalent to GrabLyrics\n"
                + "J - is equivalent to Search Button\n"
                + "P - is equivalent to Customize Option\n"
                + "W - will rename the Selected Song in the Playlist as: 'Artist - Title.mp3'"
                + "A - is equivalent to Slideshow\n"
                + "[0-9] - are equivalent to Volume Set 0% - 100%.\n"
                + "SPACE - is equivalent to Pause, or action the active button selected using Tab.\n"
                + "Tab - is sliding between the openened windows, or the active window elements.\n"
                + "L_Shift - is equivalent to Move Up on the current song selection in the playlist.\n"
                + "L_Ctrl - is equivalent to Move Down on the current song selection in the playlist.\n"
                + "Delete - is equivalent to Remove on the current song selection in the playlist.\n"
                + "Enter - is equivalent to Play current selection.\n"
                + ", or < key - is equivalent to Volume Up.\n"
                + ". or > key - is equivalent to Volume Down.\n"
                + "Page Up or Up - can be used to navigate the playlist UP.\n"
                + "Page Down or Down - can be used to navigate the playlist DOWN.\n"
                + "i - will show you this message again.")
    elif event.char == "q" or event.char == "Q":
        showCuttingTool()
    elif event.char =="j" or event.char =="J":
        searchSongInPlaylist()
    elif event.char == "t" or event.char == "T":
        showSleepingTool()
    elif event.char == "h" or event.char == "H":
        Mp3TagModifierTool()
    elif event.char == "l" or event.char == "L":
        showGrabLyricsWindow()
    elif event.char == "g" or event.char == "G":
        showArtistBioWindow()

def listboxShortcuts(event):
    if event.char == "w":
        if dialog == None:
            if listBox_Song_selected_index!=None and type(dialog) != SearchTool:
                Mp3TagModifierTool(listBox_Song_selected_index)
                dialog.ComposeNameCheckButtonVar.set(1)
                dialog.checkUncheckNameComposal(event)
                dialog.SaveChanges()
                dialog.destroy()
        else:
            messagebox.showinfo("Information", "Please close the other component window to do this.")

def songInfo():
    element = play_list.validFiles[listBox_Song_selected_index]
    messagebox.showinfo("Song Info", "Filename: " + str(element.fileName) + "\n"
                                    + "Path: " + str(element.filePath) + "\n"
                                    + "Length: {:0>8}" .format(str(datetime.timedelta(seconds = int(element.Length))) ) + "\n"
                                    + "Start Time: {:0>8}" .format(str(datetime.timedelta(seconds = int(element.startPos))) ) + "\n"
                                    + "End Time: {:0>8}" .format(str(datetime.timedelta(seconds = int(element.endPos))) ) + "\n"
                                    + "Size: " + str(element.fileSize) + "\n"
                                    + "Rating: " + str(element.Rating) + "\n")

def openFileInExplorer():
    file = play_list.validFiles[listBox_Song_selected_index].filePath
    FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    subprocess.Popen([FILEBROWSER_PATH, '/select,', os.path.normpath(file)])

def rightClickListboxElement(event):
    if listBox_Song_selected_index != None:
        listboxSelectedEvent = event.widget
        if len(listboxSelectedEvent.curselection()) > 0:
            if type(dialog) != SearchTool:
                index = int(listboxSelectedEvent.curselection()[0])
            else:
                index = int(listboxSelectedEvent.curselection()[0])
                value = listbox.get(index)
                value = value.split(". ")
                index = int(value[0])
        aMenu = tk.Menu(window, tearoff=0)
        aMenu.add_command(label='Delete', command=remove_song)
        aMenu.add_command(label='File Info', command=songInfo)
        aMenu.add_command(label='Move Up', command=move_up)
        aMenu.add_command(label='Move Down', command=move_down)
        aMenu.add_command(label='Open in Explorer', command=openFileInExplorer)
        if len(listboxSelectedEvent.curselection()) > 0:
            aMenu.add_command(label='MP3 Tag Modifier', command= lambda:showMp3TagModifierWindow(index))
            aMenu.add_command(label='Grab Song Lyrics', command= lambda:showGrabLyricsWindow(index))
            aMenu.add_command(label='Grab Artist Bio', command= lambda:showArtistBioWindow(index))
        aMenu.post(event.x_root, event.y_root)

def showMp3TagModifierWindow(index):
    if dialog == None:
        Mp3TagModifierTool(index)
    else:
        messagebox.showinfo("Information", "Please close the other component window before proceed.")
        
def showAboutWindow():
    messagebox.showinfo("About",
            "Hello!\n"+
            "\nWelcome To PyPlay Mp3 Player,\n\n"+
            "This Application was developed by Dragos Vacariu from 14 June 2019 to 10 July 2019, "+
            "with the main purpose of testing programming capabilities, especially python skills.\n"+
            "Work efforts were around 100 hours, so "+
            "there might still be bugs left behind for me to find out later.\n"+
            "\nMy Contact Details are the following:\n" +
            "Email: dragos.vacariu@mail.com\n" +
            "LinkedIn: www.linkedin.com/in/dragos-vacariu-em\n"+
            "\nOther projects I test my skills on, are available at:\n"+
            "GitHub Repository: github.com/dragos-vacariu/ \n"
            "\nThank you for trying PyPlay!\n")

def showCustomizeWindow():
    if dialog == None:
        Customize(window)
    else:
        messagebox.showinfo("Information", "Please close the other component window before proceed.")

def showGrabLyricsWindow(index="empty"):
    if dialog == None:
        GrabLyricsTool(index)
    else:
        messagebox.showinfo("Information", "Please close the other component window before proceed.")

def showArtistBioWindow(index="empty"):
    if dialog == None:
        GrabArtistBio(index)
    else:
        messagebox.showinfo("Information", "Please close the other component window before proceed.")

def showSlideshowWindow():
    if Slideshow.top == None:
        Slideshow()
    else:
        messagebox.showinfo("Information", "Slideshow is already opened.")

def rightClickOnWindow(event):
    if window.winfo_containing(event.x_root, event.y_root) != listbox: # don't execute this if the cursor is inside the listbox
        aMenu = tk.Menu(window, tearoff=0)
        aMenu.add_command(label='About', command=showAboutWindow)
        aMenu.add_command(label='Customize', command=showCustomizeWindow)
        aMenu.add_command(label='Slideshow', command=showSlideshowWindow)
        aMenu.add_command(label='SleepingTool', command=showSleepingTool)
        aMenu.add_command(label='CuttingTool', command=showCuttingTool)
        aMenu.add_command(label='SearchTool', command=searchSongInPlaylist)
        aMenu.add_command(label='GrabLyrics', command=showGrabLyricsWindow)
        aMenu.add_command(label='ArtistBio', command=showArtistBioWindow)
        aMenu.post(event.x_root, event.y_root)

def packPositionListScrolOptionProgRadio():
    #Here are set position, events, controls, styling for listbox, progressbar, scrollbar, option, radiobuttons
    listbox.pack(side = tk.LEFT, fill=tk.X) #this will place listbox on the leftside of the FRAME
    listbox.bind('<Double-Button>', elementPlaylistDoubleClicked)
    listbox.bind('<ButtonPress-3>', rightClickListboxElement)
    listbox.bind('<<ListboxSelect>>', list_selected_item)
    listbox.bind("<Return>", pressedEnter)
    listbox.bind("<Key>", listboxShortcuts)
    window.bind("<Return>", pressedEnter)
    window.bind("<Tab>", pressedTab)
    window.bind("<Key>", pressedKeyShortcut)
    window.bind("<Shift_L>", pressedShiftRight)
    window.bind("<Control_L>", pressedCtrlRight)
    window.bind("<Delete>", pressedDelete)
    window.bind('<ButtonPress-3>', rightClickOnWindow)
    frame.place(x=600, y=10)
    scroll.config(command=listbox.yview)
    scroll.pack(side = tk.RIGHT, fill=tk.Y) #this will place scrollbar on the right side of FRAME, if width is adjusted, they will be next to each other
    option.bind("<<ComboboxSelected>>", changeSkin)
    option.pack()
    option.place(x=350, y=180)
    styl.theme_use('clam')
    styl.configure("Horizontal.TProgressbar", foreground='red', background='blue')
    progress.bind("<Button>", navigationSound)
    progress.pack()
    progress.place(x=progressBarMargin, y=405)
    R1.pack()
    R2.pack()
    R3.pack()
    R4.pack()
    R5.pack()
    radioButtonLineHeight = 445
    R1.place(x=10, y=radioButtonLineHeight)
    R2.place(x=55, y=radioButtonLineHeight)
    R3.place(x=100, y=radioButtonLineHeight)
    R4.place(x=145, y=radioButtonLineHeight)
    R5.place(x=190, y=radioButtonLineHeight)

def showCuttingTool():
    if listbox.size() and listBox_Song_selected_index!= None:
        if dialog == None:
            CuttingTool(window)
        else:
            messagebox.showinfo("Information", "Please close the other component window before proceed.")
    else:
        messagebox.showinfo("No file selected", "Use the playlist to select a song.")

def showSleepingTool():
    if dialog == None:
        SleepingTool(window)
    else:
        messagebox.showinfo("Information","Please close the other component window before proceed.")

def fontTitleTransition(Message):
    Message = list(Message)
    for x in range(0, len(Message)):
        if(x+1<len(Message)):
            aux = Message[x+1]
            Message[x] = Message[x+1]
            Message[x+1] = aux
        else:
            aux = Message[0]
            Message[x] = Message[0]
            Message[0] = aux
    return "".join(Message)

def fontSeparatedTransition(Message):
    Message = list(Message)
    for x in range(0, len(Message)):
        if Message[x] == "_":
            if x+1 < len(Message):
                aux = Message[x+1]
                Message[x+1] = Message[x]
                Message[x] = aux
            else:
                Message ="".join(Message)
                Message = Message.split("_")
                Message = Message[0]
                Message = "_" + Message
            break
    return "".join(Message)

def fontTypeWritingTransition():
    global visualSongNameLabel
    if visualSongNameLabel == play_list.validFiles[play_list.currentSongIndex].fileName:
        visualSongNameLabel = visualSongNameLabel = play_list.validFiles[play_list.currentSongIndex].fileName[0]
    else:
        if visualSongNameLabel == None:
            visualSongNameLabel = play_list.validFiles[play_list.currentSongIndex].fileName[0]
        else:
            visualSongNameLabel += play_list.validFiles[play_list.currentSongIndex].fileName[len(visualSongNameLabel)]

def searchSongInPlaylist():
    if dialog == None:
        SearchTool(window)
    else:
        messagebox.showinfo("Information","Please close the other component window before proceed.")

def fadein(Position): #not yet working
    fadein_duration = play_list.validFiles[play_list.currentSongIndex].fadein_duration
    if fadein_duration > 0:
        if Position >= fadein_duration:
            pygame.mixer.music.set_volume(play_list.VolumeLevel)
        elif Position >= fadein_duration - (fadein_duration/10):
            pygame.mixer.music.set_volume(play_list.VolumeLevel- play_list.VolumeLevel/10)
        elif Position >= fadein_duration - 2*(fadein_duration/10):
            pygame.mixer.music.set_volume(play_list.VolumeLevel- 2*play_list.VolumeLevel/10)
        elif Position >= fadein_duration - 3*(fadein_duration/10):
            pygame.mixer.music.set_volume(play_list.VolumeLevel- 3*play_list.VolumeLevel/10)
        elif Position >= fadein_duration - 4*(fadein_duration/10):
            pygame.mixer.music.set_volume(play_list.VolumeLevel- 4*play_list.VolumeLevel/10)
        elif Position >= fadein_duration - 5*(fadein_duration/10):
            pygame.mixer.music.set_volume(play_list.VolumeLevel- 5*play_list.VolumeLevel/10)
        elif Position >= fadein_duration - 6*(fadein_duration/10):
            pygame.mixer.music.set_volume(play_list.VolumeLevel- 6*play_list.VolumeLevel/10)
        elif Position >= fadein_duration - 7*(fadein_duration/10):
            pygame.mixer.music.set_volume(play_list.VolumeLevel- 7*play_list.VolumeLevel/10)
        elif Position >= fadein_duration - 8*(fadein_duration/10):
            pygame.mixer.music.set_volume(play_list.VolumeLevel- 8*play_list.VolumeLevel/10)
        elif Position >= fadein_duration - 9*(fadein_duration/10):
            pygame.mixer.music.set_volume(play_list.VolumeLevel- 9*play_list.VolumeLevel/10)
        else :
            pygame.mixer.music.set_volume(0.0)

def fadeout(Position):
    fadeout_duration = play_list.validFiles[play_list.currentSongIndex].fadeout_duration
    if fadeout_duration > 0:
        if fadeout_duration - 9*(fadeout_duration/10) > Position:
            pygame.mixer.music.set_volume(play_list.VolumeLevel - 9*(play_list.VolumeLevel / 10))
        elif fadeout_duration - 8*(fadeout_duration/10) > Position:
            pygame.mixer.music.set_volume(play_list.VolumeLevel - 8*(play_list.VolumeLevel / 10))
        elif fadeout_duration - 7*(fadeout_duration/10) > Position:
            pygame.mixer.music.set_volume(play_list.VolumeLevel - 7*(play_list.VolumeLevel / 10))
        elif fadeout_duration - 6*(fadeout_duration/10) > Position:
            pygame.mixer.music.set_volume(play_list.VolumeLevel - 6*(play_list.VolumeLevel / 10))
        elif fadeout_duration - 5*(fadeout_duration/10) > Position:
            pygame.mixer.music.set_volume(play_list.VolumeLevel - 5*(play_list.VolumeLevel / 10))
        elif fadeout_duration - 4*(fadeout_duration/10) > Position:
            pygame.mixer.music.set_volume(play_list.VolumeLevel - 4*(play_list.VolumeLevel / 10))
        elif fadeout_duration - 3*(fadeout_duration/10) > Position:
            pygame.mixer.music.set_volume(play_list.VolumeLevel - 3*(play_list.VolumeLevel / 10))
        elif fadeout_duration - 2*(fadeout_duration/10) > Position:
            pygame.mixer.music.set_volume(play_list.VolumeLevel - 2*(play_list.VolumeLevel / 10))
        elif fadeout_duration - (fadeout_duration/10) > Position:
            pygame.mixer.music.set_volume(play_list.VolumeLevel - (play_list.VolumeLevel / 10))

window = tk.Tk() #tk.Tk() return a widget which is window
Project_Title = "   PyPlay MP3 Player in Python     "
window.title(Project_Title)

window.geometry("500x430+100+100")# build a window 30x280 on size at position 500 x 300 (almost center of screen)
window.protocol("WM_DELETE_WINDOW", on_closing) #delete the window when clicking cancel, on closing is the function to deal with it

SkinColor = StringVar()
SkinColor.set(skinOptions[1][play_list.skin])
backgroundFile = skinOptions[0][play_list.skin]

fontColor = StringVar()
fontColor.set("white")

background_image=tk.PhotoImage(file=backgroundFile)
background_label = tk.Label(window, image=background_image)
background_label.pack()
background_label.place(x=0, y=0, relwidth=1, relheight=1)

OpenFileButton = tk.Button(window,  #the first parameter is the widget
                   text='Open File',  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=load_file, #the width of the button, and the function which get called when clicking it
                   bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

OpenDirectoryButton = tk.Button(window,  #the first parameter is the widget
                   text='Open Directory',  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=load_directory, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

PlayButton = tk.Button(window,  #the first parameter is the widget
                   text='Play',  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=play_music, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

PausedButtonText = StringVar()
PausedButtonText.set("Pause")
PauseButton = tk.Button(window,  #the first parameter is the widget
                   textvariable=PausedButtonText,  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=pause_music, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

StopButton = tk.Button(window,  #the first parameter is the widget
                   text="Stop",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=stop_music, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                    font=allButtonsFont) #this is the font, size and type

NextButton = tk.Button(window,  #the first parameter is the widget
                   text="Next",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=next_song, #the width of the button, and the function which get called when clicking it
                       bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

PreviousButton = tk.Button(window,  #the first parameter is the widget
                   text="Previous",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=previous_song, #the width of the button, and the function which get called when clicking it
                           bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

VolumeDownButton = tk.Button(window,  #the first parameter is the widget
                   text="Volume Down",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=volume_down, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

VolumeUpButton = tk.Button(window,  #the first parameter is the widget
                   text="Volume Up",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=volume_up, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

ShuffleButtonText = StringVar()
ShuffleButtonText.set("Shuffle Off")

ShuffleButton = tk.Button(window,  #the first parameter is the widget
                   textvariable=ShuffleButtonText,  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=shuffle, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

SavePlaylistButton = tk.Button(window,  #the first parameter is the widget
                   text="Save Playlist",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=save_playlist, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

NewPlaylistButton = tk.Button(window,  #the first parameter is the widget
                   text="New Playlist",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=new_playlist, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

ViewPlaylistButtonText = StringVar()
ViewPlaylistButtonText.set("Compact View")

ViewPlaylistButton = tk.Button(window,  #the first parameter is the widget
                   textvariable=ViewPlaylistButtonText,  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=view_playlist, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

RepeatButtonText = StringVar()
RepeatButtonText.set("Repeat All")

RepeatButton = tk.Button(window,  #the first parameter is the widget
                   textvariable=RepeatButtonText,  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=repeat, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

RendomizeListButton = tk.Button(window,  #the first parameter is the widget
                   text="Randomize List",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=randomize, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

RemoveSongButton = tk.Button(window,  #the first parameter is the widget
                   text="Remove Song",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=remove_song, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

SortButtonText = StringVar()
SortButtonText.set("Sorted")

SortListButton = tk.Button(window,  #the first parameter is the widget
                   textvariable=SortButtonText,  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=sort_list, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

MoveUpButton = tk.Button(window,  #the first parameter is the widget
                   text="Move Up",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=move_up, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

MoveDownButton = tk.Button(window,  #the first parameter is the widget
                   text="Move Down",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=move_down, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

CutSelectedButton = tk.Button(window,  #the first parameter is the widget
                   text="Cut Selected",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=showCuttingTool, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

SearchButton = tk.Button(window,  #the first parameter is the widget
                   text="Search File",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=searchSongInPlaylist, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

SleepButton = tk.Button(window,  #the first parameter is the widget
                   text="Sleep \ Wake",  # the text on the button
                    height=allButtonsHeight,
                   width=allButtonsWidth, command=showSleepingTool, #the width of the button, and the function which get called when clicking it
                    bg=SkinColor.get(), fg=fontColor.get(),  #bg is the background color of the button, fg is the text color
                   font=allButtonsFont) #this is the font, size and type

packPositionButton()

labelBackground = StringVar()
labelBackground.set("lightgray")

#Building the labels
SongName = StringVar()
SongName.set("Playing: ")

labelPlaying = tk.Label(window, textvariable=SongName, compound=tk.CENTER, padx=10, bd=2 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window

SongDuration = StringVar()
SongDuration.set("Time Elapsed: ")

labelDuration = tk.Label(window, textvariable=SongDuration, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window

SongSize = StringVar()
SongSize.set("Size: ")

labelSize = tk.Label(window, textvariable=SongSize, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window
textVolumeLevel = StringVar()
textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel*100)) + "%")
labelVolumeLevel = tk.Label(window, textvariable=textVolumeLevel, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window

textFilesToPlay = StringVar()
textFilesToPlay.set("Files: " + str(len(play_list.validFiles)))
labelFilesToPlay = tk.Label(window, textvariable=textFilesToPlay, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window

textLength = StringVar()
textLength.set("Length: ")
labelLength = tk.Label(window, textvariable=textLength, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window

textGenre = StringVar()
textGenre.set("Genre: ")
labelGenre = tk.Label(window, textvariable=textGenre, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window

textStartTime = StringVar()
textStartTime.set("Start Time: ")
labelStartTime = tk.Label(window, textvariable=textStartTime, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window

textEndTime = StringVar()
textEndTime.set("End Time: ")
labelEndTime = tk.Label(window, textvariable=textEndTime, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window

textTotalPlayTime = StringVar()
textTotalPlayTime.set("Total PlayTime: ")
labelTotalPlayTime = tk.Label(window, textvariable=textTotalPlayTime, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window

textFallAsleep = StringVar()
textFallAsleep.set("Fall Asleep: Never")
labelFallAsleep = tk.Label(window, textvariable=textFallAsleep, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window						

textWakeUp = StringVar()
textWakeUp.set("Wake Up: Never")
labelWakeUp = tk.Label(window, textvariable=textWakeUp, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window

textFadeIn = StringVar()
textFadeIn.set("FadeIn: ")
labelFadeIn = tk.Label(window, textvariable=textFadeIn, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window

textFadeOut = StringVar()
textFadeOut.set("FadeOut: ")
labelFadeOut = tk.Label(window, textvariable=textFadeOut, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())

textMonoStereoMode = StringVar()
textMonoStereoMode.set("Mode: ")
labelMonoStereoMode = tk.Label(window, textvariable=textMonoStereoMode, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())

textSampleRate = StringVar()
textSampleRate.set("Sample Rate: ")
labelSampleRate = tk.Label(window, textvariable=textSampleRate, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())

textNofPlays = StringVar()
textNofPlays.set("No. of Plays: ")
labelNofPlays = tk.Label(window, textvariable=textNofPlays, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())

textDanthologyMode = StringVar()
textDanthologyMode.set("Danthology Mode: OFF")
labelDanthologyMode = tk.Label(window, textvariable=textDanthologyMode, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())

textArtist = StringVar()
textArtist.set("Artist: ")
labelArtist = tk.Label(window, textvariable=textArtist, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())         

textAlbum = StringVar()
textAlbum.set("Album: ")
labelAlbum = tk.Label(window, textvariable=textAlbum, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())      

textTitle = StringVar()
textTitle.set("Title: ")
labelTitle = tk.Label(window, textvariable=textTitle, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())         

textYear = StringVar()
textYear.set("Year: ")
labelYear = tk.Label(window, textvariable=textYear, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())                           
                        
packPositionLabels()


style = ttk.Style()
style.theme_use('clam')

style.configure("Horizontal.TScrollbar", gripcount=0,
                background="Green", darkcolor="DarkGreen", lightcolor="LightGreen",
                troughcolor="gray", bordercolor="blue", arrowcolor="white")



#Creating a listbox
frame = tk.Frame(window)
scroll = tk.Scrollbar(frame, orient="vertical", width=15)
listbox = tk.Listbox(frame, fg=fontColor.get(), font=allButtonsFont, width=80, bg=SkinColor.get(), height=35, \
                     yscrollcommand=scroll.set)

#Creating Combobox
option = Combobox(window, textvariable=SkinColor, values = skinOptions[1])

#Creating style for progressbar
styl = ttk.Style()

#Creating Progress bar
progress = Progressbar(orient=tk.HORIZONTAL, length=470, mode=play_list.ProgressBarType, value=0, maximum = 100, \
                       style="Horizontal.TProgressbar",) #using the same style

#Creating RadioButton
songRating = StringVar()
songRating.set("0") # initialize

R1 = tk.Radiobutton(window, text="1", variable=songRating, value=1, width=3, bg=radioButtonsDefaultColor, command=UpdateSongRating, fg = fontColor.get(), selectcolor="black", font=allButtonsFont)
R2 = tk.Radiobutton(window, text="2", variable=songRating, value=2, width=3, bg=radioButtonsDefaultColor, command=UpdateSongRating, fg = fontColor.get(), selectcolor="black", font=allButtonsFont)
R3 = tk.Radiobutton(window, text="3", variable=songRating, value=3, width=3, bg=radioButtonsDefaultColor, command=UpdateSongRating, fg = fontColor.get(), selectcolor="black", font=allButtonsFont)
R4 = tk.Radiobutton(window, text="4", variable=songRating, value=4, width=3, bg=radioButtonsDefaultColor, command=UpdateSongRating, fg = fontColor.get(), selectcolor="black", font=allButtonsFont)
R5 = tk.Radiobutton(window, text="5", variable=songRating, value=5, width=3, bg=radioButtonsDefaultColor, command=UpdateSongRating, fg = fontColor.get(), selectcolor="black", font=allButtonsFont)

packPositionListScrolOptionProgRadio()

scheduler = sched.scheduler(time.time, time.sleep)

#Load backup if possible
if os.path.exists(automaticallyBackupFile):
    loadPlaylistFile(automaticallyBackupFile)

window.mainloop() #loop through the window