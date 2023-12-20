from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Ruta para obtener todos los registros del Excel en formato JSON
@app.route('/api/get_all_records', methods=['GET'])
def get_all_records():
    try:
        # Obtiene la ruta del archivo desde los parámetros de la URL
        file_path = request.args.get('file_path')

        if not file_path:
            return jsonify({'error': 'Debes proporcionar la ruta del archivo Excel en la URL.'})

        # Limpia la ruta de cualquier carácter de nueva línea o espacio en blanco
        file_path = file_path.strip()

        excel_file = pd.read_excel(file_path)
        records = excel_file.head(100).to_dict(orient='records')  # Limita la cantidad de registros

         # Respuesta exitosa con mensaje personalizado
        return jsonify({'success': True, 'message': '¡Datos obtenidos exitosamente!', 'data': records})

    except FileNotFoundError:
        return jsonify({'error': 'Archivo no encontrado.'}), 404

    except pd.errors.EmptyDataError:
        return jsonify({'error': 'El archivo está vacío.'}), 500

    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
# Nueva ruta para filtrar registros por ID
@app.route('/api/get_record_by_id/<int:record_id>', methods=['GET'])
def get_record_by_id(record_id):
    try:
        # Obtiene la ruta del archivo desde los parámetros de la URL
        file_path = request.args.get('file_path')

        if not file_path:
            return jsonify({'error': 'Debes proporcionar la ruta del archivo Excel en la URL.'})

        # Limpia la ruta de cualquier carácter de nueva línea o espacio en blanco
        file_path = file_path.strip()

        # Lee el archivo Excel
        excel_file = pd.read_excel(file_path)

        # Filtra el DataFrame por el índice específico
        filtered_record = excel_file.loc[[record_id]].to_dict(orient='records')

        return jsonify({'success': True, 'data': filtered_record})
    
    except FileNotFoundError:
        return jsonify({'error': 'Archivo no encontrado.'}), 404

    except pd.errors.EmptyDataError:
        return jsonify({'error': 'El archivo está vacío.'}), 500

    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500
    
# Nueva ruta para obtener un campo específico por ID
@app.route('/api/get_field_by_id/<int:record_id>/<field_name>', methods=['GET'])
def get_field_by_id(record_id, field_name):
    try:
        # Obtiene la ruta del archivo desde los parámetros de la URL
        file_path = request.args.get('file_path')

        if not file_path:
            return jsonify({'error': 'Debes proporcionar la ruta del archivo Excel en la URL.'})

        # Limpia la ruta de cualquier carácter de nueva línea o espacio en blanco
        file_path = file_path.strip()

        # Lee el archivo Excel
        excel_file = pd.read_excel(file_path)

        # Filtra el DataFrame por el índice específico y obtiene el campo deseado
        field_value = excel_file.loc[record_id, field_name]

        return jsonify({'success': True, 'data': {field_name: field_value}})

    except FileNotFoundError:
        return jsonify({'error': 'Archivo no encontrado.'}), 404

    except pd.errors.EmptyDataError:
        return jsonify({'error': 'El archivo está vacío.'}), 500

    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
