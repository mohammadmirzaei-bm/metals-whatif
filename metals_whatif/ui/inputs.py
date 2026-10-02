"""ویجت‌های ورودی Streamlit؛ خروجی: DashboardInputs (مدل core)."""
from __future__ import annotations
from .styles import section_heading
from dataclasses import dataclass
from typing import Optional

import streamlit as st

from metals_whatif.core import (
    CertificateParams,
    DashboardInputs,
    MarketPrices,
    ScenarioAxis,
)


# ---------------------------------------------------------
# ورودی‌های محور سناریو
# ---------------------------------------------------------

@dataclass(frozen=True)
class AxisInputSpec:
    key: str
    banner: str
    banner_kind: str          # info | warning | success | error
    base_label: str
    step_label: str
    up_label: str
    down_label: str
    base_default: float
    base_step: float
    base_format: str
    step_default: float
    step_step: float
    step_min: float
    step_format: str
    steps_up_default: int = 4
    steps_down_default: int = 4


USD_SPEC = AxisInputSpec(
    key="usd",
    banner="💵 **دلار آزاد (تومان)**",
    banner_kind="info",
    base_label="قیمت پایه دلار",
    step_label="گام تغییرات دلار",
    up_label="سناریو بالا (دلار)",
    down_label="سناریو پایین (دلار)",
    base_default=200000, base_step=1000, base_format="%d",
    step_default=5000, step_step=500, step_min=1, step_format="%d",
)

GOLD_SPEC = AxisInputSpec(
    key="gold",
    banner="🌍 **انس طلا (دلار)**",
    banner_kind="warning",
    base_label="قیمت پایه انس طلا",
    step_label="گام تغییرات انس طلا",
    up_label="سناریو بالا (طلا)",
    down_label="سناریو پایین (طلا)",
    base_default=4000.0, base_step=100.0, base_format="%.1f",
    step_default=50.0, step_step=10.0, step_min=0.1, step_format="%.1f",
)

SILVER_SPEC = AxisInputSpec(
    key="silver",
    banner="⚪ **انس نقره (دلار)**",
    banner_kind="success",
    base_label="قیمت پایه انس نقره",
    step_label="گام تغییرات انس نقره",
    up_label="سناریو بالا (نقره)",
    down_label="سناریو پایین (نقره)",
    base_default=50.0, base_step=0.5, base_format="%.2f",
    step_default=10.0, step_step=0.5, step_min=0.01, step_format="%.2f",
)

COPPER_SPEC = AxisInputSpec(
    key="copper",
    banner="🟠 **مس کاتد LME (دلار/تن)**",
    banner_kind="error",
    base_label="قیمت پایه مس LME",
    step_label="گام تغییرات مس",
    up_label="سناریو بالا (مس)",
    down_label="سناریو پایین (مس)",
    base_default=14000.0, base_step=100.0, base_format="%.1f",
    step_default=250.0, step_step=50.0, step_min=1.0, step_format="%.1f",
)

ZINC_SPEC = AxisInputSpec(
    key="zinc",
    banner="🔘 **شمش روی LME (دلار/تن)**",
    banner_kind="info",
    base_label="قیمت پایه روی LME",
    step_label="گام تغییرات روی",
    up_label="سناریو بالا (روی)",
    down_label="سناریو پایین (روی)",
    base_default=3000.0, base_step=50.0, base_format="%.1f",
    step_default=100.0, step_step=50.0, step_min=1.0, step_format="%.1f",
    steps_up_default=6,
    steps_down_default=5,
)


def render_axis_inputs(spec: AxisInputSpec) -> ScenarioAxis:
    getattr(st, spec.banner_kind)(spec.banner)

    base = st.number_input(
        spec.base_label,
        value=spec.base_default,
        step=spec.base_step,
        format=spec.base_format,
        key=f"{spec.key}_base",
    )
    step = st.number_input(
        spec.step_label,
        value=spec.step_default,
        step=spec.step_step,
        min_value=spec.step_min,
        format=spec.step_format,
        key=f"{spec.key}_step",
    )

    col_up, col_down = st.columns(2)
    with col_up:
        steps_up = st.number_input(
            spec.up_label,
            value=spec.steps_up_default,
            min_value=0, max_value=20, step=1,
            key=f"{spec.key}_steps_up",
        )
    with col_down:
        steps_down = st.number_input(
            spec.down_label,
            value=spec.steps_down_default,
            min_value=0, max_value=20, step=1,
            key=f"{spec.key}_steps_down",
        )

    return ScenarioAxis(
        base=base,
        step=step,
        steps_down=int(steps_down),
        steps_up=int(steps_up),
    )


