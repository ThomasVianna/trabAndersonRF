from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base


class PorteEmpresa(Base):
    __tablename__ = 'porte_empresa'

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoria = Column(String(100), nullable=False)
    faturamento = Column(String(100), nullable=False)

    empresa = relationship('Empresa', back_populates='porte_empresa')
