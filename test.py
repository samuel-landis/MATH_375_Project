import numpy as np
import matplotlib.pyplot as plt

# --- your update rule unchanged ---
def update(grid, x):
    size = grid.shape[0]
    new = grid.copy()
    for i in range(size):
        for j in range(size):
            s = np.sum(grid[max(0, i-1):i+2, max(0, j-1):j+2]) - grid[i, j]
            delta = 0.1 * np.exp(-(s-3)**2) - x
            new[i, j] = np.clip(grid[i, j] + delta, 0, 1)
    return new

# --- experiment parameters ---
messy = True
size     = 6
steps    = 300
runs     = 40
frames   = 50         # only redraw every 5 steps to speed up animation
x_values = np.linspace(-0.005, 0.08, 200)
#x_values = np.linspace(0.04, 0.05, 10)
# --- set up interactive plotting ---
plt.ion()
fig, (ax_grid, ax_mean, ax_std) = plt.subplots(3, 1, figsize=(6, 12))
plt.subplots_adjust(hspace=0.4)

# image for the CA
im = ax_grid.imshow(np.zeros((size, size)), cmap='viridis', vmin=0, vmax=1)
ax_grid.set_title("")

# lines for summary stats
line_mean, = ax_mean.plot([], [], label="mean of final means")
ax_mean.set_ylabel("Mean(cell value)")
ax_mean.set_xlim(x_values[0], x_values[-1])
ax_mean.set_ylim(0, 1)
ax_mean.legend()

line_std, = ax_std.plot([], [], label="std of final means")
ax_std.set_ylabel("Std(cell value)")
ax_std.set_xlabel("x")
ax_std.set_xlim(x_values[0], x_values[-1])
ax_std.set_ylim(0, 0.3)
ax_std.legend()

mean_of_means = []
std_of_means  = []

for xi in x_values:
    ax_grid.set_title(f"Running CA at x = {xi:.4f}")
    final_means = []

    for run in range(runs):
        # start from slightly noisy 0.8 grid
        if messy:
            grid = np.full((size, size), 0.8) + 0.05 * np.random.randn(size, size)
            grid = np.clip(grid, 0, 1)
        else:
            starting_value = 0.8
            grid = np.full((size, size), starting_value)
        for t in range(steps):
            grid = update(grid, xi)
            # animate every `frames` steps
            if (t % frames) == 0:
                im.set_data(grid)
                fig.canvas.draw()
                plt.pause(0.0001)

        final_means.append(grid.mean())

    # collect across-run stats for this xi
    mean_of_means.append(np.mean(final_means))
    std_of_means.append(np.std(final_means))
    # update summary plots
    xs = x_values[: len(mean_of_means)]
    line_mean.set_data(xs, mean_of_means)
    line_std .set_data(xs, std_of_means)
    fig.canvas.draw()
    plt.pause(0.001)

plt.ioff()
plt.show()