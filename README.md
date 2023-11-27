# Shortest Path
An interactive application to visualize a path-finding algorithm that finds the shortest route between two points given obstacles in the way.

## Technologies
Python 3.10

PyGame 2.5.2

## Features
This application allows a user to draw an obstacle course between two adjustable points in a grid. The grid can be fully turned off via a slider on the right. The path is updated live so the user can see immediate feedback about the walls (invalid cells) they have placed. There are four ways to interact with the grid:
* Left-Click: Adds walls to the grid. Users can hold down left-click to draw multiple walls in succession.
* Right-click: Removes walls to the grid. Users can hold down right-click to remove multiple walls in succession.
* Shift + Left-Click: Moves starting location (green cell).
* Shift + Right-Click: Moves ending location (red cell).

The user has the option to remove the automatic drawing of the line. This allows for reduced lag when drawing on grids with much larger cells. Inside the settings file the user can adjust various options such as the number of cells in the grid (adjust TILESIZE, TILEWIDTH, and TILEHEIGHT).

## Approach
This project was created in a couple of phases. The initial phase was a proof of concept of a working algorithm and I programmed it to just output the optimal path of a 5x5 grid in the console. Other than some tweaks and optimizations to the algorithm, once it was functioning, the main logic of the application was left largely untouched. This was done for a deliberate reason, as one of the challenges I had for myself was to try to keep different parts of the program isolated. It's very easy to have logic features implemented via limitations in the GUI (for example, in a game of hangman, not allowing a letter to be chosen because the user can't click on it, even if the backend would allow it). I wanted the GUI to be a shell that I could put on top of an already functioning console application.

I chose PyGame as the GUI for this project as I have some level of familiarity with it from other projects. Other libraries/frameworks considered were Matplotlib, tkinter, and PySimpleGui. None of these seemed to offer anything I couldn't already do in PyGame, however, and more often were more limited in their functionality and features.

Additionally, to continue keeping the separation of code the best I could, I tried building modules for the first time. The slider and the switch were both made with the intention of having no program-specific logic in them. It should allow them to be imported into another PyGame application and be fully functional.

Finally, the algorithm chosen was a breadth-first search. This algorithm is the most intuitive to me, even though not the most efficient. Each orthogonally connected cell has a distance of 1 and each diagonally connected cell has a distance of about 1.412.

## Challenges
Several aspects of this project have proved to be challenging, but most were resolved. One issue that plagued the application for a while was a rounding error that was handled unnecessarily in very large grids. This led to weird situations where the grid could go from a suitable path to a wildly unsuitable one with a single wall placement.

Another solved challenge was getting the transparency of the grid to function correctly. PyGame has an issue where you can not make lines transparent if it is on the base surface, so it requires adding an additional surface that can handle them. Additionally, the grid lines even when fully transparent would still prevent other colors on the same surface from existing in that same space. It took a lot of fiddling around with different layers to get the colors to function as intended.

One core challenge I'm working on is improving the application to handle larger grids. At the moment when going above 1500ish cells, the algorithm slows enough to be noticeable while drawing walls or moving the starting point. This only gets more extreme as the grid grows. One solution I have implemented to help combat this is adding an early exit to the algorithm if the target cell is found. This helps reduce lag if not utilizing the whole grid. I also have added the ability to stop calculations in two ways. First, while drawing walls the algorithm freezes unless in "live update" mode. Live update mode is when the line is being displayed and the algorithm speed is set to "instant". The algorithm can be turned off entirely using a button. Additionally, I know the A* algorithm is likely more efficient for this project and I plan to implement it as well. 

The last major challenge I faced in the project was getting the algorithm to run "in the background" while the PyGame continued to draw frames. Initially, the algorithm calculation was one step of the update process, and when the algorithm got sufficiently slow enough, the whole application noticeably lagged as new frames could not be drawn until the algorithm finished. There were a few options I considered when trying to fix this issue: multithreading, multiprocessing, and asynchronous functions. I attempted to learn about and implement each of these, the most successful of which was running the algorithm in a different thread. But it wasn't perfect and there were many bugs to work out. In the discovery process of some solutions, I came across a 4th method that was better for my use case: tick rate. By adjusting the algorithm to only calculate X number of cells per frame, I could adjust how fast or how slow I wanted the algorithm to run. This led to a great new feature where I added a sliding bar to the window that allows the user to control how fast the algorithm runs, opening up the ability to see it working visually on the screen.

## Features Planned
The scope of this project has grown a little and I now want to implement the A* algorithm alongside the BFS algorithm. By giving the user an option to enable both and slow the tick rate, a visual comparison of the two algorithms will be shown.

Additionally, I am regularly thinking of different widgets (like the transparency slider) to try to add for more interaction. One button that is sorely needed is a "clear walls" button, for example.

## Images and GIFs

Example of live pathfinding while adding walls and moving endpoints.

![](./imgs/Pathing.gif)

Demonstration of features to alter the state of the application (grid transparency, removal of path visual).

![](./imgs/Features.gif)

Implementation of the tick rate system and a sliding bar allowing user control of algorithm calculation speed.
![](./imgs/Tick%20Rate.gif)
