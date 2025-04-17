from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class CreditCard(Base):
    __tablename__ = 'credit_card'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    number = Column(String(12), nullable=False)
    expiration_year = Column(Integer, nullable=False)
    cvv = Column(String(3), nullable=False)
    exp_month = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), unique=True)

    def __repr__(self):
        return f'<CreditCard {self.name}>'
    
    def to_dict(self):
        return {
            "name": self.name,
            "first_digits" : self.number[:4],
            "last_digits": self.number[-4:],
            "expiration_year": self.expiration_year,
            "exp_month": self.exp_month,
        }