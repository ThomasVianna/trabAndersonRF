from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from models.base import Base


class RegimeTributario(Base):
    __tablename__ = 'regime_tributario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tributacao = Column(String(100), nullable=False, unique=True)
    descricao = Column(String(255), nullable=False)

    empresas = relationship('Empresa', back_populates='regime_tributario')

    @validates('tributacao', 'descricao')
    def validate_strings(self, key, value):
        """Valida strings não vazias"""
        if not value or not value.strip():
            raise ValueError(f"{key} não pode ser vazio")
        return value.strip()

    def __repr__(self):
        return f"<RegimeTributario(id={self.id}, tributacao='{self.tributacao}')>"

