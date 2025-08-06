# PMPD-Based Scheduling and Visualization on Alibaba Cluster Dataset

## 📌 Project Overview

This project implements the **Memory Priority Scheduling Algorithm (PMPD)** proposed in the IEEE paper _"Memory Priority Scheduling Algorithm for Cloud Data Center Based on Machine Learning Dynamic Clustering Algorithm"_ by Bin Liang and Di Wu. It is applied to real-world **Alibaba Cluster Data (2018)** to optimize scheduling, analyze workload patterns, and visualize system performance.

---

## 📊 Data Visualization Phase

### 🔗 Data Source
Dataset: [Alibaba Cluster Trace v2018](https://github.com/alibaba/clusterdata/blob/master/cluster-trace-v2018/fetchData.sh)  


### 📦 Data Preprocessing
The project extracts  a sample of the `batch_instance.tar.gz` file to simulate a scalable big data environment:

```
    import tarfile

    with tarfile.open('batch_instance.tar.gz', 'r:gz') as tar:
        members = tar.getmembers()
        tar.extractall(path='extracted_batch_instance', members=members[:int(len(members) * 0.2)])

    Then it loads and cleans the dataset with assigned schema:

```
    columns = ["instance_name", "task_name", "job_name", "task_type", "status", "start_time", "end_time",
            "machine_id", "seq_no", "total_seq_no", "cpu_avg", "cpu_max", "mem_avg", "mem_max"]
    df = pd.read_csv("extracted_batch_instance/batch_instance.csv", names=columns)
    df["duration"] = df["end_time"].astype(int) - df["start_time"].astype(int)
df = df[df['duration'] >= 0]

## 📈 Visualization with Plotly
Visualization with Plotly

* Duration vs. Instance
* Color-coded by status (Running, Terminated, Failed, Interrupted)
* Interactive scrolling with rangeslider

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
