# Projet : Pipeline de Traitement et d'Exploration pour Corpus Visuels

## Contexte et Objectifs

Ce projet a été réalisé comme illustration à l'offre d'Ingénieur d’études en production, traitement, analyse de données et enquêtes (UAR3225-KETFOU-001) pour le consortium PictorIA. Il vise à démontrer de manière concrète, avec un projet très simple, la maîtrise de la chaîne de traitement complète d'un corpus visuel numérique, de sa structuration initiale à sa valorisation via une plateforme d'exploration interactive.

L'objectif est de simuler un cas d'usage en Sciences Humaines et Sociales (SHS) : prendre un corpus d'images hétérogènes issues des collections de la BnF et le transformer en une ressource de connaissance structurée, interrogeable et interopérable.

## Le Pipeline de Traitement

Le projet s'articule autour d'un pipeline en quatre étapes séquentielles, où chaque sortie devient l'entrée de l'étape suivante :

1.  **Structuration (METS)** : Les métadonnées descriptives du corpus sont formalisées dans un fichier `METS.xml`, un standard robuste pour la description d'objets numériques complexes.
2.  **Enrichissement (IA)** : Un modèle d'IA (OpenAI CLIP) est utilisé en mode "Zero-Shot" pour analyser le contenu de chaque image et générer des mots-clés sémantiques pertinents, sans nécessiter de ré-entraînement.
3.  **Standardisation (IIIF)** : Les métadonnées descriptives et sémantiques sont agrégées pour générer un manifeste au format IIIF Presentation API 3.0 pour chaque image, garantissant une interopérabilité maximale.
4.  **Exploration (PoC)** : Une preuve de concept sous la forme d'une page web interactive est développée. Elle intègre la visionneuse Mirador 3 pour permettre la navigation, la comparaison et l'étude du corpus enrichi.

## Compétences Démontrées

Ce projet met en œuvre les compétences suivantes, requises par la fiche de poste :

-   **Programmation scientifique** : Utilisation de Python et de l'écosystème JupyterLab pour le traitement de données.
-   **Intelligence Artificielle** : Application d'un modèle d'apprentissage profond (CLIP) à l'analyse de corpus visuels.
-   **Standards patrimoniaux** : Structuration des données en XML-METS et génération de manifestes IIIF.
-   **Conception de protocoles** : Élaboration d'un pipeline de traitement complet, reproductible et documenté.
-   **Mise en ligne de plateformes** : Déploiement d'une preuve de concept fonctionnelle via GitHub Pages.
-   **Collaboration et reproductibilité** : Utilisation de Git/GitHub et fourniture d'un environnement documenté (`requirements.txt`).
-   **Rédaction et communication** : Documentation claire de la méthodologie et des résultats.

## Guide d'Installation et d'Utilisation

Pour reproduire ce projet en local :

1.  **Cloner le dépôt :**
    ```bash
    git clone [https://github.com/SeidSmatti/candidature-pictoria](https://github.com/SeidSmatti/candidature-pictoria)
    cd candidature-pictoria
    ```

2.  **Créer et activer un environnement virtuel :**
    ```bash
    python -m venv venv
    # Sur Mac/Linux
    source venv/bin/activate
    # Sur Windows
    # venv\Scripts\activate
    ```

3.  **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Exécuter le pipeline :**
    Les scripts doivent être exécutés dans l'ordre depuis la racine du projet.
    ```bash
    # 1. Générer le fichier METS.xml
    python scripts/01_build_mets.py

    # 2. Lancer l'analyse IA (via le notebook ou un script équivalent)
    # Ouvrir et exécuter notebooks/02_enrichment_ai.ipynb

    # 3. Générer les manifestes IIIF (penser à ajuster la BASE_URL pour un test local)
    python scripts/03_generate_iiif.py
    ```

5.  **Lancer le serveur de test local :**
    ```bash
    python -m http.server
    ```
    Puis, ouvrez votre navigateur à l'adresse `http://localhost:8000/docs/`.

## Structure du Projet
.
├── corpus/               # Données brutes et générées
│   ├── images/
│   ├── metadata.csv
│   ├── METS.xml
│   └── ai_results.json
├── docs/                 # Fichiers de la démo en ligne (GitHub Pages)
│   ├── images/           # Rajouté en double pour GH pages
│   ├── manifests/
│   ├── index.html
│   └── ...
├── notebooks/            # Notebooks d'expérimentation
│   └── 02_enrichment_ai.ipynb
├── scripts/              # Scripts d'automatisation du pipeline
│   ├── 01_build_mets.py
│   └── 03_generate_iiif.py
├── .gitignore            # Fichiers à ignorer par Git
├── README.md             # Ce fichier
└── requirements.txt      # Dépendances Python

## Pistes d'amélioration

-   **Extraction des dimensions** : Le script de génération IIIF pourrait être amélioré pour extraire dynamiquement les dimensions réelles de chaque image.
-   **Interface de recherche** : La preuve de concept pourrait être étendue avec une interface de recherche textuelle ou par facettes basées sur les tags IA.
-   **Annotation collaborative** : Les manifestes IIIF pourraient servir de base à une plateforme d'annotation collaborative, où les chercheurs pourraient corriger ou enrichir les tags générés par l'IA.

## Licence et Droits d'Auteur

Le code source de ce projet est distribué sous la licence **GNU General Public License v3.0**.

Les images utilisées dans ce corpus proviennent des collections en ligne de la **Bibliothèque nationale de France (BnF)**. Elles restent la propriété de la BnF et sont utilisées ici à des fins de démonstration technique uniquement, dans le cadre de ce projet. Toute réutilisation de ces images doit se conformer aux conditions d'utilisation spécifiées par la BnF.

