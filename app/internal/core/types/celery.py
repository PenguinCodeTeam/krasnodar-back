from enum import Enum


class CeleryTaskStatus(str, Enum):
    OK = 'ok'
    IN_PROGRESS = 'in_progress'
    ERROR = 'error'
