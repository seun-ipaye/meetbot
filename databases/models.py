import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Date, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from databases.database import Base

class User(Base):
    __tablename__ = "users"

    discord_user_id: Mapped[str] = mapped_column(String, primary_key=True)
    google_email:    Mapped[str] = mapped_column(String, nullable=False)
    calendar_id:     Mapped[str] = mapped_column(String, default="primary")
    access_token:    Mapped[str] = mapped_column(String, nullable=False)
    refresh_token:   Mapped[str] = mapped_column(String, nullable=False)
    token_expiry:    Mapped[datetime] = mapped_column(DateTime(timezone=True))
    timezone:        Mapped[str] = mapped_column(String, nullable=False)
    created_at:      Mapped[datetime] = mapped_column(
                         DateTime(timezone=True), server_default=text("now()")
                     )

class Meeting(Base):
    __tablename__ = "meetings"

    id:                Mapped[str] = mapped_column(
                           String, primary_key=True,
                           default=lambda: str(uuid.uuid4())
                       )
    guild_id:          Mapped[str] = mapped_column(String, nullable=False)
    channel_id:        Mapped[str] = mapped_column(String, nullable=False)
    organizer_id:      Mapped[str] = mapped_column(String, nullable=False)
    title:             Mapped[str] = mapped_column(String, nullable=False)
    duration_minutes:  Mapped[int] = mapped_column(Integer, nullable=False)
    date_range_start:  Mapped[datetime] = mapped_column(Date, nullable=False)
    date_range_end:    Mapped[datetime] = mapped_column(Date, nullable=False)
    status:            Mapped[str] = mapped_column(String, default="pending")
    confirmed_slot:    Mapped[datetime] = mapped_column(
                           DateTime(timezone=True), nullable=True
                       )
    created_at:        Mapped[datetime] = mapped_column(
                           DateTime(timezone=True), server_default=text("now()")
                       )

class MeetingAttendee(Base):
    __tablename__ = "meeting_attendees"

    meeting_id:      Mapped[str] = mapped_column(
                         String, ForeignKey("meetings.id"), primary_key=True
                     )
    discord_user_id: Mapped[str] = mapped_column(String, primary_key=True)
    status:          Mapped[str] = mapped_column(String, default="invited")