from flask import Flask, jsonify, request
import pandas as pd
import os  # Agrega la importación de la biblioteca os

app = Flask(__name__)

# Obtiene la ruta del archivo desde los parámetros de la URL o la variable de entorno
file_path = os.environ.get('EXCEL_FILE_PATH')

# Resto del código ...

# Ruta para obtener todos los registros del Excel en formato JSON
@app.route('/api/get_all_records', methods=['GET'])
def get_all_records():
    try:
        if not file_path:
            return jsonify({'error': 'Debes proporcionar la ruta del archivo Excel en la URL o como variable de entorno.'})

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

# Resto del código ...

if __name__ == '__main__':
    app.run(debug=True)
