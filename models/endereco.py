from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, validates
from models.base import Base


class Endereco(Base):
    __tablename__ = 'endereco'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cidade = Column(String(100), nullable=False)
    rua = Column(String(150), nullable=False)
    numero = Column(String(20), nullable=False)
    bairro = Column(String(100), nullable=False)

    empresas = relationship('Empresa', back_populates='endereco')

    @validates('cidade', 'rua', 'numero', 'bairro')
    def validate_strings(self, key, value):
        """Valida strings não vazias"""
        if not value or not value.strip():
            raise ValueError(f"{key} não pode ser vazio")
        return value.strip()

    def __repr__(self):
        return f"<Endereco(id={self.id}, rua='{self.rua}', numero='{self.numero}', bairro='{self.bairro}', cidade='{self.cidade}')>"

