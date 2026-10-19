"""Tax-on-tax gross-up.

The employer pays the employee's UK tax, and that tax is itself taxable pay.
So the tax T satisfies   T = UKTax(I + T)   where I is pay before any tax.

UK rates change between bands and the personal allowance is withdrawn above
£100,000, so there is no single multiplier. We solve it by fixed-point
iteration: guess T = 0, compute UKTax(I + T), feed the result back in, repeat
until it stops moving.

This converges because the highest marginal rate (60% in the allowance taper
zone) is below 100%: each pass shrinks the remaining error.
"""

from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal as D


class GrossUpError(Exception):
    """Raised if the iteration does not settle."""


@dataclass(frozen=True)
class GrossUpStep:
    iteration: int
    assumed_tax: D  # the T we fed in
    resulting_tax: D  # UKTax(I + assumed_tax)


@dataclass(frozen=True)
class GrossUpResult:
    initial_pay: D  # I
    tax: D  # T
    taxable_pay: D  # I + T
    steps: list[GrossUpStep]

    @property
    def iterations(self) -> int:
        return len(self.steps)


def gross_up(
    initial_pay: D,
    tax_fn: Callable[[D], D],
    tolerance: D = D("0.01"),
    max_iterations: int = 100,
) -> GrossUpResult:
    tax = D("0")
    steps: list[GrossUpStep] = []

    for iteration in range(1, max_iterations + 1):
        new_tax = tax_fn(initial_pay + tax)
        steps.append(GrossUpStep(iteration, tax, new_tax))
        if abs(new_tax - tax) < tolerance:
            return GrossUpResult(
                initial_pay=initial_pay,
                tax=new_tax,
                taxable_pay=initial_pay + new_tax,
                steps=steps,
            )
        tax = new_tax

    raise GrossUpError(f"Gross-up did not settle within {max_iterations} iterations.")
