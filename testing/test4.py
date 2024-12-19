import matplotlib.pyplot as plt
import numpy as np

def create_hr_diagram():
    # Define temperature and luminosity ranges for different star regions
    temperatures = np.linspace(3000, 30000, 1000)

    # Main sequence band
    ms_luminosity_upper = 10**((4.5 - np.log10(temperatures)) * 0.8)
    ms_luminosity_lower = 10**((4.5 - np.log10(temperatures)) * 1.2)

    # Giant stars
    giants_luminosity = 10**((5.5 - np.log10(temperatures)) * 0.7)

    # Supergiants
    supergiants_luminosity = 10**((6 - np.log10(temperatures)) * 0.5)

    # White dwarfs
    wd_luminosity = 10**((2.5 - np.log10(temperatures)) * 1.3)

    # Create the plot
    plt.figure(figsize=(10, 8))

    # Plot main sequence region
    plt.fill_between(temperatures, ms_luminosity_lower, ms_luminosity_upper, color='blue', alpha=0.3, label='Main Sequence')

    # Plot giant stars
    plt.plot(temperatures, giants_luminosity, color='orange', linestyle='--', label='Giants')

    # Plot supergiants
    plt.plot(temperatures, supergiants_luminosity, color='red', linestyle='-', label='Supergiants')

    # Plot white dwarfs
    plt.plot(temperatures, wd_luminosity, color='gray', linestyle=':', label='White Dwarfs')

    # Plot the Sun
    sun_temperature = 5778  # K
    sun_luminosity = 1  # L☉
    plt.scatter(sun_temperature, sun_luminosity, color='yellow', edgecolor='k', s=100, label='Sun')

    # Logarithmic scales
    plt.xscale('log')
    plt.yscale('log')

    # Reverse the x-axis (hot stars on the left)
    plt.gca().invert_xaxis()

    # Add labels and title
    plt.xlabel("Temperature (K, decreasing)", fontsize=12)
    plt.ylabel("Luminosity (L☉, logarithmic)", fontsize=12)
    plt.title("Hertzsprung-Russell Diagram", fontsize=14)

    # Add legend
    plt.legend(fontsize=10, title="Regions", loc="upper right")

    # Add a fine grid
    plt.grid(alpha=0.3)

    # Add ticks with finer steps
    temperature_ticks = [3000, 4000, 5000, 6000, 7000, 10000, 15000, 20000, 30000]
    luminosity_ticks = [0.01, 0.1, 1, 10, 100, 1000, 10000]
    plt.xticks(temperature_ticks, labels=[f"{t}" for t in temperature_ticks])
    plt.yticks(luminosity_ticks, labels=[f"{l}" for l in luminosity_ticks])

    # Show the plot
    plt.show()

# Run the function
create_hr_diagram()