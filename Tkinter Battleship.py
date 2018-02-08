from random import randint  # Imports random integer generator
from Tkinter import *
import StoreData
import ttk

StoreData.__init__()

try:
    stats = StoreData.file_import('battleship.stats')
except IOError:
    stats = {
        "Wins": 0,
        "Losses": 0
        }

# Need to do
# Allow player to use a random board
    # Make it reset the whole board then randomly generate a whole new one

# Bugs
    # Sometimes the computer places a ship on the top- and bottom-right corner invalidly (same ship on both corners)

# AI Summary:
# Level 1: Random Shooting
    # Completely random

# Level 2: Targeting
    # After a random or previously found hit, shoot in a valid direction adjacent to that hit
    # If two consecutive hits are achieved, maintain shots along that line
    # If a line ends in a miss, and not a sink, revert to the initial hit location and continue in the opposite
        # direction of the initial line
    # Stop shooting along that line if a ship is sunk
    # Search for hits on the board that haven't resulted in sinks and start on step 1

# Level 3: Smarter Shooting
    # Replaces random shooting with a smarter guessing
    # Will not shoot where the largest remaining ship cannot possibly be
    # Ex. If there is a 4-long stretch of not-shot-at spaces, but the player's carrier (5 long) is still alive, it will
        # not shoot anywhere along that line
    # Will shoot randomly until it has sunk one ship (otherwise it's first shots are very predictable)

# Results:
    # It's almost impossible to lose to level 1, so I'm not gonna test game that
    # Against level 2, I got __ games against the AI's __
    # Against level 3, I got 9 games against the AI's 11


def build_root():  # Rebuilds the root window and places it on the screen at (600, 150) from top-left
    global root
    root.destroy()
    root = Tk()
    root.resizable(width=False, height=False)
    root.geometry('+600+100')


def shoot():
    shot_location = randint(0, 99)
    return shot_location


def finish_up():
    StoreData.file_export('battleship.stats', stats)
    root.destroy()


def end_game(text):
    for i in range(100):
        comp.computer_button_list[i].configure(state=DISABLED)
    ttk.Separator(root, orient='vertical').grid(row=0, column=2, rowspan=100, sticky='ns')
    endFrame = Frame(root)
    endFrame.grid(row=0, rowspan=10, column=3)
    winnerLabel = Label(endFrame, text=text)
    winnerLabel.pack()
    spacer = Label(endFrame, text='')
    spacer.pack()
    playAgain = Button(endFrame, text='Play again', command=player.__init__)
    playAgain.pack()
    spacer2 = Label(endFrame, text='')
    spacer2.pack()
    quitButton = Button(endFrame, text='Quit', command=finish_up)
    quitButton.pack()
    if text == 'You win!':
        stats['Wins'] += 1
    elif text == 'You lose!':
        stats['Losses'] += 1
    spacer3 = Label(endFrame, text='', width=20)
    spacer3.pack()
    statsLabel = Label(endFrame, text='Stats:')
    statsLabel.pack()
    winsLabel = Label(endFrame, text='Wins: ' + str(stats['Wins']))
    winsLabel.pack()
    lossesLabel = Label(endFrame, text='Losses: ' + str(stats['Losses']))
    lossesLabel.pack()

ships = {
    "Carrier": 5,
    "Battleship": 4,
    "Cruiser": 3,
    "Submarine": 3,
    "Destroyer": 2
    }
root = Tk()


