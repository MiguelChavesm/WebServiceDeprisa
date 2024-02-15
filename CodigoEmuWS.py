from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth

app = Flask(__name__)
basic_auth = BasicAuth(app)

# Configuración de usuarios y contraseñas
app.config['BASIC_AUTH_USERNAME'] = '101'
app.config['BASIC_AUTH_PASSWORD'] = 'CubiScan*123'
SERVICE_KEY = 'tu_service_key'


@app.route('/endpoint', methods=['POST'])
@basic_auth.required
def emulate_web_service():
    try:
        # Verificar la clave de servicio desde la URL
        service_key_from_url = request.args.get('Service-Key')

        # Si no está en la URL, intentar obtenerla de los encabezados
        if service_key_from_url is None:
            service_key_from_headers = request.headers.get('Service-Key')
            if service_key_from_headers != SERVICE_KEY:
                return jsonify({'error': 'Clave de servicio inválida'}), 401
        else:
            if service_key_from_url != SERVICE_KEY:
                return jsonify({'error': 'Clave de servicio inválida'}), 401

        data = request.json
        response_data = {'message': 'Solicitud recibida Jefferson', 'data': data}
        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
