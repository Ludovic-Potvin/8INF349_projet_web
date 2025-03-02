from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    in_stock = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    weight = Column(Float, nullable=True)
    image = Column(String(255), nullable=True)

    orders = relationship('Order', back_populates='product')

    def __repr__(self):
        return f'<Product {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            #Supposed to be quantity
            'in_stock': self.in_stock,
        }