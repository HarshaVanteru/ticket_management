from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.schemas.ticket import TicketCreate, TicketResponse
from app.dependencies.auth import get_db, require_admin
from app.dependencies.auth import get_current_user
from app.services.ticket_service import create_ticket, get_my_tickets, get_all_tickets, resolve_ticket
from app.models.user import User

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=TicketResponse)
def raise_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_ticket(
        db=db,
        title=ticket_data.title,
        description=ticket_data.description,
        current_user=current_user
    )

@router.get("/my", response_model=list[TicketResponse])
def my_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_my_tickets(db, current_user.id)

@router.get("/admin/all", response_model=list[TicketResponse])
def all_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)
    return get_all_tickets(db)

@router.put("/admin/{ticket_id}/resolve", response_model=TicketResponse)
def resolve_ticket_api(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    ticket = resolve_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket

