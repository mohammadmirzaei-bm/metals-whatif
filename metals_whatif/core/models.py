"""مدل‌های ورودی داشبورد (بدون وابستگی به UI)."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .scenarios import ScenarioAxis


class AssetKey(str, Enum):
    # مقدار هر عضو دقیقاً با نام فیلد در MarketPrices یکی است.
    GOLD_18K = "gold_18k"
    MAZANEH = "mazaneh"
    SILVER_999 = "silver_999"
    SILVER_CERT = "silver_cert"
    COPPER = "copper"
    ZINC = "zinc"


@dataclass(frozen=True)
class CertificateParams:
    """پارامترهای گواهی سپرده فلزی (مس / روی / نقره)."""
    premium_pct: float = 0.0
    include_costs: bool = False
    vat_pct: float = 10.0
    fee_pct: float = 0.24


def _default_silver_cert_params() -> CertificateParams:
    # معامله گواهی از VAT معاف است و نرخ VAT تحویل نقره در مشخصات ذکر نشده؛
    # بنابراین پیش‌فرض صفر است.
    return CertificateParams(vat_pct=0.0)


@dataclass(frozen=True)
class MarketPrices:
    """قیمت‌های بازار (تومان)؛ صفر یعنی وارد نشده."""
    gold_18k: float = 0
    mazaneh: float = 0
    silver_999: float = 0
    copper: float = 0
    zinc: float = 0
    silver_cert: float = 0

    def for_asset(self, key: AssetKey) -> float:
        return getattr(self, key.value)


@dataclass(frozen=True)
class DashboardInputs:
    usd: ScenarioAxis
    gold: ScenarioAxis
    silver: ScenarioAxis      # مشترک بین نقره خام و گواهی نقره
    copper: ScenarioAxis
    zinc: ScenarioAxis
    bubble_pct: float = 0.0
    copper_params: CertificateParams = field(default_factory=CertificateParams)
    zinc_params: CertificateParams = field(default_factory=CertificateParams)
    market_prices: MarketPrices = field(default_factory=MarketPrices)
    silver_cert_params: CertificateParams = field(
        default_factory=_default_silver_cert_params
    )