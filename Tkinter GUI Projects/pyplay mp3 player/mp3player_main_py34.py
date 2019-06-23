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

class Playlist:
    def __init__(self):
        self.isSongPause = False
        self.isSongStopped = False
        self.VolumeLevel=1.0
        self.dirFilePath = None
        self.skin=0
        self.SHUFFLE = False
        self.isListOrdered = 0 #0-onrating ; 1-sorted 2-reversed; 3-random;
        self.validFiles = []
        self.slideImages = []
        self.slideImagesTransitionSeconds = 0;
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

class Song:
    def __init__(self, filename, filepath, filesize):
        self.fileName = filename
        self.filePath = filepath
        self.fileSize = filesize
        self.Rating = 0
        audio = MP3(self.filePath)
        self.sample_rate = audio.info.sample_rate
        self.channels = audio.info.channels
        self.Length = audio.info.length
        audio = EasyID3(self.filePath)
        try:
            self.Genre = audio["genre"]
        except: #enter here if you can't get the genre
            self.Genre = "Various"
        else:
            self.Genre = self.Genre[0]
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
            self.top.geometry("340x360+100+100")
            allButtonsFont = skinOptions[2][play_list.skin]
            self.InfoLabelText = StringVar()
            self.InfoLabelText.set("Welcome to MP3 Cutting capability:\n\n"
                               +"Please enter Start and End value and Hit OK.\n"
                                +"This will NOT change the original file.\n\n\n")
            self.labelInfo = tk.Label(self.top, textvariable=self.InfoLabelText, fg=fontColor.get(), font=allButtonsFont, bg=color).pack()
            self.labelStartValue = tk.Label(self.top, text="Start Value (0 - " + str(int(play_list.validFiles[play_list.currentSongIndex].Length)) + "):", fg=fontColor.get(), font=allButtonsFont, bg=color).pack()

            self.startValue = tk.Entry(self.top)
            self.startValue.pack(padx=5)
            self.startValue.bind("<Return>", self.cutItem)

            self.labelEndValue = tk.Label(self.top, text="End Value (0 - " + str(int(play_list.validFiles[play_list.currentSongIndex].Length)) + "):", fg=fontColor.get(), font=allButtonsFont, bg=color).pack()
            self.endValue = tk.Entry(self.top)
            self.endValue.pack(padx=5)

            self.endValue.bind("<Return>", self.cutItem)
            self.b = tk.Button(self.top, text="OK", command=self.ok, bg=color, fg=fontColor.get(), font=allButtonsFont)
            self.b.pack(pady=5)

            self.labelFadeIn = tk.Label(self.top, text="Add FadeIn: ", fg=fontColor.get(),
                                           font=allButtonsFont, bg=color).pack()
            self.FadeIn = StringVar()
            self.FadeIn.set("0")
            fadeOptions = ["5","10","15", "20"]
            self.fadeInBox = Combobox(self.top, textvariable=self.FadeIn, values=fadeOptions)
            self.fadeInBox.pack(pady=5)
            self.fadeInBox.bind("<<ComboboxSelected>>", self.addFadeIn)

            self.labelFadeOut = tk.Label(self.top, text="Add FadeOut: ", fg=fontColor.get(),
                                        font=allButtonsFont, bg=color).pack()
            self.FadeOut = StringVar()
            self.FadeOut.set("0")
            self.fadeOutBox = Combobox(self.top, textvariable=self.FadeOut, values=fadeOptions)
            self.fadeOutBox.pack(pady=5)
            self.fadeOutBox.bind("<<ComboboxSelected>>", self.addFadeOut)
            self.top.bind("<Escape>", self.destroyEsc)
            self.top.bind("<Tab>", self.focus_Input)
            dialog = self #each instance of CuttingTool will be assigned to this variable:

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
        self.ok()

    def ok(self):
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
        self.top.protocol("WM_DELETE_WINDOW", self.destroy)
        allButtonsFont = skinOptions[2][play_list.skin]
        InfoLabelText = StringVar()
        InfoLabelText.set("Search for song: \n")
        tk.Label(self.top, textvariable=InfoLabelText, fg=fontColor.get(), font=allButtonsFont, bg=color).pack()
        tk.Label(self.top, text="Value: ", fg=fontColor.get(), font=allButtonsFont, bg=color).pack()
        self.searchValue = tk.Entry(self.top)
        self.searchValue.bind("<Key>", self.showResults)
        self.top.bind("<Key>", self.focus_Input)
        self.top.bind("<Tab>", self.focus_out)
        self.searchValue.bind("<Return>", self.playNextSearch)
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
        self.destroy()

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
        play_music()

    def destroy(self):
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
        play_list.slideImagesTransitionSeconds = Slideshow.seconds.get()

    def clearSlideshow(self):
        play_list.slideImages.clear()
        self.numberOfImages.set("Number of Images: " + str(len(play_list.slideImages)))

    def destroy(self):
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
        color = OpenFileButton["bg"] # get the color which the rest of elements is using at the moment
        self.top = tk.Toplevel(parent, bg=color)
        self.top.protocol("WM_DELETE_WINDOW", self.destroy)
        Window_Title = "Customize"
        self.top.title(Window_Title)
        self.top.geometry("380x470+100+100")
        if type(allButtonsFont) == StringVar:
            allButtonsFont = allButtonsFont.get()
        self.InfoLabelText = StringVar()
        self.InfoLabelText.set("Welcome to Customize capability:\n\n"
                                +"Here you can customize your player appearance\n"
                                 +"in any way you like.\n\n\n")
        self.labelInfo = tk.Label(self.top, textvariable=self.InfoLabelText, fg=fontColor.get(), font=allButtonsFont, bg=color).pack()
        
        self.labelFontColor = tk.Label(self.top, text="Button&Label Color: ", fg=fontColor.get(), font=allButtonsFont, bg=color).pack()
        
        self.colorBox = Combobox(self.top, textvariable=SkinColor, values=custom_color_list)
        self.colorBox.pack()
        self.colorBox.bind("<<ComboboxSelected>>", changingBackgroundElementColor)
        
        self.labelFont = tk.Label(self.top, text="Font: ", fg=fontColor.get(), font=allButtonsFont, bg=color).pack()
        
        aux = allButtonsFont
        allButtonsFont = StringVar() #making this string variable.
        allButtonsFont.set(aux)
        self.fontBox = Combobox(self.top, textvariable=allButtonsFont, values=custom_font_list)
        self.fontBox.pack()
        self.fontBox.bind("<<ComboboxSelected>>", customFontChange)
        self.labelBackgroundColor = tk.Label(self.top, text="Label Background: ", fg=fontColor.get(), font=allButtonsFont.get(), bg=color).pack()
        self.labelColorBox = Combobox(self.top, textvariable=labelBackground, values=custom_color_list)
        self.labelColorBox.pack()
        self.labelColorBox.bind("<<ComboboxSelected>>", changingLabelBackgroundColor)
        self.FontMainColor = tk.Label(self.top, text="Font Color: ", fg=fontColor.get(), font=allButtonsFont.get(), bg=color).pack()
        self.FontMainColorBox = Combobox(self.top, textvariable=fontColor, values=custom_color_list)
        self.FontMainColorBox.pack()
        self.FontMainColorBox.bind("<<ComboboxSelected>>", changingFontColor)

        self.useColorOnBackgroundedLabels = tk.Label(self.top, text="Color Bg Labels: ", fg=fontColor.get(), font=allButtonsFont.get(),
                                      bg=color).pack()

        self.colorBgLabels = StringVar()
        self.colorBgLabels.set("False")
        self.RbFalse = tk.Radiobutton(self.top, text="False", variable=self.colorBgLabels, value=False, width=3, bg=color,
                            command=lambda: changingBackgroundedLabelsColor(self.colorBgLabels,0), fg=fontColor.get(), selectcolor="black", font=allButtonsFont.get())
        self.RbTrue = tk.Radiobutton(self.top, text="True", variable=self.colorBgLabels, value=True, width=3, bg=color,
                            command=lambda: changingBackgroundedLabelsColor(self.colorBgLabels,0), fg=fontColor.get(), selectcolor="black", font=allButtonsFont.get())
        self.RbFalse.pack(padx=5)
        self.RbTrue.pack(padx=5)
        self.browseBackgroundPicture = tk.Button(self.top, text="Load Background", command=self.browse_background_picture, bg=color, fg=fontColor.get(), font=allButtonsFont.get())
        self.browseBackgroundPicture.pack(pady=15)

        self.startSlideshow = tk.Button(self.top, text="Start Slideshow",
                                                 command=self.slideshowBegin, bg=color, fg=fontColor.get(),
                                                 font=allButtonsFont.get())
        self.startSlideshow.pack()
        self.top.bind("<Escape>", self.destroyEsc)
        self.top.bind("<Tab>", self.focus_Input)
        dialog = self

    def destroy(self):
        global dialog
        self.top.destroy()
        dialog = None

    def destroyEsc(self, event):
        self.destroy()

    def focus_Input(self, event):
        if self.colorBox.focus_get():
            self.fontBox.focus_force()
        elif self.fontBox.focus_get():
            self.labelColorBox.focus_force()
        elif self.labelColorBox.focus_get():
            self.FontMainColorBox.focus_force()
        elif self.FontMainColorBox.focus_get():
            self.colorBox.focus_force()

    def take_focus(self):
        self.top.wm_attributes("-topmost", 1)
        self.top.grab_set()
        self.colorBox.focus_force()

    def slideshowBegin(self):
        Slideshow()

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
        self.top.geometry("450x170+100+100")
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

