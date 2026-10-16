from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

CAPACITY = 10.0

RESULTS_FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "experiments"
    / "scalability_results.csv"
)


EXPECTED_ALGORITHMS = {
    "FCFS",
    "Round Robin",
    "WFQ",
    "Max-Min"
}

EXPECTED_USERS = {
    5,
    10,
    20,
    50
}


# ============================================================
# VALIDATION
# ============================================================

def main():

    print()
    print("=" * 70)
    print(
        "          FAIR BANDWIDTH ALLOCATION"
    )
    print(
        "                 SYSTEM VALIDATION"
    )
    print("=" * 70)

    if not RESULTS_FILE.exists():

        print("\nERROR:")
        print(
            "Scalability results file not found."
        )

        print(
            "\nRun:"
        )

        print(
            "python run_experiments.py"
        )

        return

    results = pd.read_csv(
        RESULTS_FILE
    )

    errors = []

    # ========================================================
    # CHECK 1 - REQUIRED COLUMNS
    # ========================================================

    print("\n[1] Required Column Check")

    required_columns = {
        "Users",
        "Algorithm",
        "Throughput (Mbps)",
        "Fairness Index",
        "Utilization (%)",
        "Packet Loss (%)",
        "Latency Indicator"
    }

    missing_columns = (
        required_columns
        - set(results.columns)
    )

    if not missing_columns:

        print("PASS")
        print(
            "All required result columns are present."
        )

    else:

        print("FAIL")

        print(
            "Missing:",
            ", ".join(
                sorted(missing_columns)
            )
        )

        errors.append(
            "Required column check failed."
        )

    # ========================================================
    # CHECK 2 - ALGORITHMS
    # ========================================================

    print("\n[2] Algorithm Check")

    actual_algorithms = set(
        results["Algorithm"].unique()
    )

    if actual_algorithms == EXPECTED_ALGORITHMS:

        print("PASS")
        print(
            "All four algorithms are present."
        )

    else:

        print("FAIL")

        missing = (
            EXPECTED_ALGORITHMS
            - actual_algorithms
        )

        extra = (
            actual_algorithms
            - EXPECTED_ALGORITHMS
        )

        if missing:

            print(
                "Missing:",
                ", ".join(sorted(missing))
            )

        if extra:

            print(
                "Unexpected:",
                ", ".join(sorted(extra))
            )

        errors.append(
            "Algorithm check failed."
        )

    # ========================================================
    # CHECK 3 - FAIRNESS
    # ========================================================

    print("\n[3] Fairness Index Check")

    invalid_fairness = results[
        (results["Fairness Index"] < 0)
        |
        (results["Fairness Index"] > 1)
    ]

    if invalid_fairness.empty:

        print("PASS")
        print(
            "All fairness values are between 0 and 1."
        )

    else:

        print("FAIL")

        print(
            invalid_fairness[
                [
                    "Users",
                    "Algorithm",
                    "Fairness Index"
                ]
            ].to_string(
                index=False
            )
        )

        errors.append(
            "Fairness range check failed."
        )

    # ========================================================
    # CHECK 4 - UTILIZATION
    # ========================================================

    print("\n[4] Utilization Check")

    invalid_utilization = results[
        (results["Utilization (%)"] < 0)
        |
        (results["Utilization (%)"] > 100)
    ]

    if invalid_utilization.empty:

        print("PASS")
        print(
            "All utilization values are between 0% and 100%."
        )

    else:

        print("FAIL")

        print(
            invalid_utilization[
                [
                    "Users",
                    "Algorithm",
                    "Utilization (%)"
                ]
            ].to_string(
                index=False
            )
        )

        errors.append(
            "Utilization range check failed."
        )

    # ========================================================
    # CHECK 5 - THROUGHPUT
    # ========================================================

    print("\n[5] Throughput Check")

    invalid_throughput = results[
        (results["Throughput (Mbps)"] < 0)
        |
        (results["Throughput (Mbps)"] > CAPACITY)
    ]

    if invalid_throughput.empty:

        print("PASS")
        print(
            f"No throughput exceeds "
            f"{CAPACITY:.2f} Mbps."
        )

    else:

        print("FAIL")

        print(
            invalid_throughput[
                [
                    "Users",
                    "Algorithm",
                    "Throughput (Mbps)"
                ]
            ].to_string(
                index=False
            )
        )

        errors.append(
            "Throughput capacity check failed."
        )

    # ========================================================
    # CHECK 6 - PACKET LOSS
    # ========================================================

    print("\n[6] Packet / Demand Loss Check")

    invalid_loss = results[
        (results["Packet Loss (%)"] < 0)
        |
        (results["Packet Loss (%)"] > 100)
    ]

    if invalid_loss.empty:

        print("PASS")
        print(
            "All loss values are between 0% and 100%."
        )

    else:

        print("FAIL")

        print(
            invalid_loss[
                [
                    "Users",
                    "Algorithm",
                    "Packet Loss (%)"
                ]
            ].to_string(
                index=False
            )
        )

        errors.append(
            "Packet loss range check failed."
        )

    # ========================================================
    # CHECK 7 - LATENCY
    # ========================================================

    print("\n[7] Latency Indicator Check")

    invalid_latency = results[
        (results["Latency Indicator"] < 0)
        |
        (results["Latency Indicator"] > 100)
    ]

    if invalid_latency.empty:

        print("PASS")
        print(
            "All latency indicators are between 0% and 100%."
        )

    else:

        print("FAIL")

        print(
            invalid_latency[
                [
                    "Users",
                    "Algorithm",
                    "Latency Indicator"
                ]
            ].to_string(
                index=False
            )
        )

        errors.append(
            "Latency indicator check failed."
        )

    # ========================================================
    # CHECK 8 - USER COUNTS
    # ========================================================

    print("\n[8] Scalability Test Check")

    actual_users = set(
        results["Users"].unique()
    )

    if actual_users == EXPECTED_USERS:

        print("PASS")
        print(
            "5, 10, 20 and 50-user experiments found."
        )

    else:

        print("FAIL")

        print(
            "Expected:",
            sorted(EXPECTED_USERS)
        )

        print(
            "Found:",
            sorted(actual_users)
        )

        errors.append(
            "Scalability user-count check failed."
        )

    # ========================================================
    # CHECK 9 - DUPLICATE EXPERIMENTS
    # ========================================================

    print("\n[9] Experiment Completeness Check")

    expected_rows = (
        len(EXPECTED_USERS)
        * len(EXPECTED_ALGORITHMS)
    )

    actual_rows = len(results)

    if actual_rows == expected_rows:

        print("PASS")

        print(
            f"Expected {expected_rows} rows; "
            f"found {actual_rows}."
        )

    else:

        print("FAIL")

        print(
            f"Expected {expected_rows} rows; "
            f"found {actual_rows}."
        )

        errors.append(
            "Experiment completeness check failed."
        )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("=" * 70)

    if not errors:

        print(
            "             ALL VALIDATION CHECKS PASSED"
        )

        print("=" * 70)

        print(
            "\nSystem validation successful."
        )

        print(
            "The implementation is ready for final testing."
        )

    else:

        print(
            "             VALIDATION FAILED"
        )

        print("=" * 70)

        print("\nProblems found:")

        for error in errors:

            print(
                "-",
                error
            )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()