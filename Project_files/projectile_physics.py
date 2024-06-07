import math


def physics_sim(velocity: float, angle: float) -> tuple[float]:
    """
    Simulates projectile motion given initial velocity and launch angle.

    Parameters:
        velocity (float): Initial velocity of the projectile.
        angle (float): Launch angle of the projectile in degrees.

    Returns:
        tuple: Tuple containing the horizontal range and maximum height of the projectile.
    """
    # Convert angle from degrees to radians
    angle_rad = math.radians(angle)

    # Calculate horizontal and vertical components of velocity
    x_velocity = velocity * math.cos(angle_rad)
    y_velocity = velocity * math.sin(angle_rad)

    # Calculate time of flight
    time_of_flight = (2 * y_velocity) / 9.81

    # Calculate horizontal range
    horizontal_range =  x_velocity * time_of_flight

    # Calculate maximum height
    max_height = (y_velocity ** 2) / (2 * 9.81)

    return horizontal_range, max_height
