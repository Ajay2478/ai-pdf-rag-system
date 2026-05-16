"""
Audit Service
Handles audit logging (DB persistence)
"""

from sqlalchemy.orm import Session
from typing import Optional

from app.models.audit_log import AuditLog


def log_action(
    db: Session,
    user_id: int,
    action: str,
    resource: str,
    resource_id: Optional[int] = None,
    details: Optional[str] = None
):
    """
    Create audit log entry

    IMPORTANT:
    - Must be lightweight
    - Should not fail main request
    """

    log = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        resource_id=resource_id,
        details=details
    )

    db.add(log)
    db.commit()