import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Parameters
x = 0.04              # Threshold parameter for cell change
size = 100            # Size of the grid (100x100)
z = 10                # Interval of steps to record living cell count
grid = np.zeros((size, size))  # Initialize the grid with zeros (dead cells)

# Define the initial pattern (3x3 block of live cells)
pattern = np.array([[1, 1, 0],
                    [1, 1, 0],
                    [0, 1, 0]])

# Place the pattern in the center of the grid
center = size // 2
start_row = center - pattern.shape[0] // 2
start_col = center - pattern.shape[1] // 2
grid[start_row:start_row+pattern.shape[0], start_col:start_col+pattern.shape[1]] = pattern

# Define the update function for the cellular automaton
def update(grid, x):
    new = grid.copy()  # Create a copy to store new values
    for i in range(size):
        for j in range(size):
            # Calculate sum of neighbors (excluding the cell itself)
            s = np.sum(grid[max(0, i-1):min(size, i+2), max(0, j-1):min(size, j+2)]) - grid[i, j]
            
            # Gaussian change rule
            delta = 0.1 * (np.exp(-(s-3)**2)) - x
            value = grid[i, j] + delta
            
            # Enforce boundaries (cell value between 0 and 1)
            if value < 0:
                new[i, j] = 0
            elif value > 1:
                new[i, j] = 1
            else:
                new[i, j] = value
    return new

# Enable interactive mode for plotting
plt.ion()

# Create figure and axes for grid and living cells plot
fig, (ax_grid, ax_sum) = plt.subplots(2, 1, figsize=(6, 8))
plt.subplots_adjust(bottom=0.25)  # Adjust space for the slider

# Display the initial grid
im = ax_grid.imshow(grid, cmap='viridis', vmin=0, vmax=1)
ax_grid.set_title("Gaussian Cellular Automaton")

# Create a slider to control the 'x' parameter interactively
x_slider = Slider(ax=plt.axes([0.25, 0.1, 0.65, 0.03]), label='x', valmin=0.0, valmax=0.09, valinit=x)

# Prepare lists to store sum of living cells over time
sum_data = []
time_data = []

# Setup the plot for the living cells count
line, = ax_sum.plot([], [])
ax_sum.set_title("Living Cells")
ax_sum.set_xlabel("Timestep")
ax_sum.set_ylabel("Cells")
ax_sum.set_ylim(0, size * size)
ax_sum.set_xlim(0, 500)

# Simulation step counter
step = 0

# Lists to hold living cell counts and time steps (redundant init but harmless)
sum_data = []
time_data = []

# Main loop to run the simulation
while True:
    grid = update(grid, x_slider.val)  # Update grid based on current x value
    im.set_data(grid)                  # Update grid visualization

    # Record data every z steps
    if step % z == 0:
        current_sum = np.sum(grid)         # Sum of living cells
        sum_data.append(current_sum)       # Add to sum data
        time_data.append(step)             # Add corresponding timestep

        # Update the living cells plot
        line.set_data(time_data, sum_data)
        ax_sum.set_xlim(time_data[0], time_data[-1] if time_data else 100)

    step += 1
    plt.pause(0.001)  # Pause briefly to allow plot to update (animation)