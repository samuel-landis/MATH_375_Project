import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Parameters
#x = 0.03678794411714429377085(randomness begins at aprox. 1/10e)
x = 0.0659          # Threshold parameter for cell change 
size = 100            # Size of the grid (100x100)
frames = 5 
starting_value = 0.8
messy = False
use_pattern = False
pattern = np.array([[1, 1, 0],
                    [1, 1, 0],
                    [0, 1, 0]])

if use_pattern:              
    grid = np.zeros((size, size))
    center = size // 2
    start_row = center - pattern.shape[0] // 2
    start_col = center - pattern.shape[1] // 2
    grid[start_row:start_row+pattern.shape[0], start_col:start_col+pattern.shape[1]] = pattern

elif messy:
    grid = np.full((size, size), 0.8) + 0.05 * np.random.randn(size, size)
    grid = np.clip(grid, 0, 1)
else:
    grid = np.full((size, size), starting_value)



# Define the update function for the cellular automaton
def update(grid, x):
    new = grid.copy()
    for i in range(size):
        for j in range(size):
            s = np.sum(grid[max(0, i-1):min(size, i+2), max(0, j-1):min(size, j+2)]) - grid[i, j]
            delta = 0.1 * (np.exp(-(s-3)**2)) - x
            value = grid[i, j] + delta
            if value < 0:
                new[i, j] = 0
            elif value > 1:
                new[i, j] = 1
            else:
                new[i, j] = value
    return new

plt.ion()

fig, (ax_grid, ax_sum) = plt.subplots(2, 1, figsize=(6, 8))
plt.subplots_adjust(bottom=0.25)

im = ax_grid.imshow(grid, cmap='viridis', vmin=0, vmax=1)
ax_grid.set_title("Gaussian Cellular Automaton")

x_slider = Slider(ax=plt.axes([0.25, 0.1, 0.65, 0.03]), label='x', valmin=-0.01, valmax=0.1, valinit=x)

sum_data = []
time_data = []

line, = ax_sum.plot([], [])
ax_sum.set_title("Living Cells")
ax_sum.set_xlabel("Timestep")
ax_sum.set_ylabel("Cells")
ax_sum.set_ylim(0, size * size)
ax_sum.set_xlim(0, 500)

step = 0

while True:
    grid = update(grid, x_slider.val)
    

    if step % frames == 0:
        im.set_data(grid)
        current_sum = np.sum(grid)
        sum_data.append(current_sum)
        time_data.append(step)

        line.set_data(time_data, sum_data)
        ax_sum.set_xlim(time_data[0], time_data[-1] if time_data else 100)

        # Clear previous numeric annotations
        for txt in ax_sum.texts:
            txt.remove()

        # Display numeric value of the sum
        ax_sum.text(time_data[-1], current_sum, f"{current_sum:.1f}", fontsize=9, verticalalignment='bottom')

    step += 1
    plt.pause(0.001)
