# BreakCesar -  Déchiffrement automatique d'un message chiffré par la méthode de César
# Auteurs : Océanely TRUONG & Yaniv DOUIEB
# WebApp : https://breakcesar.streamlit.app/

# Importation des modules
import streamlit as st
from st_cytoscape import cytoscape
import unidecode

# Dictionnaire des lettres les plus fréquentes dans les 13 langues prisent en charge par le programme
# Source : https://fr.wikipedia.org/wiki/Fr%C3%A9quence_d%27apparition_des_lettres#Dans_d'autres_langues
frequence_lettres = {
    "Anglais": "e",
    "Français": "e",
    "Allemand": "e",
    "Espagnol": "e",
    "Portugais": "a",
    "Italien": "e",
    "Turc": "a",
    "Suédois": "e",
    "Polonais": "a",
    "Danois": "e",
    "Finnois": "a",
    "Tchèque": "a",
    "Lituanien": "i"
}

# Fonctions
def analyse_frequence(texte):
    """Analyse de la fréquence des lettres dans un texte
    :param texte: Texte à analyser <str>
    :return: Dictionnaire de la fréquence des lettres <dict>
    """
    
    # Initialisation du dictionnaire
    frequence = {}
    
    # Pour chaque lettre du texte
    for lettre in texte:
        
        # Si la lettre est une lettre de l'alphabet
        if lettre.isalpha():
            
            # Si la lettre est déjà dans le dictionnaire
            if lettre in frequence:
                
                # On incrémente la valeur de la lettre
                frequence[lettre] += 1
            
            # Sinon
            else:
                
                # On ajoute la lettre au dictionnaire
                frequence[lettre] = 1
    
    # On retourne le dictionnaire
    return frequence

def caractere_plus_frequent(frequence):
    """Renvoie le caractère le plus fréquent dans un dictionnaire de fréquence
    :param frequence: Dictionnaire de la fréquence des lettres <dict>
    :return: Caractère le plus fréquent <str>
    """
    
    # Initialisation des variables
    max_lettre = ""
    max_frequence = 0
    
    # Pour chaque lettre du dictionnaire
    for lettre in frequence:
        
        # Si la fréquence de la lettre est supérieure à la fréquence maximale
        if frequence[lettre] > max_frequence:
            
            # On met à jour la fréquence maximale et la lettre associée
            max_frequence = frequence[lettre]
            max_lettre = lettre
    
    # On retourne la lettre la plus fréquente
    return max_lettre

def calculer_decalage(lettre_langue, lettre_texte):
    """Calcule le décalage entre deux lettres
    :param lettre_langue: Lettre la plus fréquente dans la langue <str>
    :param lettre_texte: Lettre la plus fréquente dans le texte <str>
    :return: Décalage entre les deux lettres <int>
    """
    
    # On calcule le décalage entre les deux lettres
    decalage = ord(lettre_texte) - ord(lettre_langue)
    
    # On retourne le décalage
    return decalage

def dechiffrement_cesar(texte, langue):
    """Déchiffre un texte chiffré par la méthode de César
    :param texte: Texte à déchiffrer <str>
    :param langue: Langue du texte <str>
    :return: Texte déchiffré <str>
    """
    
    # Initialisation des variables
    texte_dechiffre = ""
    frequence = analyse_frequence(texte)
    lettre_langue = frequence_lettres[langue]
    lettre_texte = caractere_plus_frequent(frequence)
    decalage = calculer_decalage(lettre_langue, lettre_texte)
    
    # Pour chaque lettre du texte
    for lettre in texte:
        # Mettre la lettre en minuscule
        lettre_minuscule = lettre.lower()

        # Si la lettre est une lettre de l'alphabet (a-z)
        if lettre_minuscule in "abcdefghijklmnopqrstuvwxyz":
            
            # On calcule la position de la lettre dans l'alphabet
            position = ord(lettre_minuscule) - ord("a")

            # On calcule la nouvelle position de la lettre
            nouvelle_position = (position - decalage) % 26

            # On calcule la nouvelle lettre
            nouvelle_lettre = chr(nouvelle_position + ord("a"))

            # Si la lettre était en majuscule
            if lettre.isupper():
                
                # On met la nouvelle lettre en majuscule
                nouvelle_lettre = nouvelle_lettre.upper()
            
            # On ajoute la nouvelle lettre au texte déchiffré
            texte_dechiffre += nouvelle_lettre
        
        # Sinon
        else:
            
            # On ajoute la lettre au texte déchiffré
            texte_dechiffre += lettre
    
    # On retourne le texte déchiffré
    return texte_dechiffre

def initialisation_session():
    """Initialise les variables de session de Streamlit
    :param: None
    :return: None
    """

    if "texte_chiffre" not in st.session_state:
        st.session_state.texte_chiffre = ""

    if "texte_dechiffre" not in st.session_state:
        st.session_state.texte_dechiffre = ""

    if "langue" not in st.session_state:
        st.session_state.langue = ""
    
    if "decalage" not in st.session_state:
        st.session_state.decalage = 0

    if "id_fichier" not in st.session_state:
        st.session_state.id_fichier = 0

    if "en_cours_execution" not in st.session_state:
        st.session_state.en_cours_execution = False

