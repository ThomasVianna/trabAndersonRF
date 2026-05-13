from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from models.base import Base


class PorteEmpresa(Base):
    __tablename__ = 'porte_empresa'

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoria = Column(String(100), nullable=False, unique=True)
    faturamento = Column(String(100), nullable=False)

    empresas = relationship('Empresa', back_populates='porte_empresa')

    @validates('categoria', 'faturamento')
    def validate_strings(self, key, value):
        """Valida strings não vazias"""
        if not value or not value.strip():
            raise ValueError(f"{key} não pode ser vazio")
        return value.strip()

    def __repr__(self):
        return f"<PorteEmpresa(id={self.id}, categoria='{self.categoria}', faturamento='{self.faturamento}')>"

