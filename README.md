## CROSS SUM
#### A Python Implementation of the Cross Sum Puzzle Game

##### DESCRIPTION
*Cross Sum*, or *Kakuro* in Japan, is a puzzle game that takes place on a grid
that consists of black-and-white squares. The white squares can be grouped by
rows or columns that are capped by the black squares. Each 'cap' black square
contains a number that represents the sum of the numbers in the corresponding
horizontal or vertical white squares. The object of the game is to place the
correct integer values in each white box such that each horizontal and vertical
line correctly add up to the value in the cap, and no two integers are repeated
in any one row or column.

For more information, visit [WikiPedia]https://en.wikipedia.org/wiki/Kakuro

##### HOW TO RUN
in the program direction, run one of the commands:  
    `python3 main.py`  
    or  
    `py main.py`  
or from an IDE, run the main.py file.

###### FILES
There are 3 files included in the program:

*app.py*
    This file contains the "frontend" for the game. It contains the code for 
    the GUI, which is responsible for displaying the information to the player 
    and accepting input to play the game

*cross_sum.py*
    This file contains the "backend" for the game. It contains the algorithms 
    for generating and solving the puzzles, as well as the functionality for 
    checking solutions.

*main.py*
    This is the main file for the game that creates an instance of the 
    application to run.