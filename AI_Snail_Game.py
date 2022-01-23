from re import I
import arcade
import arcade.gui
from arcade.color import WHITE_SMOKE

import math
import os

# os.chdir(r"C:\Users\Z\OneDrive\Desktop\LAB_2_AI")
bg_texture = arcade.load_texture("Game_bg.jpg")  #
audio_1 = arcade.sound.load_sound("1.wav")  # loading sounds for the every successful move
main_audio = arcade.sound.load_sound("main.wav")  # background sound loaded
audio_1f = arcade.sound.load_sound("1fool.wav")  # sound for wrong moves

WIDTH = 1100  # the size of the window when it is minimized
HEIGHT = 700
scale = 0.3


# *************************************** Menu View Class ***************************************

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.main = arcade.sound.play_sound(main_audio, 1, 0,
                                            True)  # playing sound in continuous loop until move to next screen

        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="Start Game", height=100, width=400)
        menu_button = arcade.gui.UIFlatButton(text="Menu Game", height=100, width=400)
        quit_button = arcade.gui.UIFlatButton(text="Quit Game", height=100, width=400)

        start_button.on_click = self.on_click_start  # adding on click action behaviour to all three buttons
        menu_button.on_click = self.on_click_menu
        quit_button.on_click = self.on_click_quit

        # Loaded all the buttons in V_BOX.
        self.v_box.add(start_button.with_space_around(bottom=20))
        self.v_box.add(menu_button.with_space_around(bottom=20))
        self.v_box.add(quit_button.with_space_around(bottom=20))

        self.uimanager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))
        # Adding button in our uimanager

    # event is important because it is carrying the information of button.

    def on_click_start(self, event):  # when the start button clicked game start
        arcade.sound.stop_sound(self.main)
        self.uimanager.disable()
        game_view = Welcome()
        self.window.show_view(game_view)

    def on_click_menu(self, event):  # when the menu button clicked menu window is called
        arcade.sound.stop_sound(self.main)
        self.uimanager.disable()
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)

    def on_click_quit(self, event):  # when the menu button clicked we exit the arcade
        arcade.sound.stop_sound(self.main)
        arcade.exit()

    def on_show(self):  # Called when this view is shown and if window dispatches a on_show event.
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):  # Called when this view should draw
        arcade.start_render()
        background = arcade.load_texture("Main_bg.jpg")

        arcade.draw_scaled_texture_rectangle(690, 350, background, 1.35, 0)
        self.uimanager.draw()

    def on_key_press(self, symbol, modifier):  # this key press function minimized the screen
        if symbol == arcade.key.F:
            self.window.set_fullscreen(not self.window.fullscreen)  # this will exist the full screen mode


# *************************************** Instruction View Class ***************************************
class InstructionView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        background = arcade.load_texture("Menu_bg.jpg")
        arcade.draw_scaled_texture_rectangle(690, 350, background, 1.70, 0)
        arcade.draw_text("Instructions", 780, 680, arcade.color.BLACK, 30)
        arcade.draw_text("1) It is a two players game on (10x10) size grid.", 700, 630, arcade.color.BLACK,
                         15)  # this is the text which are the set of the rules
        arcade.draw_text("2) UP, DOWN, LEFT and RIGHT keys are used to move ", 700, 600, arcade.color.BLACK,
                         15)  # written on the screen
        arcade.draw_text("   sprite in respective direction 'Box'.", 700, 570, arcade.color.BLACK, 15)
        arcade.draw_text("3) Whenever, a sprite moves from one Box to another ", 700, 540, arcade.color.BLACK, 15)
        arcade.draw_text("   blank Box, it leaves a splash behind.", 700, 510, arcade.color.BLACK, 15)
        arcade.draw_text("4) If sprite moves on filled Box (splash), it will slides on the ", 700, 480,
                         arcade.color.BLACK, 15)
        arcade.draw_text("   grid until it reach a blank Box in respective direction.", 700, 450, arcade.color.BLACK,
                         15)
        arcade.draw_text("5) Sprite will lose its turn if it tries to move on 2nd player's ", 700, 420,
                         arcade.color.BLACK, 15)
        arcade.draw_text("   splash or cross the grid size.", 700, 390, arcade.color.BLACK, 15)
        arcade.draw_text("Winning Criteria", 190, 330, arcade.color.BLACK, 30)
        arcade.draw_text(" Maximum number of splash leads a Sprite ", 120, 280, arcade.color.BLACK, 15)
        arcade.draw_text("  to Win the game.", 120, 250, arcade.color.BLACK, 15)

        arcade.draw_text("Click Anywhere To Start", 80, 550, arcade.color.BLACK, 25, 270, "center", "arial", True, True,
                         "left", "baseline", True)

    def on_key_press(self, symbol, modifier):  # same as in the menu class this function use to minimize the window
        if symbol == arcade.key.F:
            self.window.set_fullscreen(not self.window.fullscreen)

    def on_mouse_press(self, x: float, y: float, button: int,
                       modifiers: int):  # on the screen any where when the mouse button is presseed game start
        gameview = Welcome()
        self.window.show_view(gameview)


