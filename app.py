from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from database import crear_tabla, guardar_mensaje, cargar_historial
import requests
import os

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODELO = "nvidia/nemotron-3-super-120b-a12b:free"
SYSTEM_PROMPT = "Eres un tutor de programación experto llamado Kai. Explicas todo simple y con ejemplos prácticos."

app = Flask(__name__)
crear_tabla()

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/preguntar", methods=["POST"])
def preguntar():
    datos = request.json
    mensaje = datos["mensaje"]
    guardar_mensaje("user", mensaje)

    historial = [{"role": "system", "content": SYSTEM_PROMPT}]
    historial += cargar_historial()

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
        print("RESPUESTA API:", response.json())
        respuesta = response.json()["choices"][0]["message"]["content"]
        guardar_mensaje("assistant", respuesta)
        return jsonify({"respuesta": respuesta})
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)