from enum import Enum


class PriorityEnum(str, Enum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class TaskStatusEnum(str, Enum):
    OPEN = 'open'
    APPOINTED = 'appointed'
    CLOSED = 'closed'