# ***************************************  Main Game Class  ***************************************

class Welcome(arcade.View):
    def __init__(self):  # InstructionView(False)
        super().__init__()
        self.array = [[0 for i in range(10)] for j in range(10)]  # creating 2d array having all entries 0
        self.turn = "1"
        self.move = 0
        self.draw_counter = 0

        self.player_score1 = 0  # setting the player scores
        self.player_score2 = 0

        self.player_list = arcade.SpriteList()  # list having all the properties which a sprite can have
        self.splash_list1 = arcade.SpriteList()
        self.splash_list2 = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        self.player_sprite1 = arcade.Sprite("human_sprite.jpg", .49)  # making the sprite1 player1
        self.player_sprite1.center_x = 235  # setting the x axis
        self.player_sprite1.center_y = 35  # setting  the y axis

        self.player_sprite2 = arcade.Sprite("boot_sprite.jpg", .32)  # making the sprite2 player2
        self.player_sprite2.center_x = 865  # setting the x axis
        self.player_sprite2.center_y = 665  # setting  the y axis

        self.player_sprite3 = arcade.Sprite("human_sprite.jpg", .49)  # static sprites
        self.player_sprite3.center_x = 100
        self.player_sprite3.center_y = 400

        self.player_sprite4 = arcade.Sprite("boot_sprite.jpg", .32)  # static sprites
        self.player_sprite4.center_x = 1000
        self.player_sprite4.center_y = 400

        self.player_list.append(self.player_sprite1)
        self.player_list.append(self.player_sprite2)
        self.player_list.append(self.player_sprite3)
        self.player_list.append(self.player_sprite4)

    def on_show(self):
        arcade.set_background_color(arcade.color.SEA_GREEN)

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

    def on_draw(self):

        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1400, 800, bg_texture)  # rectangle covering the whole screen

        for i in range(200, 901, 70):  # drawing grid
            arcade.draw_line(i, 0, i, 700, arcade.color.BLACK, 2)
        for j in range(0, 901, 70):
            arcade.draw_line(200, j, 901, j, arcade.color.BLACK, 2)

        arcade.draw_rectangle_filled(100, 350, 150, 200, WHITE_SMOKE)  # drawing rectangles inside the big rectangles
        arcade.draw_rectangle_filled(1000, 350, 150, 200, WHITE_SMOKE)

        PointList = ((908, 700), (1092, 700), (908, 0), (1092, 0),

                     (910, 0), (910, 700), (1090, 0), (1090, 700),

                     (8, 0), (192, 0), (8, 700), (192, 700),

                     (10, 0), (10, 700), (190, 0), (190, 700),

                     (23, 250), (177, 250), (23, 450), (177, 450),

                     (25, 250), (25, 450), (175, 250), (175, 450),

                     (923, 250), (1077, 250), (923, 450), (1077, 450),

                     (925, 250), (925, 450), (1075, 250), (1075, 450))

        arcade.draw_lines(PointList, arcade.color.BLACK, 4)  # highlighting the rectangles which are on sides

        output = f"Human Score: {self.player_score1}"  # Show human score
        arcade.draw_text(output, 40, 340, arcade.color.BLACK, 12)

        output1 = f"Bot Score: {self.player_score2}"  # show bot score
        arcade.draw_text(output1, 940, 340, arcade.color.BLACK, 12)

        self.splash_list1.draw()
        self.splash_list2.draw()
        self.player_list.draw()

    def update_array(self, coloumn, row, player, val):

        coloumn = (coloumn - 235) // 70
        row = (row - 35) // 70

        if player == "1" and self.array[row][coloumn] != 10 and self.array[row][coloumn] != 100 and self.array[row][
            coloumn] != 20 and self.array[row][coloumn] != 200:

            self.array[row][coloumn] = val
        elif player == "2" and self.array[row][coloumn] != 20 and self.array[row][coloumn] != 200 and self.array[row][
            coloumn] != 10 and self.array[row][coloumn] != 100:

            self.array[row][coloumn] = val

        self.update_grid()
        return row, coloumn

    def legal_move(self, x, y, check):

        if check == 1:
            if self.array[x][y] == 0 or self.array[x][y] == 100 or self.array[x][y] == 10 or self.array[x][y] == 1:
                return True
        if check == 2:
            if self.array[x][y] == 0 or self.array[x][y] == 200 or self.array[x][y] == 20 or self.array[x][y] == 2:
                return True
        # pass

    def sliding_player1(self, row, coloumn, button_pressed, check):
        
        count = 0
        if button_pressed == "Left":

            coloumn = coloumn - 1
            if coloumn != 0:
                while coloumn >= 0 and self.array[row][coloumn] == check:
                    count += 1
                    coloumn = coloumn - 1
            if count == 0:
                return 70
            else:
                value = count * 70
                return value

        if button_pressed == "Right":
            coloumn = coloumn + 1
            if coloumn != 9:
                while coloumn <= 9 and self.array[row][coloumn] == check:
                    count += 1

                    coloumn = coloumn + 1

            if count == 0:
                return 70
            else:
                value = count * 70
                return value

        if button_pressed == "Up":
            row = row + 1
            if row != 9:
                while row <= 9 and self.array[row][coloumn] == check:
                    count += 1
                    row = row + 1

            if count == 0:
                return 70
            else:
                value = count * 70
                return value

        if button_pressed == "Down":
            row = row - 1
            if row != 0:
                while row >= 0 and self.array[row][coloumn] == check:
                    count += 1
                    row = row - 1

            if count == 0:
                return 70
            else:
                value = count * 70
                return value
    def update_score(self):
        for i in range(10):
            for j in range(10):
                if self.array[i][j] == 10:
                    self.player_score1 += 1
                    self.array[i][j] = 100

                if self.array[i][j] == 20:
                    self.player_score2 += 1
                    self.array[i][j] = 200
        if self.player_score1 > 50:
            # player1_win = True
            win = "1"
            game_over = GameOverView(win)
            self.window.show_view(game_over)

        if self.player_score2 > 50:
            win = "2"
            # player2_win = True
            game_over = GameOverView(win)
            self.window.show_view(game_over)

        if self.player_score2 == 50 and self.player_score1 == 50:
            win = "3"
            game_over = GameOverView(win)
            self.window.show_view(game_over)
        
        if self.draw_counter > 103:
            win = "3"
            game_over = GameOverView(win)
            self.window.show_view(game_over)


    def update_grid(self):
        for row in range(10):
            for colomn in range(10):
                if self.array[row][colomn] == 10:
                    k = colomn
                    j = row

                    k = (k * 70) + 235
                    j = (j * 70) + 35
                    self.splash1 = arcade.Sprite("D1.jpeg", .3)
                    self.splash1.center_x = k
                    self.splash1.center_y = j
                    self.splash_list1.append(self.splash1)

        for row in range(10):
            for colomn in range(10):
                if self.array[row][colomn] == 20:
                    k = colomn
                    j = row

                    k = (k * 70) + 235
                    j = (j * 70) + 35
                    self.splash2 = arcade.Sprite("D2.jpeg", .3)
                    self.splash2.center_x = k
                    self.splash2.center_y = j
                    self.splash_list2.append(self.splash2)

    def player_turn(self, a):
        self.turn = a

    def heuristic(self):
        winningChances = 0
        column = (self.player_sprite2.center_x - 235) // 70
        row = ((self.player_sprite2.center_y - 35) // 70)

        # First Condition
        for i in range(10):
            for j in range(10):
                if self.array[i][j] == 200:
                    winningChances += 1

        # Second Condition
        # If below box is empty
        if row + 1 < 10 and self.array[row + 1][column] == 0:
            winningChances += 1

            # If above box is empty
        if column + 1 < 10 and self.array[row][column + 1] == 0:
            winningChances += 1

            # If left box is empty
        if row - 1 > 0 and self.array[row - 1][column] == 0:
            winningChances += 1

            # If right box is empty
        if column - 1 > 0 and self.array[row][column - 1] == 0:
            winningChances += 1

        # 3rd Condition
        if (row, column) == (4, 4) or (row, column) == (4, 5) or (row, column) == (5, 4) or (row, column) == (5, 5):
            winningChances += 10
        if (row, column) == (3, 3) or (row, column) == (3, 6) or (row, column) == (6, 3) or (row, column) == (6, 6):
            winningChances += 5
        return winningChances

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def minimax(self, curDepth, nodeIndex, maxTurn, targetDepth):
        scores = self.heuristic()
        # base case : targetDepth reached
        if (curDepth == targetDepth):
            return scores

        if (maxTurn):
            return max(self.minimax(curDepth + 1, nodeIndex * 2, False, targetDepth),
                       self.minimax(curDepth + 1, nodeIndex * 2 + 1, False, targetDepth))

        else:
            return min(self.minimax(curDepth + 1, nodeIndex * 2, True, targetDepth),
                       self.minimax(curDepth + 1, nodeIndex * 2 + 1, True, targetDepth))

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def find_best_move(self):
        moveVal = -1000
        bestMove = 0
        Dictionary = {}
        checker2 = False
        checker = False    # For checking if their is no empty box near sprite.
        
        # Current row and column
        column = ((self.player_sprite2.center_x - 235) // 70)
        row = ((self.player_sprite2.center_y - 35) // 70)
        print(row,column)

        if column < 9 and self.array[row][column + 1] == 0:
            checker = True
            checker2 = True
            self.array[row][column + 1] = 200
            a = self.minimax(0, 0, True, 8)
            self.array[row][column + 1] = 0  # Undo the move
            Dictionary[a] = "RIGHT"
                
        if column > 0 and self.array[row][column - 1] == 0:
            checker = True
            checker2 = True
            self.array[row][column - 1] = 200
            moveVal = self.minimax(0, 0, True, 8)
            self.array[row][column - 1] = 0  # Undo the move
            Dictionary[moveVal] = "LEFT"
            
        if row < 9 and self.array[row + 1][column] == 0:
            checker = True
            checker2 = True
            self.array[row + 1][column] = 200
            moveVal = self.minimax(0, 0, True, 8)
            self.array[row + 1][column] = 0  # Undo the move
            Dictionary[moveVal] = "UP"

        if row > 0 and self.array[row - 1][column] == 0:
            checker = True
            checker2 = True
            self.array[row - 1][column] = 200
            moveVal = self.minimax(0, 0, True, 8)
            self.array[row - 1][column] = 0  # Undo the move
            Dictionary[moveVal] = "DOWN"


        if checker == False:
            # If their is no empty box near sprite it must slide on the way near to empty spaces.
                      
            if (column + 1) < 9 and self.array[row][column + 1] == 200:
                for i in range(1,9):
                    if (column + i) < 10:
                        if self.array[row][column + i] == 0:
                            checker2 = True
                            return "RIGHT"

            if column > 0 and self.array[row][column - 1] == 200:
                for i in range(1, 9):
                    if (column - i) >= 0:
                        if self.array[row][column - i] == 0:
                            checker2 = True
                            return "LEFT"

            
            if (row + 1) < 9 and self.array[row + 1][column] == 200:
                for i in range(1,9):
                    if (row + i) < 10:
                        if self.array[row + i][column] == 0:
                            checker2 = True
                            return "UP"

            if row > 0 and self.array[row - 1][column] == 200:
                for i in range(1, 9):
                    if (row - i) >= 0:
                        if self.array[row - i][column] == 0:
                            checker2 = True
                            return "DOWN"


        # If their is no empty box in a line of sprite so we check empty spaces in upper or lower line.
        # Or in the left or right line of gride from sprite.
        if checker2 == False:
            
            if column < 9 and self.array[row][column + 1] == 200:
                for i in range(1,9):
                    if (column + i) < 10 and (row+1) < 10 and row-1 > 0:
                        if self.array[row+1][column + i] == 0 or self.array[row-1][column + i] == 0:
                            return "RIGHT"

            if column > 0 and self.array[row][column - 1] == 200:
                for i in range(1, 9):
                    if (column - i) > 0 and (row + 1) < 10 and row - 1 > 0:
                        if self.array[row+1][column - i] == 0 or self.array[row-1][column - i] == 0 :
                            return "LEFT"
            
            if row < 9 and self.array[row + 1][column] == 200:
                for i in range(1,9):
                    if (row + i) < 10 and column + 1 < 10 and column - 1 > 0:
                        if self.array[row + i][column+1] == 0 or self.array[row + i][column-1] == 0:
                            return "UP"

            if row > 0 and self.array[row - 1][column] == 200:
                for i in range(1, 9):
                    if (row - i) > 0 and column + 1 < 10 and column - 1 > 0:
                        if self.array[row - i][column+1] == 0 or self.array[row - i][column-1] == 0:
                            return "DOWN"

        for i in Dictionary:
            if i >= moveVal:
                moveVal = i 
        if Dictionary == {}:
            return "UP" 
        else:
            bestMove = Dictionary[moveVal]   
            return bestMove

    def add_move(self, move):
        if move == 0:
            return "LEFT"
        elif move == 1:
            return "LEFT"
        elif move == 2:
            return "LEFT"
        elif move == 3:
            return "DOWN"
        elif move == 4:
            return "DOWN"
        elif move == 5:
            return "DOWN"
        elif move == 6:
            return "LEFT"
        else:
            return self.find_best_move()

    def AI_player_turn_function(self, move):

        best_move = self.add_move(move)

        if best_move == "LEFT" and self.player_sprite2.center_x != 235:
            a, b = self.update_array(self.player_sprite2.center_x, self.player_sprite2.center_y, self.turn, 20)
            self.update_score()
            if self.legal_move(a, b - 1, 2) == True:
                move_left = self.sliding_player1(a, b, "Left", 200)
                self.player_sprite2.center_x -= move_left
                arcade.sound.play_sound(audio_1)
            else:
                arcade.sound.play_sound(audio_1f)
            self.update_array(self.player_sprite2.center_x, self.player_sprite2.center_y, self.turn, 2)

        elif best_move == "RIGHT" and self.player_sprite2.center_x != 865:
            a, b = self.update_array(self.player_sprite2.center_x, self.player_sprite2.center_y, self.turn, 20)
            self.update_score()
            if self.legal_move(a, b + 1, 2) == True:
                move_right = self.sliding_player1(a, b, "Right", 200)
                arcade.sound.play_sound(audio_1)
                self.player_sprite2.center_x += move_right

            else:
                arcade.sound.play_sound(audio_1f)
            self.update_array(self.player_sprite2.center_x, self.player_sprite2.center_y, self.turn, 2)

        elif best_move == "DOWN" and self.player_sprite2.center_y != 35:
            a, b = self.update_array(self.player_sprite2.center_x, self.player_sprite2.center_y, self.turn, 20)
            self.update_score()
            if self.legal_move(a - 1, b, 2) == True:
                move_down = self.sliding_player1(a, b, "Down", 200)
                arcade.sound.play_sound(audio_1)
                self.player_sprite2.center_y += -move_down
            else:
                arcade.sound.play_sound(audio_1f)
            self.update_array(self.player_sprite2.center_x, self.player_sprite2.center_y, self.turn, 2)

        if best_move == "UP" and self.player_sprite2.center_y != 665:
            a, b = self.update_array(self.player_sprite2.center_x, self.player_sprite2.center_y, self.turn, 20)
            self.update_score()
            if self.legal_move(a + 1, b, 2) == True:
                move_up = self.sliding_player1(a, b, "Up", 200)
                arcade.sound.play_sound(audio_1)
                self.player_sprite2.center_y += move_up
            else:
                arcade.sound.play_sound(audio_1f)
            self.update_array(self.player_sprite2.center_x, self.player_sprite2.center_y, self.turn, 2)

    def on_key_press(self, symbol, modifier):
        self.draw_counter += 1
        if symbol == arcade.key.F:
            self.window.set_fullscreen(not self.window.fullscreen)

        if symbol == arcade.key.LEFT and self.player_sprite1.center_x != 235:
            a, b = self.update_array(self.player_sprite1.center_x, self.player_sprite1.center_y, self.turn, 10)
            self.update_score()

            if self.legal_move(a, b - 1, 1) == True:
                move_left = self.sliding_player1(a, b, "Left", 100)
                arcade.sound.play_sound(audio_1)
                self.player_sprite1.center_x += -move_left
            else:
                arcade.sound.play_sound(audio_1f)
            self.update_array(self.player_sprite1.center_x, self.player_sprite1.center_y, self.turn, 1)


        elif symbol == arcade.key.RIGHT and self.player_sprite1.center_x != 865:
            a, b = self.update_array(self.player_sprite1.center_x, self.player_sprite1.center_y, self.turn, 10)
            self.update_score()

            if self.legal_move(a, b + 1, 1) == True:
                move_right = self.sliding_player1(a, b, "Right", 100)
                self.player_sprite1.center_x += move_right
                arcade.sound.play_sound(audio_1)
            else:
                arcade.sound.play_sound(audio_1f)
            self.update_array(self.player_sprite1.center_x, self.player_sprite1.center_y, self.turn, 1)

        # up down

        elif symbol == arcade.key.DOWN and self.player_sprite1.center_y != 35:

            a, b = self.update_array(self.player_sprite1.center_x, self.player_sprite1.center_y, self.turn, 10)
            self.update_score()
            if self.legal_move(a - 1, b, 1) == True:
                move_down = self.sliding_player1(a, b, "Down", 100)
                self.player_sprite1.center_y += -move_down
                arcade.sound.play_sound(audio_1)
            else:
                arcade.sound.play_sound(audio_1f)
            self.update_array(self.player_sprite1.center_x, self.player_sprite1.center_y, self.turn, 1)

        elif symbol == arcade.key.UP and self.player_sprite1.center_y != 665:
            a, b = self.update_array(self.player_sprite1.center_x, self.player_sprite1.center_y, self.turn, 10)
            self.update_score()
            if self.legal_move(a + 1, b, 1) == True:
                move_up = self.sliding_player1(a, b, "Up", 100)
                arcade.sound.play_sound(audio_1)
                self.player_sprite1.center_y += move_up
            else:
                arcade.sound.play_sound(audio_1f)
            self.update_array(self.player_sprite1.center_x, self.player_sprite1.center_y, self.turn, 1)

        self.AI_player_turn_function(self.move)
        self.move = self.move + 1  # First we set manual moves for AI player.


class GameOverView(arcade.View):
    def __init__(self, win):
        super().__init__()
        self.time_taken = 0
        self.win = win

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.window.set_mouse_visible(True)

    def on_draw(self):
        arcade.start_render()
        background = arcade.load_texture("Result_bg.png")
        arcade.draw_scaled_texture_rectangle(690, 350, background, 1.55, 0)
        """
        Draw "Game over" across the screen.
        """
        if self.win == "1":
            win = "Human has won the game"
        elif self.win == "2":
            win = "Bot has won the game"
        elif self.win == "3":
            win = "Match Drawn"
        arcade.draw_text("Congratulations", 480, 600, arcade.color.BLACK, 30)
        arcade.draw_text(win, 440, 490, arcade.color.BLACK, 30)
        arcade.draw_text("Click to exit", 450, 300, arcade.color.BLACK, 30)

        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.BLACK, 14)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        arcade.exit()


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Snail Game by Syed Dawood Shah & Nimrah Tariq", fullscreen=True)
    window.total_score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()

