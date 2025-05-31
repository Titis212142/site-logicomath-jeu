import os
import unicodedata

def normalize_filename(name):
    # Supprimer les accents
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    # Remplacer les espaces et caractères spéciaux
    name = name.lower().replace(" ", "_").replace("-", "_")
    # Supprimer les caractères indésirables
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789._"
    return ''.join(c for c in name if c in allowed)

def rename_images_in_directory(root_folder):
    count = 0
    for folder, subfolders, files in os.walk(root_folder):
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext.lower() not in [".jpg", ".jpeg", ".png"]:
                continue

            new_name = normalize_filename(name) + ext.lower()
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_name)

            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"✅ {filename} → {new_name}")
                count += 1

    print(f"\n🔁 {count} image(s) renommée(s) au total.")

# 👉 À personnaliser selon ton projet :
if __name__ == "__main__":
    dossier_images = "./static/images/pre_animaux"  # chemin à adapter si besoin
    rename_images_in_directory(dossier_images)
