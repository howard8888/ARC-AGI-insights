#!/usr/bin/env python
##PRAGMAS
# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=broad-exception-caught
# pylint: disable=pointless-string-statement
"""
arc_viewer.pylint

The main purpose of this code at this time is simply to access the ARC
challenge and testing examples which are posted on GitHub on
Chollet's page github.com/fchollet/arc-agi

In Chollet's ARC-AGI GitHub subdirectory 'data' note that there is a set of 'evaluation' examples and
a set of 'training' examples.

As the code is developed we will take instinctive primitives out of the
Causal Cognitive Architecture 8 (CCA8) and use them for the ARC Challenge.

Code currently written for Windows/DOS environment but should run with minimal changes in other operating systems
(pathlib should be swapped in for path operations for best cross-platform compatibility).

Written by Howard Schneider, August 2024
Free, open-source for anyone who wants to use.

"""


##IMPORTS
import json
import sys
import os
from typing import List, Dict, Any
try:
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
except Exception as e:
    print(f'Error importing a Python library with error:  {e}')
    print('Program will terminate as a result since will not run otherwise. Please fix this issue.\n')
    sys.exit(1)


##CONSTANTS
#if you go to github.com/fchollet/ARC-AGI you will find the ARC data
#copy them over to your computer and put the path into the constants below
TRAINING_FILES = r'C:\Users\howar\ARC\data\training'
EVAL_FILES = r'C:\Users\howar\ARC\data\evaluation'


##FUNCTIONS, METHODS
#consider putting into class in future work
def load_arc_dataset(dataset_path, debug=False) -> List[Dict[str, Any]]:
    """
    Load all the JSON files in the dataset directory
    Note that in calling function (main() at present) the following are declared:
    (at time of writing; this will change in near-future)
               dataset_path = TRAINING_FILES
            or dataset_path = EVAL_FILES
    And in turn, note that in CONSTANTS the following are declared:
            (note: Win OS gives file path with backslashes which I copied below,
            albeit adding an 'r' to deal with issues, but backslashes will have effects
            on comments so I just told the editor to reverse them to slashes here)
            TRAINING_FILES = r'C:/Users/howar/ARC/data/training'
            EVAL_FILES = r'C:/Users/howar/ARC/data/evaluation'

    Note that each element (i.e, 'filename') in the loop below (for TRAINING_FILES) consists of
    a Python dictionary with two keys, 'train' and 'test'.
    -The 'train' key's value will consist of a list of dictionaries, i.e., [{ }, {  }, .... {   }] ].
    Each of these dictionaries will have two keys consisting of
    'input' and 'output', and values for 'input' and 'output' are the
    input grid (i.e., an array in Python [[..], [...], ... [...]] style) and the output grid.
    -The 'test' key's value is a list, i.e., [ .....], containing a single dictionary. This dictionary
    contains two keys, again consisting of 'input' and 'output', and the values for these keys again
    consisting of grids for each.

    Parameters:
        dataset_path (str): The path where the JSON files are located.
        debug (bool): If True, prints additional debug information.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing an ARC problem.
    """
    dataset: List[Dict[str, Any]] = []
    #append ARC-AGI database into array dataset
    try:
        for filename in os.listdir(dataset_path):  #copied from GitHub to local machine, e.g., r'C:/Users/howar/ARC/data/training'
            if filename.endswith(".json"):
                with open(os.path.join(dataset_path, filename), encoding='utf-8') as f:
                    data = json.load(f)
                    dataset.append(data)

                    if debug:
                        print(filename, "----", data, '\n')
                        print(f"Number of records read from 'dataset' so is: {len(dataset)} \n")
                        input('Press for next data item')
    #quality control
    except Exception as e:
        print(f'Error trying to read the ARC challenge database,  with detected error:  {e}')
        print('Please check the specified path to see if it is valid.')
        print('Program will terminate as a result since will not run otherwise. Please fix this issue.\n')
        sys.exit(1)
    if len(dataset) == 0:
        print('Debug note: No elements detected in dataset variable read and appended from the ARC database')
        print('Program will terminate as a result since will not run properly. Please fix this issue.\n')
        sys.exit(1)
    for i, element in enumerate(dataset):
        if not isinstance(element, dict):
            print(f'Debug note: Element at index {i} in dataset is not a Python dictionary.')
            print('Program will terminate as a result since it will not run properly. Please fix this issue.\n')
            if input('Press any key to terminate the program or enter "s" to stop termination and continue running.') != 's':
                sys.exit(1)
    if debug:
        print("\n dataset list has been generated from the ARC database and passed (or allowed) initial quality checks.\n")
    # return ARC-AGI database now written in array dataset
    return dataset


