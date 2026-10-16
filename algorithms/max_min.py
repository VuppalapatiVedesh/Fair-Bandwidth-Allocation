import sys
from pathlib import Path

import pandas as pd

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from simulation.traffic_generator import TrafficGenerator


class MaxMinFairAllocator:
    """
    Max-Min Fairness bandwidth allocation.

    All active users initially receive an equal share.
    Users whose demands are completely satisfied are removed
    from the active set, and the remaining bandwidth is
    redistributed among the remaining users.

    Note:
        Standard Max-Min Fairness does not use user weights.
        The weight column is preserved for comparison with WFQ.
    """

    def __init__(self, capacity):
        self.capacity = float(capacity)

        if self.capacity < 0:
            raise ValueError("Network capacity cannot be negative.")

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

        required_columns = {"user_id", "demand", "weight"}

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

        # --------------------------------------------------
        # Clean input
        # --------------------------------------------------

        data = users.copy()

        data["demand"] = pd.to_numeric(
            data["demand"],
            errors="coerce"
        ).fillna(0.0)

        data["demand"] = data["demand"].clip(lower=0.0)

        # --------------------------------------------------
        # Initial allocations
        # --------------------------------------------------

        allocations = {
            user_id: 0.0
            for user_id in data["user_id"]
        }

        remaining_capacity = self.capacity

        # --------------------------------------------------
        # Progressive filling
        # --------------------------------------------------

        active_users = list(data["user_id"])

        while active_users and remaining_capacity > 1e-12:

            # Remaining demand for every active user
            remaining_demands = {
                user_id: max(
                    0.0,
                    float(
                        data.loc[
                            data["user_id"] == user_id,
                            "demand"
                        ].iloc[0]
                    ) - allocations[user_id]
                )
                for user_id in active_users
            }

            # Remove users whose demand is satisfied
            active_users = [
                user_id
                for user_id in active_users
                if remaining_demands[user_id] > 1e-12
            ]

            if not active_users:
                break

            # Equal progressive share
            equal_share = (
                remaining_capacity
                / len(active_users)
            )

            newly_satisfied = []

            for user_id in active_users:

                allocation = min(
                    equal_share,
                    remaining_demands[user_id]
                )

                allocations[user_id] += allocation
                remaining_capacity -= allocation

                # User demand has now been satisfied
                if (
                    remaining_demands[user_id]
                    <= equal_share + 1e-12
                ):
                    newly_satisfied.append(user_id)

            # Remove satisfied users
            for user_id in newly_satisfied:
                if user_id in active_users:
                    active_users.remove(user_id)

            # Safety against floating-point errors
            if remaining_capacity < 1e-12:
                remaining_capacity = 0.0

        # --------------------------------------------------
        # Final numerical safety
        # --------------------------------------------------

        total_allocated = sum(allocations.values())

        # Never allow allocation to exceed capacity
        if total_allocated > self.capacity:

            scale = self.capacity / total_allocated

            for user_id in allocations:
                allocations[user_id] *= scale

        # --------------------------------------------------
        # Build result
        # --------------------------------------------------

        results = []

        for _, user in data.iterrows():

            user_id = user["user_id"]

            allocation = min(
                allocations[user_id],
                float(user["demand"])
            )

            allocation = max(0.0, allocation)

            results.append({
                "user_id": user_id,
                "demand": float(user["demand"]),
                "weight": user["weight"],
                "allocation": allocation
            })

        result = pd.DataFrame(results)

        # --------------------------------------------------
        # Final capacity correction
        # --------------------------------------------------

        total = result["allocation"].sum()

        if total > self.capacity + 1e-12:

            excess = total - self.capacity

            # Reduce allocation from users with
            # the largest allocations first.
            order = (
                result["allocation"]
                .sort_values(ascending=False)
                .index
            )

            for idx in order:

                if excess <= 1e-12:
                    break

                removable = min(
                    result.loc[idx, "allocation"],
                    excess
                )

                result.loc[idx, "allocation"] -= removable
                excess -= removable

        # Round only at the very end
        result["allocation"] = result["allocation"].round(6)

        # Correct tiny floating point residue
        final_total = result["allocation"].sum()

        if final_total > self.capacity:

            excess = final_total - self.capacity

            idx = result["allocation"].idxmax()

            result.loc[idx, "allocation"] = max(
                0.0,
                result.loc[idx, "allocation"] - excess
            )

            result["allocation"] = result[
                "allocation"
            ].round(6)

        return result


# --------------------------------------------------
# TESTING
# --------------------------------------------------

if __name__ == "__main__":

    generator = TrafficGenerator()

    users = generator.generate_fixed_users()

    capacity = 10.0

    allocator = MaxMinFairAllocator(capacity)

    allocation_result = allocator.allocate(users)

    print("\n======================================")
    print("       MAX-MIN FAIR BANDWIDTH")
    print("======================================")

    print(
        "\nNetwork Capacity:",
        capacity,
        "Mbps"
    )

    print("\nUser Demands:")
    print(
        users.to_string(index=False)
    )

    print("\nMax-Min Fairness Allocation:")
    print(
        allocation_result.to_string(index=False)
    )

    total_demand = allocation_result["demand"].sum()

    total_allocated = allocation_result[
        "allocation"
    ].sum()

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
        round(total_allocated, 6),
        "Mbps"
    )

    print(
        "Unused Capacity  :",
        round(unused_capacity, 6),
        "Mbps"
    )

    print("--------------------------------------")