import os
import sys
import camera
import cv2 as cv
import tkinter as tk
import PIL.Image, PIL.ImageTk
from tkinter import simpledialog

sys.setrecursionlimit(3000)

class App:
    def __init__(self, window = tk.Tk(), window_title = "Data Generator"):
        self.window = window
        self.window_title = window_title

        n = 1
        self.counters = [n for i in range(100)]
        
        self.camera = camera.Camera()
        
        self.startGUI()

        self.delay = 15
        self.update()

        self.window.attributes('-topmost', True)
        self.window.configure(bg='black')
        self.window.mainloop()

    def startGUI(self):
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack(anchor=tk.CENTER, expand=True)

        self.classNumber = simpledialog.askstring("No. of classes", "How many classes are there? ", parent=self.window)

        classNo = int(self.classNumber)

        for i in range(1, classNo+1):
            if not os.path.exists(f'class{i}'):
                os.mkdir(f'class{i}')
            
            self.btn = tk.Button(self.window, text=f'Class{i}', width=50, command=lambda i=i: self.saveForClass(i))
            self.btn.pack(anchor=tk.CENTER, expand=True)

    def saveForClass(self, class_num):
        ret, frame = self.camera.getFrame()
        # can not save the images because of the frame no. conspiracy
        print(f'Saving for class{class_num}')
        cv.imwrite(f'class{class_num}/frame{self.counters[class_num - 1]}.jpg', cv.cvtColor(frame, cv.COLOR_BGR2RGB)) # Color data => BGR2RGB / Grayscale Data => RGB2GRAY
        img = PIL.Image.open(f'class{class_num}/frame{self.counters[class_num - 1]}.jpg')
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save(f'class{class_num}/frame{self.counters[class_num - 1]}.jpg')

        self.counters[class_num - 1] += 1

    def update(self):
        ret, frame = self.camera.getFrame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        print("Updating...")
        self.window.after(self.delay, self.update)