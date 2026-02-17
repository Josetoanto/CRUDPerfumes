from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL
from app.core.database import Base

class Perfume(Base):
    __tablename__ = "perfumes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100))
    brand = Column(String(100))
    description = Column(Text)
    stock = Column(Integer)
    price = Column(DECIMAL(10,2))
