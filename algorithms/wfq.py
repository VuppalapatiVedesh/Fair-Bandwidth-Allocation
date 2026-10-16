import sys
from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class WFQAllocator:
    """
    Weighted Fair Queuing-style bandwidth allocation.

    Active users receive bandwidth according to their weights.
    If a user's demand is fully satisfied, that user is removed
    and the remaining bandwidth is redistributed among the
    remaining active users.

    Note:
        This is a bandwidth-allocation simulation of WFQ behavior,
        not a production packet-level router implementation.
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

        data["demand"] = pd.to_numeric(
            data["demand"],
            errors="coerce"
        ).fillna(0.0)

        data["demand"] = data["demand"].clip(
            lower=0.0
        )

        data["weight"] = pd.to_numeric(
            data["weight"],
            errors="coerce"
        ).fillna(0.0)

        data["weight"] = data["weight"].clip(
            lower=0.0
        )

        allocations = {
            user_id: 0.0
            for user_id in data["user_id"]
        }

        remaining_bandwidth = self.capacity

        # ====================================================
        # WEIGHTED PROGRESSIVE ALLOCATION
        # ====================================================

        while remaining_bandwidth > 1e-12:

            active_users = []

            for _, user in data.iterrows():

                user_id = user["user_id"]

                demand = float(
                    user["demand"]
                )

                weight = float(
                    user["weight"]
                )

                remaining_demand = (
                    demand
                    - allocations[user_id]
                )

                if (
                    remaining_demand > 1e-12
                    and weight > 0
                ):

                    active_users.append(
                        {
                            "user_id": user_id,
                            "remaining_demand":
                                remaining_demand,
                            "weight": weight
                        }
                    )

            if not active_users:
                break

            total_weight = sum(
                user["weight"]
                for user in active_users
            )

            if total_weight <= 1e-12:
                break

            allocation_made = False

            # ------------------------------------------------
            # Calculate weighted shares
            # ------------------------------------------------

            for user in active_users:

                user_id = user["user_id"]

                remaining_demand = (
                    user["remaining_demand"]
                )

                weight = user["weight"]

                weighted_share = (
                    remaining_bandwidth
                    * weight
                    / total_weight
                )

                allocation = min(
                    weighted_share,
                    remaining_demand
                )

                if allocation <= 1e-12:
                    continue

                allocations[user_id] += allocation

                allocation_made = True

            if not allocation_made:
                break

            # Recalculate remaining capacity
            total_allocated = sum(
                allocations.values()
            )

            remaining_bandwidth = max(
                0.0,
                self.capacity - total_allocated
            )

        # ====================================================
        # BUILD RESULT
        # ====================================================

        results = []

        for _, user in data.iterrows():

            user_id = user["user_id"]

            allocation = min(
                allocations[user_id],
                float(user["demand"])
            )

            results.append(
                {
                    "user_id": user_id,
                    "demand": float(user["demand"]),
                    "weight": user["weight"],
                    "allocation": max(
                        0.0,
                        round(allocation, 6)
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

            scale = (
                self.capacity
                / total_allocated
            )

            result["allocation"] *= scale

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

    allocator = WFQAllocator(
        capacity
    )

    allocation_result = allocator.allocate(
        users
    )

    print("\n======================================")
    print("        WFQ BANDWIDTH ALLOCATION")
    print("======================================")

    print(
        "\nNetwork Capacity:",
        capacity,
        "Mbps"
    )

    print("\nUser Demands and Weights:")

    print(
        users.to_string(
            index=False
        )
    )

    print("\nWFQ Allocation:")

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