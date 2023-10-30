import datetime


def form_token_due_date_lifetime(raw_token_lifetime: str) -> datetime.datetime:
    token_lifetime = parse_token_lifetime(raw_token_lifetime)
    return datetime.datetime.now() + token_lifetime


def parse_token_lifetime(raw_token_lifetime) -> datetime.timedelta:
    days, hours, minutes = map(int, raw_token_lifetime.split(':'))
    return datetime.timedelta(days=days, hours=hours, minutes=minutes)
