import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import altair as alt


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# PROJECT IMPORTS
# ============================================================

from simulation.traffic_generator import TrafficGenerator
from simulation.simulator import BandwidthSimulator


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Fair Bandwidth Allocation",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.05rem;
        opacity: 0.75;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.6rem;
        font-weight: 650;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }

    .kpi-card {
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        background: rgba(128, 128, 128, 0.06);
        min-height: 130px;
    }

    .kpi-title {
        font-size: 0.9rem;
        opacity: 0.7;
        margin-bottom: 0.4rem;
    }

    .kpi-value {
        font-size: 1.35rem;
        font-weight: 700;
    }

    .kpi-subtitle {
        font-size: 0.85rem;
        opacity: 0.7;
        margin-top: 0.35rem;
    }

    .footer {
        text-align: center;
        opacity: 0.55;
        font-size: 0.8rem;
        padding-top: 1.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📡 Fair Bandwidth Allocation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Intelligent simulation and comparison of bandwidth allocation
    algorithms under constrained network conditions.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Configuration")

st.sidebar.markdown(
    "Configure the network before running the simulation."
)


capacity = st.sidebar.number_input(
    "Network Capacity (Mbps)",
    min_value=1.0,
    max_value=1000.0,
    value=10.0,
    step=1.0
)


scenario = st.sidebar.selectbox(
    "Traffic Scenario",
    [
        "Fixed Test Scenario",
        "Random Traffic"
    ]
)


number_of_users = 4


if scenario == "Random Traffic":

    number_of_users = st.sidebar.number_input(
        "Number of Users",
        min_value=2,
        max_value=50,
        value=10,
        step=1
    )


st.sidebar.markdown("---")

run_simulation = st.sidebar.button(
    "🚀 Run Simulation",
    type="primary",
    use_container_width=True
)


st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    **Algorithms**

    • FCFS  
    • Round Robin  
    • Weighted Fair Queuing  
    • Max-Min Fairness
    """
)


# ============================================================
# INITIAL SCREEN
# ============================================================

if not run_simulation:

    st.info(
        "👆 Configure the network from the sidebar and click "
        "**Run Simulation** to begin."
    )

    st.markdown(
        '<div class="section-title">🔄 System Workflow</div>',
        unsafe_allow_html=True
    )

    st.code(
        """
Traffic Generator
        |
        v
Simulation Engine
        |
        +---------+-------------+-------------+
        |         |             |             |
       FCFS   Round Robin      WFQ       Max-Min
        |         |             |             |
        +---------+-------------+-------------+
                          |
                          v
                    Metrics Engine
                          |
                          v
                 Performance Analysis
                          |
                          v
                  Streamlit Dashboard
        """,
        language="text"
    )

    st.markdown(
        '<div class="section-title">🎯 Project Objective</div>',
        unsafe_allow_html=True
    )

    st.write(
        """
        The system evaluates how different bandwidth allocation
        policies distribute limited network resources among
        competing users. The algorithms are compared using
        fairness, throughput, utilization, packet/demand loss,
        and a simulation-level latency indicator.
        """
    )

    st.markdown("---")

    st.caption(
        "Fair Bandwidth Allocation System | Simulation Prototype"
    )

    st.stop()


# ============================================================
# GENERATE TRAFFIC
# ============================================================

generator = TrafficGenerator()


if scenario == "Fixed Test Scenario":

    users = generator.generate_fixed_users()

else:

    users = generator.generate_random_users(
        number_of_users
    )


# ============================================================
# BASIC NETWORK INFORMATION
# ============================================================

total_demand = float(
    users["demand"].sum()
)

number_of_users_actual = len(users)

demand_ratio = (
    total_demand / capacity
    if capacity > 0
    else 0
)


# ============================================================
# TRAFFIC SCENARIO
# ============================================================

st.markdown(
    '<div class="section-title">📊 Traffic Scenario</div>',
    unsafe_allow_html=True
)

st.dataframe(
    users,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# NETWORK STATUS
# ============================================================

info_col1, info_col2, info_col3, info_col4 = st.columns(4)


with info_col1:

    st.metric(
        "Network Capacity",
        f"{capacity:.2f} Mbps"
    )


with info_col2:

    st.metric(
        "Total Demand",
        f"{total_demand:.2f} Mbps"
    )


with info_col3:

    st.metric(
        "Users",
        number_of_users_actual
    )


with info_col4:

    if total_demand <= capacity:

        st.metric(
            "Network Status",
            "Under Capacity"
        )

    else:

        st.metric(
            "Network Status",
            "Congested"
        )


# ============================================================
# CONGESTION INDICATOR
# ============================================================

if total_demand > capacity:

    excess = (
        total_demand
        - capacity
    )

    st.warning(
        f"""
        ⚠️ **Network congestion detected.**

        Requested bandwidth exceeds available capacity by
        **{excess:.2f} Mbps**.

        Allocation algorithms must therefore decide how the
        limited {capacity:.2f} Mbps should be distributed fairly.
        """
    )

else:

    st.success(
        """
        ✅ Network capacity is sufficient for the current
        traffic demand.
        """
    )


# ============================================================
# CREATE SIMULATOR
# ============================================================

simulator = BandwidthSimulator(
    capacity=capacity
)


# ============================================================
# RUN ALGORITHMS
# ============================================================

with st.spinner(
    "Running FCFS, Round Robin, WFQ and Max-Min..."
):

    try:

        results = simulator.run_all(
            users
        )

    except Exception as error:

        st.error(
            "An error occurred while running the simulation."
        )

        st.exception(error)

        st.stop()


st.success(
    "✅ All allocation algorithms completed successfully."
)


# ============================================================
# PERFORMANCE COMPARISON
# ============================================================

st.markdown(
    '<div class="section-title">📈 Performance Comparison</div>',
    unsafe_allow_html=True
)


comparison = (
    simulator.create_comparison_table(
        results
    )
)


st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FIND BEST ALGORITHMS
# ============================================================

best_fairness_index = comparison[
    "Fairness Index"
].idxmax()

best_throughput_index = comparison[
    "Throughput (Mbps)"
].idxmax()

best_utilization_index = comparison[
    "Utilization (%)"
].idxmax()


best_fairness_algorithm = comparison.loc[
    best_fairness_index,
    "Algorithm"
]

best_fairness_value = comparison.loc[
    best_fairness_index,
    "Fairness Index"
]


best_throughput_algorithm = comparison.loc[
    best_throughput_index,
    "Algorithm"
]

best_throughput_value = comparison.loc[
    best_throughput_index,
    "Throughput (Mbps)"
]


best_utilization_algorithm = comparison.loc[
    best_utilization_index,
    "Algorithm"
]

best_utilization_value = comparison.loc[
    best_utilization_index,
    "Utilization (%)"
]


# ============================================================
# KPI CARDS
# ============================================================

st.markdown(
    '<div class="section-title">🏆 Key Performance Indicators</div>',
    unsafe_allow_html=True
)


kpi1, kpi2, kpi3 = st.columns(3)


with kpi1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">⚖️ BEST FAIRNESS</div>
            <div class="kpi-value">{best_fairness_algorithm}</div>
            <div class="kpi-subtitle">
                Jain's Index: {best_fairness_value:.4f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🚀 BEST THROUGHPUT</div>
            <div class="kpi-value">{best_throughput_algorithm}</div>
            <div class="kpi-subtitle">
                {best_throughput_value:.2f} Mbps
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📡 BEST UTILIZATION</div>
            <div class="kpi-value">{best_utilization_algorithm}</div>
            <div class="kpi-subtitle">
                {best_utilization_value:.2f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Allocation",
        "⚖️ Fairness",
        "🚀 Performance",
        "🧠 Analysis"
    ]
)


# ============================================================
# TAB 1 - ALLOCATION
# ============================================================

with tab1:

    st.subheader(
        "Bandwidth Allocation by User"
    )

    allocation_data = []

    for algorithm, result in results.items():

        allocation_df = (
            result["allocation"]
            .copy()
        )

        allocation_df["Algorithm"] = (
            algorithm
        )

        allocation_data.append(
            allocation_df
        )

    allocation_chart_df = pd.concat(
        allocation_data,
        ignore_index=True
    )

    chart = (
        alt.Chart(
            allocation_chart_df
        )
        .mark_bar()
        .encode(
            x=alt.X(
                "user_id:N",
                title="User"
            ),
            xOffset=alt.XOffset(
                "Algorithm:N"
            ),
            y=alt.Y(
                "allocation:Q",
                title="Allocated Bandwidth (Mbps)"
            ),
            color=alt.Color(
                "Algorithm:N",
                title="Algorithm"
            ),
            tooltip=[
                "user_id",
                "Algorithm",
                alt.Tooltip(
                    "allocation:Q",
                    title="Allocation (Mbps)",
                    format=".2f"
                )
            ]
        )
        .properties(
            height=450
        )
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )

    st.subheader(
        "Detailed Allocations"
    )

    for algorithm, result in results.items():

        with st.expander(
            f"📌 {algorithm}"
        ):

            st.dataframe(
                result["allocation"],
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# TAB 2 - FAIRNESS
# ============================================================

with tab2:

    st.subheader(
        "Jain's Fairness Index"
    )

    fairness_chart = comparison[
        [
            "Algorithm",
            "Fairness Index"
        ]
    ]

    fairness_visual = (
        alt.Chart(
            fairness_chart
        )
        .mark_bar()
        .encode(
            x=alt.X(
                "Algorithm:N",
                title="Algorithm"
            ),
            y=alt.Y(
                "Fairness Index:Q",
                title="Fairness Index",
                scale=alt.Scale(
                    domain=[0, 1]
                )
            ),
            tooltip=[
                "Algorithm",
                alt.Tooltip(
                    "Fairness Index:Q",
                    format=".4f"
                )
            ]
        )
        .properties(
            height=420
        )
    )

    st.altair_chart(
        fairness_visual,
        use_container_width=True
    )

    st.info(
        """
        Jain's Fairness Index ranges from 0 to 1.

        A value closer to **1** indicates a more balanced
        allocation of bandwidth among users.
        """
    )


# ============================================================
# TAB 3 - PERFORMANCE
# ============================================================

with tab3:

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # THROUGHPUT
    # --------------------------------------------------------

    with col1:

        st.subheader(
            "🚀 Throughput"
        )

        throughput_data = comparison[
            [
                "Algorithm",
                "Throughput (Mbps)"
            ]
        ]

        throughput_chart = (
            alt.Chart(
                throughput_data
            )
            .mark_bar()
            .encode(
                x=alt.X(
                    "Algorithm:N",
                    title="Algorithm"
                ),
                y=alt.Y(
                    "Throughput (Mbps):Q",
                    title="Throughput (Mbps)"
                ),
                tooltip=[
                    "Algorithm",
                    alt.Tooltip(
                        "Throughput (Mbps):Q",
                        format=".2f"
                    )
                ]
            )
            .properties(
                height=350
            )
        )

        st.altair_chart(
            throughput_chart,
            use_container_width=True
        )

    # --------------------------------------------------------
    # UTILIZATION
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "📡 Network Utilization"
        )

        utilization_data = comparison[
            [
                "Algorithm",
                "Utilization (%)"
            ]
        ]

        utilization_chart = (
            alt.Chart(
                utilization_data
            )
            .mark_bar()
            .encode(
                x=alt.X(
                    "Algorithm:N",
                    title="Algorithm"
                ),
                y=alt.Y(
                    "Utilization (%):Q",
                    title="Utilization (%)",
                    scale=alt.Scale(
                        domain=[0, 100]
                    )
                ),
                tooltip=[
                    "Algorithm",
                    alt.Tooltip(
                        "Utilization (%):Q",
                        format=".2f"
                    )
                ]
            )
            .properties(
                height=350
            )
        )

        st.altair_chart(
            utilization_chart,
            use_container_width=True
        )

    # --------------------------------------------------------
    # LOSS
    # --------------------------------------------------------

    st.subheader(
        "📉 Packet / Demand Loss"
    )

    loss_data = comparison[
        [
            "Algorithm",
            "Packet Loss (%)"
        ]
    ]

    loss_chart = (
        alt.Chart(
            loss_data
        )
        .mark_bar()
        .encode(
            x=alt.X(
                "Algorithm:N",
                title="Algorithm"
            ),
            y=alt.Y(
                "Packet Loss (%):Q",
                title="Loss (%)",
                scale=alt.Scale(
                    domain=[0, 100]
                )
            ),
            tooltip=[
                "Algorithm",
                alt.Tooltip(
                    "Packet Loss (%):Q",
                    format=".2f"
                )
            ]
        )
        .properties(
            height=400
        )
    )

    st.altair_chart(
        loss_chart,
        use_container_width=True
    )

    # --------------------------------------------------------
    # LATENCY
    # --------------------------------------------------------

    st.subheader(
        "⏱️ Simulation Latency Indicator"
    )

    latency_data = comparison[
        [
            "Algorithm",
            "Latency Indicator"
        ]
    ]

    latency_chart = (
        alt.Chart(
            latency_data
        )
        .mark_bar()
        .encode(
            x=alt.X(
                "Algorithm:N",
                title="Algorithm"
            ),
            y=alt.Y(
                "Latency Indicator:Q",
                title="Latency Indicator (%)",
                scale=alt.Scale(
                    domain=[0, 100]
                )
            ),
            tooltip=[
                "Algorithm",
                alt.Tooltip(
                    "Latency Indicator:Q",
                    format=".2f"
                )
            ]
        )
        .properties(
            height=400
        )
    )

    st.altair_chart(
        latency_chart,
        use_container_width=True
    )

    st.caption(
        "The latency indicator is a simulation-level demand "
        "pressure indicator, not physical network latency in milliseconds."
    )


# ============================================================
# TAB 4 - ANALYSIS
# ============================================================

with tab4:

    st.subheader(
        "🧠 Simulation Interpretation"
    )

    st.success(
        f"""
        **Best Fairness:** {best_fairness_algorithm}

        Jain's Fairness Index:
        **{best_fairness_value:.4f}**
        """
    )

    st.info(
        f"""
        **Best Throughput:** {best_throughput_algorithm}

        Achieved throughput:
        **{best_throughput_value:.2f} Mbps**
        """
    )

    st.warning(
        f"""
        **Best Utilization:** {best_utilization_algorithm}

        Network utilization:
        **{best_utilization_value:.2f}%**
        """
    )

    st.markdown(
        """
        ### What the results mean

        The four allocation algorithms receive the same network
        capacity and traffic demands.

        Their performance is compared using:

        - **Fairness:** how evenly bandwidth is distributed.
        - **Throughput:** total successfully allocated bandwidth.
        - **Utilization:** percentage of network capacity used.
        - **Packet/Demand Loss:** unmet bandwidth demand.
        - **Latency Indicator:** simulation-level demand pressure
          caused by unmet demand.

        ### Algorithm characteristics

        **FCFS**
        - Simple and sequential.
        - Earlier users are prioritized.
        - Later users can experience starvation.

        **Round Robin**
        - Cycles through active users.
        - Provides more equal service opportunities.
        - Behavior depends on the configured quantum.

        **WFQ**
        - Uses user weights.
        - Higher-weight users receive proportionally more
          bandwidth when demand exists.

        **Max-Min Fairness**
        - Attempts to maximize the minimum allocation.
        - Gives equal progressive shares and redistributes
          unused bandwidth from satisfied users.
        """
    )

    st.warning(
        """
        **Important:** Packet Loss and Latency Indicator in this
        prototype are simulation-level indicators derived from
        unmet bandwidth demand. They are not measurements from
        physical network packets, queues, or propagation delay.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
    Fair Bandwidth Allocation System |
    FCFS • Round Robin • WFQ • Max-Min Fairness
    </div>
    """,
    unsafe_allow_html=True
)