from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, validates
from models.base import Base
import re


class Empresa(Base):
    __tablename__ = 'empresa'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(18), unique=True, nullable=False)
    data_abertura = Column(Date, nullable=False)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255), nullable=False)

    endereco_id = Column(Integer, ForeignKey('endereco.id', ondelete='SET NULL'))
    natureza_juridica_id = Column(Integer, ForeignKey('natureza_juridica.id', ondelete='SET NULL'))
    porte_empresa_id = Column(Integer, ForeignKey('porte_empresa.id', ondelete='SET NULL'))
    regime_tributario_id = Column(Integer, ForeignKey('regime_tributario.id', ondelete='SET NULL'))
    cnae_id = Column(Integer, ForeignKey('cnae.id', ondelete='SET NULL'))

    endereco = relationship('Endereco', back_populates='empresas', uselist=False)
    natureza_juridica = relationship('NaturezaJuridica', back_populates='empresas', uselist=False)
    porte_empresa = relationship('PorteEmpresa', back_populates='empresas', uselist=False)
    regime_tributario = relationship('RegimeTributario', back_populates='empresas', uselist=False)
    cnae = relationship('CNAE', back_populates='empresas', uselist=False)

    @validates('cnpj')
    def validate_cnpj(self, key, value):
        """Valida formato CNPJ"""
        if not value:
            raise ValueError("CNPJ não pode ser vazio")
        # Remove caracteres especiais
        cnpj_clean = re.sub(r'\D', '', value)
        if len(cnpj_clean) != 14:
            raise ValueError(f"CNPJ deve ter 14 dígitos, recebido: {len(cnpj_clean)}")
        return value

    @validates('razao_social', 'nome_fantasia')
    def validate_strings(self, key, value):
        """Valida strings não vazias"""
        if not value or not value.strip():
            raise ValueError(f"{key} não pode ser vazio")
        return value.strip()

    def __repr__(self):
        return f"<Empresa(id={self.id}, cnpj='{self.cnpj}', razao_social='{self.razao_social}')>"

