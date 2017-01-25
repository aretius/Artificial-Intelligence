# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Using constraint propogation we first find all the boxes having possible values equal to 2 that is length = 2. After applying  this constraint we can then look for pairs of such boxes having number of values 2 and the possible digits equal and both of them being in each other's peer list. With this we finally eliminate those 2 digits from the other boxes/cells of the peer list into which both the selected twins/pairs belong to.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: For Diagonal Sudoku the constraint that all the numbers on both the diagonals( main one ) should be unique that is each of them should occur once helps in reducing the search space. The normal constraints that each group( 3x3 cell) should have each digit only once and similar for rows and columns too apply. We can further use Naked Twins strategy to reduce the search space of DFS even more.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in function.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.