automaticallyBackupFile = "backup.pypl"
allButtonsWidth = 14
allButtonsHeight = 1
custom_color_list = ["green", "yellow", "purple", "black", "brown", "sienna", "cyan", "magenta", "pink", "blue", "darkblue", "darkgreen", "deeppink", "red", \
                                            "orange", "gold", "silver", "indigo"]

radioButtonsDefaultColor = "lightgray"

custom_font_list = ["Arial 10", "Consolas 10", "Courier 9", "Verdana 9", "Georgia 9", "Tahoma 9", "Rockwell 10", "Fixedsys 11", "Candara 10", "Impact 9", \
                                    "Calibri 10 italic", "Modern 10 bold", "Harrington 10 bold", "Stencil 10 italic"]
progressViewRealTime = 0.5
play_list = Playlist()
listBox_Song_selected_index = None
APPLICATION_EXIT = False
skinOptions = [["default.gif", "minilights.gif", "road.gif", "darkg.gif", "leaves.gif", "darkblue.gif", "map.gif", "space.gif", "universe.gif"],\
               ["blue", "red", "gray", "green", "deeppink", "darkblue", "sienna", "indigo", "black", "custom"],\
               ["Consolas 10 bold", "Rockwell 10 bold", "Arial 10 italic", "Candara 10 bold", "Arial 10 bold", "Calibri 10 bold", "Harrington 10 bold", "Fixedsys 11", "Stencil 10"]]

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
            if ".mp3" in file:
                fileName = re.split("/", file)
                fileName = fileName[len(fileName) - 1]
                fileSize = os.path.getsize(file) / (1024 * 1024)
                fileSize = float("{0:.2f}".format(fileSize))
                play_list.validFiles.append(Song(fileName, file, fileSize))
                play_list.currentSongIndex = 0
                textFilesToPlay.set("Files To Play: " + str(len(play_list.validFiles)))
                play_list.playTime += play_list.validFiles[play_list.currentSongIndex].Length
            elif ".pypl" in file:
                loadPlaylistFile(file)
                break
        displayElementsOnPlaylist()

