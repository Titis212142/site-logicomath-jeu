from flask import Flask, render_template, jsonify, request
import os
import json

app = Flask(__name__, static_folder="static", template_folder="templates")

ELEVE_FILE = os.path.join("data", "eleves.json")
IMAGE_JSON = os.path.join("static", "images", "images.json")

# 🔁 Charger les élèves
def load_eleves():
    if not os.path.exists(ELEVE_FILE):
        return []
    with open(ELEVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# 💾 Enregistrer les élèves
def save_eleves(data):
    with open(ELEVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# 🏠 Page d'accueil
@app.route('/')
def index():
    return render_template("index.html")

# 🎮 Catégories
@app.route('/categories')
def categories():
    return render_template("choix_categories.html")

@app.route('/classification')
def classification():
    return render_template("classification.html")

# 🎯 Jeux (pages)
@app.route('/jeu1')
def jeu1():
    return render_template("jeu1.html")

@app.route('/jeu2')
def jeu2():
    return render_template("jeu2.html")

@app.route('/jeu3')
def jeu3():
    return render_template("jeu3.html")

@app.route('/jeu4')
def jeu4():
    return render_template("jeu4.html")

@app.route('/jeu5')
def jeu5():
    return render_template("jeu5.html")

@app.route('/jeu6')
def jeu6():
    return render_template("jeu6.html")

# 📦 JSON des images
@app.route('/images/images.json')
def get_images_json():
    with open(IMAGE_JSON, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

# 📚 API élèves
@app.route('/api/eleves', methods=["GET"])
def api_get_eleves():
    return jsonify(load_eleves())

@app.route('/api/eleves/add', methods=["POST"])
def api_add_eleve():
    data = request.json
    eleves = load_eleves()
    eleves.append({
        "name": data.get("name"),
        "progression": {}
    })
    save_eleves(eleves)
    return jsonify({"status": "ok", "message": "Élève ajouté"})

@app.route('/api/eleves/update', methods=["POST"])
def api_update_progress():
    data = request.json
    index = data.get("index")
    jeu = data.get("jeu")
    success = data.get("success")

    eleves = load_eleves()
    if 0 <= index < len(eleves):
        eleves[index]["progression"][jeu] = success
        save_eleves(eleves)
        return jsonify({"status": "ok", "message": "Progression mise à jour"})

    return jsonify({"status": "error", "message": "Élève introuvable"}), 400

# ▶️ Lancer l'application
if __name__ == '__main__':
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(ELEVE_FILE):
        with open(ELEVE_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)
    app.run(debug=True)
