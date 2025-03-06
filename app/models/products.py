from sqlalchemy import Column, Integer, String, Float

from app.models.base import Base


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    type = Column(String(100), nullable=True)
    description = Column(String(255), nullable=True)
    image = Column(String(255), nullable=True)
    height = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    price = Column(Float, nullable=False)
    in_stock = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
