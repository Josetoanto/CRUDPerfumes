from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.modules.perfumes.model import Perfume
from app.modules.perfumes.exceptions import (
    PerfumeNotFound,
    PerfumeIntegrityError,
)


# ======================================
# Internal Helper
# ======================================

def _get_user_perfume(
    db: Session,
    user_id: int,
    perfume_id: int,
) -> Perfume:
    perfume = (
        db.query(Perfume)
        .filter(
            Perfume.id == perfume_id,
            Perfume.user_id == user_id,
        )
        .first()
    )

    if not perfume:
        raise PerfumeNotFound()

    return perfume


# ======================================
# Public Service Functions
# ======================================

def get_perfumes(db: Session, user_id: int) -> List[Perfume]:
    return (
        db.query(Perfume)
        .filter(Perfume.user_id == user_id)
        .all()
    )


def create_perfume(
    db: Session,
    user_id: int,
    data,
) -> Perfume:

    perfume = Perfume(
        user_id=user_id,
        **data.model_dump(),
    )

    db.add(perfume)

    try:
        db.commit()
        db.refresh(perfume)
        return perfume

    except IntegrityError as e:
        db.rollback()
        raise PerfumeIntegrityError() from e


def update_perfume(
    db: Session,
    user_id: int,
    perfume_id: int,
    data,
) -> Perfume:

    perfume = _get_user_perfume(db, user_id, perfume_id)

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(perfume, key, value)

    db.commit()
    db.refresh(perfume)

    return perfume


def delete_perfume(
    db: Session,
    user_id: int,
    perfume_id: int,
) -> None:

    perfume = _get_user_perfume(db, user_id, perfume_id)

    db.delete(perfume)
    db.commit()
