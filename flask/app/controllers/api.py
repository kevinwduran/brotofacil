from flask import Blueprint, request, jsonify, Response
from models.sensor_data import db, DadosSensor
from io import StringIO
import csv
from datetime import datetime

api_bp = Blueprint('api', __name__)

# Estado dos sensores
sensor_states = {
    "dht": True,  # Sensor DHT começa como ligado
    "luz": True,  # Sensor de luminosidade começa como ligado
    "solo": True  # Sensor de umidade de solo começa como ligado
}

# Rota para enviar dados dos sensores, mas só se o sensor estiver ligado
@api_bp.route('/api/enviar_dados', methods=['POST'])
def receber_dados():
    dados = request.json
    temperatura = dados.get('temperatura')
    umidade = dados.get('umidade')
    luminosidade = dados.get('luminosidade')
    umidadesolo = dados.get('umidadesolo')

    # Dicionário para armazenar os dados válidos
    dados_inserir = {}

    # Verificar se o sensor DHT está ligado e processar os dados
    if sensor_states["dht"]:
        if temperatura is None or umidade is None:
            return jsonify({"status": "erro", "mensagem": "Dados de temperatura ou umidade ausentes para sensor DHT"}), 400
        dados_inserir["temperatura"] = temperatura
        dados_inserir["umidade"] = umidade
    else:
        dados_inserir["temperatura"] = 0  # Usando 0 como valor padrão quando o sensor está desligado
        dados_inserir["umidade"] = 0

    # Verificar se o sensor de luminosidade está ligado e processar os dados
    if sensor_states["luz"]:
        if luminosidade is None:
            return jsonify({"status": "erro", "mensagem": "Dados de luminosidade ausentes para sensor de luminosidade"}), 400
        dados_inserir["luminosidade"] = luminosidade
    else:
        dados_inserir["luminosidade"] = 0  # Usando 0 como valor padrão quando o sensor está desligado

    # Verificar se o sensor de umidade de solo está ligado e processar os dados
    if sensor_states["solo"]:
        if umidadesolo is None:
            return jsonify({"status": "erro", "mensagem": "Dados de umidade de solo ausentes para sensor de solo"}), 400
        dados_inserir["umidadesolo"] = umidadesolo
    else:
        dados_inserir["umidadesolo"] = 0  # Usando 0 como valor padrão quando o sensor está desligado

    # Tentar inserir os dados no banco de dados
    try:
        novo_dado = DadosSensor(**dados_inserir)  # Passa o dicionário como parâmetros para o banco
        db.session.add(novo_dado)
        db.session.commit()
        return jsonify({"status": "sucesso", "dados_recebidos": dados_inserir}), 200
    except Exception as e:
        db.session.rollback()  # Rollback se houver erro
        return jsonify({"status": "erro", "mensagem": str(e)}), 500



# Rota para alternar o estado dos sensores
@api_bp.route('/toggle_sensor', methods=['POST'])
def toggle_sensor():
    sensor_type = request.json.get('sensor')
    
    if sensor_type in sensor_states:
        # Alterna o estado do sensor
        sensor_states[sensor_type] = not sensor_states[sensor_type]
        return jsonify({"success": True, "state": sensor_states[sensor_type]})
    else:
        return jsonify({"success": False, "error": "Sensor não encontrado"}), 400
    
# Rota para retornar o estado atual dos sensores
@api_bp.route('/estado_sensores', methods=['GET'])
def get_estado_sensores():
    return jsonify(sensor_states)

# Exportação dos dados em CSV
@api_bp.route('/exportar_csv', methods=['GET'])
def exportar_csv():
    dados = DadosSensor.query.order_by(DadosSensor.timestamp.asc()).all()

    if not dados:
        return jsonify({"status": "erro", "mensagem": "Nenhum dado disponível para exportação"}), 404

    colunas = ['ID', 'Temperatura (°C)', 'Umidade (%)', 'Luminosidade (%)', 'Umidade Solo (%)', 'Timestamp']
    csv_buffer = StringIO()
    escritor_csv = csv.writer(csv_buffer)
    escritor_csv.writerow(colunas)

    for dado in dados:
        escritor_csv.writerow([dado.id, dado.temperatura, dado.umidade, dado.luminosidade, dado.umidadesolo, dado.timestamp.strftime('%d/%m/%Y %H:%M:%S')])

    resposta_csv = Response(csv_buffer.getvalue(), mimetype='text/csv')
    resposta_csv.headers['Content-Disposition'] = 'attachment; filename=dados_sensores.csv'

    return resposta_csv
