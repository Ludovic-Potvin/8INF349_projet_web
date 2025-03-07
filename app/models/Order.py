from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, validates

from app.models.base import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=True)
    total_price = Column(Integer, nullable=True)
    total_price_tax = Column(Integer, nullable=True)
    transaction = Column(String(100), nullable=True)
    paid = Column(Boolean, nullable=True)
    shipping_price = Column(Integer, nullable=True)

    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship('Product', back_populates='orders')
    shipping_info = relationship('ShippingInformation', backref='order', uselist=False, lazy=True)
    creditCard = relationship('CreditCard', backref='orders', uselist=False)


    def __repr__(self):
        return f'<Order {self.email}>'
    
    def to_dict(self):
        return {
            'email': self.email,
            'shipping_info': self.shipping_info.to_dict() if self.shipping_info else {},
            'credit_card': self.creditCard.to_dict() if self.creditCard else {},
            'total_price': self.total_price,
            'total_price_tax': self.total_price_tax,
            'transaction': self.transaction,
            'paid': self.paid,
            'product': {"id": self.product_id, "quantity": self.quantity},
            'shipping_price': self.shipping_price,
            'id': self.id
        }