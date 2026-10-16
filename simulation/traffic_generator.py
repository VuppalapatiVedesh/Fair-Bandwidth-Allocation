import random
import pandas as pd


class TrafficGenerator:
    """
    Generates reproducible traffic demand scenarios for
    the Fair Bandwidth Allocation simulation.
    """

    def __init__(self, seed=42):

        self.seed = seed

    # ========================================================
    # FIXED TEST SCENARIO
    # ========================================================

    def generate_fixed_users(self):

        users = [
            {
                "user_id": "User 1",
                "demand": 4.0,
                "weight": 1
            },
            {
                "user_id": "User 2",
                "demand": 1.0,
                "weight": 2
            },
            {
                "user_id": "User 3",
                "demand": 8.0,
                "weight": 3
            },
            {
                "user_id": "User 4",
                "demand": 0.5,
                "weight": 4
            }
        ]

        return pd.DataFrame(users)

    # ========================================================
    # RANDOM TRAFFIC SCENARIO
    # ========================================================

    def generate_random_users(
        self,
        number_of_users=10,
        min_demand=0.5,
        max_demand=8.0,
        min_weight=1,
        max_weight=4
    ):

        if number_of_users < 1:
            raise ValueError(
                "Number of users must be at least 1."
            )

        if min_demand < 0:
            raise ValueError(
                "Minimum demand cannot be negative."
            )

        if max_demand < min_demand:
            raise ValueError(
                "Maximum demand must be >= minimum demand."
            )

        if min_weight < 0:
            raise ValueError(
                "Minimum weight cannot be negative."
            )

        if max_weight < min_weight:
            raise ValueError(
                "Maximum weight must be >= minimum weight."
            )

        # Local RNG.
        # This keeps experiments reproducible without changing
        # Python's global random state.
        rng = random.Random(
            self.seed + number_of_users
        )

        users = []

        for i in range(
            1,
            number_of_users + 1
        ):

            demand = round(
                rng.uniform(
                    min_demand,
                    max_demand
                ),
                2
            )

            weight = rng.randint(
                min_weight,
                max_weight
            )

            users.append(
                {
                    "user_id": f"User {i}",
                    "demand": demand,
                    "weight": weight
                }
            )

        return pd.DataFrame(users)

    # ========================================================
    # COMPATIBILITY ALIAS
    # ========================================================

    def generate_random_traffic(
        self,
        number_of_users=10
    ):

        return self.generate_random_users(
            number_of_users=number_of_users
        )


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    generator = TrafficGenerator()

    print("\n======================================")
    print("       TRAFFIC GENERATOR TEST")
    print("======================================")

    print("\nFixed Test Scenario:")

    print(
        generator.generate_fixed_users().to_string(
            index=False
        )
    )

    print("\nRandom Test Scenario:")

    print(
        generator.generate_random_users(
            number_of_users=10
        ).to_string(
            index=False
        )
    )

    print("\nTraffic generation successful!")