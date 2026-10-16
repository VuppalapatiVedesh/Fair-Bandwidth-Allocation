import sys
from pathlib import Path

# --------------------------------------------------
# MATPLOTLIB CONFIGURATION
# --------------------------------------------------

import matplotlib

# Use a non-GUI backend.
# This prevents Tkinter/Tcl errors on Windows.
matplotlib.use("Agg")

import matplotlib.pyplot as plt


# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))


# --------------------------------------------------
# PROJECT IMPORTS
# --------------------------------------------------

from simulation.traffic_generator import TrafficGenerator
from simulation.simulator import BandwidthSimulator


# --------------------------------------------------
# VISUALIZATION CLASS
# --------------------------------------------------

class BandwidthVisualizer:
    """
    Creates charts for comparing bandwidth
    allocation algorithms.
    """

    def __init__(self, output_directory="data/experiments"):

        self.output_directory = (
            PROJECT_ROOT / output_directory
        )

        # Create directory if it doesn't exist
        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    # ==================================================
    # 1. BANDWIDTH ALLOCATION
    # ==================================================

    def plot_bandwidth_allocation(self, results):

        algorithms = list(results.keys())

        first_algorithm = algorithms[0]

        users = (
            results[first_algorithm]["allocation"]
            ["user_id"]
            .tolist()
        )

        plt.figure(figsize=(10, 6))

        bar_width = 0.18

        x = list(range(len(users)))

        for i, algorithm in enumerate(algorithms):

            allocations = (
                results[algorithm]["allocation"]
                ["allocation"]
                .tolist()
            )

            positions = [
                value + (i * bar_width)
                for value in x
            ]

            plt.bar(
                positions,
                allocations,
                width=bar_width,
                label=algorithm
            )

        center_positions = [
            value + (bar_width * 1.5)
            for value in x
        ]

        plt.xticks(
            center_positions,
            users
        )

        plt.xlabel("Users")

        plt.ylabel(
            "Allocated Bandwidth (Mbps)"
        )

        plt.title(
            "Bandwidth Allocation Comparison"
        )

        plt.legend()

        plt.tight_layout()

        file_path = (
            self.output_directory
            / "bandwidth_allocation.png"
        )

        plt.savefig(
            file_path,
            dpi=300,
            bbox_inches="tight"
        )

        # IMPORTANT:
        # Do NOT use plt.show().
        plt.close()

        return file_path

    # ==================================================
    # 2. FAIRNESS
    # ==================================================

    def plot_fairness(self, results):

        algorithms = list(results.keys())

        fairness_values = [
            results[algorithm]["metrics"]
            ["fairness_index"]
            for algorithm in algorithms
        ]

        plt.figure(figsize=(9, 6))

        plt.bar(
            algorithms,
            fairness_values
        )

        plt.xlabel("Algorithm")

        plt.ylabel(
            "Jain's Fairness Index"
        )

        plt.title(
            "Fairness Comparison"
        )

        plt.ylim(0, 1)

        for i, value in enumerate(
            fairness_values
        ):

            plt.text(
                i,
                value + 0.02,
                f"{value:.4f}",
                ha="center"
            )

        plt.tight_layout()

        file_path = (
            self.output_directory
            / "fairness_comparison.png"
        )

        plt.savefig(
            file_path,
            dpi=300,
            bbox_inches="tight"
        )

        # Do not use plt.show()
        plt.close()

        return file_path

    # ==================================================
    # 3. THROUGHPUT
    # ==================================================

    def plot_throughput(self, results):

        algorithms = list(results.keys())

        throughput_values = [
            results[algorithm]["metrics"]
            ["throughput_mbps"]
            for algorithm in algorithms
        ]

        plt.figure(figsize=(9, 6))

        plt.bar(
            algorithms,
            throughput_values
        )

        plt.xlabel("Algorithm")

        plt.ylabel(
            "Throughput (Mbps)"
        )

        plt.title(
            "Throughput Comparison"
        )

        for i, value in enumerate(
            throughput_values
        ):

            plt.text(
                i,
                value + 0.1,
                f"{value:.2f}",
                ha="center"
            )

        plt.tight_layout()

        file_path = (
            self.output_directory
            / "throughput_comparison.png"
        )

        plt.savefig(
            file_path,
            dpi=300,
            bbox_inches="tight"
        )

        # Do not use plt.show()
        plt.close()

        return file_path

    # ==================================================
    # 4. UTILIZATION
    # ==================================================

    def plot_utilization(self, results):

        algorithms = list(results.keys())

        utilization_values = [
            results[algorithm]["metrics"]
            ["utilization_percent"]
            for algorithm in algorithms
        ]

        plt.figure(figsize=(9, 6))

        plt.bar(
            algorithms,
            utilization_values
        )

        plt.xlabel("Algorithm")

        plt.ylabel(
            "Utilization (%)"
        )

        plt.title(
            "Network Utilization Comparison"
        )

        plt.ylim(0, 110)

        for i, value in enumerate(
            utilization_values
        ):

            plt.text(
                i,
                value + 2,
                f"{value:.2f}%",
                ha="center"
            )

        plt.tight_layout()

        file_path = (
            self.output_directory
            / "utilization_comparison.png"
        )

        plt.savefig(
            file_path,
            dpi=300,
            bbox_inches="tight"
        )

        # Do not use plt.show()
        plt.close()

        return file_path

    # ==================================================
    # 5. PACKET / DEMAND LOSS
    # ==================================================

    def plot_packet_loss(self, results):

        algorithms = list(results.keys())

        loss_values = [
            results[algorithm]["metrics"]
            ["packet_loss_percent"]
            for algorithm in algorithms
        ]

        plt.figure(figsize=(9, 6))

        plt.bar(
            algorithms,
            loss_values
        )

        plt.xlabel("Algorithm")

        plt.ylabel(
            "Loss (%)"
        )

        plt.title(
            "Packet/Demand Loss Comparison"
        )

        for i, value in enumerate(
            loss_values
        ):

            plt.text(
                i,
                value + 0.5,
                f"{value:.2f}%",
                ha="center"
            )

        plt.tight_layout()

        file_path = (
            self.output_directory
            / "packet_loss_comparison.png"
        )

        plt.savefig(
            file_path,
            dpi=300,
            bbox_inches="tight"
        )

        # Do not use plt.show()
        plt.close()

        return file_path

    # ==================================================
    # GENERATE ALL CHARTS
    # ==================================================

    def generate_all(self, results):

        generated_files = {}

        generated_files["allocation"] = (
            self.plot_bandwidth_allocation(
                results
            )
        )

        generated_files["fairness"] = (
            self.plot_fairness(
                results
            )
        )

        generated_files["throughput"] = (
            self.plot_throughput(
                results
            )
        )

        generated_files["utilization"] = (
            self.plot_utilization(
                results
            )
        )

        generated_files["packet_loss"] = (
            self.plot_packet_loss(
                results
            )
        )

        return generated_files


