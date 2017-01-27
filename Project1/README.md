# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Naked Twins are pairs of boxes in a sudoku that belong to the same unit(row , column or 3x3 group/sqaure) and have the same possibility of digits however each box should only have a possibility of 2 digits , ie length = 2. If such a case exists then we conclude that these 2 digits can occur only in these 2 boxes and no where else. Hence we remove the 2 digits from their entire unit. This is how Naked twins creates a Constraint and we can then propogate further on this constraint to reduce our Search/State space.
# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We know the following constraints for a normal sudoku :
(1) If a square has only one possible value, then eliminate that value from the square's peers. 
(2) If a unit has only one possible place for a value, then put the value there.
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
