from dataclasses import dataclass

@dataclass
class Apartment:
    user_id: int
    city: str
    price: int
    rooms: int
    address: str
    phone:str
    description: str
    photo: str | None = None
