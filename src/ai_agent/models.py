from enum import Enum
from pydantic import BaseModel


class TicketCategory(str, Enum):
    ORDER_STATUS = "order_status"
    TECHNICAL_SUPPORT = "technical_support"
    GENERAL_INQUIRY = "general_inquiry"


class TicketClassification(BaseModel):
    category: TicketCategory
    order_id: str | None = None
    needs_order_lookup: bool = False
