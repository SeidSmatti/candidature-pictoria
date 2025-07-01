import json
import xml.etree.ElementTree as ET
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
METS_FILE_PATH = PROJECT_ROOT / 'corpus/METS.xml'
AI_RESULTS_PATH = PROJECT_ROOT / 'corpus/ai_results.json'
OUTPUT_DIR = PROJECT_ROOT / 'docs/manifests/'

BASE_URL = "https://https://github.com/SeidSmatti/candidature-pictoria"

# --- Création du dossier de sortie s'il n'existe pas ---
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Chargement des données sources ---
print("Étape 1: Chargement des données (METS et résultats IA)...")
try:
    with open(AI_RESULTS_PATH, 'r', encoding='utf-8') as f:
        ai_results = json.load(f)

    mets_tree = ET.parse(METS_FILE_PATH)
    mets_root = mets_tree.getroot()
    namespaces = {
        'mets': 'http://www.loc.gov/METS/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'xlink': 'http://www.w3.org/1999/xlink'
    }
    print("Données chargées avec succès.")
except FileNotFoundError as e:
    print(f"Erreur : Fichier non trouvé - {e}. Assurez-vous d'avoir exécuté les scripts précédents.")
    raise SystemExit

# --- Génération des manifestes ---
print("\nÉtape 2: Génération des manifestes IIIF (un par image)...")
manifest_count = 0
for div in mets_root.findall('.//mets:div[@ORDER]', namespaces):
    order_id = div.get('ORDER')
    image_filename = f"{order_id}.jpg"
    
    # Récupération des métadonnées depuis le fichier METS
    dmd_id_ref = div.find('.//mets:mptr', namespaces).get(f'{{{namespaces["xlink"]}}}href')
    dmd_id = dmd_id_ref.lstrip('#')
    dmd_element = mets_root.find(f".//mets:mdWrap[@ID='{dmd_id}']", namespaces)
    
    title = dmd_element.find('.//dc:title', namespaces).text
    creator_element = dmd_element.find('.//dc:creator', namespaces)
    date = dmd_element.find('.//dc:date', namespaces).text
    source = dmd_element.find('.//dc:source', namespaces).text

    # Structure de base du manifeste (IIIF Presentation API 3.0)
    manifest = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": f"{BASE_URL}docs/manifests/{order_id}.json",
        "type": "Manifest",
        "label": {"fr": [title]},
        "metadata": [
            {"label": {"fr": ["Titre"]}, "value": {"fr": [title]}},
            {"label": {"fr": ["Date"]}, "value": {"fr": [date]}},
            {"label": {"fr": ["Source"]}, "value": {"none": [f"<a href='{source}' target='_blank' rel='noopener noreferrer'>Voir la notice originale (BnF)</a>"]}}
        ],
        "items": [
            {
                "id": f"{BASE_URL}docs/manifests/{order_id}/canvas/1",
                "type": "Canvas",
                "height": 1200, # Valeurs arbitraires, peuvent être extraites de l'image
                "width": 1000,
                "items": [
                    {
                        "id": f"{BASE_URL}docs/manifests/{order_id}/canvas/1/page",
                        "type": "AnnotationPage",
                        "items": [
                            {
                                "id": f"{BASE_URL}docs/manifests/{order_id}/canvas/1/annotation",
                                "type": "Annotation",
                                "motivation": "painting",
                                "body": {
                                    "id": f"{BASE_URL}corpus/images/{image_filename}",
                                    "type": "Image",
                                    "format": "image/jpeg",
                                    "height": 1200,
                                    "width": 1000
                                },
                                "target": f"{BASE_URL}docs/manifests/{order_id}/canvas/1"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    # Ajout du créateur seulement s'il est présent
    if creator_element is not None and creator_element.text:
        manifest["metadata"].insert(1, {"label": {"fr": ["Créateur"]}, "value": {"fr": [creator_element.text]}})
        
    # Ajout des tags de l'IA dans les métadonnées
    if image_filename in ai_results and 'labels' in ai_results[image_filename]:
        ai_tags = ai_results[image_filename]['labels']
        manifest["metadata"].append({
            "label": {"fr": ["Analyse IA (tags)"]}, 
            "value": {"fr": [", ".join(ai_tags)]}
        })

    # Sauvegarde du manifeste individuel
    manifest_path = OUTPUT_DIR / f"{order_id}.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=4)
    manifest_count += 1

print(f"\nGénération terminée. {manifest_count} manifestes ont été créés dans le dossier : {OUTPUT_DIR}")
