from flask import Flask, request, jsonify, send_from_directory
import os
import requests

app = Flask(__name__, static_folder='.', static_url_path='')

# Clave API de OpenRouter
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")  # leer desde variable de entorno
#OPENROUTER_API_KEY = "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"

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_msg = data.get("message", "")

    system_prompt = "Actuá como un asistente experto en Sistemas de Información Geográfica (SIG) e Infraestructura de Datos Espaciales (IDE). Ayudá al usuario a entender cómo usar este visor web de mapas y tecnologías geoespaciales."

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "visor-sig",
            "Content-Type": "application/json"
        }

        body = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

        if response.status_code != 200:
            return jsonify({"reply": f"❌ Error HTTP {response.status_code}: {response.text}"})

        result = response.json()

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"]
            return jsonify({"reply": reply})
        elif "error" in result:
            return jsonify({"reply": f"❌ Error del modelo: {result['error']['message']}"})
        else:
            return jsonify({"reply": "⚠️ La respuesta no contiene datos válidos."})

    except Exception as e:
        return jsonify({"reply": f"Error al consultar el asistente: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)


