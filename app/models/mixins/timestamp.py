from sqlalchemy import DateTime, Column, func




class TimeStampMixin:
    """A mixin for timestapming with 2 fields:
    - created_at (datetime)
    - updated_at (datetime)"""

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )