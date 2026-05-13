from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base


class Endereco(Base):
    __tablename__ = 'endereco'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cidade = Column(String(100), nullable=False)
    rua = Column(String(150), nullable=False)
    numero = Column(String(20), nullable=False)
    bairro = Column(String(100), nullable=False)

    empresa = relationship('Empresa', back_populates='endereco')
