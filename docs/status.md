---
layout: default
title: Status
---

## Project Summary:

The Torchbearer A.I. has changed somewhat from our previous idea, in that its algorithms are not necessarily the same. Instead of randomly running down the series of coordinates given to it, hoping to find a good coordinate to jump off of, the A.I. now knows that an optimal solution is n-coordinates large; thus, it tries some (if not all) of the n-coordinate tests to see if it can come up with an optimal solution.

The goal of the A.I. is largely the same (in a grid nXn size, place just enough torches to light up the area), but two potential new goals include:
- Run the A.I. on grids with walls. This will effectively create two grids from one, as well as add an additional coordinate required to the n-coordinate optimal solution, but allows us to more accurately light up areas resembling actual rooms in Minecraft.
- ![image of walled grid](url)
- Run the A.I. on non-uniform patterns -- L-shapes, T-shapes, long I-shapes, U-shapes. This will give us a two additional problems to solve: non-uniform grids do not have the benefit of centralized solutions, where torches can be placed in the middle to cover the whole area; and we, as programmers, must determine what optimal solutions exist per non-uniform pattern. Once again, these patterns will more accurately resemble rooms that are actually built in Minecraft.
- ![image of odd grid](url)

Of course, these goals are rather lofty, as there are many more variables to consider outside of our simple grid system (how far does the wall go to block light? Can we make multiple grids for the A.I. to accurately travel on?), and we still have some issues to iron out before then. Still, they are things to consider as we go along with the project.

## Approach:

The Torchbearer A.I. determines the best locations to place torches in a grid by first determining the minimum amount of torches needed to light up the whole grid, then iterating over an n-sized combination of the valid coordinates of the grid, scoring each combination based on how many squares it left dark.

All of this is done in a brute-force algorithm, iterating over the whole list of n-sized combinations. We are currently working on optimizing the algorithm by breaking the grids into smaller chunks (submodular optimization), but the algorithm works fine for grids sized 7 and below in terms of time taken. Given *enough* time, the A.I. can actually find all solutions to an nXn grid; it just takes a very long while.

Our baseline test -- a 6x6 grid -- works like this:
- The minimum amount of torches is determined by the torches' reach.
  - In this case: a 6x6 grid fits into a single torch's light.
  - ![image showing square goes here](url for image goes here)
  - Mathematically, the minimum amount of torches needed is: 
    - int(math.floor(number/2)-2). 
  - In this case: 6/2 = 3; 3-2 = 1.
  - This has proven true so far for 9x9 squares and below.
- The amount of available combinations (nCr) of coordinates is determined by the minimum torches needed (1) and the amount of spaces (36).
  - In this case: n = 36, r = 1 -> 36 unique 1-sized combinations of coordinates. This list of coordinates is named **"startingList"** for the moment.
- The agent creates 6 lists, 6-size each, full of 0s to simulate the current light levels of the current test (named **"currentList"**).
- ![image showing initial 0s goes here](url for image goes here)
- The list of 36 combinations are then passed to the agent, who places a torch at each coordinate in the combination per test and checks the "score" of that placement:
  - First, the agent teleports to coordinate (x, z). This torch's coordinate in the **"currentList"** is determined first by its z-level, then by its x-level (so blocks at z-level 2 are in **currentList[1]**; a block at (3, 2) is at **currentList[1][2]**).
  - Then, the agent places a torch at its current position (x, z), in the Minecraft world.
  - After placing the torch, the agent updates what the new light levels of its surroundings should be.
    - The coordinate with the torch updates its number in **"currentList"** to 14 (**"initialNum"**).
    - ![image showing that update here](url)
    - For each coordinate in currentList that is not that coordinate, they update based on their taxicab distance away from the torch. This distance (**"tryNum"**) is equal to their difference in x coordinates + their difference in z coordinates.
    - ![image showing taxicab distance from Wikipedia article goes here](url for image goes here)
    - The new light level of that specific coordinate is equal to **"initialNum - tryNum"** unless said light level would be lower than it currently is.
    - ![image showing new light levels goes here](url for image goes here)
  - After placing all of its torches within the combination it is testing, the agent then "scores" the combination based on how many squares remain in the grid that have a light level of 7 or below. This score is named **"dark"**.
  - The combination is then placed into a dictionary **"scoredList"**, which has a variety of numeric keys and a list value. The combination is appended to the list with key **"dark"**; if that key does not exist, a new key is created with its value containing the combination.
    - An example of the **"scoredList"** would be **scoredList[1] == [[(1, 2)], [(1, 3)], [(2, 1)], [(2, 4)], [(3, 1)], [(3, 4)], [(4, 2)], [(4, 3)]]**.
    - ![image for scoredList[1]](url)
  - The agent then wipes the board of all torches and begins the next test.
- After testing and scoring each coordinate in **"startingList"**, the program runs over each score in **"scoredList"** that has a list of coordinates (or a len > 0). If that score is the lowest so far, it updates a variable "lowest" to keep track of the list.
- Finally, the program runs over the list of the lowest scoring combinations, printing each one to show the optimal combinations to place torches to light up the grid (in this case: (2, 2), (2, 3), (3, 2), (3, 3)), as well as the entirety of **"scoredList"** for viewing purposes. The in-game agent places a combination as an example optimal solution.
- ![image for scoredList goes here](url for image goes here)
- ![in-game image goes here](url for image goes here)

SCREENSHOTS GO HERE.

TODO: EVALUATION

TODO: VIDEO HERE

TODO: REMAINING GOALS AND CHALLENGES
