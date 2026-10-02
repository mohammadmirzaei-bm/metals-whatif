"""ماتریس حساسیت دوبعدی."""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Callable, Optional

import numpy as np

from .calculators import calculate_bubble_pct
from .scenarios import ScenarioAxis


@dataclass(frozen=True)
class SensitivityMatrix:
    """
    values[i, j] مربوط به row_axis.values()[i] و col_axis.values()[j] است.
    """
    values: np.ndarray
    row_axis: ScenarioAxis
    col_axis: ScenarioAxis

    def to_bubble(self, market_price: float) -> Optional["SensitivityMatrix"]:
        """ماتریس حباب (٪)؛ اگر قیمت بازار معتبر نباشد None."""
        if market_price is None or market_price <= 0:
            return None
        return replace(
            self,
            values=calculate_bubble_pct(market_price, self.values),
        )


def build_matrix(
    fn: Callable,
    row_axis: ScenarioAxis,
    col_axis: ScenarioAxis,
) -> SensitivityMatrix:
    """
    fn(row_value, col_value) باید با آرایه‌های numpy سازگار باشد.
    سطرها = row_axis، ستون‌ها = col_axis.
    """
    rows = np.asarray(row_axis.values(), dtype=float)
    cols = np.asarray(col_axis.values(), dtype=float)

    values = np.asarray(fn(rows[:, None], cols[None, :]), dtype=float)

    return SensitivityMatrix(values=values, row_axis=row_axis, col_axis=col_axis)