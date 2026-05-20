from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=50)
    citizen_id = forms.CharField(max_length=12)
    address = forms.CharField(max_length=100)

    def save(self, request):
        user = super().save(request)

        user.full_name = self.cleaned_data["full_name"]
        user.citizen_id = self.cleaned_data["citizen_id"]
        user.address = self.cleaned_data["address"]

        user.save()

        return user