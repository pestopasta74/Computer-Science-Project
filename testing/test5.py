import numpy as np
import matplotlib.pyplot as plt

def calculate_gravitational_field_strength():
    # Constants
    R_EARTH = 6371000  # Earth's radius in meters
    M_EARTH = 5.97e24  # Earth's mass in kilograms
    G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2

    # Distance array: from Earth's center to 3 times its radius
    distances = np.linspace(0, 3 * R_EARTH, 300)

    # Calculate gravitational field strength
    def field_strength(r):
        # Gravitational field inside Earth (r <= R_EARTH)
        inside_earth = G * M_EARTH * r / (R_EARTH**3)

        # Gravitational field outside Earth (r > R_EARTH)
        outside_earth = G * M_EARTH / (r**2)

        # Use conditional logic to combine results
        return np.where(r <= R_EARTH, inside_earth, outside_earth)

    # Compute field strengths for all distances
    g_values = field_strength(distances)

    # Plot setup
    plt.figure(figsize=(10, 6))
    plt.plot(distances / 1000, g_values, 'b-', linewidth=2, label='Gravitational Field Strength')

    # Earth's surface indicator
    plt.axvline(x=R_EARTH / 1000, color='r', linestyle='--', label="Earth's Surface (R)")

    # Annotate the inside-Earth relationship (g ∝ r)
    plt.annotate('g ∝ r (Inside Earth)',
                 xy=(R_EARTH / 2000, max(g_values) / 2),
                 xytext=(-90, 50),
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='black'),
                 fontsize=10)

    # Annotate the outside-Earth relationship (g ∝ 1/r²)
    plt.annotate('g ∝ 1/r² (Outside Earth)',
                 xy=(2 * R_EARTH / 1000, g_values[200]),  # Place closer to the curve
                 xytext=(50, -50),                      # Adjusted offset for better visibility
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='black'),
                 fontsize=10)


    # Highlight the maximum gravitational field strength at Earth's surface
    max_g_index = np.argmax(g_values)
    plt.scatter(distances[max_g_index] / 1000, g_values[max_g_index],
                color='red', s=100, zorder=5,
                label='Maximum Field Strength')

    # Labels, title, and grid
    plt.title('Gravitational Field Strength vs Distance from Earth\'s Center', fontsize=14)
    plt.xlabel('Distance from Earth\'s Center (km)', fontsize=12)
    plt.ylabel('Gravitational Field Strength (m/s²)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    # Legend
    plt.legend(fontsize=10)

    # Ensure layout is neat
    plt.tight_layout()

    # Show the plot
    plt.show()

# Run the function
calculate_gravitational_field_strength()
