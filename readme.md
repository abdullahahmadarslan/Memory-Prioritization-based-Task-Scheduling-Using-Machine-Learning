# PMPD-Based Scheduling and Visualization on Alibaba Cluster Dataset

## 📌 Project Overview

This project implements the **Memory Priority Scheduling Algorithm (PMPD)** proposed in the IEEE paper _"Memory Priority Scheduling Algorithm for Cloud Data Center Based on Machine Learning Dynamic Clustering Algorithm"_ by Bin Liang and Di Wu. It is applied to real-world **Alibaba Cluster Data (2018)** to optimize scheduling, analyze workload patterns, and visualize system performance.

---

## 📊 Data Visualization Phase

### 🔗 Data Source
Dataset: [Alibaba Cluster Trace v2018](https://github.com/alibaba/clusterdata/blob/master/cluster-trace-v2018/fetchData.sh)

---

### 📦 Data Preprocessing

The project extracts a sample of the `batch_instance.tar.gz` file to simulate a scalable big data environment:

```python
import tarfile

with tarfile.open('batch_instance.tar.gz', 'r:gz') as tar:
    members = tar.getmembers()
    tar.extractall(path='extracted_batch_instance', members=members[:int(len(members) * 0.2)])
```

Then it loads and cleans the dataset with assigned schema:

```python
columns = ["instance_name", "task_name", "job_name", "task_type", "status", "start_time", "end_time",
           "machine_id", "seq_no", "total_seq_no", "cpu_avg", "cpu_max", "mem_avg", "mem_max"]

df = pd.read_csv("extracted_batch_instance/batch_instance.csv", names=columns)
df["duration"] = df["end_time"].astype(int) - df["start_time"].astype(int)
df = df[df['duration'] >= 0]
```

---

### 📈 Visualization with Plotly

This visualization provides insights into instance durations across different statuses.

- Duration vs. Instance
- Color-coded by status (Running, Terminated, Failed, Interrupted)
- Interactive scrolling with `rangeslider`

Example visualization snippet:

```python
import plotly.express as px

fig = px.bar(
    sample_df,
    x="instance_name",
    y="duration",
    color="status",
    title="Instance Duration by Status",
    hover_data={
        "instance_name": True,
        "task_name": True,
        "job_name": True,
        "status": True,
        "machine_id": True,
        "mem_avg": True,
        "cpu_avg": True,
        "duration": True
    },
    category_orders={"status": ["Terminated", "Running", "Failed", "Interrupted"]}
)

fig.update_layout(
    xaxis_title="Instance Name",
    yaxis_title="Duration (s)",
    xaxis={'categoryorder': 'total descending'},
    height=600,
    margin=dict(l=40, r=40, t=60, b=100),
    xaxis_tickangle=45,
    showlegend=True,
    dragmode="pan",
    legend_title_text='Status'
)

fig.update_xaxes(
    rangeslider_visible=True,
    tickmode='auto',
    tickfont=dict(size=10)
)

fig.show()
```

---

## 🤖 PMPD Algorithm Implementation

The **PMPD (Priority Memory Priority Deployment)** algorithm is implemented as described in the paper.

### 🔍 Core Features

- Dynamically clusters PMs based on balanced CPU and memory utilization using **k-means**
- Classifies VMs based on their **CPU-to-memory ratio** and deploys them to the most suitable PM within that cluster
- Prioritizes minimizing **energy consumption** and **idle time** in data centers
- Implements the logic defined in the paper’s **Algorithm 1 and flowchart**

---

## 📓 Notebook

- `PMPD.ipynb`: contains a full implementation and testing of the PMPD algorithm using Alibaba's batch instance data.
- The notebook processes the trace, applies clustering (via `scikit-learn`), and simulates VM deployments.

The PMPD scheduling logic includes:

- CPU/memory ratio-based classification of VMs  
- Dynamic clustering of PMs  
- Smart matching using `min(abs(pmj.rt - vmi.nt))` logic  
- Deployment decisions that update PM utilization state

---

## ⚙️ Big Data Tools Used

- **Apache Kafka** – for streaming/logging (optional integration)
- **Apache Spark** – for scalable data processing

---

## 📚 Reference

Liang, B., & Wu, D. (2025).  
**Memory Priority Scheduling Algorithm for Cloud Data Center Based on Machine Learning Dynamic Clustering Algorithm**.  
*IEEE Transactions on Industrial Informatics*, 21(4), 3485–3492.  
[IEEE DOI Link](https://doi.org/10.1109/TII.2025.3528574)

---

