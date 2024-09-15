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
        print(possible_none)
        none_variables = sum([1 for var in possible_none if var is None])
        assert none_variables == 1, "Only one of S, U, V and A can be None"

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
