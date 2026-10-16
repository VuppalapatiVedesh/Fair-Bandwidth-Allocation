import sys
from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class FCFSAllocator:
    """
    First Come, First Serve bandwidth allocation.

    Users are served strictly in their arrival/order
    sequence. Earlier users can consume the available
    bandwidth before later users are served.
    """

    def __init__(self, capacity):
        self.capacity = float(capacity)

        if self.capacity < 0:
            raise ValueError(
                "Network capacity cannot be negative."
            )

    def allocate(self, users):
        """
        Parameters
        ----------
        users : pandas.DataFrame
            Required columns:
                user_id
                demand
                weight

        Returns
        -------
        pandas.DataFrame
            user_id
            demand
            weight
            allocation
        """

        required_columns = {
            "user_id",
            "demand",
            "weight"
        }

        missing = required_columns - set(users.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

        if users.empty:

            return pd.DataFrame(
                columns=[
                    "user_id",
                    "demand",
                    "weight",
                    "allocation"
                ]
            )

        data = users.copy()

        # Clean demand values
        data["demand"] = pd.to_numeric(
            data["demand"],
            errors="coerce"
        ).fillna(0.0)

        data["demand"] = data["demand"].clip(
            lower=0.0
        )

        remaining_bandwidth = self.capacity

        allocations = []

        # ====================================================
        # FCFS ALLOCATION
        # ====================================================

        for _, user in data.iterrows():

            demand = float(user["demand"])

            allocation = min(
                demand,
                remaining_bandwidth
            )

            allocation = max(
                allocation,
                0.0
            )

            allocations.append(
                allocation
            )

            remaining_bandwidth -= allocation

            if remaining_bandwidth <= 1e-12:
                remaining_bandwidth = 0.0

        data["allocation"] = allocations

        # Numerical safety
        data["allocation"] = (
            data["allocation"]
            .clip(lower=0.0)
            .round(6)
        )

        # Final capacity protection
        total_allocated = data["allocation"].sum()

        if total_allocated > self.capacity:

            excess = (
                total_allocated
                - self.capacity
            )

            for index in reversed(data.index):

                if excess <= 1e-12:
                    break

                removable = min(
                    data.loc[index, "allocation"],
                    excess
                )

                data.loc[index, "allocation"] -= (
                    removable
                )

                excess -= removable

        data["allocation"] = (
            data["allocation"]
            .clip(lower=0.0)
            .round(6)
        )

        return data[
            [
                "user_id",
                "demand",
                "weight",
                "allocation"
            ]
        ]


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    from simulation.traffic_generator import TrafficGenerator

    generator = TrafficGenerator()

    users = generator.generate_fixed_users()

    capacity = 10.0

    allocator = FCFSAllocator(
        capacity
    )

    allocation_result = allocator.allocate(
        users
    )

    print("\n======================================")
    print("        FCFS BANDWIDTH ALLOCATION")
    print("======================================")

    print(
        "\nNetwork Capacity:",
        capacity,
        "Mbps"
    )

    print("\nUser Demands:")

    print(
        users.to_string(
            index=False
        )
    )

    print("\nFCFS Allocation:")

    print(
        allocation_result.to_string(
            index=False
        )
    )

    total_demand = (
        allocation_result["demand"].sum()
    )

    total_allocated = (
        allocation_result["allocation"].sum()
    )

    unused_capacity = max(
        0.0,
        capacity - total_allocated
    )

    print("\n--------------------------------------")

    print(
        "Total Requested :",
        round(total_demand, 2),
        "Mbps"
    )

    print(
        "Total Allocated  :",
        round(total_allocated, 2),
        "Mbps"
    )

    print(
        "Unused Capacity  :",
        round(unused_capacity, 2),
        "Mbps"
    )

    print("--------------------------------------")