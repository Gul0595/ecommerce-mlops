🛒 Real-Time Ecommerce MLOps Pipeline

Production-grade, end-to-end Ecommerce ML system
Real-time streaming • Automated benchmarking • Hyperparameter tuning • Ensemble modeling • CI/CD gating • Executive analytics dashboard

📌 Overview

This project simulates a real-world ecommerce company's production ML ecosystem.

It integrates:

⚡ Real-time event streaming

🧠 Structured machine learning workflow

🔬 Automated model benchmarking

🎯 Hyperparameter tuning with Optuna

🤝 Ensemble modeling (Voting + Stacking)

🔐 CI performance gating

📊 Executive-level analytics dashboard

🚀 CI/CD automation

This is not just an ML project — it’s a Data Engineering + Machine Learning + MLOps system designed for production environments.

🏗 End-to-End System Architecture
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
Ensemble Training
        ↓
CI Quality Gate
        ↓
Streamlit Executive Dashboard

⚡ Real-Time Streaming Layer
producer.py

Simulates live ecommerce transactions

Generates structured JSON sales events

Publishes messages to Kafka topics

consumer.py

Consumes Kafka streams

Cleans & validates incoming data

Performs transformation

Inserts processed records into Railway-hosted MySQL

Zookeeper

Manages Kafka broker coordination

Ensures distributed system reliability

This layer simulates real-time production ingestion pipelines used in scalable commerce systems.

🧠 Machine Learning Pipeline

The ML system follows a structured, modular workflow.

1️⃣ Feature Engineering

build_features.py

Data preprocessing

Feature creation

Target preparation

Train-test split

Data validation

Ensures reproducibility and consistency across experiments.

2️⃣ Model Benchmarking

benchmark_models.py

Trains multiple baseline models and compares:

RMSE

MAE

R² Score

Models evaluated:

Linear Regression

Lasso

Gradient Boosting

Additional baseline regressors

Top-performing models are serialized as:

LinearRegression.pkl
Lasso.pkl
GradientBoosting.pkl


This stage ensures objective model selection instead of guesswork.

3️⃣ Hyperparameter Tuning

optuna_tune_stacking.py

Uses Optuna for automated optimization

Tunes stacking ensemble parameters

Improves generalization performance

Minimizes overfitting risk

This simulates advanced experimentation workflows in real MLOps environments.

4️⃣ Ensemble Learning
Voting Ensemble
VotingEnsemble.pkl

Stacking Ensemble
StackingEnsemble.pkl
StackingEnsemble_Optuna.pkl


Final model selection based on:

RMSE

MAE

R²

Validation stability

Cross-model consistency

🔐 CI Quality Gate (MLOps Governance)

ci_gate.py

Implements automated validation checks:

Performance threshold validation

Metric regression checks

Deployment blocking if performance degrades

This prevents low-quality models from being deployed.

✅ Model quality control
✅ Safe deployment
✅ Reproducibility
✅ Production readiness

This mirrors enterprise-level MLOps governance.

📊 Executive Analytics Dashboard

app.py
Built with:

Streamlit

Plotly

Pandas

SQLAlchemy

Dashboard Capabilities

✔ Executive KPIs
✔ Revenue trend analysis
✔ City & product-level insights
✔ Discount intelligence
✔ Time-series demand patterns
✔ Customer segmentation insights

Designed specifically for business stakeholders and decision-makers, not just engineers.

🛠 Technology Stack
Layer	Technology
Streaming	Apache Kafka
Coordination	Zookeeper
Backend	Python
Database	MySQL (Railway Cloud)
Data Processing	Pandas
ML Framework	Scikit-learn
Hyperparameter Tuning	Optuna
Ensemble Learning	Voting & Stacking
Visualization	Plotly
Dashboard	Streamlit
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

⚙️ How to Run the System
1️⃣ Start Zookeeper
zookeeper-server-start.bat config/zookeeper.properties

2️⃣ Start Kafka Broker
kafka-server-start.bat config/server.properties

3️⃣ Run Streaming Layer
python producer.py
python consumer.py

4️⃣ Train ML Models
python benchmark_models.py
python train_top_models.py
python train_stacking.py
python train_ensemble.py

5️⃣ Launch Dashboard
streamlit run app.py

🎯 Engineering Highlights

✔ Real-time distributed architecture
✔ Modular feature engineering pipeline
✔ Automated model benchmarking
✔ Optuna-based hyperparameter tuning
✔ Advanced ensemble strategies
✔ CI/CD-based performance gating
✔ Cloud database integration
✔ End-to-end MLOps lifecycle

📈 Simulated Business Impact

Revenue forecasting

Discount optimization

Demand analysis

Customer behavior insights

Executive-level monitoring

This architecture reflects how scalable ecommerce analytics systems are designed in real production environments.

👩‍💻 Author

Gulshanpreet Kaur
Machine Learning | Data Engineering | MLOps