# ---------------------------------------------------------
# تنظیمات عمومی و قیمت‌های بازار
# ---------------------------------------------------------

def render_bubble_input() -> float:
    return st.number_input(
        "٪ درصد حباب / کارمزد طلا و نقره، تأثیر روی قیمت محاسباتی",
        min_value=-20.0,
        max_value=40.0,
        value=0.0,
        step=0.5,
        format="%.2f",
        key="bubble_pct",
    )


_TABLOID_RIAL_HELP = (
    "قیمت تابلوی بورس کالا به ریال است؛ "
    "قیمت را به تومان وارد کنید"
)

# (نام فیلد MarketPrices، برچسب، گام، راهنما)
_MARKET_PRICE_FIELDS = (
    ("gold_18k", "قیمت بازار هر گرم طلای ۱۸ عیار، تومان", 10000, None),
    ("mazaneh", "قیمت بازار مظنه، تومان", 50000, None),
    ("silver_999", "قیمت بازار هر گرم نقره ۹۹۹، تومان", 1000, None),
    ("silver_cert", "قیمت تابلو هر گواهی نقره، تومان", 100,
     _TABLOID_RIAL_HELP),
    ("copper", "قیمت تابلو هر گواهی مس، تومان", 1000, None),
    ("zinc", "قیمت تابلو هر گواهی روی، تومان", 1000, _TABLOID_RIAL_HELP),
)

_MARKET_COLUMNS_PER_ROW = 3


def render_market_prices() -> MarketPrices:
    section_heading("📊 قیمت‌های بازار برای محاسبه حباب / فاصله قیمت", level=3)

    values = {}
    n = _MARKET_COLUMNS_PER_ROW

    for start in range(0, len(_MARKET_PRICE_FIELDS), n):
        chunk = _MARKET_PRICE_FIELDS[start:start + n]
        columns = st.columns(n)

        for column, (field_name, label, step, help_text) in zip(columns, chunk):
            with column:
                values[field_name] = st.number_input(
                    label,
                    value=0,
                    min_value=0,
                    step=step,
                    format="%d",
                    help=help_text,
                    key=f"market_{field_name}",
                )

    return MarketPrices(**values)


# ---------------------------------------------------------
# تنظیمات اختصاصی گواهی سپرده (مس / روی)
# ---------------------------------------------------------

def render_certificate_settings(
    *,
    key: str,
    heading: str,
    premium_label: str,
    checkbox_label: str,
    expander_label: str,
    vat_label: str,
    fee_label: str,
    premium_help: Optional[str] = None,
    expander_caption: Optional[str] = None,
    vat_default: float = 10.0,
    fee_default: float = 0.24,
) -> CertificateParams:
    section_heading(heading, level=3)

    col_premium, col_costs = st.columns(2)

    with col_premium:
        premium_pct = st.number_input(
            premium_label,
            min_value=-40.0,
            max_value=40.0,
            value=0.0,
            step=0.5,
            format="%.2f",
            help=premium_help,
            key=f"{key}_premium",
        )

    with col_costs:
        include_costs = st.checkbox(
            checkbox_label,
            value=False,
            key=f"{key}_include_costs",
        )

    with st.expander(expander_label):
        if expander_caption:
            st.caption(expander_caption)

        col_vat, col_fee = st.columns(2)
        with col_vat:
            vat_pct = st.number_input(
                vat_label,
                value=vat_default, step=0.5, min_value=0.0, format="%.2f",
                key=f"{key}_vat",
            )
        with col_fee:
            fee_pct = st.number_input(
                fee_label,
                value=fee_default, step=0.01, min_value=0.0, format="%.2f",
                key=f"{key}_fee",
            )

    return CertificateParams(
        premium_pct=premium_pct,
        include_costs=include_costs,
        vat_pct=vat_pct,
        fee_pct=fee_pct,
    )

# ---------------------------------------------------------
# جمع‌آوری همه ورودی‌ها
# ---------------------------------------------------------

