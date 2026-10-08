
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func

from backend.app.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SecurityScan(Base):
    __tablename__ = "security_scans"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    input_text = Column(Text, nullable=False)

    threat_type = Column(String, nullable=False)
    risk_level = Column(String, nullable=False)

    confidence = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())