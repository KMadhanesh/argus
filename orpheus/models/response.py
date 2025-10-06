# argus/orpheus/models/response.py

from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True) # frozen=True
class HandlerResponse:
    """
    Standard response structure for all handlers in the Orpheus system.
    """
    status: str  # e.g., "success", "failed", "clarification_needed"
    display_message: str
    metadata: dict[str, Any] = field(default_factory=dict)