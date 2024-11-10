from flask import Blueprint, render_template, session, redirect, url_for, request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import plotly.graph_objs as go
import plotly.io as pio
from flask_login import current_user
from models.sensor_data import DadosSensor
from flask_login import login_required
from decorators.role_required import role_required 

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    # Obter o parâmetro de filtragem da URL, padrão é 1 dia (24 horas)
    filtro = request.args.get('filtro', default='1dia', type=str)

    # Definir o limite de tempo com base no filtro selecionado
    agora = datetime.now(ZoneInfo('America/Sao_Paulo'))
    if filtro == '1hora':
        data_limite = agora - timedelta(hours=1)
    elif filtro == '1dia':
        data_limite = agora - timedelta(days=1)
    elif filtro == '7dias':
        data_limite = agora - timedelta(days=7)
    elif filtro == '1mes':
        data_limite = agora - timedelta(days=30)
    else:
        data_limite = agora - timedelta(days=1)  # Padrão: 1 dia

    # Consultar os dados do banco para o intervalo de tempo selecionado
    dados = DadosSensor.query.filter(DadosSensor.timestamp >= data_limite).order_by(DadosSensor.timestamp.asc()).all()

    # Extrair os valores dos dados
    timestamps = [d.timestamp.strftime('%d/%m/%Y %H:%M:%S') for d in dados]
    temperaturas = [d.temperatura for d in dados]
    umidades = [d.umidade for d in dados]
    luminosidades = [d.luminosidade for d in dados]
    umidadesolos = [d.umidadesolo for d in dados]

    # Passar os dados para o template
    return render_template(
        'dashboard.html',
        timestamps=timestamps,
        temperaturas=temperaturas,
        umidades=umidades,
        luminosidades=luminosidades,
        umidadesolos=umidadesolos,
        filtro=filtro,  # Enviar o filtro selecionado ao template
        user=current_user
    )