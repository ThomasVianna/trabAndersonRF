import os
from flask import Flask, session
from dotenv import load_dotenv
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.empresas import empresas_bp
from routes.clientes import clientes_bp
from routes.consultas import consultas_bp
from routes.financeiro import financeiro_bp
from routes.relatorios import relatorios_bp
from routes.configuracoes import config_bp
from routes.landing import landing_bp


def create_app():
    load_dotenv()

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.secret_key = os.getenv('SECRET_KEY', 'siat-secret-2026')

    app.register_blueprint(landing_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(empresas_bp, url_prefix='/empresas')
    app.register_blueprint(clientes_bp, url_prefix='/clientes')
    app.register_blueprint(consultas_bp, url_prefix='/consultas')
    app.register_blueprint(financeiro_bp, url_prefix='/financeiro')
    app.register_blueprint(relatorios_bp, url_prefix='/relatorios')
    app.register_blueprint(config_bp, url_prefix='/configuracoes')

    @app.context_processor
    def inject_admin_nome():
        return {
            'admin_nome': session.get('admin_nome', os.getenv('ADMIN_NAME', 'Administrador'))
        }

    return app


if __name__ == '__main__':
    app = create_app()
    print('🚀 Aplicação iniciada em http://localhost:5000')
    app.run(debug=True)
