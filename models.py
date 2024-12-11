from pydantic.dataclasses import dataclass


@dataclass
class Response:
    success: bool
    label: str = None
    confidence: float = None
    filename: str = None
    error: str = None