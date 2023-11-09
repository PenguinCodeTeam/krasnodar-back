from enum import Enum


class CeleryTaskStatusEnum(str, Enum):
    OK = 'ok'
    IN_PROGRESS = 'in_progress'
    ERROR = 'error'