def loadPlaylistFile(fileURL):
    global play_list
    global allButtonsFont
    global fontColor
    global listBox_Song_selected_index
    try:
        file = open(fileURL, "rb")
        content = pickle.load(file)
    except Exception as exp:
        print("Load Playlist File Exception: " + exp)
        print("File: " + str(fileURL)+ " might be corrupted.")
    else:
        if isinstance(content, Playlist):
            play_list = content
            del content
            textFilesToPlay.set("Files To Play: " + str(len(play_list.validFiles)))

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
                SongDuration.set("Progress: " + str(int(play_list.currentSongPosition)) + " s")
                #Update Length
                songLength = float("{0:.0f}".format(play_list.validFiles[play_list.currentSongIndex].Length))  # no decimals needed
                textLength.set("Length: {:0>8}".format(str(datetime.timedelta(seconds=songLength))))
                textGenre.set("Genre: " + str(play_list.validFiles[play_list.currentSongIndex].Genre))
                startPos = int(play_list.validFiles[play_list.currentSongIndex].startPos)
                textStartTime.set("Start Time: {:0>8}".format(str(datetime.timedelta(seconds=startPos))))
                endPos = int(play_list.validFiles[play_list.currentSongIndex].endPos)
                textEndTime.set("End Time: {:0>8}".format(str(datetime.timedelta(seconds=endPos))))
                textFadeIn.set("FadeIn: " + str(play_list.validFiles[play_list.currentSongIndex].fadein_duration)+"s")
                textFadeOut.set("FadeOut: " + str(play_list.validFiles[play_list.currentSongIndex].fadeout_duration) +"s")
                mode = "Stereo" if play_list.validFiles[play_list.currentSongIndex].channels == 2 else "Mono"
                textMonoStereoMode.set("Mode: " + mode)
                textTotalPlayTime.set("Total PlayTime: {:0>8}" .format(str(datetime.timedelta(seconds=int(play_list.playTime)))))
                #Select current song, and make it visible
                listbox.selection_clear(0, tk.END)
                listbox.select_set(play_list.currentSongIndex)
                listbox.see(play_list.currentSongIndex)
                listBox_Song_selected_index = play_list.currentSongIndex
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
        textFilesToPlay.set("Files To Play: " + str(len(play_list.validFiles)))
        displayElementsOnPlaylist()

