from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base


class NaturezaJuridica(Base):
    __tablename__ = 'natureza_juridica'

    id = Column(Integer, primary_key=True, autoincrement=True)
    classificacao = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=False)

    empresa = relationship('Empresa', back_populates='natureza_juridica')
