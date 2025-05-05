import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# --- experiment parameters ---
x = 0.03678794411714429377085 #randomness begins at 1/10e
size = 100  # Size of the grid (size x size)
frames = 1  # Update frequency for plotting
starting_value = 0.8  # Default value to fill grid with if not messy or pattern
messy = False  # Whether to initialize grid with noisy values
use_pattern = False  # Whether to initialize grid with a predefined pattern
pattern = np.array([[1, 1, 0],
                    [1, 1, 0],
                    [0, 1, 0]])  # The predefined pattern to use if use_pattern is True


# ------------ code ------------
if use_pattern:              
    grid = np.zeros((size, size))  # Initialize empty grid
    center = size // 2  # Calculate grid center
    start_row = center - pattern.shape[0] // 2  # Starting row to center pattern
    start_col = center - pattern.shape[1] // 2  # Starting column to center pattern
    grid[start_row:start_row+pattern.shape[0], start_col:start_col+pattern.shape[1]] = pattern  # Place pattern at center

elif messy:
    grid = np.full((size, size), 0.8) + 0.05 * np.random.randn(size, size)  # Initialize grid with noisy values
    grid = np.clip(grid, 0, 1)  # Clip values to be between 0 and 1
else:
    grid = np.full((size, size), starting_value)  # Initialize grid with uniform starting value



def update(grid, x):
    new = grid.copy()  # Copy current grid to new grid
    for i in range(size):
        for j in range(size):
            # Calculate sum of neighbors (including diagonals)
            s = np.sum(grid[max(0, i-1):min(size, i+2), max(0, j-1):min(size, j+2)]) - grid[i, j]
            
            # Calculate change (delta) using Gaussian-like function and subtracting x
            delta = 0.1 * (np.exp(-(s-3)**2)) - x
            
            # Update cell value with delta and ensure it stays within [0, 1]
            value = grid[i, j] + delta
            if value < 0:
                new[i, j] = 0
            elif value > 1:
                new[i, j] = 1
            else:
                new[i, j] = value
    return new  # Return updated grid

plt.ion()  # Turn interactive mode on

fig, (ax_grid, ax_sum) = plt.subplots(2, 1, figsize=(6, 8))  # Create figure and subplots
plt.subplots_adjust(bottom=0.25)  # Make space for slider

im = ax_grid.imshow(grid, cmap='viridis', vmin=0, vmax=1)  # Display initial grid
plt.colorbar(im, ax=ax_grid)  # Add colorbar to grid plot
ax_grid.set_title("Gaussian Cellular Automaton")  # Title of grid plot

x_slider = Slider(ax=plt.axes([0.25, 0.1, 0.65, 0.03]), label='x', valmin=-0.01, valmax=0.1, valinit=x)  # Slider to control x parameter

sum_data = []  # List to store sum of grid values (living cells)
time_data = []  # List to store time steps

line, = ax_sum.plot([], [])  # Initialize line for sum plot
ax_sum.set_title("Living Cells")  # Title of sum plot
ax_sum.set_xlabel("Timestep")  # X-axis label
ax_sum.set_ylabel("Cells")  # Y-axis label
ax_sum.set_ylim(0, size * size)  # Set Y-axis limits
ax_sum.set_xlim(0, 500)  # Set initial X-axis limits

step = 0  # Initialize step counter

while True:
    grid = update(grid, x_slider.val)  # Update grid with current x value from slider
    

    if step % frames == 0:
        im.set_data(grid)  # Update grid image
        current_sum = np.sum(grid)  # Calculate sum of grid values
        sum_data.append(current_sum)  # Store current sum
        time_data.append(step)  # Store current step

        line.set_data(time_data, sum_data)  # Update sum plot
        ax_sum.set_xlim(time_data[0], time_data[-1] if time_data else 100)  # Adjust X-axis limits dynamically

        for txt in ax_sum.texts:
            txt.remove()  # Remove previous text labels

        ax_sum.text(time_data[-1], current_sum, f"{current_sum:.1f}", fontsize=9, verticalalignment='bottom')  # Add new text label showing current sum

    step += 1  # Increment step counter
    plt.pause(0.001)  # Pause briefly to allow plot update and interaction
