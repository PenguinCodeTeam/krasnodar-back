from enum import Enum


class PriorityEnum(str, Enum):
    HIGH = 'Высокий'
    MEDIUM = 'Средний'
    LOW = 'Низкий'
