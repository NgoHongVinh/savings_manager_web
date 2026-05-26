from django.contrib import messages
from django.shortcuts import redirect, render

from dashboard.decorators import customer_required
from savings.forms import (
    TransactionForm,
    ReportForm,
)

from savings.services import (
    generate_statistics,
    get_active_saving_types,
    get_customer_transactions_context,
    get_plans_by_user,
    process_transaction_form,
)

@customer_required
def saving_plans(request):
    saving_plans = get_plans_by_user(request.user)
    saving_types = get_active_saving_types()
    transaction_form = TransactionForm(prefix="txn", saving_plans_qs=saving_plans)

    report_form = ReportForm(saving_plans_qs=saving_plans)
    statistics = None

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        try:
            if form_type == "transaction":
                transaction_form = TransactionForm(request.POST, prefix="txn", saving_plans_qs=saving_plans)

                if transaction_form.is_valid():
                    action = transaction_form.cleaned_data["action"]
                    process_transaction_form(request.user.customer, transaction_form.cleaned_data)

                    if action == "create":
                        messages.success(request, "Saving plan created successfully.")
                    elif action == "deposit":
                        messages.success(request, "Deposit completed.")
                    else:
                        messages.success(request, "Withdrawal completed.")
                    return redirect("saving_plans")

            elif form_type == "statistics":

                report_form = ReportForm(request.POST, saving_plans_qs=saving_plans)

                if report_form.is_valid():

                    statistics = generate_statistics(
                        report_form.cleaned_data,
                        month=request.POST.get("month"),
                        year=request.POST.get("year"),
                    )

                    messages.success(request, "Report generated successfully.")

        except ValueError as exc:
            messages.error(request, str(exc))

    return render(
        request,
        "savings/saving_plans.html",
        {
            "saving_plans": saving_plans,
            "saving_types": saving_types,
            "transaction_form": transaction_form,

            "report_form": report_form,
            "statistics": statistics,
        },
    )

@customer_required
def transactions(request):
    context = get_customer_transactions_context(
        request.user,
        selected_plan_id=request.GET.get("saving_plan", ""),
    )
    return render(request, "savings/transactions.html", context)
