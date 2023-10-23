from uuid import uuid4


class AppException(Exception):
    msg: str | None = NotImplemented
    error_code = 1
    module_code = 'APP'
    system_prefix: str | None = NotImplemented

    def __init__(self, msg='', value=None, cause=None, extra_data=None):
        super().__init__()
        self.msg = msg or self.msg
        self.value = value
        self.cause = cause
        self.extra_data = extra_data
        self.uuid = uuid4()

    def __str__(self):
        return self.msg or self.__doc__ or self.__class__.__name__

    def __call__(self):
        return str(self)

    @classmethod
    def full_code(cls):
        return f'{cls.system_prefix}.{cls.module_code}.{cls.error_code:0>5}'


class UnknownException(AppException):
    system_prefix = 'APP'
    msg = 'Service error'
    error_code = 1
