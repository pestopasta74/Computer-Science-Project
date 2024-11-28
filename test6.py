import numpy as np
import matplotlib.pyplot as plt

def calculate_gravitational_potential():
    # Earth's radius and mass constants
    R_earth = 6371000  # meters
    M_earth = 5.97e24  # kg
    G = 6.67430e-11  # gravitational constant

    # Create distance array from Earth's center
    # Extend from 0 to 3x Earth's radius
    distances = np.linspace(0, 3 * R_earth, 300)

    # Calculate gravitational potential
    def potential(r):
        # Inside the Earth (r < R)
        inside_earth = -G * M_earth * (3 * R_earth**2 - r**2) / (2 * R_earth**3)

        # Outside the Earth (r > R)
        outside_earth = -G * M_earth / r

        # Combine with a conditional
        return np.where(distances <= R_earth, inside_earth, outside_earth)

    # Calculate potential values
    V_values = potential(distances)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(distances / 1000, V_values, 'g-', linewidth=2)

    # Annotate key regions
    plt.axvline(x=R_earth/1000, color='r', linestyle='--', label="Earth's Surface")

    # Annotations for relationships
    plt.annotate('V ∝ r² (Inside Earth)',
                 xy=(R_earth/2000, V_values[len(V_values)//4]),
                 xytext=(10, 30),
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle='->'))

    plt.annotate('V ∝ 1/r (Outside Earth)',
                 xy=(2*R_earth/1000, V_values[-50]),
                 xytext=(10, -30),
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle='->'))

    plt.title('Gravitational Potential vs Distance from Earth\'s Center')
    plt.xlabel('Distance from Earth\'s Center (km)')
    plt.ylabel('Gravitational Potential (J/kg)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Highlight the point at Earth's surface
    surface_index = np.argmin(np.abs(distances - R_earth))
    plt.scatter(distances[surface_index]/1000, V_values[surface_index],
                color='red', s=100, zorder=5,
                label='Potential at Earth\'s Surface')

    plt.tight_layout()
    plt.show()

# Run the function
calculate_gravitational_potential()