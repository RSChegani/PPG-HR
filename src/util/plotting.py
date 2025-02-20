import matplotlib.pyplot as plt
import numpy as np

def plot_grid(
    x_vectors_list: list, 
    y_vectors_list: list = None,
    titles: list = None, 
    overal_title: str = '',
    n_rows: int = 1, 
    n_cols: int = 1, 
    color_values: list = ['blue'], 
    x_label: str = '', 
    y_label: str = '', 
    sampling_freq: int = 0,
    figure_size: tuple = (6,8), 
    xlim: tuple = None, 
    ylim: tuple = None):
    """Plots a grid of subplots for given vectors.

    Args:
        vectors_list (list): List of 1D arrays to plot.
        titles (list, optional): Titles for each subplot.. Defaults to None.
        n_rows (int, optional): Number of subplot rows. Defaults to 1.
        n_cols (int, optional): Number of subplot columns. Defaults to 1.
        color_values (list, optional): List of colors for each vector. Defaults to ['blue'].
        x_label (str, optional): X-axis label. Defaults to ''.
        y_label (str, optional): Y-axis label. Defaults to ''.
        sampling_freq (int, optional): Sampling frequency (if applicable). Defaults to 0.
        figure_size (tuple, optional): Size of the figure. Defaults to (6,8).
        xlim (tuple, optional): X-axis limits (min, max). Defaults to None.
        ylim (tuple, optional): Y-axis limits (min, max). Defaults to None.
    """
    num_plots = len(x_vectors_list)

    # Default values
    if titles is None:
        titles = [''] * num_plots
    if len(color_values) < num_plots:
        color_values = ['blue'] * num_plots

    # Time vector
    time_values = np.arange(len(x_vectors_list[0])) / sampling_freq if sampling_freq else np.arange(len(x_vectors_list[0]))
    
    fig, axs = plt.subplots(nrows = n_rows, ncols = n_cols, figsize = figure_size)
    for i in range(num_plots):
        # Plot data in each subplot
        axs[i].grid(alpha = 0.25)
        if y_vectors_list:
            axs[i].plot(x_vectors_list[i], y_vectors_list[i], color=color_values[i])
        else:
            axs[i].plot(time_values, x_vectors_list[i], color=color_values[i])
        axs[i].set_title(titles[i])
        axs[i].set_xlabel(x_label)
        axs[i].set_ylabel(y_label)
        if xlim:
            axs[i].set_xlim(xlim)
        if ylim:
            axs[i].set_ylim(ylim)
    
    fig.suptitle(overal_title, fontsize=14, fontweight="bold")
    plt.tight_layout(h_pad=2.0)
    plt.show()

    
