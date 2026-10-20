from django.shortcuts import render

from .data import immigration, swiss_rates, uk_rates
from .engine.calculator import calculate
from .forms import TEST_CASE_INITIAL, AssignmentForm


def index(request):
    context = {
        "immigration_topics": immigration.TOPICS,
        "rules": uk_rates.RULES + swiss_rates.RULES,
        "rates_verified": uk_rates.VERIFIED,
        "tax_year": uk_rates.TAX_YEAR,
        "active_tab": "cost",
    }

    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            try:
                context["result"] = calculate(form.to_inputs())
            except NotImplementedError as exc:
                context["not_built_message"] = str(exc)
    else:
        form = AssignmentForm(initial=TEST_CASE_INITIAL)

    context["form"] = form
    return render(request, "estimator/index.html", context)