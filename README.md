# Supply-Chain Late-Delivery Risk Model

A pre-shipment machine-learning risk checker built with the DataCo Smart Supply Chain dataset.

## Dataset
Source: [DataCo Smart Supply Chain for Big Data Analysis (Kaggle)](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)

Download `DataCoSupplyChainDataset.csv` and place it at `data/raw/DataCoSupplyChainDataset.csv`. The raw dataset is not included in this repository.

## Problem and features
Predict `Late_delivery_risk` (1 = late risk, 0 = no late risk) from the four project-brief inputs:
- Market
- Shipping Mode
- Product Name
- Days for shipment (scheduled)

Actual shipping duration, delivery status, actual shipping dates, and other post-outcome fields are excluded to prevent target leakage. In this dataset, Delivery Status directly identifies the target.

## Data profile
The supplied dataset contains 180,519 order-item rows, 53 columns, and 65,752 unique orders. Late-risk class share is 54.83%. Rows belonging to the same order share the same label, so evaluation uses order-grouped splits and cross-validation.

## Measured held-out results
The tuned Decision Tree achieved:
- Accuracy: 69.32%
- Precision: 84.22%
- Recall: 54.21%
- F1: 65.96%
- ROC-AUC: 0.7251

These results are on a grouped holdout of 36,104 item rows from 13,151 unseen orders. The majority-class baseline obtains 100% recall by flagging every row, so this model is more selective but does not improve recall over that trivial baseline. Do not describe it as a high-recall detector.

Detailed reports and plots are in `reports/`.

## Run locally
Python 3.13 is recommended to match the saved scikit-learn artifact.

```bash
python -m venv .venv
# activate the environment, then:
pip install -r requirements.txt
streamlit run app.py
```

The Streamlit app loads the included inference artifacts from `models/`. The raw CSV is only required to retrain or rerun the full notebook.

## Retrain
Install development dependencies from `requirements-dev.txt`, add the Kaggle CSV to `data/raw/`, then run:

```bash
python -m src.tune
python -m src.train
```

Open `notebooks/01_supply_chain_late_delivery.ipynb` to review the analysis. A local Restart & Run All check and browser-level deployment check remain necessary.

## Deploy
On [Streamlit Community Cloud](https://share.streamlit.io/), create an app from this repository, branch `main`, entrypoint `app.py`. Python 3.13 is specified in `.streamlit/config.toml` where supported.

## Limitations
This is historical decision-support research, not a delivery guarantee. The dataset's Shipping Mode and scheduled-days values are deterministically paired; the app enforces the observed mapping. Validate current operational relevance, calibration, and performance before real-world use.
