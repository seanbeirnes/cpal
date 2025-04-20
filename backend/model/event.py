from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import timezone, datetime

class QAEvent(SQLModel, table=True):
    __tablename__: str = "qa_event"

    uuid: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    question: Optional[str] = None
    chunk_ids: Optional[str] = None
    answer: Optional[str] = None
