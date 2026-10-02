"""تعریف محور سناریو (قیمت پایه، گام و تعداد گام بالا/پایین)."""
from __future__ import annotations

from dataclasses import dataclass


class EmptyScenarioError(ValueError):
    """وقتی یک یا چند محور سناریو هیچ مقدار مثبتی نداشته باشند."""

    def __init__(self, axis_names):
        self.axis_names = tuple(axis_names)
        super().__init__(
            "محورهای خالی: " + "، ".join(self.axis_names)
        )


@dataclass(frozen=True)
class ScenarioAxis:
    base: float
    step: float
    steps_down: int = 0
    steps_up: int = 0

    def __post_init__(self):
        if self.step <= 0:
            raise ValueError("step باید بزرگ‌تر از صفر باشد.")
        if self.steps_down < 0 or self.steps_up < 0:
            raise ValueError("تعداد گام‌ها نمی‌تواند منفی باشد.")

    def values(self) -> tuple:
        """مقادیر مثبت محور، از کم به زیاد."""
        result = []
        for i in range(-self.steps_down, self.steps_up + 1):
            value = self.base + i * self.step
            if value > 0:
                result.append(value)
        return tuple(result)