"""
Importation des modules.
Streamlit est utilisé pour l'interface graphique et st_cytoscape pour la visualisation du chiffrement.
"""
import streamlit as st
from st_cytoscape import cytoscape

## Dictionnaire des fréquences des lettres dans chaque langue
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
    "Néerlandais": "e",
    "Danois": "e",
    "Islandais": "a",
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
    print(freq)
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
    demo_enCourt = st.sidebar.button("Test en Anglais [29 caractères] > Clé de chiffrement : 1")
    demo_frAsLt = st.sidebar.button("Test d'un texte en Français déchiffré en Lituanien [925 caractères] > Clé de chiffrement : 5")
    st.sidebar.write("")

    ## Panel de test personnalisé
    st.sidebar.write("# Testez votre propre texte")
    langue = st.sidebar.selectbox("Sélectionnez la langue du texte chiffré", list(freq_lang.keys()))
    fichier_chiffre = st.sidebar.file_uploader("Uploadez le fichier chiffré (.txt)", key=st.session_state['file_uploader_key'], type="txt")
    st.sidebar.write("Supprimez le fichier stocké pour retourner à la démonstration")
    del_storage = st.sidebar.button("Supprimer le fichier stocké")

    ## Si un bouton de démonstration est cliqué, on réinitialise les variables de session
    if demo_frLong or demo_trLong or demo_enCourt or demo_frAsLt or fichier_chiffre:
        reset_session("frLong" if demo_frLong else "trLong" if demo_trLong else "enCourt" if demo_enCourt else "frAsLt" if demo_frAsLt else "fichier")

    ## Si le bouton de suppression du fichier stocké est cliqué, on réinitialise les variables de session et on supprime le fichier stocké en incrémentant la clé du file_uploader
    if del_storage:
        st.session_state["demoState"] = False
        st.session_state["demoType"] = ""
        st.session_state["file_uploader_key"] += 1
        st.rerun()

    ## Routage des différentes valeurs de demonstration
    if st.session_state.demoState:
        ## Si un texte par défaut est sélectionné, on récupère le texte et la langue
        if st.session_state.demoType == "frLong":
            donnees_crypter = "Jqqj jsatnj qj rfszxhwny à Xnrtsj ij Gjfzatnw vzn xtzynjsy xf uzgqnhfynts fzc Éinyntsx Lfqqnrfwi. Zsj htwwjxutsifshj x'éyfgqny jsywj jqqjx à qf kns ijx fsséjx 1960. Jqqj qzn jcuwnrj fnsxn xjx jxuéwfshjx jy xjx fyyjsyjx anx-à-anx i'zsj uzgqnhfynts ufw Lfqqnrfwi, zsj rfnxts i'éinynts à qf stytwnéyé nsyjwsfyntsfqj : « Xn atzx xfanje hj vzj o'fyyjsix ij hjyyj uzgqnhfynts ! Qf wzuyzwj fajh zsj anj ij wtzynsj jy ij wéxnlsfynts, qf kznyj js ufdx éywfsljw, q'nsiéujsifshj ufw qj ywfafnq. Atzx atdje vz'nq sj x'flny ufx xnruqjrjsy utzw rtn i'zsj xnruqj vzjxynts ij afsnyé. Utzw tgyjsnw q'fzytwnxfynts ij xtwynj, nq stzx kfzy i'fgtwi zsj fzytwnxfynts rfwnyfqj, uznx zsj fzywj tkknhnjqqj. », éhwny-jqqj ifsx zs htzwwnjw ifyé iz 23 iéhjrgwj 196722. Uznx ifsx zs fzywj htzwwnjw, ifyé hjyyj ktnx iz 5 ofsanjw 1968, jqqj éhwny jshtwj : « Oj hwfnsx gjfzhtzu ij s'fatnw ufx fxxje i'fwljsy inxutsngqj utzw atdfljw ozxvz'à Ufwnx. Oj htruyfnx ozxyjrjsy xzw zsj fafshj ij Lfqqnrfwi utzw qj kfnwj. Rts rfwn utzwwfny r'fnijw rfnx oj sj qj ajzc ufx. Stzx sj xtrrjx ufx js ywèx gtsx yjwrjx jy oj anx à xjx hwthmjyx ijuznx ansly fsx"
            langue = "Français"
        elif st.session_state.demoType == "trLong":
            donnees_crypter = "Ewjzsts twf Sda. Tmjskı twfae gvse. Gvsevs rsesf ywçajewqa çgc kwnwjae. Karw gvseı sfdslesc aklaqgjme. Gvseı csjvwşaedw hsqdsşıjıe. Vmnsjdsjıfıf jwfya esnavaj. Esna twfae wf kwnvağae jwfclaj. Çsdışes eskse hwfuwjwfaf qsfıfvsvıj. Kstsz mqsfıj mqsfesr hwfuwjwqa sçsjıe nw tajsr lwear zsns sdıjıe. Tadyaksqsjıe çsdışes eskseıf üklüfvwvaj. Csjvwşae tskcwltgd gqfsesqı çgc kwnwj. Tm qürvwf qslsğıfıf sdlıfvs taj tskcwltgd lghm nsjvıj. Vmnsjvs vs tskcwltgd gqmfumdsjıfıf jwkaedwja nsjvıj. Csjvwşae tadyaksqsj gqmfdsjıfı kwnewr ses twf çgc kwnwjae. Wf kwnvağae tadyaksqsj gqmfm sjsts qsjışıvıj. Övwndwjaea qshlıclsf kgfjs tajsr tadyaksqsj gqmfm gqfsj tajsr vs calsh gcmjme. Yüfüf tüqüc cıkeıfı gvsevs ywçajajae. Tm qürvwf gvseıf lwear nw vürwfda gdeskıfs çgc öfwe nwjajae. Fw vwjdwj tadajkafar: Skdsf qsllığı qwjvwf twdda gdmj."
            langue = "Turc"
        elif st.session_state.demoType == "enCourt":
            donnees_crypter = "Ifmmp Xpsme! J'n Cpoe, Kbnft Cpoe."
            langue = "Anglais"
        elif st.session_state.demoType == "frAsLt":
            donnees_crypter = "Jqqj jsatnj qj rfszxhwny à Xnrtsj ij Gjfzatnw vzn xtzynjsy xf uzgqnhfynts fzc Éinyntsx Lfqqnrfwi. Zsj htwwjxutsifshj x'éyfgqny jsywj jqqjx à qf kns ijx fsséjx 1960. Jqqj qzn jcuwnrj fnsxn xjx jxuéwfshjx jy xjx fyyjsyjx anx-à-anx i'zsj uzgqnhfynts ufw Lfqqnrfwi, zsj rfnxts i'éinynts à qf stytwnéyé nsyjwsfyntsfqj : « Xn atzx xfanje hj vzj o'fyyjsix ij hjyyj uzgqnhfynts ! Qf wzuyzwj fajh zsj anj ij wtzynsj jy ij wéxnlsfynts, qf kznyj js ufdx éywfsljw, q'nsiéujsifshj ufw qj ywfafnq. Atzx atdje vz'nq sj x'flny ufx xnruqjrjsy utzw rtn i'zsj xnruqj vzjxynts ij afsnyé. Utzw tgyjsnw q'fzytwnxfynts ij xtwynj, nq stzx kfzy i'fgtwi zsj fzytwnxfynts rfwnyfqj, uznx zsj fzywj tkknhnjqqj. », éhwny-jqqj ifsx zs htzwwnjw ifyé iz 23 iéhjrgwj 196722. Uznx ifsx zs fzywj htzwwnjw, ifyé hjyyj ktnx iz 5 ofsanjw 1968, jqqj éhwny jshtwj : « Oj hwfnsx gjfzhtzu ij s'fatnw ufx fxxje i'fwljsy inxutsngqj utzw atdfljw ozxvz'à Ufwnx. Oj htruyfnx ozxyjrjsy xzw zsj fafshj ij Lfqqnrfwi utzw qj kfnwj. Rts rfwn utzwwfny r'fnijw rfnx oj sj qj ajzc ufx. Stzx sj xtrrjx ufx js ywèx gtsx yjwrjx jy oj anx à xjx hwthmjyx ijuznx ansly fsx"
            langue = "Lituanien"
        ## Si un fichier est uploadé, on récupère le contenu du fichier 
        elif st.session_state.demoType == "fichier":
            donnees_crypter = fichier_chiffre.read().decode("utf-8")

        ## Affichage du texte chiffré
        st.write("## Texte chiffré")
        st.write(donnees_crypter)

        ## Affichage du texte déchiffré
        st.write("## Texte déchiffré")
        st.write(dechiffrer_cesar(donnees_crypter, langue))

        ## Affichage des informations
        st.write("## Informations")
        ## Calcul de la différence entre le caractère le plus fréquent et le caractère le plus fréquent dans la langue
        diff = abs(difference_caracteres(caractere_plus_frequent(analyse_frequence(donnees_crypter)), freq_lang[langue]))

        ## Informations de base
        st.info(f"La lettre la plus fréquente en **{langue}** est **{freq_lang[langue].upper()}**")
        st.info(f"Avec une clé de **{diff}**, la lettre **{freq_lang[langue].upper()}** devient **{caractere_plus_frequent(analyse_frequence(donnees_crypter)).upper()}** après chiffrement")

        ## Affichage des graphiques
        st.write("### Fréquence des lettres du texte chiffré")
        st.bar_chart(analyse_frequence(donnees_crypter))
        st.write("### Fréquence des lettres du texte déchiffré")
        st.bar_chart(analyse_frequence(dechiffrer_cesar(donnees_crypter, langue)))

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
