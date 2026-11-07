# Data Quality and Initial EDA Summary

## Source and structure
- Source: [DataCo Smart Supply Chain for Big Data Analysis (Kaggle)](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis), as specified in the project-ideas PDF.
- Dimensions: **180,519 rows × 53 columns**.
- Source row grain: order item; Order Item Id is unique for all 180,519 rows.
- Unique orders: **65,752**.
- Mean items per order: **2.745**; maximum: **5**.
- Exact duplicate rows: **0**; duplicate order-item identifiers: **0**.
- Order dates: 2015-01-01 through 2018-01-31; parse failures: **0**.
- Shipping dates: 2015-01-03 through 2018-02-06; parse failures: **0**.

## Target
Late_delivery_risk has 81,542 class-0 rows (45.17%) and 98,977 class-1 rows (54.83%). This is not an extreme class imbalance.

## Missing values and constants
- Product Description: 180,519 missing (100%).
- Order Zipcode: 155,679 missing (86.24%).
- Customer Lname: 8 missing.
- Customer Zipcode: 3 missing.
- Constant columns: Customer Email, Customer Password, Product Description, Product Status.
- The four selected model inputs have zero missing values in this source file.

## Leakage audit
Delivery Status exactly separates the target: Late delivery maps to class 1; Advance shipping, Shipping canceled, and Shipping on time map to class 0. It is direct target leakage and excluded. Days for shipping (real) and shipping date (DateOrders) are also excluded because they are only known after order placement / shipment progression.

## EDA observations (descriptive, not causal)
1. 180,519 item rows correspond to 65,752 orders. Each order has 1–5 item rows. Splits and CV group on Order Id.
2. First Class has the highest observed late-risk rate (95.32%, n=27,814); Standard Class has the lowest (38.07%, n=107,752).
3. Shipping mode and scheduled days are perfectly paired. The app derives scheduled days from shipping mode to avoid unsupported combinations.
4. Market late-risk rates are closer together, ranging from 54.36% to 55.21%.
5. Class 1 accounts for 54.83%; accuracy alone is insufficient, so precision, recall, F1, and ROC-AUC are reported.

## Modeling decision
Use only Market, Shipping Mode, Product Name, and Days for shipment (scheduled), matching the project brief. Exclude post-order, outcome-revealing, identifier, personal, constant, and out-of-scope columns. Evaluate using group-aware splits on Order Id.