def searchFilesInDirectories(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if ".mp3" in file:
                fileSize = os.path.getsize(root + "/" + file) / (1024 * 1024)
                fileSize = float("{0:.2f}".format(fileSize))
                song = Song(file, root + "/" + file, fileSize)
                play_list.validFiles.append(song)
                play_list.playTime += song.Length

def play_music():
    global visualSongNameLabel
    if len(play_list.validFiles) > 0 and play_list.currentSongIndex!=None:
        try:
            pygame.init()
            pygame.mixer.init(play_list.validFiles[play_list.currentSongIndex].sample_rate, -16, play_list.validFiles[play_list.currentSongIndex].channels, 1024*32) #standard values for stereo
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
                play_list.currentSongPosition=0
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
                    play_list.currentSongPosition = start_pos
                pygame.mixer.music.set_pos(start_pos)
                play_list.RESUMED = True
        except Exception as e:
            print("Play Music Function: " + str(e))
        else:
            SongName.set("Playing: " + play_list.validFiles[play_list.currentSongIndex].fileName)
            SongSize.set("Size: " + str(play_list.validFiles[play_list.currentSongIndex].fileSize) + " MB")
            songLength = float("{0:.0f}".format(play_list.validFiles[play_list.currentSongIndex].Length))  # no decimals needed
            textLength.set("Length: {:0>8}".format(str(datetime.timedelta(seconds=songLength))))
            textGenre.set("Genre: " + str(play_list.validFiles[play_list.currentSongIndex].Genre))
            startPos = int(play_list.validFiles[play_list.currentSongIndex].startPos)
            textStartTime.set("Start Time: {:0>8}" .format(str(datetime.timedelta(seconds=startPos))))
            endPos = int(play_list.validFiles[play_list.currentSongIndex].endPos)
            textEndTime.set("End Time: {:0>8}" .format(str(datetime.timedelta(seconds=endPos))))
            textFadeIn.set("FadeIn: " + str(play_list.validFiles[play_list.currentSongIndex].fadein_duration)+"s")
            textFadeOut.set("FadeOut: " + str(play_list.validFiles[play_list.currentSongIndex].fadeout_duration) +"s")
            mode = "Stereo" if play_list.validFiles[play_list.currentSongIndex].channels == 2 else "Mono"
            textMonoStereoMode.set("Mode: " + mode)
            progress["maximum"] = play_list.validFiles[play_list.currentSongIndex].Length
            songRating.set(str(play_list.validFiles[play_list.currentSongIndex].Rating))
            updateRadioButtons()
            visualSongNameLabel = "_"+play_list.validFiles[play_list.currentSongIndex].fileName
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
    if pygame.mixer.get_init():
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                SongName.set("Playing: ")
                SongDuration.set("Progress: ")
                SongSize.set("Size: ")
                play_list.isSongStopped = True
                play_list.currentSongPosition=0
                play_list.RESUMED = False
                PausedButtonText.set("Pause")
                play_list.isSongPause = False
        except Exception as e:
            print("Stop Music Function: " +str(e))

def next_song():
    global listBox_Song_selected_index
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
        play_list.currentSongPosition=0
        play_music()

def previous_song():
    global listBox_Song_selected_index
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
        play_list.currentSongPosition = 0
        play_music()

def viewProgress():
    global play_list
    global progress
    global Project_Title
    global visualSongNameLabel
    if play_list.usingSlideShow == True:
        Slideshow.countSeconds()
    if APPLICATION_EXIT == False:
        if pygame.mixer.music.get_busy() and play_list.isSongPause == False:
            Project_Title = fontTransition(Project_Title)
            window.title(Project_Title) #add animation to font when playing music
            if visualSongNameLabel != None:
                visualSongNameLabel = fontMovingTransition(visualSongNameLabel)
                SongName.set("Playing: " + visualSongNameLabel)
            if play_list.RESUMED:
                local_position = play_list.currentSongPosition + (pygame.mixer.music.get_pos() / 1000)
                local_positionDisplay = float("{0:.0f}".format(local_position)) #no decimals needed
                SongDuration.set("Progress: {:0>8}" .format(str(datetime.timedelta(seconds=local_positionDisplay))))
                progress["value"] = local_position
                if play_list.validFiles[play_list.currentSongIndex].fadein_duration > 0:
                    fadein(local_position - play_list.validFiles[play_list.currentSongIndex].startPos)
                if play_list.validFiles[play_list.currentSongIndex].fadeout_duration > 0:
                    fadeout(play_list.validFiles[play_list.currentSongIndex].endPos - local_position)
                if local_position >= play_list.validFiles[play_list.currentSongIndex].endPos:
                    stop_music()
                    play_list.isSongStopped = False #song is not stopped in this circumstances, song has finished

            else:
                play_list.currentSongPosition = (pygame.mixer.music.get_pos()/1000)
                local_positionDisplay = float("{0:.0f}".format(play_list.currentSongPosition))#no decimals needed
                SongDuration.set("Progress: {:0>8}" .format(str(datetime.timedelta(seconds=local_positionDisplay))))
                progress["value"] = play_list.currentSongPosition
                if play_list.validFiles[play_list.currentSongIndex].fadein_duration > 0:
                    fadein(play_list.currentSongPosition - play_list.validFiles[play_list.currentSongIndex].startPos)
                if play_list.validFiles[play_list.currentSongIndex].fadeout_duration > 0:
                    fadeout(play_list.validFiles[play_list.currentSongIndex].endPos - play_list.currentSongPosition)
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

def clearLabels():
    textFilesToPlay.set("Files To Play: " + str(len(play_list.validFiles)))
    textVolumeLevel.set("Volume Level: " + str(int(play_list.VolumeLevel * 100)) + "%")
    textGenre.set("Genre: ")
    textFadeIn.set("FadeIn: ")
    textMonoStereoMode.set("Mode: ")
    textEndTime.set("End Time: ")
    textStartTime.set("Start Time")
    textLength.set("Length: ")
    SongDuration.set("Progress: ")

def new_playlist():
    global play_list
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
    textTotalPlayTime.set("Total PlayTime: {:0>8}" .format(str(datetime.timedelta(seconds=int(play_list.playTime)))))

def changingBackgroundElementColor(event):
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
        if dialog == None:
            Customize(window)
        else:
            messagebox.showinfo("Information", "Please close the other component window before proceed.")
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
    if len(play_list.validFiles) > 0 and play_list.currentSongIndex!= None:
        e = event.widget
        x = play_list.validFiles[play_list.currentSongIndex].Length / 470
        play_list.currentSongPosition = (event.x * x)
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(play_list.currentSongPosition)
        progress["value"] = play_list.currentSongPosition
        play_list.RESUMED = True

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
        if listBox_Song_selected_index!=None:
            del play_list.validFiles[listBox_Song_selected_index]
            displayElementsOnPlaylist()
            textFilesToPlay.set("Files To Play: " + str(len(play_list.validFiles)))
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

def sort_list():
    # 0-onrating, 1-sorted, 2-reversed, 3-random
    if len(play_list.validFiles) > 0 and play_list.currentSongIndex!=None:
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
    labelTotalPlayTime.place(x=10, y=550)
    labelFallAsleep.place(x=10, y=570)
    labelWakeUp.place(x=10, y=590)
    labelFadeIn.place(x=300, y=330)
    labelFadeOut.place(x=300, y=350)
    labelMonoStereoMode.place(x=300, y=370)

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
    elif event.char == "a":
        if Slideshow.top==None:
            Slideshow()
    elif event.char == "P":
        Customize(window)
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
                + "T - is equivalent to Sleep\Wake Button\n"
                + "J - is equivalent to Search Button\n"
                + "P - is equivalent to Customize Option\n"
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
    elif event.char == "q":
        showCuttingTool()
    elif event.char =="j":
        searchSongInPlaylist()
    elif event.char == "t":
        showSleepingTool()

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
        aMenu = tk.Menu(window, tearoff=0)
        aMenu.add_command(label='Delete', command=remove_song)
        aMenu.add_command(label='File Info', command=songInfo)
        aMenu.add_command(label='Move Up', command=move_up)
        aMenu.add_command(label='Move Down', command=move_down)
        aMenu.add_command(label='Open in Explorer', command=openFileInExplorer)
        aMenu.post(event.x_root, event.y_root)

def packPositionListScrolOptionProgRadio():
    #Here are set position, events, controls, styling for listbox, progressbar, scrollbar, option, radiobuttons
    listbox.pack(side = tk.LEFT, fill=tk.X) #this will place listbox on the leftside of the FRAME
    listbox.bind('<Double-Button>', elementPlaylistDoubleClicked)
    listbox.bind('<ButtonPress-3>', rightClickListboxElement)
    listbox.bind('<<ListboxSelect>>', list_selected_item)
    listbox.bind("<Return>", pressedEnter)
    window.bind("<Return>", pressedEnter)
    window.bind("<Tab>", pressedTab)
    window.bind("<Key>", pressedKeyShortcut)
    window.bind("<Shift_L>", pressedShiftRight)
    window.bind("<Control_L>", pressedCtrlRight)
    window.bind("<Delete>", pressedDelete)
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
    progress.place(x=10, y=405)
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

def fontMovingTransition(Message):
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
Project_Title = "_PyPlay MP3 Player in Python_"
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

labelPlaying = tk.Label(window, textvariable=SongName, compound=tk.CENTER, padx=10 \
                        , fg=SkinColor.get(), font=allButtonsFont, background = labelBackground.get())  # creating a label on the window

SongDuration = StringVar()
SongDuration.set("Progress: ")

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
textFilesToPlay.set("Files To Play: " + str(len(play_list.validFiles)))
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
progress = Progressbar(orient=tk.HORIZONTAL, length=470, mode='determinate', value=0, maximum = 100, \
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