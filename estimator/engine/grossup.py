from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal as D


class GrossUpError(Exception):
    """Raised if the iteration does not settle."""


@dataclass(frozen=True)
class GrossUpStep:
    iteration: int
    assumed_tax: D  
    resulting_tax: D  


@dataclass(frozen=True)
class GrossUpResult:
    initial_pay: D  
    tax: D  
    taxable_pay: D  
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
