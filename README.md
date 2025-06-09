# Dynamic Customer Segmentation and Lifetime Value Prediction

## Overview
This project develops a machine learning pipeline to segment customers and predict their lifetime value (CLV) using the UCI Online Retail dataset. It combines clustering (K-means, DBSCAN), NLP for review analysis, and Gradient Boosting for CLV prediction. A SQL-driven ETL pipeline preprocesses data, and a PowerBI dashboard visualizes segment profiles and marketing strategies.

## Objectives
- Segment customers based on RFM metrics and behavioral features.
- Predict CLV to identify high-value customers.
- Provide actionable insights via an interactive PowerBI dashboard.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/customer-segmentation-clv.git


Set Up the Conda Environment:

conda create -n customer_segmentation python=3.11
conda activate customer_segmentation
pip install -r requirements.txt


## Download the Dataset:
Download the UCI Online Retail dataset from UCI Machine Learning Repository or Kaggle.
Place the dataset (Online Retail.xlsx or Online_Retail.csv) in the data/raw/ directory.

## Structure
data/: Raw and processed datasets.
src/: Python scripts for ETL, NLP, modeling, and visualization.
notebooks/: Jupyter notebooks for exploration and prototyping.
dashboards/: PowerBI dashboard file.
models/: Saved machine learning models.
scripts/: Main pipeline script.
tests/: Unit tests.
docs/: Project documentation.


## Usage
Run the main pipeline:
python scripts/main.py

## Open the PowerBI dashboard (dashboards/customer_segmentation_dashboard.pbix) to explore results.

Author
Sikhakolli Venu  vs912@scarletmail.rutgers.edu

