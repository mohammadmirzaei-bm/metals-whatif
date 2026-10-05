"""کامپوننت‌های نمایش ماتریس قیمت و ماتریس حباب."""
import numpy as np
import pandas as pd
import streamlit as st

from metals_whatif.core import SensitivityMatrix
from .styles import section_heading
from .assets import AssetView
from .charts import PLOTLY_CONFIG, plot_heatmap
from .labels import axis_labels

X_TITLE = "دلار آزاد (تومان)"
COLUMN_PREFIX = "دلار"


def matrix_to_dataframe(
    matrix: SensitivityMatrix, view: AssetView
) -> pd.DataFrame:
    """تبدیل ماتریس عددی به DataFrame با برچسب‌های قابل نمایش."""
    return pd.DataFrame(
        matrix.values,
        index=axis_labels(matrix.row_axis, view.row_prefix, view.row_decimals),
        columns=axis_labels(matrix.col_axis, COLUMN_PREFIX, 0),
    )


def render_price_matrix(matrix: SensitivityMatrix, view: AssetView) -> None:
    df = matrix_to_dataframe(matrix, view)

    figure = plot_heatmap(
        df=df,
        x_title=X_TITLE,
        y_title=view.y_title,
        colorbar_title=view.color_label,
        colorscale="Blues",
        number_format=",.0f",
        hover_format=",.0f",
    )
    st.plotly_chart(figure, width="stretch", config=PLOTLY_CONFIG)

    with st.expander("📋 مشاهده جدول داده‌های قیمت"):
        st.dataframe(
            df.style.format("{:,.0f}").background_gradient(
                cmap="Blues", axis=None
            ),
            width='stretch',
            height=400,
        )


def render_bubble_matrix(
    bubble: SensitivityMatrix | None,
    market_price: float,
    view: AssetView,
) -> None:
    asset_name = view.bubble_asset_name

    if bubble is None:
        st.warning(
            f"برای مشاهده ماتریس حباب {asset_name}، "
            "قیمت بازار یا تابلو را بزرگ‌تر از صفر وارد کنید."
        )
        return

    df = matrix_to_dataframe(bubble, view)

    st.markdown("---")
    section_heading(f"📊 ماتریس حباب / فاصله قیمت بازار {view.bubble_asset_name}")
    st.caption(
        "حباب مثبت (قرمز) یعنی قیمت بازار بالاتر از مقدار محاسباتی است؛ "
        "حباب منفی (سبز) یعنی قیمت بازار پایین‌تر از مقدار محاسباتی است."
    )
    st.metric(
        label=f"قیمت بازار واردشده برای {asset_name}",
        value=f"{market_price:,.0f} تومان",
    )

    figure = plot_heatmap(
        df=df,
        x_title=X_TITLE,
        y_title=view.y_title,
        colorbar_title="حباب قیمت (درصد)",
        colorscale="RdYlGn_r",
        number_format=",.1f",
        hover_format=",.2f",
        value_suffix="٪",
        color_midpoint=0,
    )
    st.plotly_chart(figure, width="stretch", config=PLOTLY_CONFIG)


    max_abs = float(np.abs(df.to_numpy()).max())

    with st.expander("📋 مشاهده جدول داده‌های حباب"):
        st.dataframe(
            df.style.format("{:,.2f}%").background_gradient(
                cmap="RdYlGn_r", axis=None, vmin=-max_abs, vmax=max_abs
            ),
            width='stretch',
            height=400,
        )