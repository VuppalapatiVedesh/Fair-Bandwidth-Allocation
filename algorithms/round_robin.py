import sys
from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class RoundRobinAllocator:
    """
    Round Robin bandwidth allocation.

    Each active user receives a fixed quantum in rotation
    until the available bandwidth is exhausted or all
    demands are satisfied.
    """

    def __init__(self, capacity, quantum=0.5):

        self.capacity = float(capacity)
        self.quantum = float(quantum)

        if self.capacity < 0:
            raise ValueError(
                "Network capacity cannot be negative."
            )

        if self.quantum <= 0:
            raise ValueError(
                "Round Robin quantum must be greater than zero."
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

        data["demand"] = pd.to_numeric(
            data["demand"],
            errors="coerce"
        ).fillna(0.0)

        data["demand"] = data["demand"].clip(
            lower=0.0
        )

        allocations = {
            user_id: 0.0
            for user_id in data["user_id"]
        }

        remaining_bandwidth = self.capacity

        # ====================================================
        # ROUND ROBIN
        # ====================================================

        while remaining_bandwidth > 1e-12:

            allocation_made = False

            for _, user in data.iterrows():

                user_id = user["user_id"]
                demand = float(user["demand"])

                remaining_demand = (
                    demand
                    - allocations[user_id]
                )

                if remaining_demand <= 1e-12:
                    continue

                allocation = min(
                    self.quantum,
                    remaining_demand,
                    remaining_bandwidth
                )

                if allocation <= 1e-12:
                    continue

                allocations[user_id] += allocation

                remaining_bandwidth -= allocation

                allocation_made = True

                if remaining_bandwidth <= 1e-12:

                    remaining_bandwidth = 0.0
                    break

            if not allocation_made:
                break

        # ====================================================
        # BUILD RESULT
        # ====================================================

        results = []

        for _, user in data.iterrows():

            user_id = user["user_id"]

            results.append(
                {
                    "user_id": user_id,
                    "demand": float(user["demand"]),
                    "weight": user["weight"],
                    "allocation": round(
                        min(
                            allocations[user_id],
                            float(user["demand"])
                        ),
                        6
                    )
                }
            )

        result = pd.DataFrame(results)

        # ====================================================
        # FINAL CAPACITY PROTECTION
        # ====================================================

        total_allocated = (
            result["allocation"].sum()
        )

        if total_allocated > self.capacity:

            excess = (
                total_allocated
                - self.capacity
            )

            for index in reversed(result.index):

                if excess <= 1e-12:
                    break

                removable = min(
                    result.loc[index, "allocation"],
                    excess
                )

                result.loc[index, "allocation"] -= (
                    removable
                )

                excess -= removable

        result["allocation"] = (
            result["allocation"]
            .clip(lower=0.0)
            .round(6)
        )

        return result


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    from simulation.traffic_generator import TrafficGenerator

    generator = TrafficGenerator()

    users = generator.generate_fixed_users()

    capacity = 10.0
    quantum = 0.5

    allocator = RoundRobinAllocator(
        capacity=capacity,
        quantum=quantum
    )

    allocation_result = allocator.allocate(
        users
    )

    print("\n======================================")
    print("      ROUND ROBIN BANDWIDTH ALLOCATION")
    print("======================================")

    print(
        "\nNetwork Capacity:",
        capacity,
        "Mbps"
    )

    print(
        "Quantum:",
        quantum,
        "Mbps"
    )

    print("\nUser Demands:")

    print(
        users.to_string(
            index=False
        )
    )

    print("\nRound Robin Allocation:")

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