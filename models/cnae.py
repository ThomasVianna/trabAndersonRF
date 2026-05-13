from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from models.base import Base


class CNAE(Base):
    __tablename__ = 'cnae'

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(20), nullable=False, unique=True)
    descricao = Column(String(255), nullable=False)

    empresas = relationship('Empresa', back_populates='cnae')

    @validates('codigo', 'descricao')
    def validate_strings(self, key, value):
        """Valida strings não vazias"""
        if not value or not value.strip():
            raise ValueError(f"{key} não pode ser vazio")
        return value.strip()

    def __repr__(self):
        return f"<CNAE(id={self.id}, codigo='{self.codigo}', descricao='{self.descricao}')>"

