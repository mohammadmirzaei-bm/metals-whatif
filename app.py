"""نقطه ورود داشبورد: streamlit run app.py"""
import streamlit as st

from metals_whatif.core import EmptyScenarioError, run_analysis
from metals_whatif.ui.inputs import collect_dashboard_inputs
from metals_whatif.ui.styles import configure_page, inject_css
from metals_whatif.ui.tabs import render_tabs


def main() -> None:
    configure_page()  
    inject_css()

    inputs = collect_dashboard_inputs()

    try:
        results = run_analysis(inputs)
    except EmptyScenarioError as exc:
        st.error(
            f"⚠️ با تنظیمات فعلی، بازه‌ی این موارد خالی شده است: "
            f"{'، '.join(exc.axis_names)}. "
            "گام تغییرات یا تعداد سناریوهای پایین را کاهش دهید."
        )
        st.stop()

    st.markdown("---")
    render_tabs(results, inputs)


main()