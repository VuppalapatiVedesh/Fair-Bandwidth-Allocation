import sys
from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

from algorithms.fcfs import FCFSAllocator
from algorithms.round_robin import RoundRobinAllocator
from algorithms.wfq import WFQAllocator
from algorithms.max_min import MaxMinFairAllocator

from metrics.metrics import MetricsCalculator


class BandwidthSimulator:
    """
    Main simulation engine.

    Runs FCFS, Round Robin, WFQ and Max-Min Fairness
    on exactly the same traffic scenario.
    """

    def __init__(self, capacity=10.0):

        self.capacity = float(capacity)

        if self.capacity <= 0:
            raise ValueError(
                "Network capacity must be greater than zero."
            )

        self.metrics_calculator = (
            MetricsCalculator(
                self.capacity
            )
        )

    # ========================================================
    # RUN ONE ALGORITHM
    # ========================================================

    def run_algorithm(
        self,
        algorithm_name,
        users
    ):

        if algorithm_name == "FCFS":

            allocator = FCFSAllocator(
                self.capacity
            )

        elif algorithm_name == "Round Robin":

            allocator = RoundRobinAllocator(
                capacity=self.capacity,
                quantum=0.5
            )

        elif algorithm_name == "WFQ":

            allocator = WFQAllocator(
                self.capacity
            )

        elif algorithm_name == "Max-Min":

            allocator = MaxMinFairAllocator(
                self.capacity
            )

        else:

            raise ValueError(
                f"Unknown algorithm: {algorithm_name}"
            )

        return allocator.allocate(
            users
        )

    # ========================================================
    # RUN ALL ALGORITHMS
    # ========================================================

    def run_all(self, users):

        algorithms = [
            "FCFS",
            "Round Robin",
            "WFQ",
            "Max-Min"
        ]

        results = {}

        for algorithm in algorithms:

            allocation = self.run_algorithm(
                algorithm,
                users
            )

            metrics = (
                self.metrics_calculator.calculate_all(
                    allocation
                )
            )

            results[algorithm] = {
                "allocation": allocation,
                "metrics": metrics
            }

        return results

    # ========================================================
    # COMPARISON TABLE
    # ========================================================

    def create_comparison_table(
        self,
        results
    ):

        comparison = []

        for algorithm, result in results.items():

            metrics = result["metrics"]

            comparison.append(
                {
                    "Algorithm": algorithm,

                    "Throughput (Mbps)":
                        metrics[
                            "throughput_mbps"
                        ],

                    "Fairness Index":
                        metrics[
                            "fairness_index"
                        ],

                    "Utilization (%)":
                        metrics[
                            "utilization_percent"
                        ],

                    "Packet Loss (%)":
                        metrics[
                            "packet_loss_percent"
                        ],

                    "Latency Indicator":
                        metrics[
                            "latency_indicator"
                        ]
                }
            )

        return pd.DataFrame(
            comparison
        )


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    from simulation.traffic_generator import (
        TrafficGenerator
    )

    print("\n==============================================")
    print("       FAIR BANDWIDTH ALLOCATION SIMULATOR")
    print("==============================================")

    capacity = 10.0

    generator = TrafficGenerator()

    users = generator.generate_fixed_users()

    print(
        "\nNetwork Capacity:",
        capacity,
        "Mbps"
    )

    print("\nTraffic Scenario:")

    print(
        users.to_string(
            index=False
        )
    )

    simulator = BandwidthSimulator(
        capacity=capacity
    )

    results = simulator.run_all(
        users
    )

    for algorithm, result in results.items():

        print(
            "\n=============================================="
        )

        print(
            f"       {algorithm.upper()} ALLOCATION"
        )

        print(
            "=============================================="
        )

        print(
            result["allocation"].to_string(
                index=False
            )
        )

    comparison = (
        simulator.create_comparison_table(
            results
        )
    )

    print(
        "\n\n=============================================="
    )

    print(
        "           ALGORITHM COMPARISON"
    )

    print(
        "=============================================="
    )

    print(
        comparison.to_string(
            index=False
        )
    )

    print(
        "\nSimulation completed successfully!"
    )