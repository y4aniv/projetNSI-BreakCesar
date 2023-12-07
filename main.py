"""
BreakCesar - Déchiffrement automatique d'un code César
Auteur : Yaniv & Océanely
WebApp: https://breakcesar.streamlit.app/
"""

#Importation des modules.
import streamlit as st
from st_cytoscape import cytoscape
from langdetect import detect, DetectorFactory

## Dictionnaire des lettres les plus fréquentes dans chaque langue
freq_lang = {
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


def analyse_frequence(texte):
    """
    Analyse la fréquence des lettres dans un texte
    -> text <str>
    <- freq <dict>
    """

    ## Initialisation du dictionnaire
    freq = {}
    ## Parcours du texte
    for caractere in texte:
        ## Conversion en minuscule
        caractere = caractere.lower()
        ## Si le caractère n'est pas une lettre, on passe au suivant
        if not caractere.isalpha():
            continue
        ## Si le caractère est déjà dans le dictionnaire, on incrémente sa valeur
        if caractere in freq:
            freq[caractere] += 1
        ## Sinon, on l'ajoute au dictionnaire
        else:
            freq[caractere] = 1
    ## On retourne le dictionnaire
    return freq

def pourcentage_frequence(freq):
    """
    Convertit les valeurs d'un dictionnaire en pourcentage
    -> freq <dict>
    <- freq <dict>
    """
    ## Calcul du total des valeurs. Utilisation de sum() pour éviter une boucle et améliorer les performances
    total = sum(freq.values())
    ## Parcours du dictionnaire
    for caractere in freq:
        ## Calcul du pourcentage
        freq[caractere] = (freq[caractere] / total) * 100
    ## On retourne le dictionnaire
    return freq

def caractere_plus_frequent(freq):
    """
    Retourne le caractère le plus fréquent dans un dictionnaire
    -> freq <dict>
    <- max_caractere <str>
    """
    ## Initialisation de la variable
    max_caractere = ""
    ## Parcours du dictionnaire
    for caractere in freq:
        ## Si le caractère est le plus fréquent, on le stocke
        if max_caractere == "" or freq[caractere] > freq[max_caractere]:
            max_caractere = caractere
    ## On retourne le caractère le plus fréquent
    return max_caractere

def difference_caracteres(caractere1, caractere2):
    """
    Retourne la différence entre deux caractères
    -> caractere1 <str>, caractere2 <str>
    <- pos2 - pos1 <int>
    """
    ## Conversion des caractères en nombres avec la table ASCII
    pos1 = ord(caractere1) - 97 ## On soustrait 97 pour obtenir la position dans l'alphabet car la table ASCII commence à 97 pour les minuscules
    pos2 = ord(caractere2) - 97 ## On soustrait 97 pour obtenir la position dans l'alphabet car la table ASCII commence à 97 pour les minuscules
    ## On retourne la différence entre les deux caractères
    return pos2 - pos1

def dechiffrer_cesar(texte, lang="Français"):
    """
    Déchiffre un texte chiffré avec un code César
    -> texte <str>, lang <str>
    <- texte_dechiffre <str>
    """
    ## Analyse de la fréquence des lettres dans le texte
    freq = analyse_frequence(texte)
    ## Conversion des valeurs en pourcentage
    freq = pourcentage_frequence(freq)
    ## Récupération du caractère le plus fréquent
    max_caractere = caractere_plus_frequent(freq)
    ## Calcul de la différence entre le caractère le plus fréquent et le caractère le plus fréquent dans la langue
    diff = difference_caracteres(max_caractere, freq_lang[lang])
    ## Initialisation de la variable
    texte_dechiffre = ""
    ## Parcours du texte
    for caractere in texte:
        ## Conversion en minuscule
        caractere_lower = caractere.lower()
        ## Si le caractère n'est pas une lettre, on l'ajoute au texte déchiffré
        if caractere_lower in "abcdefghijklmnopqrstuvwxyz":
            ## Calcul de la nouvelle position du caractère
            pos = ord(caractere_lower) - 97 ## On soustrait 97 pour obtenir la position dans l'alphabet car la table ASCII commence à 97 pour les minuscules
            ## Calcul de la nouvelle position du caractère
            nouvelle_pos = (pos + diff) % 26 ## On utilise le modulo 26 pour éviter de dépasser 26
            ## Conversion de la nouvelle position en caractère
            nouveau_caractere = chr(nouvelle_pos + 97) ## On ajoute 97 pour obtenir la position dans la table ASCII
            ## Si le caractère était en majuscule, on le convertit
            if caractere.isupper():
                nouveau_caractere = nouveau_caractere.upper()
            ## Ajout du caractère au texte déchiffré
            texte_dechiffre += nouveau_caractere
        else:
            texte_dechiffre += caractere
    ## On retourne le texte déchiffré
    return texte_dechiffre

def reset_session(type):
    """
    Réinitialise les variables de session
    -> type <str>
    <- None
    """
    ## Réinitialisation des variables de session 
    st.session_state["demoState"] = True
    st.session_state["demoType"] = type

def iso3166_to_lang(iso3166):
    """
    Convertit un code ISO 3166-1 en langue
    -> iso3166 <str>
    <- lang <str>
    """
    lang = {
        "en": "Anglais",
        "fr": "Français",
        "de": "Allemand",
        "es": "Espagnol",
        "pt": "Portugais",
        "it": "Italien",
        "tr": "Turc",
        "sv": "Suédois",
        "pl": "Polonais",
        "da": "Danois",
        "fi": "Finnois",
        "cs": "Tchèque",
        "lt": "Lituanien"
    }

    return lang[iso3166]

## Configuration de la page
st.set_page_config(page_title="BreakCesar", page_icon="🔓", layout="centered", initial_sidebar_state="auto")

## Titre et sous-titre
st.title("🔓 BreakCesar")
st.subheader("Déchiffrement automatique d'un code César")

try:
        ## Titre de la section
    st.sidebar.write("# Démonstration")

    ## Initialisation des variables de session si elles n'existent pas
    if 'demoState' not in st.session_state:
        ## La variable de session demoState permet de savoir si un texte chiffré a été sélectionné
        st.session_state['demoState'] = False
    if 'demoType' not in st.session_state:
        ## La variable de session demoType permet de savoir quel texte chiffré a été sélectionné
        st.session_state['demoType'] = ""
    if 'file_uploader_key' not in st.session_state:
        ## La variable de session file_uploader_key permet de réinitialiser le file_uploader
        st.session_state['file_uploader_key'] = 0

    ## Boutons de démonstration
    demo_frLong = st.sidebar.button("Test en Français [925 caractères] > Clé de chiffrement : 5")
    demo_trLong = st.sidebar.button("Test en Turc [710 caractères] > Clé de chiffrement : 18")
    demo_sdLong = st.sidebar.button("Test en Suédois [22434 caractères] > Clé de chiffrement : 65")
    demo_enCourt = st.sidebar.button("Test en Anglais [29 caractères] > Clé de chiffrement : 1")
    demo_frAsLt = st.sidebar.button("Test d'un texte en Français déchiffré en Lituanien [925 caractères] > Clé de chiffrement : 5")
    st.sidebar.write("")

    ## Panel de test personnalisé
    st.sidebar.write("# Testez votre propre texte")
    langue = st.sidebar.selectbox("Sélectionnez la langue du texte chiffré", list(freq_lang.keys()))
    fichier_chiffre = st.sidebar.file_uploader("Uploadez le fichier chiffré (.txt)", key=st.session_state['file_uploader_key'], type="txt")

    ## Si un bouton de démonstration est cliqué, on réinitialise les variables de session
    if demo_frLong or demo_trLong or demo_enCourt or demo_frAsLt or fichier_chiffre or demo_sdLong:
        reset_session("frLong" if demo_frLong else "trLong" if demo_trLong else "enCourt" if demo_enCourt else "frAsLt" if demo_frAsLt else "demo_sdLong" if demo_sdLong else "fichier")
        if demo_frLong or demo_trLong or demo_enCourt or demo_frAsLt or demo_sdLong:
            st.session_state["file_uploader_key"] += 1
            st.rerun()

    ## Routage des différentes valeurs de demonstration
    if st.session_state.demoState:
        ## Si un texte par défaut est sélectionné, on récupère le texte et la langue
        if st.session_state.demoType == "frLong":
            donnees_crypter = open('./assets/frLong.txt', 'r').read()
            langue = "Français"
        elif st.session_state.demoType == "trLong":
            donnees_crypter = open('./assets/trLong.txt', 'r').read()
            langue = "Turc"
        elif st.session_state.demoType == "enCourt":
            donnees_crypter = open('./assets/enCourt.txt', 'r').read()
            langue = "Anglais"
        elif st.session_state.demoType == "frAsLt":
            donnees_crypter = open('./assets/frLong.txt', 'r').read()
            langue = "Lituanien"
        elif st.session_state.demoType == "demo_sdLong":
            donnees_crypter = open('./assets/sdLong.txt', 'r').read()
            langue = "Suédois"
        ## Si un fichier est uploadé, on récupère le contenu du fichier 
        elif st.session_state.demoType == "fichier":
            donnees_crypter = fichier_chiffre.read().decode("utf-8")
        
        ## Affichage du texte chiffré
        st.write("## Texte chiffré")
        # Maximum de 1000 caractères pour éviter les problèmes de performances.
        st.write(donnees_crypter[:1000] + (f"... **{len(donnees_crypter) - 1000} caractères restant**" if len(donnees_crypter) > 1000 else ""))

        ## Affichage du texte déchiffré
        st.write("## Texte déchiffré")
        # Maximum de 1000 caractères pour éviter les problèmes de performances.
        st.write(dechiffrer_cesar(donnees_crypter, langue)[:1000] + (f"... **{len(donnees_crypter) - 1000} caractères restant**" if len(donnees_crypter) > 1000 else ""))

        ## Affichage des informations
        st.write("## Informations")
        ## Calcul de la différence entre le caractère le plus fréquent et le caractère le plus fréquent dans la langue
        diff = abs(difference_caracteres(caractere_plus_frequent(analyse_frequence(donnees_crypter)), freq_lang[langue]))

        founded = 0

        wordlist = open(f'./assets/wordlists/{langue}.txt', 'r').read()
        for word in dechiffrer_cesar(donnees_crypter, langue).split(" "):
            if word in wordlist:
                founded += 1
        
        score = founded / len(dechiffrer_cesar(donnees_crypter, langue).split(" "))

        DetectorFactory.seed = 0
        langue_detectee = iso3166_to_lang(detect(dechiffrer_cesar(donnees_crypter, langue)))

        if(score > 0.5):
            if(langue_detectee.lower() != langue.lower()):
                st.warning(f"Le texte ne semble pas avoir été déchiffré avec succès... (score: {score} - Erreur dans la concordance de la langue)")
            else:
                st.success(f"Le texte à été déchiffré avec succès ! (score: {score})")
        else:
            st.warning(f"Le texte ne semble pas avoir été déchiffré avec succès... (score: {score})")

        ## Informations de base
        st.info(f"La lettre la plus fréquente en **{langue}** est **{freq_lang[langue].upper()}**")
        st.info(f"Avec une clé de **{diff}**, la lettre **{freq_lang[langue].upper()}** devient **{caractere_plus_frequent(analyse_frequence(donnees_crypter)).upper()}** après chiffrement")

        ## Affichage de la clé de chiffrement
        st.write(f"### Clé de chiffrement (valeur estimée) : {diff}")
        st.write(
            "La clé de chiffrement est une valeur estimée étant donné que, dès que l'on atteint le chiffre 26, l'alphabet recommence. Ainsi, plusieurs clés de chiffrement peuvent être générées."
        )
        st.write(f"D'autres clés de chiffrement sont possibles, telles que : **{diff+26}, {diff+52}, ...**")
        st.write(f'La valeur **{diff}** est la plus petite possible et représente le nombre de lettres à décaler pour chiffrer le texte.')

        ## Initialisation du dictionnaire contenant les éléments du graphique
        elements = []

        for i in range(26):
            elements.append({"data": {"id": f"c{str(i)}", "label": chr(i + 97).upper()}})
        for i in range(26):
            elements.append({"data": {"id": f"d{str(i)}", "label": chr(i + 97).upper()}})
        for i in range(26):
            elements.append({"data": {"source": f"c{str(i)}", "target": f"d{str((i + diff) % 26)}"}})

        ## Ajout de styles
        stylesheet = [
            {"selector": "node", "style": {"label": "data(label)", "width": 20, "height": 20}},
            {
                "selector": "edge",
                "style": {
                    "width": 3
                },
            },
            {
                "selector": "[id ^= 'c']",
                "style": {
                    "background-color": "#ff0000",
                    "shape": "rectangle",
                },
            },
            {
                "selector": "[id ^= 'd']",
                "style": {
                    "background-color": "#00ff00",
                    "shape": "rectangle",
                },
            },
        ]

        ## Configuration du layout du graphique
        layout = {"name": "grid", "rows": 2}

        ## Affichage du graphique
        st.write("## Visualisation")
        cytoscape(elements, stylesheet, key="graph", layout=layout)

    else:
        ## Si aucun texte chiffré n'est sélectionné, on affiche un message d'erreur
        st.warning("Aucun texte chiffré n'a été sélectionné")
except Exception as e:
    ## Si une erreur se produit, on affiche un message d'erreur
    st.error("Une erreur s'est produite")
    st.error(e)
