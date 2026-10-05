import html
import streamlit as st

PERSIAN_FONT_FAMILY = (
    "Vazirmatn, IRANSansX, IRANSans, Tahoma, Arial, sans-serif"
)

# تگ‌های style در ابتدا و انتها بسیار مهم هستند
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&display=swap');

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: "Vazirmatn", Tahoma, Arial, sans-serif !important;
}

/* راست‌چین کردن قطعی کل رابط استریم‌لیت در نسخه‌های جدید */
.stApp, 
.main,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMainBlockContainer"],
[data-testid="stBottomBlockContainer"],
[data-testid="stHeader"] {
    direction: rtl !important;
    text-align: right !important;
}

/* ورودی‌های عددی باید چپ‌چین و چپ‌به‌راست (LTR) بمانند */
[data-testid="stNumberInput"] input,
[data-testid="stNumberInput"] div[data-baseweb="input"] {
    direction: ltr !important;
    text-align: left !important;
}

[data-testid="stSlider"] {
    direction: rtl;
}

/* محیط نمودارهای Plotly باید LTR بماند تا محورها به‌‌هم نریزند */
.js-plotly-plot, .plot-container, .svg-container, [data-testid="stPlotlyChart"] {
    direction: ltr !important;
    text-align: left !important;
}

/* 🟢 راست‌چین کردن متون توضیحی (Caption) و پاراگراف‌ها */
[data-testid="stCaptionContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stText"],
.stCaption {
    direction: rtl !important;
    text-align: right !important;
}

[data-testid="stDataFrame"] {
    direction: rtl;
}

button[data-baseweb="tab"] {
    font-family: "Vazirmatn", Tahoma, Arial, sans-serif !important;
}

/* استایل‌دهی یکپارچه تیترها */
h1, h2, h3, h4, h5, h6,
[data-testid="stHeading"],
[data-testid="stHeadingWithActionElements"],
[data-testid="stMarkdownContainer"] {
    font-family: "Vazirmatn", Tahoma, Arial, sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}

/* راست‌چین و منعطف کردن دکمه‌های انتخاب دارایی */
div[data-testid="stSegmentedControl"],
div[data-testid="stRadio"] > div[role="radiogroup"] {
    direction: rtl !important;
    justify-content: flex-start !important;
    flex-wrap: wrap !important;
    gap: 8px !important;
}

</style>
"""

def configure_page() -> None:
    st.set_page_config(
        page_title="داشبورد جامع طلا، نقره، مس و روی",
        page_icon="📈",
        layout="wide",
    )

def inject_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)

def section_heading(text: str, level: int = 3) -> None:
    """تیتر راست‌به‌چپ با جهت صریح روی خود تگ."""
    safe_text = html.escape(text)
    # اضافه شدن &rlm; برای میخ‌‌کوب کردن ایموجی‌ها در سمت راست
    st.markdown(
        f'<h{level} dir="rtl" style="text-align:right; direction:rtl; '
        f'unicode-bidi:isolate;">&rlm;{safe_text}&rlm;</h{level}>',
        unsafe_allow_html=True,
    )