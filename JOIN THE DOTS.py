#Author - Ayush D. Jariwala
#Avantika University
#AU20B1009



#importing everything from tkinter
from tkinter import *
import numpy as np

size_of_board = 700
number_of_dots = 4
dot_size = (size_of_board / 3 - size_of_board / 8) / 2


#Colors for both the players
dot_color = '#FFFFEF'
player1_color = '#00FF00'
player1_color_light = '#B3FF9F'
player2_color = '#FF34EA'
player2_color_light = '#FFC2D3'
Orange_color = '#FF9F91'

#Dot and edge widths
dot_width = 0.25 * size_of_board / number_of_dots
edge_width = 0.1 * size_of_board / number_of_dots

#Distance between two dots
distance_between_dots = size_of_board / (number_of_dots)

#Making class for the game
class JoinThe_Dots():

    # Initializing functions

    def __init__(self):

        self.window = Tk()
        self.window.title('JOIN THE DOTS')
        self.window.minsize(700, 700)
        self.window.maxsize(700, 700)
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board, bg='black')
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click) #Click input and binding whole window
        self.player1_starts = True
        self.refresh_board()
        self.play_again()

    def play_again(self):

        #Making dots/circles
        self.refresh_board()
        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))

        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts #input and store
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()

    def mainloop(self):

        self.window.mainloop()


    # Logical Functions
    # The modules required to carry out game logic and functions


    def grid_occupied(self, logical_position, type):

        r = logical_position[0]  #row = r
        c = logical_position[1]  #column = c
        occupied = True

        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False

        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False

        return occupied

    def grid_to_logical_position(self, grid_position):

        grid_position = np.array(grid_position)
        position = (grid_position - distance_between_dots / 4) // (distance_between_dots / 2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:

            r = int((position[0] - 1) // 2)
            c = int(position[1] // 2)
            logical_position = [r, c]
            type = 'row'

        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:

            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    #Creating shading the box function which will be called later for shading the box for each players after they got 1 - 1 complete grid
    def shade_box(self, box, color):

        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width / 2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width / 2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def mark_box(self):

        #Finding the indices of array elements that are non-zero
        boxes = np.argwhere(self.board_status == -4)
        for box in boxes:

            if list(box) not in self.already_marked_boxes and list(box) != []:

                self.already_marked_boxes.append(list(box))
                color = player1_color_light
                self.shade_box(box, color) #Shading the non-zero box for player 1

        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:

            if list(box) not in self.already_marked_boxes and list(box) != []:

                self.already_marked_boxes.append(list(box))
                color = player2_color_light
                self.shade_box(box, color)  #Shading the non-zero box for player 2

    def update_board(self, type, logical_position): #updating the grid board.

        r = logical_position[0]
        c = logical_position[1]
        val = 1
        if self.player1_turn:

            val = - 1

        if c < (number_of_dots - 1) and r < (number_of_dots - 1):

            self.board_status[c][r] += val

        if type == 'row':

            self.row_status[c][r] = 1
            if c >= 1:

                self.board_status[c - 1][r] += val

        elif type == 'col':
            self.col_status[c][r] = 1

            if r >= 1:
                self.board_status[c][r - 1] += val




    # Drawing Functions--
    # The modules required to draw required game based object on canvas


    def make_edge(self, type, logical_position):

        #This will help in making the lines between two dots

        if type == 'row':

            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x + distance_between_dots
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y

        elif type == 'col':

            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x

        #Colours of the line for both the players
        if self.player1_turn:
            color = player1_color

        else:
            color = player2_color
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=edge_width) #This will create lines for the players of their colours.

    def display_turn_text(self):

        #giving both player chances one by one
        text = 'Next turn: '

        if self.player1_turn:
            text += 'Player1'
            color = player1_color

        else:
            text += 'Player2'
            color = player2_color

        #Printing the turn texts for the players on the canavas
        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5 * len(text),
                                                       size_of_board - distance_between_dots / 8,
                                                       font="cmr 15 bold", text=text, fill=color)


    def display_gameover(self):

        #Calculating scores for both the players
        player1_score = len(np.argwhere(self.board_status == -4))
        player2_score = len(np.argwhere(self.board_status == 4))

        #printing/announcing winner based on the score using conditions
        if player1_score > player2_score:

            text = 'Winner :    Player 1 '
            color = player1_color

        elif player2_score > player1_score:

            text = 'Winner :    Player 2 '
            color = player2_color

        else:

            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")  #Erasing whole screen and displaying the new one
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 40 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 20 bold", fill=Orange_color,
                                text=score_text)

        score_text = 'Player 1 : ' + str(player1_score) + '\n'  #displaying the scores
        score_text += 'Player 2 : ' + str(player2_score) + '\n'

        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 15 bold", fill=Orange_color,
                                text=score_text)
        self.reset_board = True

        #starting the game again by taking inout in form of mouse click
        score_text = 'Click any where on the screen to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)


    def is_gameover(self):

        return (self.row_status == 1).all() and (self.col_status == 1).all()

    #Function for click to start game again
    def click(self, event):

        if not self.reset_board:

            grid_position = [event.x, event.y]
            logical_positon, valid_input = self.grid_to_logical_position(grid_position)

            if valid_input and not self.grid_occupied(logical_positon, valid_input):

                self.update_board(valid_input, logical_positon)
                self.make_edge(valid_input, logical_positon)
                self.mark_box()
                self.refresh_board()
                self.player1_turn = not self.player1_turn

                if self.is_gameover():

                    self.display_gameover()

                else:
                    self.display_turn_text()

        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False




    #Function for refreshing the grid board
    def refresh_board(self):

        for i in range(number_of_dots):

            #Will create lines
            x = i * distance_between_dots + distance_between_dots / 2
            self.canvas.create_line(x, distance_between_dots / 2, x,
                                    size_of_board - distance_between_dots / 2,
                                    fill='gray', dash=(2, 2))
            self.canvas.create_line(distance_between_dots / 2, x,
                                    size_of_board - distance_between_dots / 2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(number_of_dots):

            for j in range(number_of_dots):

                start_x = i * distance_between_dots + distance_between_dots / 2
                end_x = j * distance_between_dots + distance_between_dots / 2
                self.canvas.create_oval(start_x - dot_width / 2, end_x - dot_width / 2, start_x + dot_width / 2,
                                        end_x + dot_width / 2, fill=dot_color,
                                        outline=dot_color)




game_instance = JoinThe_Dots()
game_instance.mainloop()