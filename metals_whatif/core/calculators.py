"""
فرمول‌های خالص قیمت‌گذاری.

همه توابع فقط عملیات حسابی انجام می‌دهند؛ بنابراین هم با عدد اسکالر و هم با
آرایه‌های numpy (Broadcasting) کار می‌کنند.
"""
from .constants import (
    KARAT_18_PURITY,
    KG_PER_TONNE,
    MAZANEH_FACTOR,
    TROY_OUNCE_GRAMS,
)


def _apply_certificate_costs(value, include_costs, vat_pct, fee_pct):
    """اعمال مالیات و کارمزد به‌صورت ضریب جمعی (در صورت فعال بودن)."""
    if include_costs:
        return value * (1 + (vat_pct + fee_pct) / 100)
    return value


def calculate_18k_gold(ounce, usd, bubble_pct=0.0):
    """قیمت هر گرم طلای ۱۸ عیار (تومان)."""
    base_price = ((ounce * usd) / TROY_OUNCE_GRAMS) * KARAT_18_PURITY
    return base_price * (1 + bubble_pct / 100)


def calculate_mazaneh(ounce, usd, bubble_pct=0.0):
    """مظنه بازار طلا (تومان)."""
    price_18k_no_bubble = calculate_18k_gold(ounce, usd, bubble_pct=0.0)
    return price_18k_no_bubble * MAZANEH_FACTOR * (1 + bubble_pct / 100)


def calculate_silver_999(ag_ounce, usd, bubble_pct=0.0):
    """قیمت هر گرم نقره خام ۹۹۹ (تومان)."""
    base_price = (ag_ounce * usd) / TROY_OUNCE_GRAMS
    return base_price * (1 + bubble_pct / 100)


def calculate_metal_certificate(
    lme_price,
    usd,
    premium_pct=0.0,
    include_costs=False,
    vat_pct=0.0,
    fee_pct=0.0,
):
    """
    ارزش نظری هر گواهی سپرده فلزی (مس کاتد / شمش روی)، تومان.

    ارزش = LME (دلار/تن) × دلار (تومان) × (1 + α) / 1000
    فرض: هر گواهی = ۱ کیلوگرم.
    """
    fair_value = (lme_price * usd * (1 + premium_pct / 100)) / KG_PER_TONNE
    return _apply_certificate_costs(fair_value, include_costs, vat_pct, fee_pct)


def calculate_silver_certificate(
    ag_ounce,
    usd,
    premium_pct=0.0,
    include_costs=False,
    vat_pct=0.0,
    fee_pct=0.0,
):
    """
    ارزش نظری هر گواهی سپرده شمش نقره (CD1SIB0001)، تومان.

    ارزش = (قیمت انس نقره ÷ 31.1034) × دلار (تومان) × (1 + α)
    فرض: هر گواهی = ۱ گرم نقره ۹۹۹.۹.
    """
    fair_value = (
        (ag_ounce * usd) / TROY_OUNCE_GRAMS
    ) * (1 + premium_pct / 100)
    return _apply_certificate_costs(fair_value, include_costs, vat_pct, fee_pct)


def calculate_bubble_pct(market_price, fair_value):
    """حباب (٪) = (بازار − محاسباتی) / محاسباتی × ۱۰۰"""
    return (market_price - fair_value) / fair_value * 100