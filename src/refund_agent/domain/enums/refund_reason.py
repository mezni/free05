from enum import StrEnum


class RefundReason(StrEnum):
    CUSTOMER_REMORSE = "customer_remorse"
    DAMAGED_ITEM = "damaged_item"
    DEFECTIVE_ITEM = "defective_item"
    WRONG_ITEM = "wrong_item"
    NOT_AS_DESCRIBED = "not_as_described"
    OTHER = "other"
