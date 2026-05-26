from decimal import Decimal

from django import forms

from savings.models import SavingPlan, SavingType


class TransactionForm(forms.Form):
    ACTION_CHOICES = [
        ("create", "Create Saving Plan"),
        ("deposit", "Deposit"),
        ("withdraw", "Withdraw"),
    ]
    action = forms.ChoiceField(choices=ACTION_CHOICES)
    saving_plan = forms.ModelChoiceField(queryset=SavingPlan.objects.none(), empty_label="Select saving plan", required=False)
    saving_type = forms.ModelChoiceField(queryset=SavingType.objects.filter(is_active=True), required=False)
    initial_balance = forms.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal("0"), required=False)
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal("0"), required=False)

    def __init__(self, *args, saving_plans_qs=None, **kwargs):
        super().__init__(*args, **kwargs)
        if saving_plans_qs is not None:
            self.fields["saving_plan"].queryset = saving_plans_qs

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get("action")

        if action == "create":
            if not cleaned_data.get("saving_type"):
                self.add_error("saving_type", "This field is required.")
            if cleaned_data.get("initial_balance") is None:
                self.add_error("initial_balance", "This field is required.")
        else:
            if not cleaned_data.get("saving_plan"):
                self.add_error("saving_plan", "This field is required.")
            if cleaned_data.get("amount") is None:
                self.add_error("amount", "This field is required.")

        return cleaned_data

class ReportForm(forms.Form):
    PERIOD_CHOICES = [("day", "By Day"), ("month", "By Month"),("year", "By Year")]
    period_type = forms.ChoiceField(choices=PERIOD_CHOICES)
    saving_plan = forms.ModelChoiceField(queryset=SavingPlan.objects.none(), empty_label="Select saving plan")
    date = forms.DateField(required=False,widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, saving_plans_qs=None, **kwargs):
        super().__init__(*args, **kwargs)
        if saving_plans_qs is not None:
            self.fields["saving_plan"].queryset = saving_plans_qs
