from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
import os
from flask import Flask, request, jsonify, render_template

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODELO = "inclusionai/ling-2.6-1t:free"

app = Flask(__name__)
historial = [{"role": "system", "content": "Eres un tutor de programación llamado Kai. Respondes de forma simple y práctica."}]

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/preguntar", methods=["POST"])
def preguntar():
    datos = request.json
    mensaje = datos["mensaje"]
    
    historial.append({"role": "user", "content": mensaje})
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODELO,
                "messages": historial
            }
        )
        respuesta = response.json()["choices"][0]["message"]["content"]
        historial.append({"role": "assistant", "content": respuesta})
        return jsonify({"respuesta": respuesta})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)