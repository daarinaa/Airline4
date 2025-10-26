from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
from sqlalchemy import Column, String

class Passenger(SQLModel, table=True):
    passenger_id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(..., max_length=255)
    passport_data: str = Field(..., max_length=50)
    contact_info: Optional[str] = Field(default=None, max_length=255)
    status: Optional[str] = Field(default=None, max_length=50)

class Plane(SQLModel, table=True):
    plane_id: Optional[int] = Field(default=None, primary_key=True)
    registration_number: str = Field(..., max_length=50)
    model: Optional[str] = Field(default=None, max_length=100)
    capacity: Optional[int] = None
    status: Optional[str] = Field(default=None, max_length=50)

class Seat(SQLModel, table=True):
    seat_id: Optional[int] = Field(default=None, primary_key=True)
    plane_id: int = Field(foreign_key="plane.plane_id")
    row_number: int
    seat_number: str
    class_type: str = Field(..., sa_column=Column('"class_type"', String(50)))
    status: str

class Flight(SQLModel, table=True):
    flight_id: Optional[int] = Field(default=None, primary_key=True)
    flight_number: str = Field(..., max_length=50)
    departure_date: Optional[str] = None
    arrival_date: Optional[str] = None
    status: Optional[str] = Field(default=None, max_length=50)
    plane_id: int = Field(foreign_key="plane.plane_id")

class Ticket(SQLModel, table=True):
    ticket_id: Optional[int] = Field(default=None, primary_key=True)
    ticket_number: Optional[str] = Field(default=None, max_length=50)
    status: Optional[str] = Field(default=None, max_length=50)
    passenger_id: int = Field(foreign_key="passenger.passenger_id")
    flight_id: int = Field(foreign_key="flight.flight_id")
    seat_id: int = Field(foreign_key="seat.seat_id")
    cost: Optional[float] = None

class Transaction(SQLModel, table=True, __tablename__="Operation"):
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: int = Field(foreign_key="ticket.ticket_id")
    amount: float
    status: str = Field(..., max_length=50)
    transaction_date: Optional[str] = None

class Baggage(SQLModel, table=True):
    baggage_id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: int = Field(foreign_key="ticket.ticket_id")
    weight: Optional[float] = None
    type: str = Field(..., max_length=50)
    status: Optional[str] = Field(default=None, max_length=50)

class Checkin(SQLModel, table=True):
    checkin_id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: int = Field(foreign_key="ticket.ticket_id")
    baggage_checked: Optional[bool] = None
    boarding_pass: Optional[str] = Field(default=None, max_length=50)
    status: Optional[str] = Field(default=None, max_length=50)

class Crew(SQLModel, table=True):
    crew_id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(..., max_length=255)
    position: str = Field(..., max_length=100)
    status: Optional[str] = Field(default=None, max_length=50)

class Crew_Flight(SQLModel, table=True):
    crew_id: int = Field(foreign_key="crew.crew_id", primary_key=True)
    flight_id: int = Field(foreign_key="flight.flight_id", primary_key=True)

DATABASE_URL = (
    "mssql+pyodbc:///?odbc_connect="
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=LAPTOP-FTKIEJ5B\\SQLEXPRESS;"
    "Database=AirlineDB;"
    "Trusted_Connection=yes;"
)

engine = create_engine(DATABASE_URL, echo=True)