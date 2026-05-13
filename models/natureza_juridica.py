from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from models.base import Base


class NaturezaJuridica(Base):
    __tablename__ = 'natureza_juridica'

    id = Column(Integer, primary_key=True, autoincrement=True)
    classificacao = Column(String(100), nullable=False, unique=True)
    descricao = Column(String(255), nullable=False)

    empresas = relationship('Empresa', back_populates='natureza_juridica')

    @validates('classificacao', 'descricao')
    def validate_strings(self, key, value):
        """Valida strings não vazias"""
        if not value or not value.strip():
            raise ValueError(f"{key} não pode ser vazio")
        return value.strip()

    def __repr__(self):
        return f"<NaturezaJuridica(id={self.id}, classificacao='{self.classificacao}')>"

