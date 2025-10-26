from sqlmodel import select, Session
from models import engine, Passenger, Flight, Ticket

def get_registered_passengers():
    with Session(engine) as session:
        stmt = select(Passenger).where(Passenger.status == "registered")
        return session.exec(stmt).all()

def get_available_flights():
    with Session(engine) as session:
        stmt = select(Flight).where(Flight.status == "planned")
        return session.exec(stmt).all()

def get_available_seats(flight_id: int):
    with Session(engine) as session:
        stmt = select(Seat).join(Ticket).where(
            Ticket.flight_id == flight_id,
            Seat.status == "free"
        )
        return session.exec(stmt).all()

def get_ticket_by_number(ticket_number: str):
    with Session(engine) as session:
        stmt = select(Ticket).where(Ticket.ticket_number == ticket_number)
        return session.exec(stmt).first()

def get_baggage_by_passenger(passenger_id: int):
    with Session(engine) as session:
        stmt = select(Baggage).join(Ticket).where(Ticket.passenger_id == passenger_id)
        return session.exec(stmt).all()

def get_crew_for_flight(flight_id: int):
    with Session(engine) as session:
        stmt = select(Crew).join(Crew_Flight).where(Crew_Flight.flight_id == flight_id)
        return session.exec(stmt).all()

if __name__ == "__main__":
    print("Зарегистрированные пассажиры:")
    for p in get_registered_passengers():
        print(f"- {p.full_name}")

    print("\nДоступные рейсы:")
    for f in get_available_flights():
        print(f"- {f.flight_number}: {f.departure_date}")