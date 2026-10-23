from django.shortcuts import render

from .data import immigration, swiss_rates, uk_benefits, uk_rates
from .engine.calculator import calculate
from .forms import TEST_CASE_INITIAL, AssignmentForm


def index(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
    else:
        form = AssignmentForm(initial=TEST_CASE_INITIAL)

    context = {
        "form": form,
        "result": calculate(form.to_inputs()) if form.is_valid() else None,
        "rules": uk_rates.RULES + uk_benefits.RULES + swiss_rates.RULES,
        "immigration_topics": immigration.TOPICS,
    }
    return render(request, "estimator/index.html", context)
