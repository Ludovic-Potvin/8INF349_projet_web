from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class OrderProduct(Base):
    __tablename__ = 'order_product'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    product = relationship("Product", back_populates="order_links", lazy='joined')
    order = relationship("Order", back_populates="product_links")

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "quantity": self.quantity
        }
