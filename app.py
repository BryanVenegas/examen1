from flask import Flask, jsonify, render_template_string, request, redirect, url_for

app = Flask(__name__)


dispositivos = {
    
}  

@app.route("/", methods=["GET"])
def raiz():
    return redirect(url_for("dispositivos_html"))

@app.route("/dispositivos_html", methods=["GET"])
def dispositivos_html():
    html = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Dispositivos</title>
</head>
<body>
    <h1>Listado de Dispositivos</h1>
    {% if dispositivos %}
        {% for d in dispositivos.values() %}
        <table border="1" cellpadding="5" cellspacing="0">
            <tr><td>id</td><td>{{ d["id"] }}</td></tr>
            <tr><td>nombre</td><td>{{ d["nombre"] }}</td></tr>
            <tr><td>descripcion</td><td>{{ d["descripcion"] }}</td></tr>
            <tr><td>ip</td><td>{{ d["ip"] }}</td></tr>
            <tr><td>mac</td><td>{{ d["mac"] }}</td></tr>
            <tr><td>ubicacion</td><td>{{ d["ubicacion"] }}</td></tr>
            <tr><td>tipo</td><td>{{ d["tipo"] }}</td></tr>
            <tr><td>otros</td><td>{{ d["otros"] }}</td></tr>
        </table>
        <br>
        {% endfor %}
    {% else %}
        <p>No hay dispositivos registrados.</p>
    {% endif %}
</body>
</html>
"""
    return render_template_string(html, dispositivos=dispositivos)

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
