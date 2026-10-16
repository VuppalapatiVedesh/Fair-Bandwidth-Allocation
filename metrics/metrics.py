import pandas as pd


class MetricsCalculator:
    """
    Calculates performance metrics for the
    Fair Bandwidth Allocation simulation.

    Important:
        Packet loss and latency are simulation-level
        demand-based indicators. They are NOT measurements
        from physical network packets or real milliseconds.
    """

    def __init__(self, capacity):

        self.capacity = float(capacity)

        if self.capacity <= 0:
            raise ValueError(
                "Network capacity must be greater than zero."
            )

    # ========================================================
    # THROUGHPUT
    # ========================================================

    def calculate_throughput(self, allocations):

        if allocations.empty:
            return 0.0

        throughput = float(
            allocations["allocation"].sum()
        )

        return round(
            min(
                throughput,
                self.capacity
            ),
            6
        )

    # ========================================================
    # UTILIZATION
    # ========================================================

    def calculate_utilization(self, allocations):

        throughput = self.calculate_throughput(
            allocations
        )

        utilization = (
            throughput
            / self.capacity
        ) * 100

        return round(
            min(utilization, 100.0),
            4
        )

    # ========================================================
    # JAIN'S FAIRNESS INDEX
    # ========================================================

    def calculate_fairness(self, allocations):

        if allocations.empty:
            return 0.0

        values = (
            pd.to_numeric(
                allocations["allocation"],
                errors="coerce"
            )
            .fillna(0.0)
            .clip(lower=0.0)
            .tolist()
        )

        if not values:
            return 0.0

        numerator = sum(values) ** 2

        denominator = (
            len(values)
            * sum(
                value ** 2
                for value in values
            )
        )

        if denominator <= 1e-12:
            return 0.0

        fairness = (
            numerator
            / denominator
        )

        return round(
            min(
                max(fairness, 0.0),
                1.0
            ),
            4
        )

    # ========================================================
    # PACKET / DEMAND LOSS
    # ========================================================

    def calculate_packet_loss(self, allocations):

        if allocations.empty:
            return 0.0

        total_demand = float(
            allocations["demand"].sum()
        )

        total_allocated = float(
            allocations["allocation"].sum()
        )

        if total_demand <= 1e-12:
            return 0.0

        unmet_demand = max(
            total_demand - total_allocated,
            0.0
        )

        packet_loss = (
            unmet_demand
            / total_demand
        ) * 100

        return round(
            min(packet_loss, 100.0),
            4
        )

    # ========================================================
    # LATENCY INDICATOR
    # ========================================================

    def calculate_latency(self, allocations):

        """
        Simulation-level latency indicator.

        Because this project does not simulate packet timestamps,
        propagation delay, queue timestamps, or transmission
        events, real latency in milliseconds cannot be calculated.

        Therefore the current latency indicator represents the
        percentage of demand that remains unmet.
        """

        return self.calculate_packet_loss(
            allocations
        )

    # ========================================================
    # ALL METRICS
    # ========================================================

    def calculate_all(self, allocations):

        return {
            "throughput_mbps":
                self.calculate_throughput(
                    allocations
                ),

            "fairness_index":
                self.calculate_fairness(
                    allocations
                ),

            "utilization_percent":
                self.calculate_utilization(
                    allocations
                ),

            "packet_loss_percent":
                self.calculate_packet_loss(
                    allocations
                ),

            "latency_indicator":
                self.calculate_latency(
                    allocations
                )
        }