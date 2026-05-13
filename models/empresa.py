from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.base import Base


class Empresa(Base):
    __tablename__ = 'empresa'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String(18), unique=True, nullable=False)
    data_abertura = Column(Date, nullable=False)
    razao_social = Column(String(255), nullable=False)
    nome_fantasia = Column(String(255), nullable=False)

    endereco_id = Column(Integer, ForeignKey('endereco.id'))
    natureza_juridica_id = Column(Integer, ForeignKey('natureza_juridica.id'))
    porte_empresa_id = Column(Integer, ForeignKey('porte_empresa.id'))
    regime_tributario_id = Column(Integer, ForeignKey('regime_tributario.id'))
    cnae_id = Column(Integer, ForeignKey('cnae.id'))

    endereco = relationship('Endereco', back_populates='empresa')
    natureza_juridica = relationship('NaturezaJuridica', back_populates='empresa')
    porte_empresa = relationship('PorteEmpresa', back_populates='empresa')
    regime_tributario = relationship('RegimeTributario', back_populates='empresa')
    cnae = relationship('CNAE', back_populates='empresa')
