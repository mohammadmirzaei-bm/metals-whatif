"""برچسب‌های دوطرفه (Bidi) برای Plotly و جدول‌ها."""
import math
from typing import List

from metals_whatif.core import ScenarioAxis

RLI = "\u2067"   # Right-to-Left Isolate
LRI = "\u2066"   # Left-to-Right Isolate
PDI = "\u2069"   # Pop Directional Isolate


def rtl_isolate(text: str) -> str:
    return f"{RLI}{text}{PDI}"


def ltr_isolate(text: str) -> str:
    return f"{LRI}{text}{PDI}"


def make_plotly_label(prefix, value, decimals=0, pinned=False) -> str:
    pin = "📌 " if pinned else ""
    formatted_value = f"{value:,.{decimals}f}"
    return rtl_isolate(f"{pin}{prefix}: {ltr_isolate(formatted_value)}")


def axis_labels(axis: ScenarioAxis, prefix: str, decimals: int = 0) -> List[str]:
    """برچسب هر مقدار محور؛ مقدار پایه با 📌 مشخص می‌شود."""
    return [
        make_plotly_label(
            prefix, value, decimals, pinned=math.isclose(value, axis.base)
        )
        for value in axis.values()
    ]