import base64
import contextvars
import uuid


request_id_var: contextvars.ContextVar = contextvars.ContextVar('request_id', default='-')


def generate_request_id() -> str:
    return base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b'=').decode()
