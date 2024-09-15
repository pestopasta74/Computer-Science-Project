import math


class Physics:
    def __init__(
            self,
            initial_velocity=None,
            final_velocity=None,
            theta=45,
            starting_displacement=None,
            gravity=-9.81
        ):
        self.acceleration = gravity
        self.initial_velocity = initial_velocity
        self.starting_displacement = starting_displacement
        self.theta = theta
        self.final_velocity = final_velocity

        # Only one of S, U, V and A can be None
        possible_none = [self.starting_displacement, self.initial_velocity, self.final_velocity, self.acceleration]
        none_variables = sum([1 for var in possible_none if var is None])
        assert none_variables == 1, "Only one of S, U, V and A can be None"
        self.frame = 0

    def calculate(self, t=0):
        """
        Calculate the missing variable at a given time t
        """
        if self.starting_displacement is None:
            # S = Ut + 0.5 * A * t^2
            return self.initial_velocity * t + 0.5 * self.acceleration * t ** 2
        elif self.initial_velocity is None:
            # U = V - At
            return self.starting_displacement - 0.5 * self.acceleration * t ** 2
        elif self.final_velocity is None:
            # V = U + At
            return self.initial_velocity + self.acceleration * t
        elif self.acceleration is None:
            # A = (V - U) / t
            return (self.final_velocity - self.initial_velocity) / t

    def state(self, t=0):
        missing = self.calculate(t)
        return {
            "initial_velocity": self.initial_velocity or missing,
            "final_velocity": self.final_velocity or missing,
            "theta": self.theta,
            "starting_displacement": self.starting_displacement or missing,
            "acceleration": self.acceleration or missing,
            "time": t
        }

    @property
    def landing_x(self):
        xv = math.cos(math.radians(self.theta)) * self.initial_velocity
        # Using s = vt
        return xv * self.landing_time

    @property
    def landing_time(self):
        # There will be 2 landing times, one on/before the start and one after
        # We want the one after the start
        # Find where y = 0 and t > 0
        state = self.state()
        a = 0.5 * state["acceleration"]
        b = state["initial_velocity"] * math.sin(math.radians(state["theta"]))
        c = state["starting_displacement"]
        # Use the quadratic formula
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return 0
        t1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return max(t1, t2)

    @property
    def max_height(self):
        state = self.state()
        return state["initial_velocity"] ** 2 * math.sin(math.radians(state["theta"])) ** 2 / (2 * -state["acceleration"])

    @property
    def x_at_max_height(self):
        state = self.state()
        return state["initial_velocity"] ** 2 * math.sin(math.radians(state["theta"])) ** 2 / -state["acceleration"]

    def porabola(self, t_cutoff=0, steps=100):
        self.frame += 1
        x = []
        y = []
        # Generate 100 steps from t=0 and t=landing_time
        for i in range(steps + 1):
            t = self.landing_time * i / steps
            state = self.state(t)
            # Filter out any times less than t_cutoff
            if t < t_cutoff:
                continue
            # Using s = vt
            x.append(state["initial_velocity"] * t * math.cos(math.radians(state["theta"])))
            # Using s = ut + 0.5 * a * t^2
            y.append(state["initial_velocity"] * t * math.sin(math.radians(state["theta"])) - 0.5 * -state["acceleration"] * t ** 2 + state["starting_displacement"])
        return x, y

    def ball_position(self, t=0):
        state = self.state(t)
        x = state["initial_velocity"] * t * math.cos(math.radians(state["theta"]))
        y = state["initial_velocity"] * t * math.sin(math.radians(state["theta"])) - 0.5 * -state["acceleration"] * t ** 2 + state["starting_displacement"]
        return x, y
