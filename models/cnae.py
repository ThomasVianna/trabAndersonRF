from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base


class CNAE(Base):
    __tablename__ = 'cnae'

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(20), nullable=False)
    descricao = Column(String(255), nullable=False)

    empresa = relationship('Empresa', back_populates='cnae')
