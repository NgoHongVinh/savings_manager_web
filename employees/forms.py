from django import forms

from users.models import EmployeeRole, Employee

class EmployeeChangeForm(forms.Form):
    hasRead = forms.BooleanField(required=False)
    hasWrite = forms.BooleanField(required=False)

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        if self.user.is_employee:
            self.fields["hasRead"].initial = True
            self.fields["hasWrite"].initial = user.employee.role == EmployeeRole.WRITE

    def clean(self):
        cleaned_data = super().clean()

        has_write = cleaned_data.get("hasWrite")
        if has_write:
            cleaned_data["hasRead"] = True

        return cleaned_data

    def save(self):
        has_read = self.cleaned_data["hasRead"]
        has_write = self.cleaned_data["hasWrite"]

        if not has_read:
            if self.user.is_employee:
                self.user.employee.delete()
            return None

        if has_write:
            role = EmployeeRole.WRITE
        else:
            role = EmployeeRole.READ

        employee, created = Employee.objects.get_or_create(user=self.user, defaults={"role": role})
        if employee.role != role:
            employee.role = role
            employee.save(update_fields=["role"])

        return employee