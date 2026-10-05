"""هماهنگ‌کننده محاسبات: DashboardInputs → AnalysisResult برای هر دارایی."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Dict, Hashable, Optional, Tuple

from .calculators import (
    calculate_18k_gold,
    calculate_mazaneh,
    calculate_metal_certificate,
    calculate_silver_999,
    calculate_silver_certificate,
)
from .matrix import SensitivityMatrix, build_matrix
from .models import AssetKey, CertificateParams, DashboardInputs
from .scenarios import EmptyScenarioError, ScenarioAxis


@dataclass(frozen=True)
class AnalysisResult:
    price: SensitivityMatrix
    market_price: float
    bubble: Optional[SensitivityMatrix]


# دارایی‌هایی که پارامترشان فقط bubble_pct است
_BUBBLE_CALCS: Dict[AssetKey, Callable] = {
    AssetKey.GOLD_18K: calculate_18k_gold,
    AssetKey.MAZANEH: calculate_mazaneh,
    AssetKey.SILVER_999: calculate_silver_999,
}

# دارایی‌هایی که پارامترشان CertificateParams است
_CERT_CALCS: Dict[AssetKey, Callable] = {
    AssetKey.SILVER_CERT: calculate_silver_certificate,
    AssetKey.COPPER: calculate_metal_certificate,
    AssetKey.ZINC: calculate_metal_certificate,
}


def _certificate_fn(calc: Callable, params: CertificateParams) -> Callable:
    """اتصال یک تابع محاسبه گواهی به پارامترهای آن (price, usd) → ارزش."""
    def fn(price, usd):
        return calc(
            price,
            usd,
            params.premium_pct,
            params.include_costs,
            params.vat_pct,
            params.fee_pct,
        )
    return fn


def _ensure_axes_not_empty(inputs: DashboardInputs) -> None:
    axes = {
        "دلار": inputs.usd,
        "طلا": inputs.gold,
        "نقره": inputs.silver,
        "مس": inputs.copper,
        "روی": inputs.zinc,
    }
    empty = [name for name, axis in axes.items() if not axis.values()]
    if empty:
        raise EmptyScenarioError(empty)


def _asset_inputs(
    key: AssetKey, inputs: DashboardInputs
) -> Tuple[ScenarioAxis, Hashable]:
    """محور سطر و پارامتر مؤثر برای هر دارایی (اجزای کلید کش)."""
    b = inputs.bubble_pct
    return {
        AssetKey.GOLD_18K: (inputs.gold, b),
        AssetKey.MAZANEH: (inputs.gold, b),
        AssetKey.SILVER_999: (inputs.silver, b),
        AssetKey.SILVER_CERT: (inputs.silver, inputs.silver_cert_params),
        AssetKey.COPPER: (inputs.copper, inputs.copper_params),
        AssetKey.ZINC: (inputs.zinc, inputs.zinc_params),
    }[key]


@lru_cache(maxsize=256)
def _price_matrix(
    key: AssetKey,
    row_axis: ScenarioAxis,
    usd_axis: ScenarioAxis,
    param: Hashable,
) -> SensitivityMatrix:
    """
    ماتریس ارزش ذاتی. فقط به ورودی‌های مؤثر وابسته است، نه قیمت بازار.
    همه آرگومان‌ها باید hashable باشند.
    """
    if key in _BUBBLE_CALCS:
        calc = _BUBBLE_CALCS[key]

        def fn(row, usd):
            return calc(row, usd, param)
    else:
        fn = _certificate_fn(_CERT_CALCS[key], param)
    return build_matrix(fn, row_axis, usd_axis)


def clear_cache() -> None:
    _price_matrix.cache_clear()


def cache_info():
    return _price_matrix.cache_info()


def run_analysis(inputs: DashboardInputs) -> Dict[AssetKey, AnalysisResult]:
    _ensure_axes_not_empty(inputs)

    results: Dict[AssetKey, AnalysisResult] = {}
    for key in (*_BUBBLE_CALCS, *_CERT_CALCS):
        row_axis, param = _asset_inputs(key, inputs)
        price = _price_matrix(key, row_axis, inputs.usd, param)
        market_price = inputs.market_prices.for_asset(key)
        results[key] = AnalysisResult(
            price=price,
            market_price=market_price,
            bubble=price.to_bubble(market_price),  # ارزان، بدون کش
        )
    return results