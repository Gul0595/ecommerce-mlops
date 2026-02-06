🛒 Real-Time Ecommerce MLOps Pipeline

Production-grade ecommerce data system with real-time streaming, automated model benchmarking, hyperparameter tuning, ensemble modeling, CI/CD gating, and executive analytics dashboard.

🔗 Repository: https://github.com/Gul0595/ecommerce-mlops

🚀 Project Overview

This project simulates a real-world ecommerce company’s production ML system.

It covers:

Real-time data ingestion using Kafka

Streaming data processing

Cloud database integration (Railway MySQL)

Feature engineering pipeline

Model benchmarking

Hyperparameter tuning (Optuna)

Ensemble learning (Stacking & Voting)

CI quality gate

Executive analytics dashboard (Streamlit)

CI/CD automation

This is a complete Data Engineering + ML + DevOps pipeline.

🏗 System Architecture
Sales Event Simulation (Producer)
        ↓
Apache Kafka
        ↓
Zookeeper
        ↓
Consumer (Data Processing)
        ↓
Feature Engineering
        ↓
MySQL (Railway Cloud)
        ↓
Model Benchmarking
        ↓
Optuna Hyperparameter Tuning
        ↓
Ensemble Model Training
        ↓
CI Gate Validation
        ↓
Streamlit Executive Dashboard

🔄 Real-Time Streaming Layer
producer.py

Simulates ecommerce transaction events

Publishes structured JSON messages to Kafka topics

consumer.py

Consumes Kafka messages

Cleans and transforms data

Stores processed records into MySQL

Zookeeper

Coordinates Kafka brokers

Ensures distributed system reliability

🧠 Machine Learning Pipeline

This project follows a structured ML workflow.

1️⃣ Feature Engineering

build_features.py

Data preprocessing

Feature creation

Target preparation

2️⃣ Model Benchmarking

benchmark_models.py

Trains multiple baseline models

Compares performance metrics

Identifies top performers

Models included:

LinearRegression

Lasso

GradientBoosting

Others

Saved models:

LinearRegression.pkl

Lasso.pkl

GradientBoosting.pkl

3️⃣ Hyperparameter Tuning

optuna_tune_stacking.py

Uses Optuna for tuning stacking ensemble

Optimizes model weights & parameters

Improves generalization performance

4️⃣ Ensemble Training
Voting Ensemble

VotingEnsemble.pkl

Stacking Ensemble

StackingEnsemble.pkl

StackingEnsemble_Optuna.pkl

Final model selected after evaluating:

RMSE

MAE

R² score

Stability on validation data

🔐 CI Quality Gate

ci_gate.py

Implements automated validation checks:

Model performance threshold validation

Regression metric verification

Prevents deployment if metrics degrade

This ensures:

Model quality control

Reproducibility

Safe deployment

Production readiness

This mimics real-world MLOps governance systems.

📊 Executive Dashboard

app.py

Built using:

Streamlit

Plotly

Pandas

SQLAlchemy

Features:

✔ Executive KPIs
✔ Revenue trends
✔ City & product analysis
✔ Discount intelligence
✔ Time-based analysis
✔ Customer segmentation

Designed for business stakeholders.

🛠 Tech Stack
Layer	Technology
Streaming	Apache Kafka
Coordination	Zookeeper
Backend	Python
Database	MySQL (Railway)
Feature Engineering	Pandas
ML	Scikit-learn
Hyperparameter Tuning	Optuna
Ensembles	Stacking & Voting
Dashboard	Streamlit
Visualization	Plotly
CI/CD	GitHub Actions
SQL Tooling	SQL Workbench
📂 Repository Structure
ecommerce-mlops/
│
├── producer.py
├── consumer.py
├── build_features.py
├── benchmark_models.py
├── train_top_models.py
├── train_stacking.py
├── train_ensemble.py
├── optuna_tune_stacking.py
├── ci_gate.py
│
├── LinearRegression.pkl
├── Lasso.pkl
├── GradientBoosting.pkl
├── VotingEnsemble.pkl
├── StackingEnsemble.pkl
├── StackingEnsemble_Optuna.pkl
│
├── app.py
├── requirements.txt
└── .github/workflows/

⚙️ Running the System
Start Zookeeper
zookeeper-server-start.bat config/zookeeper.properties

Start Kafka Broker
kafka-server-start.bat config/server.properties

Run Producer
python producer.py

Run Consumer
python consumer.py

Train Models
python benchmark_models.py
python train_top_models.py
python train_stacking.py
python train_ensemble.py

Launch Dashboard
streamlit run app.py

🎯 Key Engineering Highlights

✔ Real-time distributed data pipeline
✔ Structured feature engineering workflow
✔ Automated model benchmarking
✔ Optuna-based hyperparameter tuning
✔ Multiple ensemble strategies
✔ CI quality gating
✔ Cloud-hosted database
✔ Production-style MLOps workflow

📈 Business Value Simulation

Revenue prediction

Discount optimization

Demand analysis

Customer behavior insights

Executive-level monitoring

This architecture reflects how scalable ecommerce analytics systems are built in production.

👩‍💻 Author

Gulshanpreet Kaur
Machine Learning | Data Engineering | MLOps
