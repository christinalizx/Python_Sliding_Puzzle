"""
    Fall 2022 CS5001
    Zixi Li
    Final Project: puzzle_game.py
"""

import math
import os
import random
import time
import turtle

t = turtle.Turtle()
screen = turtle.Screen()
screen.bgcolor("white")
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
LENGTH = 100
count = 0
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)


class Initial(turtle.Turtle):
    """
    Initial manages the framework of the starting UI.
    It uses __init__ as a constructor.
    It sets the direction of the turtle upwards, and hide the turtle from the drawing process.
    It uses draw to draw the frameworks.
    """

    def __init__(self):
        """
        Function:
            Constructor of the class,
            set the direction of the turtle, and hide it.
        Parameter:
            None
        Returns:
            None
        """
        super().__init__()
        self.penup()
        self.hideturtle()

    def draw(self, x, y, px, py, color):
        """
        Function:
            Draw the frameworks.
        Parameters:
            x: int
            y: int
            px: int
            py: int
            color: str
        Returns:
            None
        """
        t.hideturtle()
        self.pensize(4)
        self.pencolor(color)
        self.goto(x, y)
        self.pd()
        self.speed(0)

        self.goto(x, y + py)
        self.goto(x - px, y + py)
        self.goto(x - px, y)
        self.goto(x, y)

        self.pu()
        self.goto(x - px / 2, y + py / 4)


class Image(turtle.Turtle):
    """
    Image governs the UI apperance after frameworks are drawn.
    It uses __init__ as a constructor.
    import_images() uploads all the imagines necessary for the UI implementation.
    splash_screen() implements the splash screen to the beginning of the program.
    """

    def __init__(self):
        """
        Function:
            Constructor of the class
        Parameter:
            None
        Returns:
            None
        """
        super().__init__()
        self.penup()
        self.hideturtle()

    def import_images(self):
        """
        Function:
            Import images to the UI.
        Parameter:
            None
        Returns: None
        """
        screen.addshape(
            "slider_puzzle_project_fall2021_assets-2022/Images/mario/mario_thumbnail.gif"
        )
        self.goto(280, 323)
        self.speed(0)
        self.shape(
            "slider_puzzle_project_fall2021_assets-2022/Images/mario/mario_thumbnail.gif"
        )
        self.stamp()

        screen.addshape(
            "slider_puzzle_project_fall2021_assets-2022/Resources/loadbutton.gif"
        )
        self.goto(80, -280)
        self.speed(0)
        self.shapesize(10)
        self.shape("slider_puzzle_project_fall2021_assets-2022/Resources/loadbutton.gif")
        self.stamp()

        self.goto(180, -280)
        screen.addshape(
            "slider_puzzle_project_fall2021_assets-2022/Resources/resetbutton.gif"
        )
        self.shape("slider_puzzle_project_fall2021_assets-2022/Resources/resetbutton.gif")
        self.stamp()

        self.goto(280, -280)
        screen.addshape(
            "slider_puzzle_project_fall2021_assets-2022/Resources/quitbutton.gif"
        )
        self.shape("slider_puzzle_project_fall2021_assets-2022/Resources/quitbutton.gif")
        self.stamp()

    def splash_screen(self):
        """
        Function:
            Creates a splash screen.
        Parameter:
            None
        Returns:
            None
        """
        t.hideturtle()
        screen.bgcolor("black")
        self.color("orange")
        self.write("Loading......", align="center", font=("Comic Mono", 20, "bold"))
        self.goto(x=-110, y=-20)
        x = -110
        y = -20
        self.pencolor("orange")
        self.pen(fillcolor="orange")
        for i in range(10):
            self.begin_fill()
            for j in range(4):
                t.hideturtle()
                self.speed(0.8)
                self.forward(10)
            self.end_fill()
            x = x + 20
            self.goto(x, y)
            self.stamp()