def display_grid(grid, title)-> None:
    """
    Display the grid and its Python-like representation.
    Each grid is represented as a list of lists, with each
    list being a row, starting from the top of the grid.
    The values in each list represent the colors of that grid row:
        black 0, blue 1, red 2, green 3, yellow 4, grey 5, pink 6, orange 7, cyan 8, brown 9

    Parameters:
        grid (List[List[int]]): A 2D list representing the grid, where each inner list is a row of the grid.
        title (str): The title of the grid to be displayed in the terminal.

    Returns:
        None
    """
    print(f"{title} (Grid {len(grid)}x{len(grid[0])}):")
    for row in grid: #row #0 represents the top row of the grid
        print(row)
    print()


def plot_grid_with_labels(ax, grid, title)-> None:
    """
    Display a grid on the desktop using matplotlib
    We set up colors corresponding to those specified by the ARC challenge
    We add titles and count the grid squares starting from #1 (arbitrary)

    Parameters:
        ax (plt.Axes): matplotlib axes object to plot on
        grid (List[List[int]]): 2D list representing the grid, where each inner list is a row of the grid
        title (str): title of the plot.

    Returns:
        None


    """
    #set up colors for matplotlib  (these colors are specified by the ARC challenge)
    color_map = {
        0: 'black',
        1: 'blue',
        2: 'red',
        3: 'green',
        4: 'yellow',
        5: 'gray',
        6: 'pink',
        7: 'orange',
        8: 'cyan',
        9: 'brown'
    }
    cmap = mcolors.ListedColormap([color_map[i] for i in range(10)])
    norm = mcolors.BoundaryNorm(range(11), cmap.N)
    #display grid image, including title and axes, with matplotlib
    #note attempt to display each coordinate of data in its own separate grid cell
    ax.imshow(grid, cmap=cmap, norm=norm, interpolation="nearest", origin='upper')
    ax.set_title(title)
    ax.set_xticks(range(len(grid[0])))
    ax.set_yticks(range(len(grid)))
    ax.set_xticklabels([str(i + 1) for i in range(len(grid[0]))])
    ax.set_yticklabels([str(i + 1) for i in range(len(grid))])
    for x in range(len(grid[0]) + 1):
        ax.axvline(x - 0.5, color='white', linewidth=2)
    for y in range(len(grid) + 1):
        ax.axhline(y - 0.5, color='white', linewidth=2)
    ax.tick_params(axis='both', which='both', length=0)


