/**
 * Gestion dynamique des adresses basées sur le gouvernorat sélectionné
 * TAWSILA24 - Plateforme de covoiturage tunisienne
 */

document.addEventListener('DOMContentLoaded', function() {
    // Configuration des paires gouvernorat-adresse pour les formulaires
    const configs = [
        { cityId: 'id_departure_city', addressId: 'id_departure_address' },
        { cityId: 'id_arrival_city', addressId: 'id_arrival_address' },
        { cityId: 'id_recurring_departure_city', addressId: 'id_recurring_departure_address' },
        { cityId: 'id_recurring_arrival_city', addressId: 'id_recurring_arrival_address' }
    ];

    configs.forEach(config => {
        const citySelect = document.getElementById(config.cityId);
        const addressSelect = document.getElementById(config.addressId);

        if (citySelect && addressSelect) {
            // Charger les adresses lors du changement de gouvernorat
            citySelect.addEventListener('change', function() {
                const governorateCode = this.value;
                loadAddresses(governorateCode, addressSelect);
            });

            // Charger les adresses initiales si un gouvernorat est déjà sélectionné
            if (citySelect.value) {
                loadAddresses(citySelect.value, addressSelect);
            }
        }
    });
});

/**
 * Charge les adresses pour un gouvernorat donné
 * @param {string} governorateCode - Code du gouvernorat
 * @param {HTMLSelectElement} addressSelect - Élément select pour les adresses
 */
function loadAddresses(governorateCode, addressSelect) {
    if (!governorateCode) {
        // Réinitialiser la liste des adresses
        addressSelect.innerHTML = '<option value="">Sélectionnez d\'abord un gouvernorat</option>';
        return;
    }

    // Afficher un message de chargement
    addressSelect.innerHTML = '<option value="">Chargement...</option>';
    addressSelect.disabled = true;

    // Récupérer les adresses depuis l'API
    const url = `/trips/api/addresses/${governorateCode}/`;
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors du chargement des adresses');
            }
            return response.json();
        })
        .then(data => {
            // Réinitialiser la liste
            addressSelect.innerHTML = '';
            
            // Ajouter une option par défaut
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Sélectionnez une adresse';
            addressSelect.appendChild(defaultOption);

            // Ajouter les adresses
            if (data.addresses && data.addresses.length > 0) {
                data.addresses.forEach(address => {
                    const option = document.createElement('option');
                    option.value = address;
                    option.textContent = address;
                    addressSelect.appendChild(option);
                });
                
                // Ajouter une option "Autre"
                const otherOption = document.createElement('option');
                otherOption.value = 'autre';
                otherOption.textContent = 'Autre (spécifier)';
                addressSelect.appendChild(otherOption);
            } else {
                addressSelect.innerHTML = '<option value="">Aucune adresse disponible</option>';
            }

            addressSelect.disabled = false;
        })
        .catch(error => {
            console.error('Erreur:', error);
            addressSelect.innerHTML = '<option value="">Erreur de chargement</option>';
            addressSelect.disabled = false;
        });
}

/**
 * Permet la saisie libre d'adresse si "Autre" est sélectionné
 */
document.addEventListener('DOMContentLoaded', function() {
    const addressSelects = [
        'id_departure_address',
        'id_arrival_address',
        'id_recurring_departure_address',
        'id_recurring_arrival_address'
    ];

    addressSelects.forEach(selectId => {
        const select = document.getElementById(selectId);
        if (select) {
            select.addEventListener('change', function() {
                if (this.value === 'autre') {
                    // Convertir le select en input pour saisie libre
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.id = this.id;
                    input.name = this.name;
                    input.className = this.className;
                    input.placeholder = 'Entrez l\'adresse complète';
                    input.required = this.required;
                    
                    // Remplacer le select par l'input
                    this.parentNode.replaceChild(input, this);
                    input.focus();
                }
            });
        }
    });
});