class Game(turtle.Turtle):
    """
    Game() sets all the methods for the puzzle game to run properly.
    __init__ acts as constructor of the whole class.
    get_user_name() asks user to input his/her name.
    ask_puzzle_choice() pops up a separate terminal to let user input their choice of puzzle.
    load() loads the puzzle accoridng to user's choice of puzzle.
    quit() end the program once the user clicks the quit button.
    draw_coordinate() imports the specific images
    corresponding the coordinates stored in key.
    draw_puzzle() is the driver method of draw_coordinate().
    draw_file_with_puzzle_choice() gets the dictionary corresponding user's choice of puzzle.
    draw_file() reads the puzz file and process its information,
    creates dictionary using coordinates as key, shuffled image paths as value.
    get_puzzle_choice() stores the puzzle choice for other methods.
    reset() manages which puzzle to draw the puzzle according to the unshuffled dictionary
    after clicked reset button.
    set_blank_coordinates() tells the coordinates of the blank image.
    is_adjacent_to_blank() determines whether puzzle image user clicked is adjacent to the blank space.
    is_contained_within() judges whether the click is within a specific tile.
    get_moves() asks user to input the number of moves s/he wishes to unscramble the puzzle.
    swap() swaps the tile with the blank, if the click is within the tile and adjacent to the blank image.
    is_win() determines whether the user wins.
    show_messages() shows the different images based on the winning or losing status.
    write_leadersboard() checks if there is a leadersboard.txt exists. If not, create one.
    load_leadersboard() load the leadersboard information from leadersboard.txt and arrange in ascending order.
    draw_leadersboard() draws the leadersboard to the right column.
    """

    def __init__(self):
        """
        Function:
            Constructor of the class,
            set the attributes needed for other methods.
        Parameter:
            None
        Returns:
            None
        """
        super().__init__()
        turtle.hideturtle()
        self.puzzle_choice = "mario"
        self.blank_x = None
        self.blank_y = None
        self.leadersboard = []
        self.user_name = ""
        self.moves = 0
        self.count = 0
        self.puzzle_finished = None
        self.puzzle_choice_to_file_path = {
            f"{self.puzzle_choice}": f"slider_puzzle_project_fall2021_assets-2022/{self.puzzle_choice}.puz"
        }
        self.load_leadersboard()
        self.draw_leadersboard()
        self.draw_file_with_puzzle_choice(self.puzzle_choice)

    def get_user_name(self):
        """
        Function:
            Asks user to input his/her name and store it.
        Parameter:
            None
        Returns:
            the name user inputs.
        """
        user_name = turtle.textinput("Name", "Please enter your name: ")
        self.user_name = user_name
        return user_name

    def ask_puzzle_choice(self):
        """
        Function:
            Asks user to input the name of the puzzle.
        Parameter:
            None
        Returns:
            The string user inputs.
        """
        try:
            choice_name = turtle.textinput(
                "Select the puzzle you want",
                "Please enter the name of your choice",
            )

            self.puzzle_choice = choice_name
            word = "malformed"
            self.puzzle_choice_to_file_path.update({
                    f"{self.puzzle_choice}": f"slider_puzzle_project_fall2021_assets-2022/{self.puzzle_choice}.puz"
                })
            if word in choice_name:
                with open("5001_puzzle.err", mode="a+") as out_file:
                    now = time.ctime()
                    out_file.write(f"\n{now}//Error: Malformed data")
            return choice_name

        except ValueError:
            with open("5001_puzzle.err", mode="a+") as out_file:
                now = time.ctime()
                out_file.write(f"\n{now}//Error: Entered wrong value")

        except FileNotFoundError:
            with open("5001_puzzle.err", mode="a+") as out_file:
                now = time.ctime()
                out_file.write(f"\n{now}//Error: File not found")

    def load(self, x, y):
        """
        Function:
            draw the puzzle according to user's choice, when user clicks load.
        Parameter:
            x: float
            y: float
        Returns:
            None
        """
        if 49 < x < 121 and -337 < y < -267:
            self.hideturtle()
            puzzle_choice = self.ask_puzzle_choice()
            self.goto(-320, 290)
            self.pencolor("white")
            self.pen(fillcolor="white")
            self.begin_fill()
            for j in range(4):
                t.hideturtle()
                self.speed(0)
                self.forward(405)
                self.right(90)
            self.end_fill()
            self.draw_file_with_puzzle_choice(puzzle_choice)

    def quit(self, x, y):
        """
        Function:
            quit the program once the user clicks quit.
        Parameters:
            x: float
            y: float
        Returns:
            None
        """
        if 240 < x < 335 and -325 < y < -270:
            quit()

    def draw_coordinate(self, key, value):
        """
        Function:
            Draw image onto a coordinate defined by key (x, y)
        Parameter:
            key: (float, float)
            value: str
        Returns:
            None
        """
        self.speed(0)
        self.pencolor("white")
        self.goto(key[0], key[1])
        screen.addshape(f"slider_puzzle_project_fall2021_assets-2022/{value}")
        self.shape(f"slider_puzzle_project_fall2021_assets-2022/{value}")
        self.stamp()

    def draw_puzzle(self, data=None):
        """
        Function:
            loop through the dictionary of coordinate-image pair and draw it, if data is not provided,
            draw using self.puzzle
        Parameter:
            data: None
        Returns:
            None
        """
        if data is None:
            # redraw the puzzle
            for key, value in self.puzzle.items():
                self.draw_coordinate(key, value)
        else:
            for key, value in data.items():
                self.draw_coordinate(key, value)

    def draw_file_with_puzzle_choice(self, puzzle_choice):
        """
        Function:
            draw the file corresponding to puzzle_choice
        Parameter:
            puzzle_choice: str
        Returns:
            None
        """
        self.draw_file(self.puzzle_choice_to_file_path[f"{puzzle_choice}"])

    def draw_file(self, path):
        """
        Function:
            read the file into self.puzzle_finished and self_puzzle,
            and then call draw_puzzle to draw the puzzle
        Parameter:
            path: str
        Returns:
            dictionary of finished and shuffled puzzle.
        """
        try:
            with open(path, mode="r") as file:
                contents = file.read().split("\n")
                for line in contents:
                    temp = line.split(":")
                    if "number" in temp[0]:
                        number = temp[1]
                        number = number.strip()
            file_path = []
            with open(path, mode="r") as file:
                contents = file.read().split("\n")
                for line in contents:
                    temp = line.split(":")
                    if temp[0].isnumeric():
                        file_path.append(temp[1].replace(" ", ""))

                coordinates = []
                x = -270
                y = 240
                row = int(math.sqrt(int(number)))
                for i in range(row):
                    for j in range(row):
                        coordinates.append((x, y))
                        x = x + 101
                    x = -270
                    y = y - 101

                picture = file_path
                # save unshuffled puzzle to compare with the result in swap() for winning conditions
                self.puzzle_finished = dict(zip(coordinates, picture))

                random.shuffle(picture)
                puzzle = dict(zip(coordinates, picture))

                self.puzzle = puzzle
                self.set_blank_coordinates()
                self.count = 0

            self.draw_puzzle()
            return self.puzzle
        except FileNotFoundError:
            with open("5001_puzzle.err", mode="a+") as out_file:
                now = time.ctime()
                out_file.write(f"\n{now}//Error: File not found")

    def get_puzzle_choice(self, puzzle_choice):
        """
        Function:
            stores user's puzzle choice
        Parameter:
            puzzle_choice: str
        Returns:
            the puzzle choice.
        """
        self.puzzle_choice = puzzle_choice
        return self.puzzle_choice

    def reset(self, x, y):
        """
        Function:
            draw the puzzle according to the unshuffled dictionary of the selected puzzle.
        Parameters:
            x: float
            y: float
        Returns:
            None
        """
        if 140 < x < 228 and -342 < y < -240:
            self.draw_puzzle(self.puzzle_finished)
            self.puzzle = self.puzzle_finished
            self.set_blank_coordinates()
            self.write_leadersboard()

    def set_blank_coordinates(self):
        """
        Function:
            find the blank tile and set self.blank_x and self.blank_y
        Parameter:
            None
        Return:
            None
        """
        for key, value in self.puzzle.items():
            if "blank.gif" in value:
                self.blank_x = key[0]
                self.blank_y = key[1]

    def is_adjacent_to_blank(self, x, y):
        """
        Function:
            if a coordinate (x, y) is adjacent to blank tile defined by center (self.blank_x, self.blank_y)
        Parameter:
            x: float
            y: float
        Returns:
            a boolean value
        """
        x_dist = x - self.blank_x
        y_dist = y - self.blank_y
        # if the click point is at the top of the blank tile
        if (0 < y_dist < 1.5 * LENGTH) and abs(x_dist) < LENGTH / 2:
            return True
        # bottom
        if (-1.5 * LENGTH < y_dist < 0) and abs(x_dist) < LENGTH / 2:
            return True
        # left
        if (-1.5 * LENGTH < x_dist < 0) and abs(y_dist) < LENGTH / 2:
            return True
        # right
        if (0 < x_dist < 1.5 * LENGTH) and abs(y_dist) < LENGTH / 2:
            return True

        return False

    def is_contained_within(self, x1, y1, x2, y2):
        """
        Function:
            if a coordinate (x1, y1) is contained within the tile centerd at (x2, y2)
        Parameters:
            x1: float
            y1: float
            x2: int
            y2: int
        Returns:
            a boolean value
        """
        if abs(x1 - x2) < LENGTH / 2 and abs(y1 - y2) < LENGTH / 2:
            return True

        return False

    def get_moves(self):
        """
        Function:
            asks user how many moves s/he wants to unscramble the puzzle.
        Parameter:
            None
        Returns:
            the number of moves.
        """
        self.moves = turtle.numinput(
            "Enter the number of moves", "range 5-200", 5, minval=5, maxval=200
        )
        return self.moves

    def swap(self, x, y):
        """
        Function:
            swaps the tile with the blank, if the click is within the tile and adjacent to the blank image.
        Parameters:
            x: float
            y: float
        Returns:
            None
        """
        # if the click point is adjacent to the blank tile
        if y > -150 and self.is_adjacent_to_blank(x, y):
            # loop through self.puzzle to find which tile the user clicks on
            for key in self.puzzle:
                if self.is_contained_within(x, y, key[0], key[1]):
                    # the tile the user clicks on
                    tile_clicked = key
                    # swap the tile the user clicks on with the blank tile
                    tmp = self.puzzle[tile_clicked]
                    self.puzzle[tile_clicked] = self.puzzle[(self.blank_x, self.blank_y)]
                    self.puzzle[(self.blank_x, self.blank_y)] = tmp
                    self.draw_puzzle(
                        {
                            (self.blank_x, self.blank_y): tmp,
                            tile_clicked: self.puzzle[tile_clicked],
                        }
                    )
                    self.blank_x = tile_clicked[0]
                    self.blank_y = tile_clicked[1]
                    self.count = self.count + 1
                    is_win = self.is_win()
                    if is_win:
                        self.show_message(is_win=True)
                        self.write_leadersboard()
                    else:
                        if self.count > self.moves:
                            self.show_message(is_win=False)
                    break

    def is_win(self):
        """
        Function:
            determines if the user wins or loses, the winning condition being the user
            unscrambles the puzzle within the number of moves.
        Parameter:
            None
        Returns:
            a boolean value.
        """
        if count <= self.moves and self.puzzle == self.puzzle_finished:
            return True

        return False

    def show_message(self, is_win):
        """
        Function:
            show winning or losing messages based on game output
        Parameter:
            is_win: boolean
        Returns:
            None
        """
        gif_name = "winner.gif" if is_win else "Lose.gif"
        self.goto(0, 0)
        screen.addshape(
            f"slider_puzzle_project_fall2021_assets-2022/Resources/{gif_name}"
        )
        self.shape(f"slider_puzzle_project_fall2021_assets-2022/Resources/{gif_name}")
        self.stamp()
        turtle.delay(5000)
        screen.addshape(
            "slider_puzzle_project_fall2021_assets-2022/Resources/quitmsg.gif"
        )
        self.shape("slider_puzzle_project_fall2021_assets-2022/Resources/quitmsg.gif")
        self.stamp()

    def write_leadersboard(self):
        """
        Function:
            write current user and moves to leadersboard.txt, if the file doesn't exist, create an empty file
        Parameter:
            None
        Returns:
            None
        """
        if not os.path.exists("leadersboard.txt"):
            mode = "w+"
        else:
            mode = "a+"
        with open("leadersboard.txt", mode=mode) as file:
            file.write(f"{self.user_name},{self.count}\n")

    def load_leadersboard(self):
        """
        Function:
            load records from leadersboard.txt into a list of tuples (name, move),
            also sort by moves in ascending order
        Parameter:
            None
        Returns:
            None
        """
        if os.path.exists("leadersboard.txt"):
            with open("leadersboard.txt", mode="r") as file:
                result = []
                contents = file.readlines()
                for line in contents:
                    name, move = line.strip("\n").split(",")
                    result.append((name, move))

                self.leadersboard = sorted(result, key=lambda x: int(x[1]))
        else:
            with open("leadersboard.txt", mode="w+") as file:
                file.write("")
            self.leadersboard = []

    def draw_leadersboard(self):
        """
        Function:
            draws the leadersboard to the right column.
        Parameter:
            None
        Returns:
            None
        """
        y = 280
        x = 160
        self.hideturtle()
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.write("Leaders: ", align="center", font=("Comic Mono", 15, "bold"))
        if len(self.leadersboard) > 0:
            self.color("black")
            for i, v in enumerate(self.leadersboard, 1):
                y = y - 20
                self.goto(x, y)
                self.pendown()
                self.write(
                    f"{i}. {v[0]}: {v[1]}",
                    align="center",
                    font=("Comic Mono", 15, "bold"),
                )
                self.penup()


image = Image()
image.splash_screen()
screen.clear()

menu = Initial()
menu.draw(-333, 323, -427, -500, "#3B3A4C")
menu.draw(116, 323, -219, -500, "#8BA3C7")
menu.draw(-333, -230, -668, -113, "#BFA782")

image.import_images()
game = Game()

game.get_moves()
game.get_user_name()
screen.onclick(game.load, add=True)
screen.onclick(game.reset, add=True)
screen.onclick(game.quit, add=True)
screen.onclick(game.swap, add=True)

turtle.title("Welcome to Sliding Puzzle Game!!")

turtle.mainloop()
