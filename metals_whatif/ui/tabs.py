"""تب‌های نتایج."""
from typing import Dict

import streamlit as st

from metals_whatif.core import (
    AnalysisResult,
    AssetKey,
    CertificateParams,
    DashboardInputs,
)

from .assets import ASSET_VIEWS
from .components import render_bubble_matrix, render_price_matrix
from .styles import section_heading

def _certificate_notice(
    metal_name: str,
    premium_phrase: str,
    params: CertificateParams,
    extra_note: str = "",
) -> None:
    if params.include_costs:
        st.info(
            f"در محاسبه {metal_name}، پریمیوم {params.premium_pct:.2f}٪، "
            f"مالیات {params.vat_pct:.2f}٪ و "
            f"کارمزد {params.fee_pct:.2f}٪ اعمال شده است."
            f"{extra_note}"
        )
    else:
        st.info(
            f"در محاسبه {metal_name} فقط {premium_phrase} "
            f"{params.premium_pct:.2f}٪ اعمال شده و مالیات و "
            "کارمزد لحاظ نشده‌اند."
        )


def _render_notice(key: AssetKey, inputs: DashboardInputs) -> None:
    if key is AssetKey.COPPER:
        _certificate_notice(
            "مس", "پریمیوم / رقابت", inputs.copper_params
        )
    elif key is AssetKey.ZINC:
        _certificate_notice(
            "روی",
            "پریمیوم α برابر",
            inputs.zinc_params,
            extra_note=(
                " توجه: مالیات فقط در صورت ترخیص و تحویل فیزیکی "
                "(حداقل ۲۱٬۰۰۰ ورقه) از خریدار دریافت می‌شود."
            ),
        )
    elif key is AssetKey.SILVER_CERT:
        _certificate_notice(
            "گواهی نقره",
            "پریمیوم α برابر",
            inputs.silver_cert_params,
            extra_note=(
                " توجه: معامله گواهی از VAT معاف است و مالیات فقط در "
                "صورت تحویل فیزیکی (حداقل ۱٬۰۰۰ ورقه) مطرح می‌شود. "
                "هزینه انبارداری و ارزیابی تحویل لحاظ نشده‌اند."
            ),
        )

def render_tabs(
    results: Dict[AssetKey, AnalysisResult], inputs: DashboardInputs
) -> None:
    tabs = st.tabs([view.tab_title for view in ASSET_VIEWS])

    for tab, view in zip(tabs, ASSET_VIEWS):
        result = results[view.key]

        with tab:
            section_heading(view.subheader)   # قبلاً: st.subheader(view.subheader)
            st.caption(view.caption)

            _render_notice(view.key, inputs)

            render_price_matrix(result.price, view)
            render_bubble_matrix(result.bubble, result.market_price, view)