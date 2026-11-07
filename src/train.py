from __future__ import annotations
import numpy as np

def engineer_schedule_features(values):
    """Create deterministic schedule-derived inputs used by the fitted pipeline."""
    days = np.clip(np.asarray(values, dtype=float).reshape(-1), 0, 7)
    return np.column_stack([days, (days <= 1).astype(float), (days >= 4).astype(float)])