# ======================================================
# MAIN PROGRAM
# ======================================================

if __name__ == "__main__":

    print("\n==============================================")
    print("        BANDWIDTH VISUALIZATION")
    print("==============================================")

    # --------------------------------------------------
    # NETWORK CAPACITY
    # --------------------------------------------------

    capacity = 10.0

    print(
        "\nNetwork Capacity:",
        capacity,
        "Mbps"
    )

    # --------------------------------------------------
    # GENERATE FIXED TEST SCENARIO
    # --------------------------------------------------

    generator = TrafficGenerator()

    users = (
        generator.generate_fixed_users()
    )

    print("\nTraffic Scenario:")

    print(
        users.to_string(index=False)
    )

    # --------------------------------------------------
    # CREATE SIMULATOR
    # --------------------------------------------------

    simulator = BandwidthSimulator(
        capacity=capacity
    )

    # --------------------------------------------------
    # RUN ALL ALGORITHMS
    # --------------------------------------------------

    print(
        "\nRunning allocation algorithms..."
    )

    results = simulator.run_all(
        users
    )

    print(
        "Algorithms completed."
    )

    # --------------------------------------------------
    # CREATE VISUALIZER
    # --------------------------------------------------

    visualizer = BandwidthVisualizer()

    # --------------------------------------------------
    # GENERATE CHARTS
    # --------------------------------------------------

    print(
        "\nGenerating charts..."
    )

    generated_files = (
        visualizer.generate_all(
            results
        )
    )

    # --------------------------------------------------
    # DISPLAY OUTPUT
    # --------------------------------------------------

    print(
        "\n=============================================="
    )

    print(
        "       CHARTS GENERATED SUCCESSFULLY"
    )

    print(
        "=============================================="
    )

    for chart_name, file_path in (
        generated_files.items()
    ):

        print(
            f"{chart_name}: {file_path}"
        )

    print(
        "\nAll visualization files have been "
        "saved successfully."
    )