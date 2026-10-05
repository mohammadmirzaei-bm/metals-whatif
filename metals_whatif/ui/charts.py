"""ساخت نمودار Heatmap با Plotly (بدون منطق مالی)."""
import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go

import functools
import time




from .labels import rtl_isolate
from .styles import PERSIAN_FONT_FAMILY

PLOTLY_CONFIG = {
    "displaylogo": False,
    "responsive": True,
    "scrollZoom": False,
    "showTips": False,
    "modeBarButtonsToRemove": ["select2d", "lasso2d"],
    "toImageButtonOptions": {
        "format": "png",
        "filename": "sensitivity-analysis",
        "height": 900,
        "width": 1800,
        "scale": 3,
    },
}


def get_text_colors(values, zmin, zmax, colorscale="RdYlGn_r"):
    """رنگ متن داخل سلول‌ها بر اساس روشنایی پس‌زمینه."""
    values = np.asarray(values, dtype=float)

    if zmax <= zmin:
        return np.full(values.shape, "#172033", dtype=object)

    normalized = (values - zmin) / (zmax - zmin)

    if colorscale == "Blues":
        return np.where(normalized >= 0.65, "#FFFFFF", "#172033")

    return np.where(
        (normalized <= 0.20) | (normalized >= 0.80),
        "#FFFFFF",
        "#172033",
    )


def format_heatmap_values(values, number_format, suffix=""):
    result = []
    for row in values:
        formatted_row = []
        for value in row:
            if pd.isna(value):
                formatted_row.append("")
            else:
                formatted_row.append(
                    f"{format(float(value), number_format)}{suffix}"
                )
        result.append(formatted_row)
    return result


def plot_heatmap(
    df,
    x_title,
    y_title,
    colorbar_title,
    colorscale="RdYlGn_r",
    number_format=",.0f",
    hover_format=",.0f",
    value_suffix="",
    color_midpoint=None,
):

    values = df.to_numpy(dtype=float)
    x_labels = list(df.columns)
    y_labels = list(df.index)

    finite_values = values[np.isfinite(values)]

    if finite_values.size == 0:
        zmin, zmax = 0, 1
    elif color_midpoint is not None:
        max_distance = np.max(np.abs(finite_values - color_midpoint))
        if max_distance == 0:
            max_distance = 1
        zmin = color_midpoint - max_distance
        zmax = color_midpoint + max_distance
    else:
        zmin = float(np.nanmin(finite_values))
        zmax = float(np.nanmax(finite_values))
        if math.isclose(zmin, zmax):
            zmax = zmin + 1

    cell_text = format_heatmap_values(
        values, number_format=number_format, suffix=value_suffix
    )
    text_colors = get_text_colors(values, zmin, zmax, colorscale)

    row_count, column_count = values.shape
    chart_height = max(520, min(1050, 210 + row_count * 40))

    if column_count <= 11:
        cell_font_size = 11
    elif column_count <= 15:
        cell_font_size = 10
    else:
        cell_font_size = 9

    fig = go.Figure()

    fig.add_trace(
        go.Heatmap(
            z=values.tolist(),          # قبلاً: z=values
            x=[str(x) for x in x_labels],
            y=[str(y) for y in y_labels],
            colorscale=colorscale,
            zmin=zmin,
            zmax=zmax,
            colorbar=dict(
                title=dict(
                    text=rtl_isolate(colorbar_title),
                    side="top",
                    font=dict(
                        family=PERSIAN_FONT_FAMILY, size=12, color="#667085"
                    ),
                ),
                x=1.025,
                xanchor="left",
                xpad=10,
                y=0.5,
                yanchor="middle",
                len=0.72,
                thickness=18,
                outlinewidth=0,
                tickformat=hover_format,
                separatethousands=True,
                tickfont=dict(
                    family=PERSIAN_FONT_FAMILY, size=11, color="#667085"
                ),
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "<b>%{x}</b><br>"
                f"{rtl_isolate(colorbar_title)}: "
                f"%{{z:{hover_format}}}{value_suffix}"
                "<extra></extra>"
            ),
            hoverongaps=False,
            showscale=True,
        )
    )

    text_x, text_y, text_values, text_color_values = [], [], [], []

    for r, y_label in enumerate(y_labels):
        for c, x_label in enumerate(x_labels):
            text_x.append(x_label)
            text_y.append(y_label)
            text_values.append(cell_text[r][c])
            text_color_values.append(text_colors[r][c])

    fig.add_trace(
        go.Scatter(
            x=text_x,
            y=text_y,
            mode="text",
            text=text_values,
            textposition="middle center",
            textfont=dict(
                family=PERSIAN_FONT_FAMILY,
                size=cell_font_size,
                color=text_color_values,
            ),
            hoverinfo="skip",
            showlegend=False,
            cliponaxis=True,
        )
    )

    fig.update_layout(
        height=chart_height,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family=PERSIAN_FONT_FAMILY, size=12, color="#344054"),
        margin=dict(l=165, r=145, t=100, b=35, pad=5),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#D0D5DD",
            font=dict(family=PERSIAN_FONT_FAMILY, size=12, color="#101828"),
            align="right",
        ),
        showlegend=False,
    )

    fig.update_xaxes(
        side="top",
        title=dict(
            text=rtl_isolate(x_title),
            standoff=14,
            font=dict(family=PERSIAN_FONT_FAMILY, size=13, color="#667085"),
        ),
        type="category",
        categoryorder="array",
        categoryarray=x_labels,
        tickmode="array",
        tickvals=x_labels,
        ticktext=x_labels,
        tickangle=0,
        ticks="",
        ticklen=0,
        tickfont=dict(family=PERSIAN_FONT_FAMILY, size=11, color="#667085"),
        showgrid=False,
        zeroline=False,
        showline=False,
        fixedrange=False,
        automargin=True,
    )

    fig.update_yaxes(
        title=dict(
            text=rtl_isolate(y_title),
            standoff=24,
            font=dict(family=PERSIAN_FONT_FAMILY, size=13, color="#667085"),
        ),
        type="category",
        categoryorder="array",
        categoryarray=y_labels,
        autorange="reversed",   
        tickmode="array",
        tickvals=y_labels,
        ticktext=y_labels,
        ticks="",
        ticklen=0,
        tickfont=dict(family=PERSIAN_FONT_FAMILY, size=11, color="#667085"),
        showgrid=False,
        zeroline=False,
        showline=False,
        fixedrange=False,
        automargin=True,
    )

    # اضافه کردن واترمارک به مرکز نمودار
    fig.add_annotation(
        text="@themohammadm",  
        xref="paper", 
        yref="paper",
        x=0.5, 
        y=0.5,
        showarrow=False,
        font=dict(
            family=PERSIAN_FONT_FAMILY,
            size=80,  
            color="rgba(150, 150, 150, 0.12)"  
        ),
        textangle=-30, 
        align="center",
    )

    return fig
