from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base


class RegimeTributario(Base):
    __tablename__ = 'regime_tributario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tributacao = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=False)

    empresa = relationship('Empresa', back_populates='regime_tributario')
