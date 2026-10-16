
# 🚦 Fair Bandwidth Allocation System

A Python-based network bandwidth allocation simulator that compares **FCFS, Round Robin, Weighted Fair Queuing (WFQ), and Max-Min Fairness** algorithms under different traffic conditions.

The project evaluates how different allocation strategies distribute limited network bandwidth among multiple users using performance metrics such as throughput, fairness, and bandwidth utilization.

## 📌 Project Overview

Network bandwidth is a limited resource that must be shared efficiently among competing users. An allocation strategy that favors certain users may lead to unfair resource distribution, while inefficient allocation can result in unused bandwidth.

This project simulates different bandwidth allocation algorithms and compares their performance under fixed and varying traffic demands. It also provides a Streamlit-based interface for exploring the results and visualizing algorithm performance.

## ✨ Features

- **Multiple allocation algorithms:** Compare four bandwidth allocation strategies.
- **Interactive dashboard:** Explore simulations through a Streamlit interface.
- **Fixed traffic scenarios:** Test algorithms with predefined user demands.
- **Random traffic generation:** Simulate varying traffic conditions with different numbers of users.
- **Performance evaluation:** Measure throughput, fairness, utilization, and unmet demand.
- **Scalability experiments:** Evaluate performance with different user counts.
- **Data visualization:** Generate plots to compare algorithm performance.
- **Validation tools:** Run system checks to verify the implementation.
- **Experiment results:** Store simulation outputs for further analysis.

## ⚙️ Algorithms Implemented

### 1. First-Come, First-Served (FCFS)
Allocates bandwidth according to the order in which users are processed. Earlier users may receive bandwidth before later users, potentially leading to an uneven distribution.

### 2. Round Robin
Distributes bandwidth across users in a cyclic manner, promoting balanced access to the available resource.

### 3. Weighted Fair Queuing (WFQ)
Allocates bandwidth according to user weights, allowing users with higher weights to receive a proportionally larger share of available bandwidth.

### 4. Max-Min Fairness
Distributes bandwidth to maximize the minimum allocation among users while respecting their demands and the total available capacity.

## 📊 Performance Metrics

| Metric | Description |
|---|---|
| Throughput | Total bandwidth allocated to users. |
| Jain's Fairness Index | Measures how fairly bandwidth is distributed, typically from 0 to 1. |
| Bandwidth Utilization | Percentage of available bandwidth used. |
| Demand Loss (%) | Indicates the proportion of requested bandwidth that remains unallocated. |

**Note:** Demand loss and any latency-related indicators in this simulator are model-derived indicators. They should not be interpreted as actual network packet loss or measured latency in milliseconds.

## 🛠️ Technology Stack

- **Language:** Python
- **Dashboard:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib
- **Version Control:** Git and GitHub

## 📁 Project Structure

```text
Fair_Bandwidth_Allocation/
│
├── algorithms/
│   ├── fcfs.py
│   ├── round_robin.py
│   ├── wfq.py
│   └── max_min.py
│
├── simulation/
│   ├── traffic_generator.py
│   └── simulator.py
│
├── metrics/
│   └── metrics.py
│
├── data/
│   └── experiments/
│
├── app.py
├── run_experiments.py
├── generate_scalability_plots.py
├── validate_system.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or later (use the version compatible with your installed dependencies).
- pip
- Git (optional, for cloning the repository)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Fair-Bandwidth-Allocation.git
cd Fair-Bandwidth-Allocation
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If the virtual environment is already active, you can skip this step.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the dashboard.

## 🧪 Running Experiments

Run the experiment script to evaluate the allocation algorithms:

```bash
python run_experiments.py
```

Generate scalability plots:

```bash
python generate_scalability_plots.py
```

Run the validation script:

```bash
python validate_system.py
```

**Note:** Run each command from the project root directory. The generated files and results depend on the implementation and configuration in your local project.

## 📈 Experimental Evaluation

The simulator can be used to compare the algorithms under different traffic conditions, including scenarios with different numbers of users.

The experiments focus on:

- Bandwidth distribution among competing users.
- Fairness of resource allocation.
- Total throughput achieved.
- Efficient utilization of available bandwidth.
- Changes in allocation behavior as the number of users increases.

Actual outcomes depend on the simulation configuration, user demands, weights, and algorithm implementations. Consult the generated experiment results before drawing conclusions about which algorithm performs best.

## 🎯 Applications

- Computer Networks coursework and demonstrations.
- Network resource allocation studies.
- Fairness analysis in shared communication systems.
- Simulation-based comparison of scheduling algorithms.
- Academic projects and experimental research.

## 🔮 Future Improvements

- Introduce dynamic bandwidth capacity and changing network conditions.
- Add configurable QoS priorities and user classes.
- Incorporate queue-length and delay models.
- Compare additional scheduling algorithms.
- Extend the simulator with more detailed packet-level network behavior.

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Submit a pull request.

## 👨‍💻 Author

**Vedesh Vuppalapati**

Computer Science Engineering — Artificial Intelligence and Machine Learning

SRM Institute of Science and Technology, Ramapuram, Chennai

## 📄 License

This project is available for educational and research purposes. Add a `LICENSE` file to the repository if you want to specify formal permissions for reuse and distribution.
