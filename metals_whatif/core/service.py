"""هماهنگ‌کننده محاسبات: DashboardInputs → AnalysisResult برای هر دارایی."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional

from .calculators import (
    calculate_18k_gold,
    calculate_mazaneh,
    calculate_metal_certificate,
    calculate_silver_999,
    calculate_silver_certificate,
)
from .matrix import SensitivityMatrix, build_matrix
from .models import AssetKey, CertificateParams, DashboardInputs
from .scenarios import EmptyScenarioError


@dataclass(frozen=True)
class AnalysisResult:
    price: SensitivityMatrix
    market_price: float
    bubble: Optional[SensitivityMatrix]


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


def run_analysis(inputs: DashboardInputs) -> Dict[AssetKey, AnalysisResult]:
    _ensure_axes_not_empty(inputs)

    b = inputs.bubble_pct
    definitions = {
        AssetKey.GOLD_18K: (
            inputs.gold, lambda o, u: calculate_18k_gold(o, u, b)),
        AssetKey.MAZANEH: (
            inputs.gold, lambda o, u: calculate_mazaneh(o, u, b)),
        AssetKey.SILVER_999: (
            inputs.silver, lambda a, u: calculate_silver_999(a, u, b)),
        AssetKey.SILVER_CERT: (
            inputs.silver,
            _certificate_fn(
                calculate_silver_certificate, inputs.silver_cert_params
            ),
        ),
        AssetKey.COPPER: (
            inputs.copper,
            _certificate_fn(
                calculate_metal_certificate, inputs.copper_params
            ),
        ),
        AssetKey.ZINC: (
            inputs.zinc,
            _certificate_fn(
                calculate_metal_certificate, inputs.zinc_params
            ),
        ),
    }

    results: Dict[AssetKey, AnalysisResult] = {}
    for key, (row_axis, fn) in definitions.items():
        price = build_matrix(fn, row_axis, inputs.usd)
        market_price = inputs.market_prices.for_asset(key)
        results[key] = AnalysisResult(
            price=price,
            market_price=market_price,
            bubble=price.to_bubble(market_price),
        )
    return results