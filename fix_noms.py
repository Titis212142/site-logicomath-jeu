import os
import json

# Dossier contenant les images
IMAGE_ROOT = os.path.join("static", "images")
JSON_PATH = os.path.join(IMAGE_ROOT, "images.json")

# Mapping des noms à remplacer
REPLACEMENTS = {
    "numéros 1 à 5": "numeros_1_a_5",
    "numéros 6 à 10": "numeros_6_a_10",
    "numéros 11 à 20": "numeros_11_a_20",
    "numéros 21 à 30": "numeros_21_a_30",
    "numéros 31 à 45": "numeros_31_a_45",
    "numéros 46 à 60": "numeros_46_a_60",
}

# 1. Renommer les dossiers
for old_name, new_name in REPLACEMENTS.items():
    old_path = os.path.join(IMAGE_ROOT, old_name)
    new_path = os.path.join(IMAGE_ROOT, new_name)
    if os.path.exists(old_path) and not os.path.exists(new_path):
        os.rename(old_path, new_path)
        print(f"📁 Dossier renommé : {old_name} → {new_name}")
    elif not os.path.exists(old_path):
        print(f"⚠️ Dossier introuvable : {old_name}")
    else:
        print(f"✅ Dossier déjà renommé : {new_name}")

# 2. Corriger les chemins dans images.json
if os.path.exists(JSON_PATH):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        for old, new in REPLACEMENTS.items():
            if old in item["filename"]:
                item["filename"] = item["filename"].replace(old, new)
                item["groupe"] = item["groupe"].replace(old, new)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✅ Chemins mis à jour dans images.json")
else:
    print("❌ Le fichier images.json est introuvable !")
