# Project Brief #
This project is a Python Sliding Puzzle game using only the turtle library to manage GUI. 

The game includes a splash screen, player input for name and move count, tile movements, reset and load puzzle functions, error logging, and a quit button.

Skills and tools used: Python, GUI programming, file handling, error handling, user input validation, problem- solving, and project management.

## Design 
### Overview 

I created three classes to manage the game. The first two classes are about UI implementation, the last class is
about the function of the game. After I made decent efforts to this project, a lot of things such as "class" I didn't
quite comprehend became very clear to me.

### Design
The first class is to draw the frames of the UI. Initially I only have two classes, one for UI, one for
the gaming function. However, the first frame cannot be properly displayed, but somehow putting them in separate
classes solved this problem.

The second class is the main image section. It imports or draws every image needed for the game to function
properly at the beginning, the header, the buttons, and the splash screen.

The last class is to make the game working. Because we are required to load the puzzle randomly every time, but save
possibility of "unscramble" the puzzle with one click, but the overall position of all puzzles should remain in the
frame I drew earlier, I think it is the best to use dictionary. My inspiration of swapping came from the bubble sort
we learned in class.

