import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path

# --- Configuration ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CSV_FILE_PATH = PROJECT_ROOT / 'corpus/metadata.csv'
METS_OUTPUT_PATH = PROJECT_ROOT / 'corpus/METS.xml'
IMAGE_BASE_PATH = 'images/'

def pretty_print_xml(elem):
    """Fonction utilitaire pour l'indentation du XML final."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

# Déclaration des namespaces pour la conformité du fichier METS.
ET.register_namespace('mets', "http://www.loc.gov/METS/")
ET.register_namespace('xlink', "http://www.w3.org/1999/xlink")
ET.register_namespace('dc', "http://purl.org/dc/elements/1.1/")

# Création de l'élément racine <mets:mets>
mets_root = ET.Element('{http://www.loc.gov/METS/}mets')


# 1. Création de l'en-tête METS (metsHdr)
metsHdr = ET.SubElement(mets_root, '{http://www.loc.gov/METS/}metsHdr', attrib={'CREATEDATE': '2025-07-01T22:30:00Z'})
agent = ET.SubElement(metsHdr, '{http://www.loc.gov/METS/}agent', attrib={'ROLE': 'CREATOR', 'TYPE': 'INDIVIDUAL'})
name = ET.SubElement(agent, '{http://www.loc.gov/METS/}name')
name.text = "Seïd Smatti" 


# 2. Initialisation des sections principales
dmdSec = ET.SubElement(mets_root, '{http://www.loc.gov/METS/}dmdSec')
fileSec = ET.SubElement(mets_root, '{http://www.loc.gov/METS/}fileSec')
fileGrp = ET.SubElement(fileSec, '{http://www.loc.gov/METS/}fileGrp', attrib={'USE': 'images'})
structMap = ET.SubElement(mets_root, '{http://www.loc.gov/METS/}structMap', attrib={'TYPE': 'PHYSICAL'})
main_div = ET.SubElement(structMap, '{http://www.loc.gov/METS/}div', attrib={'TYPE': 'sequence'})


# 3. Lecture du CSV et remplissage de la structure METS
print(f"Lecture du fichier : {CSV_FILE_PATH}...")
with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        image_id = row['id_image'].split('.')[0]

        # Création de l'entrée descriptive (dmdSec)
        mdWrap = ET.SubElement(dmdSec, '{http://www.loc.gov/METS/}mdWrap', attrib={'ID': f'dmd_{image_id}', 'MDTYPE': 'DC'})
        xmlData = ET.SubElement(mdWrap, '{http://www.loc.gov/METS/}xmlData')
        
        dc_title = ET.SubElement(xmlData, '{http://purl.org/dc/elements/1.1/}title')
        dc_title.text = row['titre']
        
        if row['createur']:
            dc_creator = ET.SubElement(xmlData, '{http://purl.org/dc/elements/1.1/}creator')
            dc_creator.text = row['createur']
        
        dc_date = ET.SubElement(xmlData, '{http://purl.org/dc/elements/1.1/}date')
        dc_date.text = row['date']

        dc_source = ET.SubElement(xmlData, '{http://purl.org/dc/elements/1.1/}source')
        dc_source.text = row['source_url']

        # Création de l'entrée pour le fichier (fileSec)
        file_element = ET.SubElement(fileGrp, '{http://www.loc.gov/METS/}file', attrib={'ID': f'file_{image_id}'})
        FLocat = ET.SubElement(file_element, '{http://www.loc.gov/METS/}FLocat', attrib={
            '{http://www.w3.org/1999/xlink}href': f"{IMAGE_BASE_PATH}{row['id_image']}",
            'LOCTYPE': 'URL'
        })
        
        # Création du lien structurel dans la structMap
        div = ET.SubElement(main_div, '{http://www.loc.gov/METS/}div', attrib={'ORDER': image_id})
        div.append(ET.Element('{http://www.loc.gov/METS/}mptr', attrib={'{http://www.w3.org/1999/xlink}href': f'#dmd_{image_id}'}))
        div.append(ET.Element('{http://www.loc.gov/METS/}fptr', attrib={'FILEID': f'file_{image_id}'}))

print("Génération de la structure METS terminée.")

# 4. Écriture du fichier XML final
with open(METS_OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(pretty_print_xml(mets_root))

print(f"Fichier METS sauvegardé : {METS_OUTPUT_PATH}")
