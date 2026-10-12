from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TicketCategory(str, Enum):
    ORDER_STATUS = "order_status"
    TECHNICAL_SUPPORT = "technical_support"
    GENERAL_INQUIRY = "general_inquiry"


class RawTicketInput(BaseModel):
    """Data contract for incoming raw ticket payloads."""

    # Ignore unexpected keys automatically; strip whitespace from strings
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    text: str = Field(..., min_length=1, description="Raw ticket payload text")
    user_id: str | None = Field(default=None, description="Optional sender ID")

    @field_validator("text")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Ticket text cannot be empty or pure whitespace.")
        return value


class TicketClassification(BaseModel):
    """Strict execution output contract."""

    model_config = ConfigDict(extra="forbid")

    category: TicketCategory
    order_id: str | None = None
    needs_order_lookup: bool = False