class Human:

    def __init__(self):
        self.difficulty = 2
        self.main_menu()
        self.shipList = []
        for key in ships:
            self.shipList.append(key)
        self.placing = 0
        self.shipNum = 0
        global turn
        turn = 1
        self.ship_locs = {}

    def main_menu(self):  # Builds the starting game menu
        build_root()
        title = Label(root, text='Battleship!', height=3, width=20)
        title.pack()
        spacer = Label(root, text='')
        spacer.pack()
        begin = Button(root, text='Start Game', command=self.choose_difficulty, height=2)
        begin.pack()

    def set_diff(self, choice):  # Sets the difficulty chosen by the player and resets the buttons
        self.difficulty = choice
        global comp
        if self.difficulty == 1:
            comp = AI()
        elif self.difficulty == 2:
            comp = AI_two()
        elif self.difficulty == 3:
            comp = AI_three()
        if self.easyButton.cget('relief') == SUNKEN:
            self.easyButton.configure(relief=RAISED, state=NORMAL)
        elif self.medButton.cget('relief') == SUNKEN:
            self.medButton.configure(relief=RAISED, state=NORMAL)
        elif self.hardButton.cget('relief') == SUNKEN:
            self.hardButton.configure(relief=RAISED, state=NORMAL)
        if choice == 1:
            self.easyButton.configure(relief=SUNKEN, state=DISABLED)
        elif choice == 2:
            self.medButton.configure(relief=SUNKEN, state=DISABLED)
        elif choice == 3:
            self.hardButton.configure(relief=SUNKEN, state=DISABLED)

    def choose_difficulty(self):  # Allows the player to choose the difficulty
        build_root()
        chooseLabel = Label(text='Choose the difficulty')
        chooseLabel.grid(row=0, column=1)
        spacer = Label(root, text='')
        spacer.grid(row=1, columnspan=3, column=1)
        self.easyButton = Button(root, text='Really Easy', command=lambda j=1: self.set_diff(j))
        self.easyButton.grid(row=2, column=0)
        self.medButton = Button(root, text='Intermediate', command=lambda j=2: self.set_diff(j),
                                relief=SUNKEN, state=DISABLED)
        self.medButton.grid(row=2, column=1)
        self.hardButton = Button(root, text='A lil\' harder', command=lambda j=3: self.set_diff(j))
        self.hardButton.grid(row=2, column=2)
        spacer2 = Label(root, text='')
        spacer2.grid(row=3, columnspan=3)
        continueButton = Button(root, text='Next', command=self.build_player_board)
        continueButton.grid(row=4, column=1)
        global comp
        comp = AI_two()

    def reset_placement(self):
        self.placing = 0
        self.shipNum = 0
        self.infoFrame.destroy()
        self.build_player_board()

    def build_player_board(self):  # Allows the player to build their own board
        if self.placing == 0:
            build_root()
            self.titleFrame = Frame(root)
            self.titleFrame.grid(row=0,columnspan=10)
            self.boardFrame = Frame(root)
            self.boardFrame.grid(row=2)
            title = Label(self.titleFrame, text='You will now build your board', height=3)
            title.grid(row=0, columnspan=100)
            self.infoFrame = Frame(root)
            self.infoFrame.grid(row=0, rowspan=10, column=10)
            self.player_list = []
            self.player_list = self.build_board_base(self.boardFrame)
            self.placing = 1
            self.player_board = []
            for i in range(100):
                self.player_board.append(0)
        if self.placing == 1:
            if self.shipNum < 5:
                self.clear_info_frame()
                self.currentShipLabel = Label(self.infoFrame, text='Place your ' + self.shipList[self.shipNum],
                                              width=30)
                self.currentShipLabel.pack()
                self.shipLength = ships[self.shipList[self.shipNum]]
                self.shipLengthLabel = Label(self.infoFrame, text='Length: ' + str(self.shipLength))
                self.shipLengthLabel.pack()
                self.spacer = Label(self.infoFrame, text='')
                self.spacer.pack()
            if self.shipNum >= 5:
                for i in range(100):
                    self.player_list[i].configure(state=DISABLED)
                self.clear_info_frame()
                continueButton = Button(self.infoFrame, text='Let\'s Play!', command=self.start_game)
                continueButton.pack()
                spacer3 = Label(self.infoFrame, text='', width=30)
                spacer3.pack()
                restartButton = Button(self.infoFrame, text='Reset Ships', command=self.reset_placement)
                restartButton.pack()

    def clear_info_frame(self):
        try:
            self.upButton.destroy()
        except (AttributeError, TclError):
            pass
        try:
            self.downButton.destroy()
        except (AttributeError, TclError):
            pass
        try:
            self.leftButton.destroy()
        except (AttributeError, TclError):
            pass
        try:
            self.rightButton.destroy()
        except (AttributeError, TclError):
            pass
        try:
            self.currentShipLabel.destroy()
        except (AttributeError, TclError):
            pass
        try:
            self.shipLengthLabel.destroy()
        except (AttributeError, TclError):
            pass
        try:
            self.spacer.destroy()
        except (AttributeError, TclError):
            pass

    def place_player_ships(self, direction, ind, length):
        # Places the player ships on the visual and computer-tracked board
        if direction == 1:  # Up
            for i in range(length):
                self.player_board[ind - 10 * i - 1] = self.shipNum + 1
                if self.placing != 2:
                    self.player_list[ind - 10 * i - 1].configure(bg='gray54')
                elif self.placing == 2:
                    self.player_list[ind - 10 * i - 1].configure(bg='red')
        elif direction == 2:  # Down
            for i in range(length):
                self.player_board[ind + 10 * i - 1] = self.shipNum + 1
                if self.placing != 2:
                    self.player_list[ind + 10 * i - 1].configure(bg='gray54')
                elif self.placing == 2:
                    self.player_list[ind + 10 * i - 1].configure(bg='red')
        elif direction == 3:  # Left
            for i in range(length):
                self.player_board[ind - i - 1] = self.shipNum + 1
                if self.placing != 2:
                    self.player_list[ind - i - 1].configure(bg='gray54')
                elif self.placing == 2:
                    self.player_list[ind - i - 1].configure(bg='red')
        elif direction == 4:  # Right
            for i in range(length):
                self.player_board[ind + i - 1] = self.shipNum + 1
                if self.placing != 2:
                    self.player_list[ind + i - 1].configure(bg='gray54')
                elif self.placing == 2:
                    self.player_list[ind + i - 1].configure(bg='red')
        self.shipNum += 1
        temp = self.shipNum
        if self.placing != 2:
            try:
                self.prevButton.configure(relief=RAISED, state=NORMAL)
            except (AttributeError, TclError):
                pass
            self.ship_locs[temp] = [direction, ind, length]
        self.build_player_board()

    def build_board_base(self, frame):  # Builds the base of 100 buttons and outputs them as a list
        button_list = []
        q = 0
        for i in range(10):
            for j in range(10):
                q += 1
                button = Button(frame, width=5, height=2,
                                command=lambda n=q: self.get_chosen_spot(n), bg='DeepSkyBlue2')
                button_list.append(button)
                button.grid(row=i + 1, column=j)
        return button_list

    def get_chosen_spot(self, ind):  # Gets the index of the button chosen by the player
        self.ind = ind
        if self.placing == 1:
            self.buttonClicked = self.player_list[ind-1]
            self.buttonClicked.configure(relief=SUNKEN, state=DISABLED)
            try:
                self.prevButton.configure(relief=RAISED, state=NORMAL)
            except (AttributeError, TclError):
                pass
        elif self.placing == 2:
            self.buttonClicked = comp.computer_button_list[ind-1]
            self.player_turn()

        self.prevButton = self.buttonClicked
        if self.placing == 1:
            try:
                self.upButton.destroy()
            except (AttributeError, TclError):
                pass
            try:
                self.downButton.destroy()
            except (AttributeError, TclError):
                pass
            try:
                self.leftButton.destroy()
            except (AttributeError, TclError):
                pass
            try:
                self.rightButton.destroy()
            except (AttributeError, TclError):
                pass
            if ind > (self.shipLength-1)*10: # Up
                self.temp = 0
                for i in range(self.shipLength):
                    if self.player_board[ind - 10*i - 1] != 0:
                        self.temp = 1
                        break
                if self.temp == 0:
                    self.upButton = Button(self.infoFrame, text='Up',
                                           command=lambda j=1: self.place_player_ships(j, ind, self.shipLength))
                    self.upButton.pack()
            if ind % 10 >= self.shipLength or ind % 10 == 0:  # Left
                self.temp = 0
                for i in range(self.shipLength):
                    if self.player_board[ind - i - 1] != 0:
                        self.temp = 1
                        break
                if self.temp == 0:
                    self.leftButton = Button(self.infoFrame, text='Left',
                                             command=lambda j=3: self.place_player_ships(j, ind, self.shipLength))
                    self.leftButton.pack()
            if ind <= 100 - (self.shipLength-1)*10:  # Down
                self.temp = 0
                for i in range(self.shipLength):
                    if self.player_board[ind + 10*i - 1] != 0:
                        self.temp = 1
                        break
                if self.temp == 0:
                    self.downButton = Button(self.infoFrame, text='Down',
                                             command=lambda j=2: self.place_player_ships(j, ind, self.shipLength))
                    self.downButton.pack()
            if 11 - (ind % 10) >= self.shipLength and ind % 10 != 0:  # Right
                self.temp = 0
                for i in range(self.shipLength):
                    if self.player_board[ind + i - 1] != 0:
                        self.temp = 1
                        break
                if self.temp == 0:
                    self.rightButton = Button(self.infoFrame, text='Right',
                                              command=lambda j=4: self.place_player_ships(j, ind, self.shipLength))
                    self.rightButton.pack()

    def start_game(self):  # Sets up the boards for each the player and the computer (final stage, actual game)
        self.placing = 2
        self.titleFrame.destroy()
        self.infoFrame.destroy()
        playerInfoFrame = Frame(root)
        playerInfoFrame.grid(row=2, column=1)
        ttk.Separator(root, orient='horizontal').grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.boardFrame.grid(row=2)
        playerBoardLabel = Label(self.boardFrame, text='Your Board:', height=2)
        playerBoardLabel.grid(row=0, columnspan=10)
        shipsLeftLabel = Label(playerInfoFrame, text='Player Ships Left:', width=22)
        shipsLeftLabel.pack()
        self.shipNum = 7
        self.shipLabelList = []
        for key in self.shipList:
            ship = Label(playerInfoFrame, text=key)
            self.shipLabelList.append(ship)
            ship.pack()

        global comp
        comp.start_game()

        q = 0
        for i in range(10):
            for j in range(10):
                self.player_list[q].grid(row=i+1, column=j)
                self.player_list[q].configure(relief=RAISED, state=DISABLED)
                q += 1

    def player_turn(self):
        global turn
        if turn == 1:
            if comp.computer_board[self.ind-1] != 0 and comp.computer_board[self.ind-1] != 6:
                self.buttonClicked.configure(bg='Orange')
                comp.computer_board[self.ind-1] = 6
            else:
                self.buttonClicked.configure(bg='white')
                comp.computer_board[self.ind-1] = 7
            self.end_turn()

    def end_turn(self):
        global turn
        turn = 2
        for i in range(5):
            try:
                if i+1 not in comp.computer_board:
                    comp.shipLabelList[i].destroy()
                    comp.place_ship(comp.ship_locs[i+1][0], comp.ship_locs[i+1][1], comp.ship_locs[i+1][2])
                    if i == 0:
                        comp.shipList.remove('Submarine')
                    elif i == 1:
                        comp.shipList.remove('Battleship')
                    elif i == 2:
                        comp.shipList.remove('Carrier')
                    elif i == 3:
                        comp.shipList.remove('Destroyer')
                    elif i == 4:
                        comp.shipList.remove('Cruiser')
            except (IndexError, ValueError):
                pass
        if not comp.shipList:
            end_game('You win!')
        else:
            comp.computer_turn()


