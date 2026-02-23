from sqlalchemy.orm import Session

from app.models import Role, Permission
from app.security import ROLE_MATRIX


def seed_roles_permissions(db: Session):
    for role_name, matrix in ROLE_MATRIX.items():
        role = db.query(Role).filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name)
            db.add(role)
            db.flush()
        for module, (can_read, can_write) in matrix.items():
            perm = db.query(Permission).filter_by(role_id=role.id, module=module).first()
            if not perm:
                db.add(Permission(role_id=role.id, module=module, can_read=can_read, can_write=can_write))
            else:
                perm.can_read = can_read
                perm.can_write = can_write
    db.commit()
