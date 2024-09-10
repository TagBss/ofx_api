from flask import Flask, request, jsonify
from conversor import process_ofx
import ofxparse

# Criar uma instância da aplicação Falsk
app = Flask(__name__)
app.secret_key = "5e83f80f0619a59a35a94d40186a9d2d" # Define a chave secreta para a aplicação Flask

# Rota padrão
@app.route('/')
def padrao():
    return "<h1>Api leitura OFX</h1>"

# Rota para upload do arquivo OFX
@app.route('/upload_ofx', methods=["POST"])
def upload_ofx():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400
    
    try:
        ofx_data = ofxparse.OfxParser.parse(file)
        result = process_ofx(ofx_data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Executa a aplicação Flask em modo de depuração
    app.run(debug=True, host='0.0.0.0')
