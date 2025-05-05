import numpy as np
import matplotlib.pyplot as plt


# --- experiment parameters ---
messy = True  # Whether to start grid with random noisy values
size     = 20  # Grid size (size x size)
steps    = 500  # Number of steps per simulation run
runs     = 10  # How many independent runs per x value
frames   = 250  # How often to update the visualization
x_values = np.linspace(-0.005, 0.08, 100)  # Values of x to test across the experiment


# ------------ code ------------
def update(grid, x):
    size = grid.shape[0]  # Get grid size
    new = grid.copy()  # Copy grid to avoid in-place modification
    for i in range(size):
        for j in range(size):
            # Sum of neighboring cells including diagonals (but exclude self)
            s = np.sum(grid[max(0, i-1):i+2, max(0, j-1):j+2]) - grid[i, j]
            
            # Calculate delta using Gaussian-like function
            delta = 0.1 * np.exp(-(s-3)**2) - x
            
            # Update cell value and clip to [0, 1] range
            new[i, j] = np.clip(grid[i, j] + delta, 0, 1)
    return new  # Return updated grid


plt.ion()  # Turn interactive plotting on
fig, (ax_grid, ax_mean, ax_std) = plt.subplots(3, 1, figsize=(6, 12))  # Create subplots for grid, mean, and std plots
plt.subplots_adjust(hspace=0.4)  # Add space between subplots
im = ax_grid.imshow(np.zeros((size, size)), cmap='viridis', vmin=0, vmax=1)  # Initialize grid display
plt.colorbar(im, ax=ax_grid)  # Add colorbar for grid plot


# Initialize mean plot
line_mean, = ax_mean.plot([], [], label=f"Mean of Total Cells", linewidth=2)
ax_mean.set_ylabel(f"Mean")  # Y-axis label
ax_mean.set_xlabel("x")  # X-axis label
ax_mean.set_xlim(x_values[0], x_values[-1])  # Set X-axis range
ax_mean.set_ylim(0, 1)  # Set Y-axis range for mean
ax_mean.legend()  # Show legend
ax_mean.set_title(f"Average Total Cells vs X Parameter (steps: {steps}, size of grid: {size}, runs: {runs}, random starting grid: {messy})")  # Title

# Initialize std deviation plot
line_std, = ax_std.plot([], [], label=f"Std Dev of Total Cells", linewidth=2)
ax_std.set_ylabel(f"σ")  # Y-axis label
ax_std.set_xlabel("x")  # X-axis label
ax_std.set_xlim(x_values[0], x_values[-1])  # Set X-axis range
ax_std.set_ylim(0, 0.25)  # Set Y-axis range for std dev
ax_std.legend()  # Show legend
ax_std.set_title(f"Variability of Total Cells vs X Parameter (steps: {steps}, size of grid: {size}, runs: {runs}, random starting grid: {messy})")  # Title

mean_of_means = []  # Store mean cell values per x value
std_of_means  = []  # Store std deviation of cell values per x value

for xi in x_values:
    ax_grid.set_title(f"Running with x = {xi:.4f}")  # Update grid title with current x
    final_means = []  # Store final grid means for each run at this x

    for run in range(runs):
        if messy:
            # Initialize grid with random noise around 0.8
            grid = np.full((size, size), 0.8) + 0.05 * np.random.randn(size, size)
            grid = np.clip(grid, 0, 1)
        else:
            # Initialize grid uniformly if not messy
            starting_value = 0.8
            grid = np.full((size, size), starting_value)
        
        # Run simulation for defined steps
        for t in range(steps):
            grid = update(grid, xi)  # Update grid at each step
            
            if (t % frames) == 0:
                im.set_data(grid)  # Update grid plot
                fig.canvas.draw()  # Redraw plot
                plt.pause(0.0001)  # Pause briefly to allow update

        final_means.append(grid.mean())  # Record mean cell value at end of run

    mean_of_means.append(np.mean(final_means))  # Average of means from all runs
    std_of_means.append(np.std(final_means))  # Std deviation of means from all runs

    xs = x_values[: len(mean_of_means)]  # X-axis data for plots
    line_mean.set_data(xs, mean_of_means)  # Update mean plot
    line_std .set_data(xs, std_of_means)  # Update std dev plot
    fig.canvas.draw()  # Redraw plots
    plt.pause(0.001)  # Pause briefly to keep plots responsive

plt.ioff()  # Turn interactive plotting off
plt.show()  # Display final plots