class AI:

    def __init__(self):
        self.computer_board = []
        for i in range(100):
            self.computer_board.append(0)
        self.shot_location = 0
        self.shipNum = 0
        self.shipList = []
        for key in ships:
            self.shipList.append(key)
        self.shot_list = []
        self.targeting = 0
        self.shot_direction = -1
        self.attempt = 1
        self.ship_locs = {}
        self.hit_loc = -1
        self.hit_loc_iter = 0

    def start_game(self):
        computerFrame = Frame(root)
        self.computer_button_list = Human.build_board_base(player, computerFrame)
        computerFrame.grid(row=0)
        computerInfoFrame = Frame(root)
        computerInfoFrame.grid(row=0, rowspan=2, column=1)
        computerBoardLabel = Label(computerFrame, text='Computer\'s Board:', height=2)
        computerBoardLabel.grid(row=0, columnspan=10)
        self.shipLabelList = []
        shipsLeftLabel = Label(computerInfoFrame, text='Computer Ships Left:')
        shipsLeftLabel.pack()
        for key in self.shipList:
            ship = Label(computerInfoFrame, text=key)
            self.shipLabelList.append(ship)
            ship.pack()
        self.build_board()

    def place_ship(self, direction, ind, length):
        if direction == 1:  # Up
            for i in range(length):
                self.computer_board[ind - 10*i - 1] = self.shipNum + 1
                if self.shipNum >= 5:
                    self.computer_button_list[ind - 10 * i - 1].configure(bg='red')
        elif direction == 2:  # Down
            for i in range(length):
                self.computer_board[ind + 10*i - 1] = self.shipNum + 1
                if self.shipNum >= 5:
                    self.computer_button_list[ind + 10 * i - 1].configure(bg='red')
        elif direction == 3:  # Left
            for i in range(length):
                self.computer_board[ind - i - 1] = self.shipNum + 1
                if self.shipNum >= 5:
                    self.computer_button_list[ind - i - 1].configure(bg='red')
        elif direction == 4:  # Right
            for i in range(length):
                self.computer_board[ind + i - 1] = self.shipNum + 1
                if self.shipNum >= 5:
                    self.computer_button_list[ind + i - 1].configure(bg='red')
        self.shipNum += 1
        self.ship_locs[self.shipNum] = [direction, ind, length]
        self.build_board()

    def build_board(self):
        if self.shipNum < 5:
            shipLength = ships[self.shipList[self.shipNum]]
            ind = shoot()
            dir_ops = []
            if ind > (shipLength - 1) * 10:  # Up
                temp = 0
                for i in range(shipLength):
                    if self.computer_board[ind - 10 * i - 1] != 0:
                        temp = 1
                        break
                if temp == 0:
                    dir_ops.append(1)
            if ind % 10 >= shipLength or ind % 10 == 0:  # Left
                temp = 0
                for i in range(shipLength):
                    if self.computer_board[ind - i - 1] != 0:
                        temp = 1
                        break
                if temp == 0:
                    dir_ops.append(3)
            if ind < (100 - (shipLength - 1) * 10):  # Down
                temp = 0
                for i in range(shipLength):
                    if self.computer_board[ind + 10 * i - 1] != 0:
                        temp = 1
                        break
                if temp == 0:
                    dir_ops.append(2)
            if 11 - (ind % 10) >= shipLength and ind % 10 != 0:  # Right
                temp = 0
                for i in range(shipLength):
                    if self.computer_board[ind + i - 1] != 0:
                        temp = 1
                        break
                if temp == 0:
                    dir_ops.append(4)
            if not dir_ops:
                self.build_board()
            else:
                direction = dir_ops[randint(1, len(dir_ops))-1]
                self.place_ship(direction, ind, shipLength)

    def random_shooting(self):
        shot = shoot()
        while shot in self.shot_list:
            shot = shoot()
        return shot

    def shot_result(self, shot):
        self.shot_list.append(shot)
        self.hit_loc_iter = 0
        if 6 > player.player_board[shot] > 0:
            player.player_board[shot] = 6
            player.player_list[shot].configure(bg='Orange')
            self.hit_loc = shot
            return True
        else:
            player.player_list[shot].configure(bg='white')
            player.player_board[shot] = 7
            return False

    def computer_turn(self):
        global turn
        if turn == 2:
            for i in range(100):
                self.computer_button_list[i].configure(state=DISABLED)
            shot = self.random_shooting()
            self.shot_result(shot)
            self.end_turn()

    def end_turn(self):
        global turn
        turn = 1
        for i in range(100):
            if not player.shipList or not comp.shipList:
                    self.computer_button_list[i].configure(state=DISABLED)
            elif self.computer_button_list[i].cget('bg') == 'DeepSkyBlue2':
                self.computer_button_list[i].configure(state=NORMAL)
        for i in range(5):
            try:
                if i+1 not in player.player_board:
                    player.shipLabelList[i].destroy()
                    player.place_player_ships(player.ship_locs[i+1][0],
                                              player.ship_locs[i+1][1], player.ship_locs[i+1][2])
                    if i == 0:
                        player.shipList.remove('Submarine')
                    elif i == 1:
                        player.shipList.remove('Battleship')
                    elif i == 2:
                        player.shipList.remove('Carrier')
                    elif i == 3:
                        player.shipList.remove('Destroyer')
                    elif i == 4:
                        player.shipList.remove('Cruiser')
                    self.targeting = 0
            except (IndexError, ValueError):
                pass
        if not player.shipList:
            end_game('You lose!')


