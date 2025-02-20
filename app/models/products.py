from sqlalchemy import Column, Integer, String, Float

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

    def __repr__(self):
        return f'<Product {self.name}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