# On essaie d'exécuter le programme
try:
    # Interface graphique (WebApp)

    # Configuration de la WebApp et initialisation de la session
    st.set_page_config(
        page_title="BreakCesar",
        page_icon=":key:",
    )
    initialisation_session()

    # Titre et Description
    st.title(":key: BreakCesar")
    st.subheader("Déchiffrement automatique d'un message chiffré par la méthode de César")

    # Création de la sidebar pour la configuration
    st.sidebar.title(":gear: Configuration")

    # Choix de différentes préconfigurations
    st.sidebar.subheader("Préconfiguration")
    preconfiguration_FR = st.sidebar.button("**Français** - Clé: 7")
    preconfiguration_FI = st.sidebar.button("**Finnois** - Clé: 39")
    preconfiguration_LT = st.sidebar.button("**Lituanien** - Clé: 12")
    preconfiguration_EN = st.sidebar.button("**Anglais** - Clé: 1")
    preconfiguration_FRasPL = st.sidebar.button("**Français** déchiffré en **Polonais** - Clé: 7")

    # Importation d'un fichier texte chiffré personnalisé
    st.sidebar.subheader("Fichier personnalisé")
    langue = st.sidebar.selectbox("Langue du texte", frequence_lettres.keys())
    fichier = st.sidebar.file_uploader("Sélectionnez un fichier texte chiffré (.txt)", type=["txt"], key=st.session_state.id_fichier)

    # Si une des préconfigurations est sélectionnée ou si un fichier est importé
    if preconfiguration_FR or preconfiguration_FI or preconfiguration_LT or preconfiguration_EN or preconfiguration_FRasPL or fichier or st.session_state.en_cours_execution:

        # Si c'est une préconfiguration
        if preconfiguration_FR or preconfiguration_FI or preconfiguration_LT or preconfiguration_EN or preconfiguration_FRasPL:

            # On supprime le fichier importé en changeant la valeur de l'IDFalse
            st.session_state.id_fichier += 1

            # On met la variable d'exécution à True
            st.session_state.en_cours_execution = True


        if preconfiguration_FR:

            # On ajoute le texte chiffré et la langue aux variables de session
            st.session_state["texte_chiffre"] = open("./assets/textes_chiffres/fr.txt", "r").read()
            st.session_state["langue"] = "Français"
        if preconfiguration_FI:

            # On ajoute le texte chiffré et la langue aux variables de session
            st.session_state["texte_chiffre"] = open("./assets/textes_chiffres/fi.txt", "r").read()
            st.session_state["langue"] = "Finnois"
        if preconfiguration_LT:

            # On ajoute le texte chiffré et la langue aux variables de session
            st.session_state["texte_chiffre"] = open("./assets/textes_chiffres/lt.txt", "r").read()
            st.session_state["langue"] = "Lituanien"
        if preconfiguration_EN:

            # On ajoute le texte chiffré et la langue aux variables de session
            st.session_state["texte_chiffre"] = open("./assets/textes_chiffres/en.txt", "r").read()
            st.session_state["langue"] = "Anglais"
        if preconfiguration_FRasPL:

            # On ajoute le texte chiffré et la langue aux variables de session
            st.session_state["texte_chiffre"] = open("./assets/textes_chiffres/fr.txt", "r").read()
            st.session_state["langue"] = "Polonais"
        if fichier:

            # On ajoute le texte chiffré (décoder UTF-8) et la langue aux variables de session
            st.session_state["texte_chiffre"] = fichier.read().decode("utf-8")
            st.session_state["langue"] = langue

            # On met la variable d'exécution à True
            st.session_state.en_cours_execution = True

        # On définit les variables
        st.session_state["texte_dechiffre"] = dechiffrement_cesar(st.session_state.texte_chiffre, st.session_state.langue)
        st.session_state["decalage"] = calculer_decalage(frequence_lettres[st.session_state.langue], caractere_plus_frequent(analyse_frequence(st.session_state.texte_chiffre)))

        # On affiche le texte chiffré (max 1000 caractères)
        st.subheader(":lock: Texte chiffré")
        st.write(st.session_state.texte_chiffre[:1000] + (f"... **({len(st.session_state.texte_chiffre)} caractères restants)**" if len(st.session_state.texte_chiffre) > 1000 else ""))

        # On affiche le texte déchiffré (max 1000 caractères)
        st.subheader(":unlock: Texte déchiffré")
        st.write(st.session_state.texte_dechiffre[:1000] + (f"... **({len(st.session_state.texte_dechiffre)} caractères restants)**" if len(st.session_state.texte_dechiffre) > 1000 else ""))

        # On affiche la cohérence du texte déchiffré
        st.subheader(":mag: Cohérence du texte déchiffré")

        # On récupère une liste de mots dans la langue du texte
        liste_mots = open(f"./assets/liste_mots/{st.session_state.langue}.txt", "r").read()

        # On initialise un compteur de mots trouvés
        mots_trouves = 0

        # Pour chaque mot du texte déchiffré
        for mot in st.session_state.texte_dechiffre.split(" "):
            
            # Supprimer les accents et les caractères spéciaux et mettre en minuscule
            mot = unidecode.unidecode(mot).translate(str.maketrans('', '', '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')).lower()

            # Si le mot est dans la liste des mots
            if mot in liste_mots:
                
                # On incrémente le compteur
                mots_trouves += 1
            
            # Sinon
            else:

                # On passe au mot suivant
                pass

        # On calcule le score de cohérence
        score_cohérence = mots_trouves / len(st.session_state.texte_dechiffre.split(" "))

        # Si le score de cohérence est supérieur à 0.5
        if score_cohérence >= 0.5:
            
            # On affiche un message de cohérence
            st.success(f"Le texte déchiffré semble cohérent avec la langue **{st.session_state.langue}** (score: **{score_cohérence}**)")

        # Sinon
        else:
            
            # On affiche un message d'incohérence
            st.error(f"Le texte déchiffré ne semble pas cohérent avec la langue **{st.session_state.langue}** (score: **{score_cohérence}**)")

        # On affiche des informations globales sur le texte
        st.subheader(":bar_chart: Informations globales")

        st.info(f"En **{st.session_state.langue}** la lettre la plus fréquente est **{frequence_lettres[st.session_state.langue].upper()}**")
        st.info(f"Avec une clé de **{st.session_state.decalage}**, **A** devient **{chr(ord('a') + st.session_state.decalage).upper()}**")
        st.info(f"La lettre **{caractere_plus_frequent(analyse_frequence(st.session_state.texte_chiffre)).upper()}** est la plus fréquente dans le texte chiffré, elle devrait donc correspondre à **{frequence_lettres[st.session_state.langue].upper()}**")

        # On affiche la clé de chiffrement
        st.subheader(":key: Clé de chiffrement")
        st.write(f"La clé de chiffrement estimée est **{st.session_state.decalage}**")
        st.write(f"La clé de chiffrement est une valeur estimée étant donné que, dès que l'on atteint le chiffre 26, l'alphabet recommence. Ainsi, plusieurs clés de chiffrement peuvent être générées.")
        st.write(f"D'autres clés de chiffrement possibles sont : **{st.session_state.decalage + 26}**, **{st.session_state.decalage + 52}**, **{st.session_state.decalage + 78}**, etc...")
        st.write(f"La valeur **{st.session_state.decalage}** est la plus petite possible et représente le nombre de lettres à décaler pour chiffrer le texte.")

        # On affiche un graphique visualisant le décalage des lettres
        st.subheader(":chart_with_upwards_trend: Visualisation")

        # On initialise le dictionnaire contenant les éléments du graphique
        elements = []

        # Pour chaque lettre de l'alphabet
        for i in range(26):
            
            # On ajoute la lettre chiffré au dictionnaire
            elements.append({"data": {"id": f"chiffre_{chr(i + ord('a'))}", "label": chr(i + ord("a"))}})

        # Pour chaque lettre de l'alphabet
        for i in range(26):

            # On effectue la meme opération pour la lettre déchiffré
            elements.append({"data": {"id": f"dechiffre_{chr(i + ord('a'))}", "label": chr(i + ord("a"))}})

        # Pour chaque lettre de l'alphabet
        for i in range(26):

            # On ajoute les liens entre les lettres
            elements.append({"data": {"source": f"chiffre_{chr(i + ord('a'))}", "target": f"dechiffre_{chr((i + st.session_state.decalage) % 26 + ord('a'))}"}})

        # Ajout du style du graphique
        feuille_style = [
                {"selector": "node", "style": {"label": "data(label)", "width": 20, "height": 20}},
                {
                    "selector": "edge",
                    "style": {
                        "width": 3
                    },
                },
                {
                    "selector": "[id ^= 'chiffre_']",
                    "style": {
                        "background-color": "#EFA8B8",
                        "shape": "roundrectangle"
                    },
                },
                {
                    "selector": "[id ^= 'dechiffre_']",
                    "style": {
                        "background-color": "#53D8FB",
                        "shape": "roundrectangle"
                    },
                },
            ]
            
        # Configuration du layout du graphique
        layout = {"name": "grid", "rows": 2}

        # Affichage du graphique
        cytoscape(elements, feuille_style, key="graph", layout=layout)
    else:
        # On affiche un message d'attente
        st.info("Veuillez sélectionner une préconfiguration ou importer un fichier texte chiffré pour commencer.")

# Si une erreur est survenue
except Exception as e:

    # On affiche le message d'erreur
    st.error(f"Une erreur est survenue : {e}")