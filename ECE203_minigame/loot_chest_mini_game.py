
__author__ = 'Mark Catugas'


import random
import time
from Tkinter import *


class LootChest:

    canvas_width = 600
    canvas_height = 464


    def __init__(self, master):
        self.master = master

        self.coins_coor = []
        self.coin_areas = []
        self.imageIDs = []
        self.coin_dict = {}
        self.coin_index = 0

        self.chesttimerlist = [5,10,15]
        self.chesttimer = 0
        self.coins_collected = 0

        self.dcoins_coor = []
        self.dcoin_areas = []
        self.imageIDds = []
        self.dcoin_dict = {}
        self.dcoin_index = 0

        self.stop_coin = 'false'

        # Commands
        master.title('Loot Box Mini Game - Get the loot!')

        # Widgets
        Label(master, text='Countdown',).grid(row=3,column=2)
        self.countdown_widget = Entry(master,justify=CENTER)
        self.countdown_widget.grid(row=1,column=2)

        Label(master, text='Coins Collected').grid(row=3,column=3)
        self.collected_coins_display = Entry(master,justify=CENTER)
        self.collected_coins_display.grid(row=1,column=3)
        self.collected_coins_display.insert(0, self.coins_collected)

        # Buttons
        self.startButton = Button(master, text='Open Chest',command = self.open_chest)
        self.startButton.grid(row=3, column = 0)

        # Chest Images
        self.game_map = Canvas(master, width = self.canvas_width, height = self.canvas_height, bg = 'lightblue')
        self.open_chest_image = PhotoImage(file='images/chest.gif')
        self.game_map.grid(row=0, column=0)
        self.game_map.create_image(0,0, image = self.open_chest_image,anchor=NW)

        # Coin Image/Reference
        self.coin_image = PhotoImage(file='images/coin.gif')
        label = Label(image=self.coin_image)
        label.image = self.coin_image

        self.dcoin_image = PhotoImage(file='images/devil.gif')
        label = Label(image=self.dcoin_image)
        label.image = self.coin_image

    # Methods

    def get_coins(self, event):
        x1, y1 = event.x, event.y  # Get mouse click coordinates. (0,0) is the top left corner of the map.
        for i in range(20):
            try:
                # print 'debug coor x: %s, %s' % (self.coin_areas[i][0],self.coin_areas[i][1])
                # print 'debug coor y: %s, %s' % (self.coin_areas[i][2], self.coin_areas[i][3])
                if self.coin_areas[i][0] <= x1 <= self.coin_areas[i][1] and self.coin_areas[i][2] <= y1 <= self.coin_areas[i][3]:
                    self.game_map.delete(self.coin_dict[i])
                    self.coins_collected += 1
                    self.collected_coins_display.delete(0, END)
                    self.collected_coins_display.insert(0, self.coins_collected)
                if self.dcoin_areas[i][0] <= x1 <= self.dcoin_areas[i][1] and self.dcoin_areas[i][2] <= y1 <= self.dcoin_areas[i][3]:
                    self.game_map.delete(self.dcoin_dict[i])
                    self.coins_collected -= 1
                    self.collected_coins_display.delete(0, END)
                    self.collected_coins_display.insert(0, self.coins_collected)

            except:
                pass

    def do_nothing(self, event):
        pass

    def gen_coin(self):
        x = random.randint(0,600)
        xmin = x - 30 # Sets minimum x for coin hitbox
        xmax = x + 30 # Sets maximum x for coin hitbox
        y = random.randint(0,464)
        ymin = y - 30 # Sets minimum y for coin hitbox
        ymax = y + 30 # Sets maximum y for coin hitbox
        self.coins_coor.append([x,y])
        self.coin_areas.append([xmin,xmax,ymin,ymax])

    def gen_dcoin(self):
        x = random.randint(0,600)
        xmin = x - 30 # Sets minimum x for devil coin hitbox
        xmax = x + 30 # Sets maximum x for devil coin hitbox
        y = random.randint(0,464)
        ymin = y - 30 # Sets minimum y for devil coin hitbox
        ymax = y + 30 # Sets maximum y for devil coin hitbox
        self.dcoins_coor.append([x,y])
        self.dcoin_areas.append([xmin,xmax,ymin,ymax])

    def show_coins(self):
        self.gen_coin()
        coors = random.choice(self.coins_coor)
        imageID = self.game_map.create_image(coors, image=self.coin_image)
        self.coin_dict[self.coin_index] = imageID
        self.coin_index += 1
        self.coins_coor.remove(coors)

    def show_dcoins(self):
        self.gen_dcoin()
        coors = random.choice(self.dcoins_coor)
        imageIDd = self.game_map.create_image(coors, image=self.dcoin_image)
        self.dcoin_dict[self.dcoin_index] = imageIDd
        self.dcoin_index += 1
        self.dcoins_coor.remove(coors)

    def countdown(self):
        self.countdown_widget.delete(0, END)
        self.countdown_widget.insert(0, self.chesttimer)
        self.chesttimer -= 1
        if self.chesttimer == 0:
            self.countdown_widget.delete(0, END)
            self.countdown_widget.insert(0, self.chesttimer)
            self.game_map.bind("<Button-1>", self.do_nothing)
            # Top Level GUI
            top = Toplevel()
            msg = Message(top, text='Congrats, you collected %s coin(s)!' % self.coins_collected)
            msg.pack()
            quitButton = Button(top,text='quit',command=self.quit_command)
            quitButton.pack()

    def open_chest(self):
        self.chesttimer = random.choice(self.chesttimerlist)
        self.startButton.config(state=DISABLED)
        self.game_map.bind("<Button-1>", self.get_coins)  # Activate mouse binding for the canvas named w.
        self.jobs = []
        for k in range(20):
            next_job = master.after(k * 700, self.show_coins)
            self.jobs.append(next_job)

        for k in range(20):
            next_job = master.after(k * 500, self.show_dcoins)
            self.jobs.append(next_job)

        for k in range(self.chesttimer):
            next_job = master.after(k * 1000, self.countdown)
            self.jobs.append(next_job)

    def quit_command(self):
        exit()

master = Tk()
gameGUI = LootChest(master)
master.mainloop()