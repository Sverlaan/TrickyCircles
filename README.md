# TrickyCircles
A puzzle game and solver using the Breadth First Search algorithm, made with pygame.

The idea of the game was inspired by the game *Tricky Animals*, see: http://www.tricky-animals.de/. 
The main attraction for this project was creating a solver which could solve any level from the game using the Breadth First Search algorithm.

## Game Explanation
The game can be started by running *play.py*. A GUI will appear that the user can interact with.

The goal of this game is to get the colored circles in the right order: from red (left) to violet (right), like a rainbow.
To accomplish this goal, the following buttons and signs are available:
* A: swap the first two circles.
* B: swap the last two circles.
* X: shift the circles in the middle.
* MOVES: shows the current number of actions executed and the minimum number of moves required to solve the level.
* SOLVE: the computer auto-solves the level and displays the solution using animations.
* RESET: the level restarts in the begin-order, so that the user can try again from scratch.
* +: adds a circle, which increases the difficulty. The maximum number of circles is 8.
* -: removes a circle, which decreases the difficulty. The minimum number of circles is 4.
* ?: shows a brief explanation text.

## Screenshot
![screenshot](/resources/screenshot.png)

## Authors
* Stan Verlaan

This project was inspired by an assignment from the course Datastructures and Algorithms for Artificial Intelligence, AI - Utrecht University 2020.
For this bonus assignment, an algorithm for solving the *Tricky Animals* game needed to be designed. 
I figured I would implement it using pygame to create my own version of the game in order to visualize the solver.
