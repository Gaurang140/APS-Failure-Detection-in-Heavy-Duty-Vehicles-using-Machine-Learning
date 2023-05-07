

## Problem statement

* The Air Pressure System (APS) is an essential component of heavy-duty vehicles that relies on compressed air to create pressure for braking and gear changes. Unlike hydraulic systems, APS uses natural air, making it readily available and sustainable over the long term. This project involves a binary classification problem where a positive class denotes failures caused by a specific APS component, and a negative class indicates failures due to other factors. The objective is to minimize the cost of unnecessary repairs by minimizing false predictions. The project focuses on detecting faults in the APS system through a dataset of component failure records.


## Solution

* The primary system under consideration in this project is the Air Pressure system (APS) which produces compressed air to perform critical functions in heavy-duty vehicles, including braking and gear shifts. The project's dataset includes two classes: the positive class represents failures of a specific component within the APS system, while the negative class corresponds to failures caused by other factors unrelated to the APS.

* The main objective of the project is to minimize the cost of unnecessary repairs by reducing the number of false predictions. To achieve this goal, the project focuses on detecting and predicting failures of APS components using machine learning algorithms and real-time sensor data analysis.

## Tech Stack Used
The following technologies were used in this project:

1. Python
2. Machine learning algorithms
3. Docker
4. MongoDB
5. Airflow

## Infrastructure required for deployment :
1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions



### Step 1 - Install the requirements

```bash
pip install -r requirements.txt
```

### Step 2 - Run main.py file

```bash
python main.py
```

To download your dataset

```
wget https://github.com/Gaurang140/APS-Failure-Detection-in-Heavy-Duty-Vehicles-using-Machine-Learning/blob/main/aps_failure_training_set1.csv
```