class AI_two(AI):

    def __init__(self):
        AI.__init__(self)

    def computer_turn(self):
        global turn
        hits = [i for i, x in enumerate(player.player_board) if x == 6]  # Gets a list of every hit on the board
        if turn == 2:
            for i in range(100):
                self.computer_button_list[i].configure(state=DISABLED)
            if self.targeting == 0:  # Random firing
                shot = self.random_shooting()
                if 6 in player.player_board:  # Checks if there are unsunk hits on the board
                    self.hit_loc = hits[self.hit_loc_iter]
                    self.targeting = 1
                    self.computer_turn()
                    self.attempt = 1
                    return
                if self.shot_result(shot):
                    self.targeting = 1
                    self.hit_loc_init = shot
            elif self.targeting == 1:  # Trying to find the second shot after a hit on a ship
                shot_ops = []
                try:
                    if player.player_board[self.hit_loc - 10] < 6 and self.hit_loc > 9:  # Up
                        shot_ops.append(1)
                except IndexError:
                    pass
                try:
                    if player.player_board[self.hit_loc + 10] < 6 and self.hit_loc < 90:  # Down
                        shot_ops.append(2)
                except IndexError:
                    pass
                try:
                    if player.player_board[self.hit_loc - 1] < 6 and self.hit_loc % 10 != 0:  # Left
                        shot_ops.append(3)
                except IndexError:
                    pass
                try:
                    if (player.player_board[self.hit_loc + 1] < 6 and self.hit_loc % 10 != 9) or \
                            (player.player_board[self.hit_loc + 1] < 6 and self.hit_loc == 0):  # Right
                        shot_ops.append(4)
                except IndexError:
                    pass
                if not shot_ops:
                    self.targeting = 0
                    self.hit_loc_iter += 1
                    self.computer_turn()
                    return
                self.shot_direction = shot_ops[randint(0, len(shot_ops)) - 1]
                if self.shot_direction == 1:
                    shot = self.hit_loc - 10
                elif self.shot_direction == 2:
                    shot = self.hit_loc + 10
                elif self.shot_direction == 3:
                    shot = self.hit_loc - 1
                elif self.shot_direction == 4:
                    shot = self.hit_loc + 1
                if self.shot_result(shot):
                    self.targeting = 2
            elif self.targeting == 2:  # Continuing along the line of two consecutive hits on a ship
                # ( 1 H H 1 1 ) --> ( 1 H H H 1 ) --> ( 1 H H H H )
                temp = 0
                try:
                    if self.shot_direction == 1:
                        if self.hit_loc > 9:
                            shot = self.hit_loc - 10
                        else:
                            temp = 1
                    elif self.shot_direction == 2:
                        if self.hit_loc < 90:
                            shot = self.hit_loc + 10
                        else:
                            temp = 1
                    elif self.shot_direction == 3:
                        if self.hit_loc % 10 != 0:
                            shot = self.hit_loc - 1
                        else:
                            temp = 1
                    elif self.shot_direction == 4:
                        if self.hit_loc % 10 != 9:
                            shot = self.hit_loc + 1
                        else:
                            temp = 1
                    try:
                        if shot in self.shot_list:
                            temp = 1
                    except UnboundLocalError:
                        pass
                    if temp == 1:
                        if self.attempt == 1:
                            self.targeting = 3
                        elif self.attempt > 1:
                            self.targeting = 0
                        self.attempt = 1
                        self.computer_turn()
                        return
                    if self.shot_result(shot):
                        self.targeting = 2
                    elif not self.shot_result(shot):
                        if self.attempt == 1:
                            self.targeting = 3
                        elif self.attempt > 1:
                            self.targeting = 0
                    self.attempt = 1
                except IndexError:
                    self.targeting = 0
            elif self.targeting == 3:
                # Continuing along the line of two consecutive hits on a ship,
                # but in the opposite direction if missed and not sunk
                # ( 1 H H 0 0 ) --> ( 1 H H X 0 ) --> ( H H H X 0 )
                self.hit_loc = self.hit_loc_init
                if self.shot_direction == 1:
                    self.shot_direction = 2
                elif self.shot_direction == 2:
                    self.shot_direction = 1
                elif self.shot_direction == 3:
                    self.shot_direction = 4
                elif self.shot_direction == 4:
                    self.shot_direction = 3
                self.targeting = 2
                self.attempt += 1
                self.computer_turn()
                return
            self.end_turn()


