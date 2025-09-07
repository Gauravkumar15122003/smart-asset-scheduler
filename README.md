# 🔧 Smart Asset Scheduler

## Project Overview

The Smart Asset Scheduler is an end-to-end solution designed to predict asset failures, prioritize maintenance tasks, and provide actionable explanations for scheduling decisions. It leverages machine learning for predictive maintenance and automates the scheduling pipeline using Apache Airflow, all presented through an interactive Streamlit dashboard.

## Features

* **Predictive Failure Analysis**: Utilizes machine learning (RandomForestClassifier) to predict the probability of asset failures based on sensor data.
* [cite_start]**Intelligent Scheduling Rules**: Applies predefined business rules to categorize assets into "Urgent," "Medium," and "Low" priority based on their predicted failure probability.
* **Actionable Explanations**: Generates human-readable explanations for why an asset is assigned a particular priority, aiding in maintenance decision-making.
* **Automated Pipeline (Airflow)**: Orchestrates the entire data processing, model prediction, and scheduling pipeline using Apache Airflow, ensuring daily execution and updated schedules.
* **Interactive Dashboard**: A Streamlit application provides a comprehensive visual interface to explore sensor trends, historical failures, predicted outcomes, priority breakdowns, and comparative analysis.
* **Dockerized Environment**: The entire application, including the Airflow setup and the Streamlit dashboard, is containerized using Docker and Docker Compose for easy setup and deployment.

## Technology Stack

* **Python**: Core programming language.
* [cite_start]**Pandas**: Data manipulation and analysis.
* **Scikit-learn**: Machine Learning (RandomForestClassifier, LabelEncoder).
* **Streamlit**: Interactive web dashboard development.
* **Plotly Express & Seaborn**: Data visualization in the dashboard.
* **Apache Airflow**: Workflow management and pipeline orchestration.
* **Docker & Docker Compose**: Containerization and environment orchestration.
* **PostgreSQL**: Airflow metadata database.

## Folder Structure

SMART_ASSET_SCHEDULER
├── .env                           # Environment variables for Docker Compose 
├── .gitignore                     # Specifies intentionally untracked files to ignore 
├── asset_scheduler_dag.py         # Apache Airflow DAG definition
├── app.py                         # Streamlit dashboard application
├── data/
│   ├── final_schedule.csv         # Output of the pipeline: scheduled assets with predictions,priority.
│   └── synthetic_asset_data.csv   # Input data for assets, including sensor readings.
├── docker-compose.yaml            # Docker Compose configuration for Airflow and PostgreSQL
├── Dockerfile                     # Dockerfile for the main application (used for local main.py run)
├── main.py                        # Main script to run the entire scheduling pipeline locally 
├── pipeline/
│   ├── explanation_agent.py       # Module to generate human-readable explanations for scheduling decisions
│   ├── scheduler_model.py         # Module containing the ML model training and prediction logic
│   └── scheduling_rules.py        # Module defining rules for assigning priority to assets 
└── requirements.txt               # Python dependencies


## Getting Started

These instructions will get your project up and running on your local machine.

### Prerequisites

* **Docker Desktop**: Ensure Docker and Docker Compose are installed on your system.

### Setup Steps

1.  **Clone the Repository**:
    ```bash
    git clone <your-repository-url>
    cd smart-asset-scheduler
    ```

2.  **Create `requirements.txt`**:
    Ensure you have a `requirements.txt` file in your root directory listing all Python dependencies. A minimal `requirements.txt` for this project would include:
    ```
    pandas
    scikit-learn
    streamlit
    plotly
    seaborn
    apache-airflow==2.8.1
    apache-airflow-providers-postgres
    psycopg2-binary
    ```

3.  **Prepare Data**:
    Place your `synthetic_asset_data.csv` (and if existing, `final_schedule.csv`) into the `data/` directory. If `final_schedule.csv` does not exist, it will be generated upon first pipeline run.

4.  **Start Airflow Environment**:
    Navigate to the root directory of your project (where `docker-compose.yaml` is located) and run:
    ```bash
    docker-compose up -d
    ```
    This command will:
    * Build the Airflow images (if not already built).
    * Start the PostgreSQL database.
    * Initialize the Airflow database (`airflow-init` service).
    * Start the Airflow webserver (accessible at `http://localhost:8081`).
    * Start the Airflow scheduler.

5.  **Unpause the DAG in Airflow UI**:
    * Open your browser and go to `http://localhost:8081`.
    * Log in with default credentials: `airflow` / `airflow`.
    * Navigate to the "DAGs" section.
    * Find `asset_scheduler_dag` and toggle the button to unpause it.
    * You can manually trigger the DAG by clicking the "Play" button next to it or wait for its scheduled run (`@daily`).
    * Once the DAG runs successfully, `final_schedule.csv` will be generated/updated in your `data/` folder.

6.  **Run the Streamlit Dashboard**:
    Open a new terminal, navigate to the project root, and run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
    This will open the dashboard in your default web browser (usually `http://localhost:8501`).

## Usage

### Running the pipeline locally (without Airflow)

You can execute the entire pipeline once locally using `main.py`:
```bash
python main.py
This script will read 

synthetic_asset_data.csv, process it, and save the output to data/final_schedule.csv.

Using the Streamlit Dashboard
Once the Streamlit app is running, you can:

Filter assets by their IDs using the sidebar.
View sensor trends (Usage Hours, Temperature, Pressure) over time.
Analyze historical failure counts and visualize them on a heatmap.
Examine predicted failure distributions and probabilities.
See the most common explanations for predicted failures.
Review asset priority levels and a specific list of high-risk assets.
Compare actual vs. predicted failures.
Understand sensor data correlations.
Browse the full raw and prediction output data tables.

Airflow Automation
The asset_scheduler_dag.py defines a daily scheduled job that automatically runs the predictive maintenance pipeline. This ensures that your final_schedule.csv is always up-to-date with the latest predictions and priorities, reflecting the synthetic_asset_data.csv content.

Data
synthetic_asset_data.csv: Contains time-series data for various assets, including unique Asset_ID, Date, Usage_Hours, Temperature, Pressure, and a Failure flag (1 for failure, 0 for no failure).


final_schedule.csv: The output of the pipeline, including all columns from the input data, plus Failure_Prob (predicted probability of failure), Predicted_Failure (boolean indicating predicted failure), Priority (Urgent, Medium, Low), and Explanation.

Model Details
The project uses a RandomForestClassifier from scikit-learn to predict asset failures. It is trained on Asset_ID_Code (derived from Asset_ID using Label Encoding), Usage_Hours, Temperature, and Pressure.

Scheduling and Explanation Logic
Prioritization: Assets are categorized based on Failure_Prob:

Failure_Prob > 0.85: "Urgent"
0.7 < Failure_Prob <= 0.85: "Medium"
Failure_Prob <= 0.7: "Low"

Explanations: The explanation_agent generates dynamic explanations based on the assigned Priority:

"Urgent": {Asset_ID} shows high risk of failure based on usage and temp. Immediate maintenance required.
"Medium": {Asset_ID} is under moderate stress. Maintenance needed soon.
"Low": {Asset_ID} is operating normally.

#change the pwd of Airflow
docker exec -it smart-asset-scheduler-airflow-webserver-1 airflow users create --username airflow --firstname Gaurav --lastname Kumar --role Admin --email gaurav@example.com --password airflow

Run with Docker

docker run -v ${PWD}/data:/app/data smart-scheduler
