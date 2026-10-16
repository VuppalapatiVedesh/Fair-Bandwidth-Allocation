import sys
from pathlib import Path

import pandas as pd

import matplotlib

# Non-GUI backend for Windows
matplotlib.use("Agg")

import matplotlib.pyplot as plt


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

RESULTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "experiments"
    / "scalability_results.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "experiments"
)


# ============================================================
# LOAD RESULTS
# ============================================================

def load_results():

    if not RESULTS_FILE.exists():

        raise FileNotFoundError(
            f"Results file not found:\n"
            f"{RESULTS_FILE}\n\n"
            "Run 'python run_experiments.py' first."
        )

    df = pd.read_csv(
        RESULTS_FILE
    )

    required_columns = {
        "Users",
        "Algorithm",
        "Throughput (Mbps)",
        "Fairness Index",
        "Utilization (%)",
        "Packet Loss (%)",
        "Latency Indicator"
    }

    missing = (
        required_columns
        - set(df.columns)
    )

    if missing:

        raise ValueError(
            "Missing columns in results file: "
            f"{sorted(missing)}"
        )

    return df.sort_values(
        by=[
            "Users",
            "Algorithm"
        ]
    )


# ============================================================
# GENERIC LINE PLOT
# ============================================================

def create_line_plot(
    df,
    y_column,
    y_label,
    title,
    filename,
    y_limit=None
):

    plt.figure(
        figsize=(10, 6)
    )

    for algorithm in df["Algorithm"].unique():

        data = df[
            df["Algorithm"] == algorithm
        ].sort_values(
            "Users"
        )

        plt.plot(
            data["Users"],
            data[y_column],
            marker="o",
            linewidth=2,
            label=algorithm
        )

    plt.xlabel(
        "Number of Users"
    )

    plt.ylabel(
        y_label
    )

    plt.title(
        title
    )

    if y_limit is not None:

        plt.ylim(
            *y_limit
        )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend()

    plt.tight_layout()

    output = (
        OUTPUT_DIR
        / filename
    )

    plt.savefig(
        output,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    return output


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 65)
    print(
        "       SCALABILITY VISUALIZATION"
    )
    print("=" * 65)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df = load_results()

    print("\nLoaded experimental results:")

    print(
        df.to_string(
            index=False
        )
    )

    files = []

    # --------------------------------------------------------
    # FAIRNESS
    # --------------------------------------------------------

    files.append(
        create_line_plot(
            df,
            "Fairness Index",
            "Jain's Fairness Index",
            "Fairness Comparison vs Number of Users",
            "scalability_fairness.png",
            (0, 1.05)
        )
    )

    # --------------------------------------------------------
    # THROUGHPUT
    # --------------------------------------------------------

    files.append(
        create_line_plot(
            df,
            "Throughput (Mbps)",
            "Throughput (Mbps)",
            "Throughput Comparison vs Number of Users",
            "scalability_throughput.png"
        )
    )

    # --------------------------------------------------------
    # UTILIZATION
    # --------------------------------------------------------

    files.append(
        create_line_plot(
            df,
            "Utilization (%)",
            "Network Utilization (%)",
            "Network Utilization vs Number of Users",
            "scalability_utilization.png",
            (0, 105)
        )
    )

    # --------------------------------------------------------
    # PACKET / DEMAND LOSS
    # --------------------------------------------------------

    files.append(
        create_line_plot(
            df,
            "Packet Loss (%)",
            "Packet / Demand Loss (%)",
            "Packet / Demand Loss vs Number of Users",
            "scalability_packet_loss.png",
            (0, 105)
        )
    )

    # --------------------------------------------------------
    # LATENCY INDICATOR
    # --------------------------------------------------------

    files.append(
        create_line_plot(
            df,
            "Latency Indicator",
            "Simulation Latency Indicator (%)",
            "Latency Indicator vs Number of Users",
            "scalability_latency.png",
            (0, 105)
        )
    )

    # ========================================================
    # OUTPUT
    # ========================================================

    print("\n")
    print("=" * 65)
    print(
        "           PLOTS GENERATED"
    )
    print("=" * 65)

    for file in files:

        print(
            f"\n{file}"
        )

    print("\n")
    print("=" * 65)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()