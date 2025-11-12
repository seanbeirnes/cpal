from sqlmodel import Session, create_engine
from model.event import QAEvent
from typing import Optional
import os

DATABASE_URL: str | None = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

def log_qa(
    question: Optional[str] = None,
    chunk_ids: Optional[str] = None,
    answer: Optional[str] = None,
):
    with Session(engine) as session:
        event = QAEvent(question=question, chunk_ids=chunk_ids, answer=answer)
        session.add(event)
        session.commit()
        session.refresh(event)
    return event

