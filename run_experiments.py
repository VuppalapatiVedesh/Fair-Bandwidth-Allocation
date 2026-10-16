import sys
from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

from simulation.traffic_generator import TrafficGenerator
from simulation.simulator import BandwidthSimulator


# ============================================================
# CONFIGURATION
# ============================================================

CAPACITY = 10.0

USER_COUNTS = [
    5,
    10,
    20,
    50
]


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def main():

    print("\n")
    print("=" * 75)
    print(
        "       FAIR BANDWIDTH ALLOCATION - EXPERIMENTS"
    )
    print("=" * 75)

    generator = TrafficGenerator(
        seed=42
    )

    simulator = BandwidthSimulator(
        capacity=CAPACITY
    )

    all_results = []

    # ========================================================
    # SCALABILITY EXPERIMENT
    # ========================================================

    for user_count in USER_COUNTS:

        print("\n")
        print("-" * 75)

        print(
            f"Testing {user_count} users..."
        )

        # ----------------------------------------------------
        # Generate ONE traffic scenario
        # ----------------------------------------------------

        users = generator.generate_random_users(
            number_of_users=user_count
        )

        total_demand = float(
            users["demand"].sum()
        )

        print(
            f"Total demand: "
            f"{total_demand:.2f} Mbps"
        )

        print(
            f"Network capacity: "
            f"{CAPACITY:.2f} Mbps"
        )

        # ----------------------------------------------------
        # Run all algorithms on EXACTLY the same users
        # ----------------------------------------------------

        results = simulator.run_all(
            users
        )

        comparison = (
            simulator.create_comparison_table(
                results
            )
        )

        # ----------------------------------------------------
        # Store results
        # ----------------------------------------------------

        for _, row in comparison.iterrows():

            result = {
                "Users":
                    user_count,

                "Algorithm":
                    row["Algorithm"],

                "Throughput (Mbps)":
                    row["Throughput (Mbps)"],

                "Fairness Index":
                    row["Fairness Index"],

                "Utilization (%)":
                    row["Utilization (%)"],

                "Packet Loss (%)":
                    row["Packet Loss (%)"],

                "Latency Indicator":
                    row["Latency Indicator"]
            }

            all_results.append(
                result
            )

            print(
                f"{row['Algorithm']:<15}"
                f" Throughput: "
                f"{row['Throughput (Mbps)']:>6.2f} Mbps"
                f" | Fairness: "
                f"{row['Fairness Index']:.4f}"
                f" | Utilization: "
                f"{row['Utilization (%)']:.2f}%"
                f" | Loss: "
                f"{row['Packet Loss (%)']:.2f}%"
            )

    # ========================================================
    # CREATE DATAFRAME
    # ========================================================

    results_df = pd.DataFrame(
        all_results
    )

    # Sort results
    results_df = results_df.sort_values(
        by=[
            "Users",
            "Algorithm"
        ]
    ).reset_index(
        drop=True
    )

    # ========================================================
    # SAVE RESULTS
    # ========================================================

    output_directory = (
        PROJECT_ROOT
        / "data"
        / "experiments"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_directory
        / "scalability_results.csv"
    )

    results_df.to_csv(
        output_file,
        index=False
    )

    # ========================================================
    # FINAL RESULTS
    # ========================================================

    print("\n")
    print("=" * 75)
    print(
        "                 FINAL RESULTS"
    )
    print("=" * 75)

    print(
        results_df.to_string(
            index=False
        )
    )

    print("\n")
    print("=" * 75)

    print(
        "Results saved to:"
    )

    print(
        output_file
    )

    print("=" * 75)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()