def display_example(example, example_idx)-> None:
    """
    Display the ARC example using matplotlib for visualized images of the grids,
    and then as the lists of rows each grid is represented as in the terminal

    Parameters:
        example (Dict[str, Any]): The example data containing grids to display.
        example_idx (int): The index of the example being displayed.

    Returns:
        None
    """
    print(f'\nPROBLEM NUMBER {example_idx}')
    print('PLEASE KEEP CLOSING THE DESKTOP IMAGES SO THE PROGRAM KEEPS GOING FORWARD')
    print('The visual representations of the selected ARC examples and their solutions are shown')
    print('via matplotlib on your desktop (not in the terminal screen). Then the test example is shown (on')
    print('the desktop) for you to figure out. However, if you close it then it will be shown again with the solution.')
    print('\nThen if you look at the terminal screen (i.e., where you are reading this now), you will see')
    print('the Python representation (i.e., the lists of each row in the grids) of the grids just')
    print('diagrammatically shown. (The rows are listed from the top of the grid.)')
    print('"Input Grid" means the example and "Output Grid" means the solution to the example.')
    print('"Train" means the examples to train you, and "Test" means example for you to try out.')
    print('color values: black 0, blue 1, red 2, green 3, yellow 4, grey 5, pink 6, orange 7, cyan 8, brown 9)\n')
    print(f'raw data for "example" parameter: {example}\n')

    #display each training example and its solution side by side
    if 'train' in example:  #make sure there is a 'train' key
        for idx, task in enumerate(example['train']):
            input_grid = task['input']
            output_grid = task['output']
            #terminal display
            display_grid(input_grid, f"PROBLEM {example_idx}: Training (i.e. example) Input Grid #{idx + 1}")
            display_grid(output_grid, f"PROBLEM {example_idx}: Training (i.e., example solution) Output Grid #{idx + 1}")
            #matplotlib display
            _, axes = plt.subplots(1, 2, figsize=(8, 4))
            plot_grid_with_labels(axes[0], input_grid, f"Training Example #{idx + 1}")
            plot_grid_with_labels(axes[1], output_grid, f"Solution #{idx + 1}")
            plt.show()


    #now display the text example by itself, and then with its solution
    if 'test' in example and len(example['test']) > 0:  #make sure there is a valid 'test' key
        first_test_input = example['test'][0]['input']
        first_test_output = example['test'][0]['output']
        #terminal display of the test example and solution
        display_grid(first_test_input, f"PROBLEM {example_idx}:Test Input Grid #1")
        display_grid(first_test_output, f"PROBLEM {example_idx}:Test Output Grid #1")
        #matplotlib display of test grid
        _, ax = plt.subplots(figsize=(4, 4)) #size for one grid
        plot_grid_with_labels(ax, first_test_input, "Solve This (Test Example #1)")
        plt.show()
        #matplotlib display of test grid along with solution grid
        _, axes = plt.subplots(1, 2, figsize=(8, 4)) #size for two grids
        plot_grid_with_labels(axes[0], first_test_input, "Solve This (Test Example #1)")
        plot_grid_with_labels(axes[1], first_test_output, "The Solution (Test Example #1)")
        plt.show()


def visualize_ARCproblems() -> None:
    """
    Allows visualization of the ARC problems taken from the GitHub ARC-AGI challenge database.
    As well, also provides the list of values in each of the rows of the problem grids.
    User can choose between the training files and the evaluation files, and then can choose the
    problem number to display, i.e., the examples and test example of the problem.

    Returns:
        None
    """
    print("\nARC-AGI database visualization.")
    dataset_path_e = EVAL_FILES
    dataset_path_t = TRAINING_FILES
    dataset_e = load_arc_dataset(dataset_path_e)
    dataset_t = load_arc_dataset(dataset_path_t)
    while True:
        if input("For default training files press ENTER, for evaluation files press 'e' and then ENTER:") == 'e':
            dataset = dataset_e
            print("The dataset containing the ARC-AGI evaluation files has been chosen.")
        else:
            dataset = dataset_t
            print("The dataset containing the ARC-AGI training files has been chosen.")
        print(f"Loaded {len(dataset)} problems. Please enter the problem number to display (0-{len(dataset)-1}), or 'q' to quit:")
        user_selection = input("Enter problem number: ")
        if user_selection.lower() == 'q':
            break
        try:
            example_idx = int(user_selection)
            if 0 <= example_idx < len(dataset):
                display_example(dataset[example_idx], example_idx)
            else:
                print(f"Invalid problem number selected. Please enter a number between 0 and {len(dataset)-1}.")
                print("Select again the training set you want then then the problem number.\n")
        except ValueError:
            print("Please enter a valid number.")
            print("Select again the training set you want then then the problem number.\n")


##MAIN
def main()-> None:
    """
    At this point just calls the ARC-AGI viewer.
    Future additions to allow solutions to the ARC challenge.
    """
    visualize_ARCproblems()
    print('Thank you for using the ARC-AGI viewer.\n')


if __name__ == "__main__":
    #note that if arc_viewer.py is not run from the command line, main() will not run, but can use
    #the various functions and classes of this module
    main()
