# Model Training and Held-Out Evaluation

## Validation design
- Source rows: 180,519 order items across 65,752 orders.
- Group-aware split: 144,415 training rows (52,601 orders) and 36,104 test rows (13,151 orders).
- Group overlap across train and test: **0 orders**.
- Cross-validation: 3-fold StratifiedGroupKFold grouped by Order Id.
- Hyperparameter search: randomized Decision Tree search on training folds only.
- Selected model: tuned Decision Tree (max_depth=10, min_samples_leaf=100, criterion=gini, class_weight=None).
- Decision threshold: 0.50.

## Training-fold cross-validation
| Model | Recall | Precision | F1 | ROC-AUC |
|---|---:|---:|---:|---:|
| Tuned Decision Tree | 0.5435 | 0.8460 | 0.6618 | 0.7260 |
| Decision Tree | 0.5427 | 0.8472 | 0.6616 | 0.7253 |
| Random Forest | 0.5409 | 0.8498 | 0.6611 | 0.7263 |
| Logistic Regression | 0.5408 | 0.8499 | 0.6610 | 0.7256 |

## Untouched grouped test set
| Metric | Majority baseline | Tuned Decision Tree |
|---|---:|---:|
| Accuracy | 0.5483 | 0.6932 |
| Precision | 0.5483 | 0.8422 |
| Recall | 1.0000 | 0.5421 |
| F1 | 0.7082 | 0.6596 |
| ROC-AUC | 0.5000 | 0.7251 |

The majority baseline predicts every row as late because class 1 is the majority. It therefore has 100% recall but flags all rows and has no useful ranking ability (ROC-AUC 0.50). The tuned model is more selective, with higher accuracy, precision, and ROC-AUC, but lower recall than the trivial baseline.

## Confusion matrix
| Actual / Predicted | Not late (0) | Late (1) |
|---|---:|---:|
| Not late (0) | 14,298 | 2,011 |
| Late (1) | 9,065 | 10,730 |

- True late-risk cases identified: 10,730 of 19,795 (54.21%).
- False negatives: 9,065 (45.79% of actual late-risk rows).
- False positives: 2,011.
- The model flags 12,741 of 36,104 test rows (35.29%).

## Business interpretation
At threshold 0.50, the model is a higher-precision triage aid, not a high-recall safety net. When it flags an item, late-class precision is about 84%; however, it misses about 46% of late-risk item rows. It should not be the only control used to prevent late delivery.

## Limitations
- Historical anonymized data may not transfer to current operations.
- The project-card feature whitelist is small and limits predictive signal.
- Shipping mode and scheduled days are perfectly paired in the supplied file.
- Results are item-level, though split by order; operational reporting should aggregate predictions to order level.
- Decision support only; it must not automatically change a carrier or promise a delivery date.
