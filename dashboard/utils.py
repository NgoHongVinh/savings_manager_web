from django.contrib.sessions.backends.base import SessionBase
from django.forms import Form
from django.forms.utils import ErrorDict, ErrorList

def read_session_errors(form: Form, session: SessionBase, error_key: str):
    errors = session.pop(error_key, None)
    if errors:
        form._errors = ErrorDict({
            field: ErrorList(errors)
            for field, errors in errors.items()
        })