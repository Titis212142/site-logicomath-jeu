import os
import json
import time
import unicodedata
from collections import Counter
from PIL import Image
from sklearn.cluster import KMeans
import numpy as np
import cv2

# ✅ Corriger ici le chemin d'accès vers tes images
IMAGE_ROOT = "./static/images"
OUTPUT_JSON = os.path.join(IMAGE_ROOT, "images.json")

# Listes de référence
colors = ['rouge', 'bleu', 'vert', 'jaune', 'noir', 'blanc', 'gris', 'rose']
motifs = ['pois', 'rayures', 'unis', 'quadrillage', 'lignes']
contours = ['rouge', 'bleu', 'vert', 'gris']
formes = ['carre', 'triangle', 'losange', 'rond', 'etoile', 'pentagone']
animaux = ['chien', 'souris', 'hippo', 'ecureuil']

def normalize(text):
    """Nettoie accents et majuscules d'un texte"""
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').lower()

def detect_from_name(name, keywords):
    """Détection d'attributs dans le nom de fichier"""
    name_clean = normalize(name.replace("-", " ").replace("_", " ").replace(".", " "))
    for word in keywords:
        if normalize(word) in name_clean:
            return word
    return None

def get_dominant_color(image, k=4):
    """Retourne la couleur dominante d'une image"""
    image = image.resize((100, 100))
    data = np.array(image).reshape((-1, 3))
    model = KMeans(n_clusters=k, n_init='auto')
    labels = model.fit_predict(data)
    counts = Counter(labels)
    center_colors = model.cluster_centers_
    dominant_color = center_colors[counts.most_common(1)[0][0]]
    return tuple(int(c) for c in dominant_color)

def rgb_to_color_name(rgb):
    r, g, b = rgb
    if r > 200 and g < 100 and b < 100: return "rouge"
    elif r < 100 and g > 200 and b < 100: return "vert"
    elif r < 100 and g < 100 and b > 200: return "bleu"
    elif r > 200 and g > 200 and b < 100: return "jaune"
    elif r > 200 and g > 200 and b > 200: return "blanc"
    elif r < 80 and g < 80 and b < 80: return "noir"
    elif r > 200 and g < 180 and b > 180: return "rose"
    else: return "gris"

def detect_shape(image_path):
    image = cv2.imread(image_path)
    if image is None: return "inconnu"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
        sides = len(approx)
        if sides == 3: return "triangle"
        elif sides == 4: return "carre"
        elif sides == 5: return "pentagone"
        elif sides == 10: return "etoile"
        elif sides > 10: return "rond"
    return "inconnu"

def detect_motif(image_path):
    image = cv2.imread(image_path)
    if image is None: return "unis"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
    if lines is not None and len(lines) > 10:
        return "rayures"
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 150:
        return "pois"
    return "unis"

def detect_familles(couleur, motif, contour, forme, animal):
    familles = []
    if couleur: familles.append(f"famille des images {couleur}s")
    if motif: familles.append(f"famille des images à {motif}")
    if contour: familles.append(f"famille des images à contour {contour}")
    if forme: familles.append(f"famille des {forme}s")
    if animal: familles.append(f"famille des {animal}s")
    if couleur and forme and contour == "gris":
        familles.append("Couleur + forme (Attention tjs même contour gris)")
    if couleur and forme and motif and contour == "gris":
        familles.append("Couleur + forme  + Motif (Attention tjs même contour gris)")
    if couleur and forme and motif and contour:
        familles.append("Couleur + forme  + Motif + contour")
    return familles

# 📦 Lancement
start_time = time.time()
results = []

if not os.path.exists(IMAGE_ROOT):
    print(f"❌ Dossier introuvable : {IMAGE_ROOT}")
    exit()

for group_folder in sorted(os.listdir(IMAGE_ROOT)):
    group_path = os.path.join(IMAGE_ROOT, group_folder)
    if not os.path.isdir(group_path): continue

    for file in sorted(os.listdir(group_path)):
        if not file.lower().endswith(('.png', '.jpg', '.jpeg')): continue

        file_path = os.path.join(group_path, file)
        name = os.path.splitext(file)[0]
        print(f"🔍 Analyse : {file_path}")

        couleur = detect_from_name(name, colors)
        motif = detect_from_name(name, motifs)
        contour = detect_from_name(name, contours)
        forme = detect_from_name(name, formes)
        animal = detect_from_name(name, animaux)

        try:
            img = Image.open(file_path).convert("RGB")
            if couleur is None:
                couleur = rgb_to_color_name(get_dominant_color(img))
        except Exception as e:
            print(f"❌ Erreur couleur : {e}")
            couleur = couleur or "inconnu"

        if not forme:
            forme = detect_shape(file_path)
        if not motif or motif == "unis":
            motif = detect_motif(file_path)

        familles = detect_familles(couleur, motif, contour, forme, animal)

        results.append({
            "filename": f"{group_folder}/{file}",
            "groupe": group_folder,
            "couleur": couleur or "inconnu",
            "motif": motif or "unis",
            "contour": contour or "inconnu",
            "forme": forme or "inconnu",
            "animal": animal or "inconnu",
            "familles": familles
        })

# 💾 Enregistrement JSON
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n✅ Analyse terminée. Fichier généré : {OUTPUT_JSON}")
print(f"⏱️ Temps total : {int(time.time() - start_time)} sec")