class AI_three(AI_two):

    def __init__(self):
        AI.__init__(self)

    def random_shooting(self):
        if len(player.shipList) == 5:
            shot = shoot()
            while shot in self.shot_list:
                shot = shoot()
            return shot
        elif len(player.shipList) <= 4:
            dir_ops = []
            rem_lengths = []
            for i in range(len(player.shipList)):
                rem_lengths.append(ships[player.shipList[i]])
            length = max(rem_lengths)
            q = 0
            shots_left = 100-len(self.shot_list)
            min_accept = 4
            shots_tried = []
            while not len(dir_ops) == min_accept or shot in self.shot_list or player.player_board[shot] > 6:
                shot = shoot()
                while shot in shots_tried or shot in self.shot_list:
                    shot = shoot()
                if shot not in shots_tried:
                    shots_tried.append(shot)
                dir_ops = []
                if shot > (length - 1) * 10:  # Up
                    temp = 0
                    for i in range(length):
                        try:
                            if player.player_board[shot - 10 * i] > 6:
                                temp = 1
                                break
                        except IndexError:
                            temp = 1
                            break
                    if temp == 0:
                        dir_ops.append(1)
                if (shot + 1) % 10 >= length and shot % 10 != 0:  # Left
                    temp = 0
                    for i in range(length):
                        try:
                            if player.player_board[shot - i] > 6:
                                temp = 1
                                break
                        except IndexError:
                            temp = 1
                            break
                    if temp == 0:
                        dir_ops.append(3)
                if shot <= 100 - (length - 1) * 10:  # Down
                    temp = 0
                    for i in range(length):
                        try:
                            if player.player_board[shot + 10 * i] > 6:
                                temp = 1
                                break
                        except IndexError:
                            temp = 1
                            break
                    if temp == 0:
                        dir_ops.append(2)
                if 10 - (shot % 10) >= length and shot % 10 != 9:  # Right
                    temp = 0
                    for i in range(length):
                        try:
                            if player.player_board[shot + i] > 6:
                                temp = 1
                                break
                        except IndexError:
                            temp = 1
                            break
                    if temp == 0:
                        dir_ops.append(4)
                q += 1
                if q >= shots_left:
                    q = 0
                    min_accept -= 1
                    shots_tried = []
                if min_accept <= 0:
                    return
            return shot

