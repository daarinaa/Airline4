from sqlmodel import Session
from models import engine, Passenger, Plane, Flight, Seat, Ticket

with Session(engine) as session:
    p1 = Passenger(full_name="Иванов Иван", passport_data="AB1234567", contact_info="ivan@example.com", status="registered")
    p2 = Passenger(full_name="Петрова Анна", passport_data="CD7654321", contact_info="anna@example.com", status="booked")
    session.add_all([p1, p2])

    plane1 = Plane(registration_number="RA-98765", model="Airbus A320", capacity=180, status="ready")
    plane2 = Plane(registration_number="VP-BBB", model="Boeing 737", capacity=150, status="in_flight")
    session.add_all([plane1, plane2])

    session.add_all([p1, p2, plane1, plane2])
    session.commit()

    flight1 = Flight(
        flight_number="SU123",
        departure_date="2025-04-01 10:00",
        arrival_date="2025-04-01 12:00",
        status="planned",
        plane_id=plane1.plane_id
    )
    session.add(flight1)
    session.commit()

    seat1 = Seat(plane_id=plane1.plane_id, row_number=1, seat_number="A", class_type="эконом", status="free")
    session.add(seat1)
    session.commit()

    ticket1 = Ticket(
        ticket_number="TICKET001",
        status="booked",
        passenger_id=p1.passenger_id,
        flight_id=flight1.flight_id,
        seat_id=seat1.seat_id,
        cost=5000.0
    )
    session.add(ticket1)
    session.commit()

    print("Тестовые данные добавлены!")