from enum import Enum


class BookStatus(Enum):
    AVAILABLE_BOOK = "available"
    ISSUED_BOOK = "issued"
    RETURNED_BOOK = "returned"
    NOT_AVAILABLE = "not_available"
