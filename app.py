from flask import Flask, request, jsonify, render_template
from baixar_youtube import BaixarDoYoutube

app = Flask(__name__)

# Rota para renderizar a página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar o download
@app.route('/baixar', methods=['POST'])
def baixar_musica():
    try:
        data = request.json
        link = data.get('link')
        
        if not link:
            return jsonify({"error": "Link não fornecido"}), 400
        
        baixar = BaixarDoYoutube(print=print, diretorio="downloads")
        baixar.Baixar(link)

        return jsonify({"message": "Download concluído com sucesso!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
