from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.dependencies import get_db, get_current_user
from app.modules.perfumes.schemas import PerfumeCreate, PerfumeResponse
from app.modules.perfumes.service import (
    get_perfumes,
    create_perfume,
    update_perfume,
    delete_perfume
)
from app.modules.perfumes.exceptions import PerfumeNotFound

router = APIRouter(
    prefix="/perfumes",
    tags=["Perfumes"]
)


# ======================================
# GET ALL PERFUMES (USER OWNED)
# ======================================

@router.get("/", response_model=list[PerfumeResponse])
def list_perfumes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_perfumes(db, current_user.id)


# ======================================
# CREATE PERFUME
# ======================================

@router.post("/", response_model=PerfumeResponse)
def add_perfume(
    data: PerfumeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return create_perfume(db, current_user.id, data)

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "DB_CONSTRAINT",
                "message": "Violación de integridad en la base de datos"
            }
        )


# ======================================
# UPDATE PERFUME
# ======================================

@router.put("/{perfume_id}", response_model=PerfumeResponse)
def edit_perfume(
    perfume_id: int,
    data: PerfumeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        return update_perfume(
            db=db,
            user_id=current_user.id,
            perfume_id=perfume_id,
            data=data,
        )

    except PerfumeNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "NOT_FOUND",
                "message": "Perfume no encontrado"
            }
        )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": "DB_CONSTRAINT",
                "message": "Violación de integridad en la base de datos"
            }
        )


# ======================================
# DELETE PERFUME
# ======================================

@router.delete("/{perfume_id}")
def remove_perfume(
    perfume_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    try:
        delete_perfume(
            db=db,
            user_id=current_user.id,
            perfume_id=perfume_id,
        )

        return {"message": "Perfume eliminado correctamente"}

    except PerfumeNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "NOT_FOUND",
                "message": "Perfume no encontrado"
            }
        )
