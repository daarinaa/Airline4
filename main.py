from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from models import engine, Passenger, Flight, Ticket, Seat, Baggage, Crew, Crew_Flight

app = FastAPI(
)

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/passengers/registered")
def get_registered_passengers(session: Session = Depends(get_session)):
    statement = select(Passenger).where(Passenger.status == "registered")
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(404, "No registered passengers")
    return results

@app.get("/flights/available")
def get_available_flights(session: Session = Depends(get_session)):
    statement = select(Flight).where(Flight.status == "planned")
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(404, "No available flights")
    return results

@app.get("/seats/available/{flight_id}")
def get_available_seats(flight_id: int, session: Session = Depends(get_session)):
    flight = session.exec(select(Flight).where(Flight.flight_id == flight_id)).first()
    if not flight:
        raise HTTPException(404, "Flight not found")
    booked_seat_ids = [t.seat_id for t in session.exec(select(Ticket).where(Ticket.flight_id == flight_id)).all()]
    statement = select(Seat).where(
        Seat.plane_id == flight.plane_id,
        Seat.seat_id.not_in(booked_seat_ids) if booked_seat_ids else True
    )
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(404, "No available seats")
    return results

@app.get("/tickets/{ticket_number}")
def get_ticket_by_number(ticket_number: str, session: Session = Depends(get_session)):
    result = session.exec(select(Ticket).where(Ticket.ticket_number == ticket_number)).first()
    if not result:
        raise HTTPException(404, "Ticket not found")
    return result

@app.get("/baggage/passenger/{passenger_id}")
def get_baggage_by_passenger(passenger_id: int, session: Session = Depends(get_session)):
    results = session.exec(select(Baggage).join(Ticket).where(Ticket.passenger_id == passenger_id)).all()
    if not results:
        raise HTTPException(404, "No baggage found")
    return results

@app.get("/crew/flight/{flight_id}")
def get_crew_for_flight(flight_id: int, session: Session = Depends(get_session)):
    results = session.exec(select(Crew).join(Crew_Flight).where(Crew_Flight.flight_id == flight_id)).all()
    if not results:
        raise HTTPException(404, "No crew found")
    return results

@app.post("/passengers")
def create_passenger(passenger: Passenger, session: Session = Depends(get_session)):
    session.add(passenger)
    session.commit()
    session.refresh(passenger)
    return passenger
