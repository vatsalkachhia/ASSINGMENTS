# from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
import re
from datetime import date, datetime, time


TIME_RE = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")  # HH:MM 24-hour
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class Event(BaseModel):
    # Required (may be null)
    title: str = Field(..., description="Concise event title (≤10 words if inferred)")
    date: str = Field(..., description="Start date in ISO format YYYY-MM-DD")
    time: str = Field(..., description="HH:MM 24-hour")
    location: Optional[str] = Field(None, description="Venue, address, or platform")
    attendees: List[str] = Field(default_factory=list, description="Deduplicated list")

    # --- Field-level validators ---

    @field_validator("date", mode="before")
    def validate_iso_date_or_null(cls, v):
        if v is None:
            return None
        if isinstance(v, date):
            return v.isoformat()
        if isinstance(v, str) and ISO_DATE_RE.match(v):
            date.fromisoformat(v)  # raises if invalid
            return v
        raise ValueError("must be ISO YYYY-MM-DD or null")

    @field_validator("time", mode="before")
    def validate_time_or_null(cls, v):
        if v is None:
            return None
        if isinstance(v, time):
            return v.strftime("%H:%M")
        if isinstance(v, str) and TIME_RE.match(v):
            return v
        raise ValueError("must be HH:MM (24-hour) or null")

    @field_validator("title")
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("title must not be empty")
        return v.strip()

    @field_validator("attendees", mode="before")
    def normalize_attendees(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            parts = re.split(r"[;,]\s*|\n", v.strip())
        elif isinstance(v, (list, tuple)):
            parts = list(v)
        else:
            parts = [str(v)]

        seen = set()
        result = []
        for p in parts:
            if not p:
                continue
            s = re.sub(r"\s+", " ", str(p).strip()).rstrip(",;")
            if s and s.lower() not in seen:
                seen.add(s.lower())
                result.append(s)
        return result






# class Event_detailed(BaseModel):
#     # """
#     # Pydantic v2 model matching the extraction schema.
#     # """

#     # Required (may be null)
#     title: str = Field(..., description="Concise event title (≤10 words if inferred)")
#     date: str = Field(..., description="Start date in ISO format YYYY-MM-DD")
#     start_time: str = Field(..., description="HH:MM 24-hour")
#     end_time: Optional[str] = Field(None, description="HH:MM 24-hour or null")
#     timezone: Optional[str] = Field(None, description="IANA or UTC offset string")
#     location: Optional[str] = Field(None, description="Venue, address, or platform")
#     attendees: List[str] = Field(default_factory=list, description="Deduplicated list")

#     # Optional
#     end_date: Optional[str] = Field(None, description="End date YYYY-MM-DD or null")
#     recurrence: Optional[str] = None
#     organizer: Optional[str] = None
#     description: Optional[str] = None
#     notes: Optional[str] = None

#     # --- Field-level validators (v2 style) ---

#     @field_validator("date", "end_date", mode="before")
#     def validate_iso_date_or_null(cls, v):
#         if v is None:
#             return None
#         if isinstance(v, date):
#             return v.isoformat()
#         if isinstance(v, str) and ISO_DATE_RE.match(v):
#             date.fromisoformat(v)  # raises if invalid
#             return v
#         raise ValueError("must be ISO YYYY-MM-DD or null")

#     @field_validator("start_time", "end_time", mode="before")
#     def validate_time_or_null(cls, v):
#         if v is None:
#             return None
#         if isinstance(v, time):
#             return v.strftime("%H:%M")
#         if isinstance(v, str) and TIME_RE.match(v):
#             return v
#         raise ValueError("must be HH:MM (24-hour) or null")

#     @field_validator("title")
#     def title_must_not_be_empty(cls, v):
#         if not v.strip():
#             raise ValueError("title must not be empty")
#         return v.strip()

#     @field_validator("attendees", mode="before")
#     def normalize_attendees(cls, v):
#         if v is None:
#             return []
#         if isinstance(v, str):
#             parts = re.split(r"[;,]\s*|\n", v.strip())
#         elif isinstance(v, (list, tuple)):
#             parts = list(v)
#         else:
#             parts = [str(v)]

#         seen = set()
#         result = []
#         for p in parts:
#             if not p:
#                 continue
#             s = re.sub(r"\s+", " ", str(p).strip()).rstrip(",;")
#             if s and s.lower() not in seen:
#                 seen.add(s.lower())
#                 result.append(s)
#         return result

#     @model_validator(mode="after")
#     def check_consistency(self):
#         if self.start_time and self.end_time:
#             fmt = "%H:%M"
#             t_start = datetime.strptime(self.start_time, fmt).time()
#             t_end = datetime.strptime(self.end_time, fmt).time()
#             if t_end < t_start and not ( self.date < self.end_date):
#                 raise ValueError("end_time must be the same as or after start_time")

#         if self.date and self.end_date:
#             d1 = date.fromisoformat(self.date)
#             d2 = date.fromisoformat(self.end_date)
#             if d2 < d1:
#                 raise ValueError("end_date must be the same as or after date")

#         return self

#     # class Config:
#     #     populate_by_name = True
#     #     json_schema_extra = {
#     #         "example": {
#     #             "title": "Town Hall",
#     #             "date": "2025-09-17",
#     #             "end_date": None,
#     #             "start_time": "15:00",
#     #             "end_time": "16:00",
#     #             "timezone": None,
#     #             "location": "Main Auditorium",
#     #             "attendees": ["Mayor Rajiv Singh", "Maria Lopez", "all staff"],
#     #             "recurrence": None,
#     #             "organizer": None,
#     #             "description": None,
#     #             "notes": None,
#     #         }
#     #     }


