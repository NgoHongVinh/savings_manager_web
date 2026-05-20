from django.contrib.sessions.backends.base import SessionBase
from django.forms import BaseForm
from django.forms.utils import ErrorDict, ErrorList

def read_session_errors(form: BaseForm, session: SessionBase, error_key: str):
    errors = session.pop(error_key, None)
    if errors:
        form._errors = ErrorDict({
            field: ErrorList(errors)
            for field, errors in errors.items()
        })