# -*- coding: utf-8 -*-
"""
Configuration des gouvernorats tunisiens et leurs adresses principales
"""

# Les 24 gouvernorats de Tunisie
GOVERNORATE_CHOICES = [
    ('tunis', 'Tunis'),
    ('ariana', 'Ariana'),
    ('ben_arous', 'Ben Arous'),
    ('manouba', 'Manouba'),
    ('nabeul', 'Nabeul'),
    ('zaghouan', 'Zaghouan'),
    ('bizerte', 'Bizerte'),
    ('beja', 'Béja'),
    ('jendouba', 'Jendouba'),
    ('kef', 'Le Kef'),
    ('siliana', 'Siliana'),
    ('kairouan', 'Kairouan'),
    ('kasserine', 'Kasserine'),
    ('sidi_bouzid', 'Sidi Bouzid'),
    ('sousse', 'Sousse'),
    ('monastir', 'Monastir'),
    ('mahdia', 'Mahdia'),
    ('sfax', 'Sfax'),
    ('gabes', 'Gabès'),
    ('medenine', 'Médenine'),
    ('tataouine', 'Tataouine'),
    ('gafsa', 'Gafsa'),
    ('tozeur', 'Tozeur'),
    ('kebili', 'Kébili'),
]

# Adresses principales pour chaque gouvernorat
GOVERNORATE_ADDRESSES = {
    'tunis': [
        'Station de métro Barcelone',
        'Gare routière Bab Alioua',
        'Avenue Habib Bourguiba',
        'Gare TGM Tunis Marine',
        'Place Pasteur',
        'Jardin Thameur',
        'Bab El Khadhra',
        'Montplaisir',
        'El Menzah',
        'Centre Urbain Nord',
    ],
    'ariana': [
        'Centre ville Ariana',
        'Cité Ettadhamen',
        'Borj Louzir',
        'Mnihla Centre',
        'Sidi Thabet',
        'Raoued',
        'Soukra Centre',
        'Ariana Essoghra',
    ],
    'ben_arous': [
        'Centre ville Ben Arous',
        'Ezzahra',
        'Hammam Lif',
        'Hammam Chott',
        'Mégrine',
        'Mohamedia',
        'Radès Centre',
        'Fouchana',
        'Medina Jedida',
    ],
    'manouba': [
        'Centre ville Manouba',
        'Douar Hicher',
        'Oued Ellil',
        'Mornaguia',
        'Tebourba',
        'Djedeida',
        'Borj El Amri',
    ],
    'nabeul': [
        'Centre ville Nabeul',
        'Gare routière Nabeul',
        'Hammamet Centre',
        'Hammamet Yasmine',
        'Kelibia',
        'Korba',
        'Menzel Temime',
        'Grombalia',
        'Dar Chaabane',
        'Beni Khalled',
    ],
    'zaghouan': [
        'Centre ville Zaghouan',
        'El Fahs',
        'Bir Mchergua',
        'Zriba',
    ],
    'bizerte': [
        'Centre ville Bizerte',
        'Gare routière Bizerte',
        'Menzel Bourguiba',
        'Mateur',
        'Ras Jebel',
        'Sejnane',
        'Menzel Jemil',
        'Joumine',
    ],
    'beja': [
        'Centre ville Béja',
        'Gare routière Béja',
        'Testour',
        'Medjez El Bab',
        'Nefza',
        'Teboursouk',
    ],
    'jendouba': [
        'Centre ville Jendouba',
        'Gare routière Jendouba',
        'Tabarka',
        'Ain Draham',
        'Fernana',
        'Ghardimaou',
        'Bou Salem',
    ],
    'kef': [
        'Centre ville Le Kef',
        'Gare routière Le Kef',
        'Dahmani',
        'Tajerouine',
        'Sers',
    ],
    'siliana': [
        'Centre ville Siliana',
        'Gare routière Siliana',
        'Makthar',
        'Bou Arada',
        'Bargou',
        'El Krib',
    ],
    'kairouan': [
        'Centre ville Kairouan',
        'Gare routière Kairouan',
        'Grande Mosquée',
        'Haffouz',
        'Sbikha',
        'Nasrallah',
        'Chebika',
    ],
    'kasserine': [
        'Centre ville Kasserine',
        'Gare routière Kasserine',
        'Sbeitla',
        'Feriana',
        'Thala',
        'Foussana',
    ],
    'sidi_bouzid': [
        'Centre ville Sidi Bouzid',
        'Gare routière Sidi Bouzid',
        'Regueb',
        'Jilma',
        'Meknassy',
        'Menzel Bouzaiene',
    ],
    'sousse': [
        'Centre ville Sousse',
        'Gare routière Sousse',
        'Port El Kantaoui',
        'Hammam Sousse',
        'M\'saken',
        'Kalaa Kebira',
        'Akouda',
        'Sahloul',
    ],
    'monastir': [
        'Centre ville Monastir',
        'Gare routière Monastir',
        'Aéroport Monastir',
        'Moknine',
        'Jemmal',
        'Ksar Hellal',
        'Teboulba',
        'Sahline',
        'Bembla',
    ],
    'mahdia': [
        'Centre ville Mahdia',
        'Gare routière Mahdia',
        'Ksour Essaf',
        'Chebba',
        'El Jem',
        'Bou Merdes',
    ],
    'sfax': [
        'Centre ville Sfax',
        'Gare routière Sfax',
        'Avenue Habib Bourguiba Sfax',
        'Sfax El Jadida',
        'Sakiet Ezzit',
        'Sakiet Eddaier',
        'Gremda',
        'El Ain',
        'Agareb',
    ],
    'gabes': [
        'Centre ville Gabès',
        'Gare routière Gabès',
        'Mareth',
        'Matmata',
        'El Hamma',
        'Menzel El Habib',
    ],
    'medenine': [
        'Centre ville Médenine',
        'Gare routière Médenine',
        'Zarzis',
        'Djerba Houmt Souk',
        'Djerba Midoun',
        'Ben Guerdane',
    ],
    'tataouine': [
        'Centre ville Tataouine',
        'Gare routière Tataouine',
        'Ghomrassen',
        'Remada',
        'Chenini',
    ],
    'gafsa': [
        'Centre ville Gafsa',
        'Gare routière Gafsa',
        'Metlaoui',
        'Redeyef',
        'Mdhilla',
        'El Ksar',
    ],
    'tozeur': [
        'Centre ville Tozeur',
        'Gare routière Tozeur',
        'Nefta',
        'Degache',
        'Hazoua',
    ],
    'kebili': [
        'Centre ville Kébili',
        'Gare routière Kébili',
        'Douz',
        'Souk Lahad',
    ],
}

def get_addresses_for_governorate(governorate_code):
    """
    Retourne la liste des adresses pour un gouvernorat donné.
    
    Args:
        governorate_code: Le code du gouvernorat (ex: 'tunis', 'sfax')
    
    Returns:
        Liste des adresses ou liste vide si gouvernorat non trouvé
    """
    return GOVERNORATE_ADDRESSES.get(governorate_code, [])

def get_address_choices_for_governorate(governorate_code):
    """
    Retourne les choix d'adresses formatés pour un formulaire Django.
    
    Args:
        governorate_code: Le code du gouvernorat
    
    Returns:
        Liste de tuples (valeur, label) pour les choix Django
    """
    addresses = get_addresses_for_governorate(governorate_code)
    return [(addr, addr) for addr in addresses]
