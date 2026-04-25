from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ErrorDetail(BaseModel):
    message: str
    error_code: str
    details: Dict[str, Any] = Field(
        default_factory=dict,
    )
    error_type: str | None = None


class ErrorResponse(BaseModel):
    detail: ErrorDetail


class ValidationErrorDetail(BaseModel):
    loc: list[str | int]
    msg: str
    type: str
    input: Optional[Any] = Field(None)


class ValidationErrorResponse(BaseModel):
    detail: list[ValidationErrorDetail]