def collect_dashboard_inputs() -> DashboardInputs:
    # ردیف اول: دلار، طلا، نقره
    col_usd, col_gold, col_silver = st.columns(3)
    with col_usd:
        usd = render_axis_inputs(USD_SPEC)
    with col_gold:
        gold = render_axis_inputs(GOLD_SPEC)
    with col_silver:
        silver = render_axis_inputs(SILVER_SPEC)

    # ردیف دوم: مس، روی
    col_copper, col_zinc, _ = st.columns(3)
    with col_copper:
        copper = render_axis_inputs(COPPER_SPEC)
    with col_zinc:
        zinc = render_axis_inputs(ZINC_SPEC)

    st.markdown("---")

    bubble_pct = render_bubble_input()
    market_prices = render_market_prices()

    st.markdown("---")

    copper_params = render_certificate_settings(
        key="copper",
        heading="🟠 تنظیمات اختصاصی مس کاتد",
        premium_label="٪ پریمیوم / رقابت مس کاتد",
        checkbox_label="اعمال مالیات و کارمزد روی مس",
        expander_label="⚙️ تنظیمات اختیاری هزینه‌های مس",
        vat_label="مالیات ارزش افزوده مس (%)",
        fee_label="کارمزد معاملات مس (%)",
    )

    st.markdown("---")

    zinc_params = render_certificate_settings(
        key="zinc",
        heading="🔘 تنظیمات اختصاصی شمش روی",
        premium_label="٪ پریمیوم α شمش روی",
        premium_help=(
            "پریمیوم رقابت بازار و هزینه‌های جانبی؛ معمولاً ۵ تا ۱۰٪. "
            "برای ارزش ذاتی خالص عدد ۰ را بگذارید."
        ),
        checkbox_label="اعمال مالیات و کارمزد روی روی",
        expander_label="⚙️ تنظیمات اختیاری هزینه‌های روی",
        expander_caption=(
            "معامله خود گواهی سپرده از VAT معاف است. مالیات ۱۰٪ فقط در "
            "صورت ترخیص و تحویل فیزیکی از انبار اعمال می‌شود. "
            "حداقل حجم تحویل ۲۱٬۰۰۰ ورقه (۲۱ تن) است."
        ),
        vat_label="مالیات ارزش افزوده روی (%)",
        fee_label="کارمزد معاملات روی (%)",
    )

    st.markdown("---")

    silver_cert_params = render_certificate_settings(
        key="silver_cert",
        heading="🥈 تنظیمات اختصاصی گواهی سپرده نقره",
        premium_label="٪ پریمیوم α گواهی نقره",
        premium_help=(
            "پریمیوم ضرب شمش، عیارسنجی و تعادل عرضه و تقاضا؛ "
            "معمولاً ۳ تا ۸٪. برای ارزش ذاتی خالص عدد ۰ را بگذارید. "
            "این پریمیوم مستقل از «حباب نقره خام» است."
        ),
        checkbox_label="اعمال مالیات و کارمزد روی گواهی نقره",
        expander_label="⚙️ تنظیمات اختیاری هزینه‌های گواهی نقره",
        expander_caption=(
            "معامله گواهی سپرده از VAT معاف است و کارمزد معامله ۰٫۲۴٪ "
            "است. نرخ VAT تحویل فیزیکی در مشخصات ذکر نشده، پس پیش‌فرض "
            "صفر است و در صورت نیاز می‌توانید آن را تغییر دهید. "
            "هزینه انبارداری (۹۹ ریال/گرم/روز، یعنی ۹٫۹ تومان) و هزینه "
            "ارزیابی تحویل (۳٫۶ میلیون ریال به ازای هر شمش ۱ کیلوگرمی) "
            "در محاسبه لحاظ نشده‌اند. حداقل تحویل ۱٬۰۰۰ ورقه است."
        ),
        vat_label="مالیات ارزش افزوده گواهی نقره (%)",
        fee_label="کارمزد معاملات گواهی نقره (%)",
        vat_default=0.0,
    )

    return DashboardInputs(
        usd=usd,
        gold=gold,
        silver=silver,
        copper=copper,
        zinc=zinc,
        bubble_pct=bubble_pct,
        copper_params=copper_params,
        zinc_params=zinc_params,
        silver_cert_params=silver_cert_params,
        market_prices=market_prices,
    )