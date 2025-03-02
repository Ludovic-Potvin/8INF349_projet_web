from sqlalchemy import Column, Integer, String, ForeignKey

from app.models.base import Base


class ShippingInformation(Base):
    __tablename__ = 'shipping_information'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=False)
    address = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    city = Column(String, nullable=False)
    province = Column(String, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), unique=True)

    def __repr__(self):
        return f'<ShippingInformation {self.address}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'country': self.country,
            'address': self.address,
            'postal_code': self.postal_code,
            'city': self.city,
            'province': self.province,
        }
