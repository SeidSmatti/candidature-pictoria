// Configuration de Mirador
const miradorConfig = {
    // ID de la div HTML où Mirador doit s'afficher
    id: 'mirador-viewer',

    // Configuration des fenêtres et des vues
    windows: [], // On commence avec aucune fenêtre ouverte
    workspace: {
        type: 'mosaic', // Permet d'afficher plusieurs fenêtres
    },
    window: {
        // Options par défaut pour chaque nouvelle fenêtre
        defaultSideBarPanel: 'info',
        sideBarOpen: true,
    },
    // Configuration du catalogue de ressources (nos manifestes)
    catalog: []
};

// Fonction pour charger la liste des manifestes et initialiser Mirador
async function initializeViewer() {
    // On génère la liste des chemins vers nos manifestes
    const manifestUrls = [];
    for (let i = 1; i <= 10; i++) {
        const manifestId = String(i).padStart(2, '0'); // Formate les nombres en "01", "02", etc.
        manifestUrls.push({ manifestId: `manifests/${manifestId}.json` });
    }

    // On ajoute nos manifestes au catalogue de Mirador
    miradorConfig.catalog = manifestUrls;

    // On choisit d'ouvrir la première image par défaut au lancement
    if (manifestUrls.length > 0) {
        miradorConfig.windows.push({
            manifestId: manifestUrls[0].manifestId,
        });
    }

    // Initialisation de Mirador avec notre configuration
    Mirador.viewer(miradorConfig);
}

// Lancement de l'initialisation
initializeViewer();
