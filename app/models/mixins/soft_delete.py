from sqlalchemy import DateTime, Column
from sqlalchemy.sql import func


# Mixin pour soft delete:

# REGLE :
    # un champ deleted_at :
        # si None : objet non delete 
        # si not None : objet a été delete (invisble)

class SoftDeleteMixin:

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    def soft_delete(self):
        self.deleted_at = func.now()

    def restore(self):
        self.deleted_at = None