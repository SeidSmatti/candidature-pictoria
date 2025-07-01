import json
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
METS_FILE_PATH = PROJECT_ROOT / 'corpus/METS.xml'
AI_RESULTS_PATH = PROJECT_ROOT / 'corpus/ai_results.json'
IMAGE_DIR = PROJECT_ROOT / 'docs/images/' 
OUTPUT_DIR = PROJECT_ROOT / 'docs/manifests/'

# --- URL de base, qui est correcte ---
BASE_URL = "https://SeidSmatti.github.io/candidature-pictoria/"

# --- Création du dossier de sortie ---
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Chargement des données ---
print("Étape 1: Chargement des données sources...")
with open(AI_RESULTS_PATH, 'r', encoding='utf-8') as f:
    ai_results = json.load(f)
mets_tree = ET.parse(METS_FILE_PATH)
mets_root = mets_tree.getroot()
namespaces = {
    'mets': 'http://www.loc.gov/METS/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'xlink': 'http://www.w3.org/1999/xlink'
}
print("Données chargées.")

# --- Génération des manifestes ---
print("\nÉtape 2: Génération des manifestes IIIF...")
manifest_count = 0
for div in mets_root.findall('.//mets:div[@ORDER]', namespaces):
    order_id = div.get('ORDER')
    image_filename = f"{order_id}.jpg"
    image_path = IMAGE_DIR / image_filename

    # Récupération des dimensions réelles de l'image
    try:
        with Image.open(image_path) as img:
            width, height = img.size
    except FileNotFoundError:
        print(f"  /!\\ Image {image_filename} non trouvée, utilisation de dimensions par défaut.")
        width, height = 1000, 1200 # Fallback

    # Récupération des métadonnées depuis le METS
    dmd_id_ref = div.find('.//mets:mptr', namespaces).get(f'{{{namespaces["xlink"]}}}href')
    dmd_id = dmd_id_ref.lstrip('#')
    dmd_element = mets_root.find(f".//mets:mdWrap[@ID='{dmd_id}']", namespaces)
    
    title = dmd_element.find('.//dc:title', namespaces).text
    creator_element = dmd_element.find('.//dc:creator', namespaces)
    date = dmd_element.find('.//dc:date', namespaces).text
    source = dmd_element.find('.//dc:source', namespaces).text

    # Construction du manifeste avec les URLs CORRIGÉES
    manifest = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": f"{BASE_URL}manifests/{order_id}.json", # Correction: sans /docs/
        "type": "Manifest",
        "label": {"fr": [title]},
        "metadata": [
            {"label": {"fr": ["Titre"]}, "value": {"fr": [title]}},
            {"label": {"fr": ["Date"]}, "value": {"fr": [date]}},
            {"label": {"fr": ["Source"]}, "value": {"none": [f"<a href='{source}' target='_blank' rel='noopener noreferrer'>Voir la notice originale (BnF)</a>"]}}
        ],
        "items": [
            {
                "id": f"{BASE_URL}manifests/{order_id}/canvas/1", # Correction
                "type": "Canvas",
                "height": height,
                "width": width,
                "items": [
                    {
                        "id": f"{BASE_URL}manifests/{order_id}/canvas/1/page", # Correction
                        "type": "AnnotationPage",
                        "items": [
                            {
                                "id": f"{BASE_URL}manifests/{order_id}/canvas/1/annotation", # Correction
                                "type": "Annotation",
                                "motivation": "painting",
                                "body": {
                                    "id": f"{BASE_URL}images/{image_filename}", # Correction: chemin direct vers les images
                                    "type": "Image",
                                    "format": "image/jpeg",
                                    "height": height,
                                    "width": width
                                },
                                "target": f"{BASE_URL}manifests/{order_id}/canvas/1" # Correction
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    if creator_element is not None and creator_element.text:
        manifest["metadata"].insert(1, {"label": {"fr": ["Créateur"]}, "value": {"fr": [creator_element.text]}})
        
    if image_filename in ai_results and 'labels' in ai_results[image_filename]:
        ai_tags = ai_results[image_filename]['labels']
        manifest["metadata"].append({
            "label": {"fr": ["Analyse IA (tags)"]}, 
            "value": {"fr": [", ".join(ai_tags)]}
        })

    manifest_path = OUTPUT_DIR / f"{order_id}.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=4)
    manifest_count += 1

print(f"\nGénération terminée. {manifest_count} manifestes corrigés ont été créés.")
