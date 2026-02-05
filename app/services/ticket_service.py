from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.models.user import User

def create_ticket(
    db: Session,
    title: str,
    description: str,
    current_user: User
):
    ticket = Ticket(
        title=title,
        description=description,
        user_id=current_user.id,
        status="OPEN"
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def get_my_tickets(db: Session, user_id: int):
    return db.query(Ticket).filter(Ticket.user_id == user_id).all()

def get_all_tickets(db: Session):
    return db.query(Ticket).all()

def resolve_ticket(db: Session, ticket_id: int):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        return None
    ticket.status = "RESOLVED"
    db.commit()
    db.refresh(ticket)
    return ticket

