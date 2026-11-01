from enum import StrEnum


class RefundStatus(StrEnum):
    RECEIVED = "received"
    EVALUATING = "evaluating"
    NEEDS_EVIDENCE = "needs_evidence"
    NEEDS_APPROVAL = "needs_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