player = Human()
comp = AI_two()

root.mainloop()

# Reflections:
    # Again I really don't feel like I used classes properly.
    # The functions I created are much too dependent on the classes (it uses specific instance names...)
    # Example: I have a system that randomly creates a board for the computer, but I would have to do a lot of
        # modification to have it do the same exact process for the player, when I could have an outside function
        # to simply do so for both without being in a class at all
    # Proper utilization might mean (with a little modification) I could have pit two AI's against each other,
        # but instead I tied the game process to the classes, instead of having the classes merely play the game.

    # I could have properly isolated the classes and game with a lot more returns and
        # inputs in functions outside of the classes, like where the visuals are created
        # (they don't need to be tied to the class, just its data)
        # end_game(text) is the perfect example of what I should have done more of

    # I don't feel that the code I wrote is bad or inefficient, but it not modular or modifiable much at all
    # The AI itself I think runs as smoothly as I could want. It's fast enough to seem like it doesn't take time to
        # decide on a move, but I can't say it's the most efficient

    # I do feel much more familiar with functions and having them interact with each other.
    # I very much need to do more inputs/returns to minimize globals or instance variables

    # Also, the internet said not to use import *, so from now on don't do that (good reasoning)

    # PyCharm is helping a bit to make my code more pythonic i.e. if not x: rather than if x == [] and readable
