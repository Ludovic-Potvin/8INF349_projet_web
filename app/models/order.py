from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
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

    product_links = relationship('OrderProduct', back_populates='order', cascade="all, delete-orphan", lazy='joined')
    shipping_info = relationship('ShippingInformation', backref='order', uselist=False, lazy=True)
    creditCard = relationship('CreditCard', backref='orders', uselist=False)


    def __repr__(self):
        return (f'<Email: {self.email},ID:{self.id},TRANSAC{self.transaction},'
                f'TOTAL PRICE{self.total_price},TOTALPRICETAX{self.total_price_tax},'
                f'PAID:{self.paid},SHIPPINGPRICE{self.shipping_price}>')
    
    def to_dict(self):
        return {
            'email': self.email,
            'shipping_info': self.shipping_info.to_dict() if self.shipping_info else {},
            'credit_card': self.creditCard.to_dict() if self.creditCard else {},
            'total_price': self.total_price,
            'total_price_tax': self.total_price_tax,
            'transaction': self.transaction,
            'paid': self.paid,
            'products': [link.to_dict() for link in self.product_links],
            'shipping_price': self.shipping_price,
            'id': self.id
        }