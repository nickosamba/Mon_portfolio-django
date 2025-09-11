/*
===============================================
PORTFOLIO ANIMATIONS - COMPLEMENTARY JS
===============================================
JavaScript complémentaire pour éviter les conflits
===============================================
*/

// ============= NOUVELLES FONCTIONNALITÉS =============

// Fonction pour ajouter des effets personnalisés
function initCustomEffects() {
    // Éviter les conflits - seulement si les éléments n'existent pas déjà
    if (document.querySelector('.custom-hover-effect')) {
        document.querySelectorAll('.custom-hover-effect').forEach(element => {
            element.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px)';
            });

            element.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    }
}

// ============= OPTIMISATIONS =============

// Éviter les doubles initialisations
if (!window.portfolioCustomLoaded) {
    window.portfolioCustomLoaded = true;

    // Initialisation sécurisée
    document.addEventListener('DOMContentLoaded', function() {
        initCustomEffects();
        console.log('🎨 Custom portfolio effects loaded!');
    });
}

// Export des fonctions pour usage externe
window.CustomPortfolio = {
    initCustomEffects: initCustomEffects
};