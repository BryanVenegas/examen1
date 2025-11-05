from flask import Flask, jsonify, render_template_string, request, redirect, url_for

app = Flask(__name__)


dispositivos = {
    
}  

@app.route("/dispositivos", methods=["POST"])
def crear_dispositivo():
    data = request.json or {}

    campos = ["id", "nombre", "descripcion", "ip", "mac", "ubicacion", "tipo"]
    for c in campos:
        if c not in data:
            return jsonify({"error": f"falta el campo {c}"}), 400

    if data["id"] in dispositivos:
        return jsonify({"error": "ya existe un dispositivo con ese id"}), 409

    data["otros"] = data.get("otros", "")

    dispositivos[data["id"]] = data
    return jsonify(data), 201

@app.route("/dispositivos/<id>", methods=["PUT"])
def modificar_dispositivo(id):
    if id not in dispositivos:
        return jsonify({"error": "no existe el dispositivo"}), 404

    data = request.json or {}

    for k in ["nombre", "descripcion", "ip", "mac", "ubicacion", "tipo", "otros"]:
        if k in data:
            dispositivos[id][k] = data[k]

    return jsonify(dispositivos[id]), 200

@app.route("/dispositivos", methods=["GET"])
def listar_json():
    return jsonify(list(dispositivos.values())), 200

if __name__ == "__main__":
    app.run(debug=True)
