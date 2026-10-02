"""متن‌ها و تنظیمات نمایشی هر دارایی (بدون منطق محاسباتی)."""
from dataclasses import dataclass

from metals_whatif.core import AssetKey


@dataclass(frozen=True)
class AssetView:
    key: AssetKey
    tab_title: str
    subheader: str
    caption: str
    row_prefix: str          # پیشوند برچسب سطرها
    row_decimals: int
    y_title: str
    color_label: str
    bubble_asset_name: str


ASSET_VIEWS = (
    AssetView(
        key=AssetKey.GOLD_18K,
        tab_title="🥇 طلای ۱۸ عیار",
        subheader="🧮 ماتریس قیمت طلای ۱۸ عیار، تومان",
        caption=(
            "این جدول قیمت محاسباتی هر گرم طلای ۱۸ عیار را بر اساس "
            "سناریوهای دلار و انس جهانی طلا نمایش می‌دهد."
        ),
        row_prefix="انس طلا",
        row_decimals=0,
        y_title="قیمت انس جهانی طلا (دلار)",
        color_label="قیمت هر گرم طلای ۱۸ عیار (تومان)",
        bubble_asset_name="هر گرم طلای ۱۸ عیار",
    ),
    AssetView(
        key=AssetKey.MAZANEH,
        tab_title="⚖️ مظنه بازار",
        subheader="🧮 ماتریس مظنه طلا، تومان",
        caption=(
            "این جدول مظنه محاسباتی بازار را بر اساس سناریوهای دلار "
            "و انس جهانی طلا نمایش می‌دهد."
        ),
        row_prefix="انس طلا",
        row_decimals=0,
        y_title="قیمت انس جهانی طلا (دلار)",
        color_label="مظنه محاسباتی طلا (تومان)",
        bubble_asset_name="مظنه طلا",
    ),
    AssetView(
        key=AssetKey.SILVER_999,
        tab_title="⚪ نقره خام (۹۹۹)",
        subheader="🧮 ماتریس نقره خام عیار ۹۹۹، تومان در گرم",
        caption=(
            "این جدول قیمت محاسباتی هر گرم نقره خام ۹۹۹ را بر اساس "
            "سناریوهای دلار و انس جهانی نقره نمایش می‌دهد."
        ),
        row_prefix="انس نقره",
        row_decimals=2,
        y_title="قیمت انس جهانی نقره (دلار)",
        color_label="قیمت هر گرم نقره ۹۹۹ (تومان)",
        bubble_asset_name="هر گرم نقره ۹۹۹",
    ),
    AssetView(
        key=AssetKey.SILVER_CERT,
        tab_title="🥈 گواهی نقره",
        subheader="🧮 ماتریس ارزش نظری گواهی سپرده شمش نقره، تومان",
        caption=(
            "فرض محاسباتی: هر ورقه گواهی سپرده (نماد CD1SIB0001) معادل "
            "۱ گرم شمش نقره با عیار ۹۹۹٫۹ است. "
            "فرمول: (انس نقره ÷ ۳۱٫۱۰۳۴) × دلار آزاد (تومان) × (۱ + α). "
            "محور قیمت انس نقره با تب نقره خام مشترک است."
        ),
        row_prefix="انس نقره",
        row_decimals=2,
        y_title="قیمت انس جهانی نقره (دلار)",
        color_label="ارزش هر گواهی نقره (تومان)",
        bubble_asset_name="هر گواهی شمش نقره",
    ),
    AssetView(
        key=AssetKey.COPPER,
        tab_title="🟠 مس کاتد",
        subheader="🧮 ماتریس ارزش نظری گواهی سپرده مس کاتد، تومان",
        caption=(
            "فرض محاسباتی: هر ورقه گواهی سپرده معادل یک کیلوگرم "
            "مس کاتد است. قیمت LME بر حسب دلار/تن و نرخ ارز بر حسب "
            "تومان/دلار در نظر گرفته شده است."
        ),
        row_prefix="مس LME",
        row_decimals=0,
        y_title="قیمت مس LME (دلار بر تن)",
        color_label="ارزش هر گواهی مس (تومان)",
        bubble_asset_name="هر گواهی مس کاتد",
    ),
    AssetView(
        key=AssetKey.ZINC,
        tab_title="🔘 شمش روی",
        subheader="🧮 ماتریس ارزش نظری گواهی سپرده شمش روی، تومان",
        caption=(
            "فرض محاسباتی: هر ورقه گواهی سپرده (نماد ZincIngot) معادل "
            "یک کیلوگرم شمش روی با عیار ۹۹.۹۷٪ است. "
            "فرمول: LME Zinc (دلار/تن) × دلار آزاد (تومان) × (۱ + α) ÷ ۱۰۰۰. "
            "قیمت LME بر حسب دلار/تن و نرخ ارز بر حسب تومان/دلار در نظر "
            "گرفته شده است."
        ),
        row_prefix="روی LME",
        row_decimals=0,
        y_title="قیمت روی LME (دلار بر تن)",
        color_label="ارزش هر گواهی روی (تومان)",
        bubble_asset_name="هر گواهی شمش روی",
    ),
)