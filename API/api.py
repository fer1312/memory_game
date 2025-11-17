from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Lista de frutas (simulando las cartas)
frutas = [
    "sandia", "platano", "guayaba", "tomate",
    "manzana", "uva", "naranja", "pera"
]

# Endpoint para crear tablero
@app.route("/crear_tablero", methods=["GET"])
def crear_tablero():
    cartas = frutas * 2  # duplicar para pares
    random.shuffle(cartas)
    return jsonify({"tablero": cartas})

# Endpoint para validar par
@app.route("/validar_par", methods=["POST"])
def validar_par():
    data = request.json
    carta1 = data.get("carta1")
    carta2 = data.get("carta2")
    es_par = carta1 == carta2
    return jsonify({"es_par": es_par})

# Endpoint para reiniciar juego
@app.route("/reiniciar", methods=["GET"])
def reiniciar():
    return jsonify({"mensaje": "Juego reiniciado"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

