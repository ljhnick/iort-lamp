import serial
import threading
import queue
import tkinter as tk
import pygame
import time

class SerialThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        flag = 1
        try:
            s = serial.Serial('/dev/tty.usbmodem141101',9600)
        except:
            flag = 0
        
        if (flag == 1):
            while True:
                if s.inWaiting():
                    bString = s.readline(s.inWaiting())
                    string = str(bString, "utf-8")
                    string = string.replace('\n','')
                    string = string.replace('\r','')
                    self.queue.put(string)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("400x300")

        self.var = tk.StringVar()
        self.disp = tk.Label(self, textvariable=self.var, bg='yellow',\
                                font=('Arial', 12), width=20, height=2)

        self.control_seq = None
        self.player_volume = 0.6
        # buttons
        self.play_button = tk.Button(self, text='play', width=15, height=2, command=self.play_music)
        self.stop_button = tk.Button(self, text='stop', width=15, height=2, command=self.stop_music)
        self.pause_button = tk.Button(self, text='pause', width=15, height=2, command=self.pause_music)
        self.unpause_button = tk.Button(self, text='continue', width=15, height=2, command=self.unpause_music)

        self.volume_up = tk.Button(self, text='volume ++', width=15, height=2, command=self.vol_up)
        self.volume_dn = tk.Button(self, text='volume --', width=15, height=2, command=self.vol_dn)
        # sliders
        self.volume_slider = tk.Scale(self, from_=0, to=100, command=self.change_volume)
        self.volume_slider.set(60)

        # pack used functions
        self.disp.pack()
        self.play_button.pack()
        self.pause_button.pack()
        self.unpause_button.pack()
        self.stop_button.pack()
        self.volume_up.pack()
        self.volume_dn.pack()
        self.volume_slider.pack()

        # music player
        self.file_path = r'/Users/kgicmd/Desktop/mbzj.ogg'
        self.mixer = pygame.mixer
        self.mixer.init()
        track = self.mixer.music.load(self.file_path)

        self.queue = queue.Queue()
        thread = SerialThread(self.queue)
        thread.start()
        self.process_serial()


    def play_music(self):
        self.mixer.music.play()
        self.var.set('playing...')

    def stop_music(self):
        self.mixer.music.stop()
        self.var.set('stopped')

    def pause_music(self):
        self.mixer.music.pause()
        self.var.set('paused')

    def unpause_music(self):
        self.mixer.music.unpause()
        self.var.set('playing...')

    def vol_up(self):
        self.player_volume = min(self.player_volume + 0.1,1)
        disp_str = 'Current Volume: ' + str(int(self.player_volume*100)) + '%'
        self.mixer.music.set_volume(self.player_volume)
        self.var.set(disp_str)

    def vol_dn(self):
        self.player_volume = max(self.player_volume - 0.1,0)
        disp_str = 'Current Volume: ' + str(int(self.player_volume*100)) + '%'
        self.mixer.music.set_volume(self.player_volume)
        self.var.set(disp_str)

    def change_volume(self, _=None):
        value_100 = self.volume_slider.get()
        value = value_100 / 100
        self.player_volume = value
        disp_str = 'Current Volume: ' + str(int(self.player_volume*100)) + '%'
        self.mixer.music.set_volume(self.player_volume)
        self.var.set(disp_str)

    def set_volume_by_ear(self, target=0):
        self.player_volume = target
        self.mixer.music.set_volume(self.player_volume)
        self.volume_slider.set(target*100)
    
    def control_by_ear(self, control_seq):
        if (control_seq == '0'):
            print('start playing')
            self.play_music()
        elif (control_seq == '11'):
            print('stop playing')
            self.stop_music()
        elif (control_seq == '1'):
            print('volume up')
            self.vol_up()
        elif (control_seq == '2'):
            print('volume dn')
            self.vol_dn()
        elif (control_seq == '4'):
            print('pause')
            self.pause_music()
        elif (control_seq == '6'):
            print('resume')
            self.unpause_music()
        else:
            # do nothing
            control_seq_int = int(control_seq)
            real_volume = (control_seq_int - 12)/255
            real_volume_int = int(real_volume)

            self.set_volume_by_ear(target=real_volume_int)

    def process_serial(self):
        while self.queue.qsize():
            try:
                ear_control = self.queue.get()
                #print(sontrol)
                self.control_by_ear(ear_control)

            except queue.Empty:
                pass
        self.after(100, self.process_serial)

app = App()
app.mainloop()