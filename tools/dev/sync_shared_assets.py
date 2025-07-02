import os
import shutil

SHARED_DIR = 'assets/icons/shared'
TARGET_BASES = [
    'apps/web_admin/assets/icons',
]

def sync_shared_assets():
    if not os.path.exists(SHARED_DIR):
        print("Erreur : dossier partagé introuvable.")
        return

    for target_base in TARGET_BASES:
        for root, dirs, files in os.walk(SHARED_DIR):
            rel_path = os.path.relpath(root, SHARED_DIR)  # chemin relatif à partir de 'shared'
            target_dir = os.path.join(target_base, rel_path)
            os.makedirs(target_dir, exist_ok=True)

            for file in files:
                src = os.path.join(root, file)
                dst = os.path.join(target_dir, file)
                shutil.copy2(src, dst)
                print(f"✅ Copié : {src} → {dst}")

SHARED_THEME_DIR = 'assets/theme/shared'
THEME_TARGETS = [
    'apps/web_admin/lib/theme',
]

def sync_shared_theme():
    if not os.path.exists(SHARED_THEME_DIR):
        print("Erreur : thème partagé introuvable.")
        return

    for target in THEME_TARGETS:
        os.makedirs(target, exist_ok=True)
        for file in os.listdir(SHARED_THEME_DIR):
            if file.endswith('.dart'):
                src = os.path.join(SHARED_THEME_DIR, file)
                dst = os.path.join(target, file)
                shutil.copy2(src, dst)
                print(f"🎨 Copié : {src} → {dst}")                

if __name__ == '__main__':
    sync_shared_assets()
    sync_shared_theme()
    