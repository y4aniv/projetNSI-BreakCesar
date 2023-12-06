## BreakCesar
## Auteur: Océanely TRUONG & Yaniv DOUIEB

## Importation des modules
import streamlit as st

## Dictionnaire des lettres les plus fréquentes dans chaque langage
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

def freq_analyse(text):
    """
    Fonction qui analyse la fréquence des lettres dans un texte
    :entrée -> text (str)
    :sortie -> freq (dict)
    """

    ## Initialisation du dictionnaire de fréquence
    freq = {}

    ## Parcours du texte
    for c in text:

        ## Si la lettre est une majuscule, on la met en minuscule
        c = c.lower()

        ## Vérification que la lettre est bien une lettre de l'alphabet (a-z)
        if c.isalpha() == False:

            ## Si ce n'est pas le cas, on passe à la lettre suivante
            continue

        ## Si la lettre est déjà dans le dictionnaire, on ajoute 1 à sa fréquence
        if c in freq:
            freq[c] += 1

        ## Sinon, on l'ajoute au dictionnaire avec une fréquence de 1
        else:
            freq[c] = 1
    return freq

def freq_prc(freq):
    """
    Fonction qui calcule la fréquence en pourcentage
    :entrée -> freq (dict)
    :sortie -> freq (dict)
    """

    ## Initialisation de la somme des fréquences
    total = 0

    ## Parcours du dictionnaire de fréquence
    for c in freq:

        ## Ajout de la fréquence au total
        total += freq[c]

    ## Parcours du dictionnaire de fréquence
    for c in freq:

        ## Calcul de la fréquence en pourcentage
        freq[c] = (freq[c] / total) * 100

    return freq

def max_char(freq):
    """
    Fonction qui renvoie la lettre la plus fréquente dans un texte
    :entrée -> freq (dict)
    :sortie -> max (str)
    """

    ## Initialisation de la lettre la plus fréquente
    max = ""

    ## Parcours du dictionnaire de fréquence
    for c in freq:

        ## Si la lettre est plus fréquente que la lettre max, on la remplace
        if max == "" or freq[c] > freq[max]:
            max = c

    return max

def diff_char(char1, char2):
    """
    Fonction qui calcule la différence entre deux lettres
    :entrée -> char1 (str), char2 (str)
    :sortie -> diff (int)
    """

    ## On récupère la position de la lettre char1 dans l'alphabet
    pos1 = ord(char1) - 97 ## 97 car 97 correspond à la lettre a en ASCII

    ## On récupère la position de la lettre char2 dans l'alphabet
    pos2 = ord(char2) - 97 ## 97 car 97 correspond à la lettre a en ASCII

    ## On calcule la différence entre les deux positions
    diff = pos2 - pos1

    return diff

def break_cesar(text, lang="Français"):
    """
    Fonction qui casse un code César
    :entrée -> text (str)
    :sortie -> text (str)
    """

    ## On analyse la fréquence des lettres dans le texte
    freq = freq_analyse(text)

    ## On calcule la fréquence en pourcentage
    freq = freq_prc(freq)

    ## On récupère la lettre la plus fréquente
    max = max_char(freq)

    ## On calcule la différence entre la lettre la plus fréquente et la lettre la plus frequente de chaque langage
    diff = diff_char(max, freq_lang[lang])

    ## On initialise le texte déchiffré
    text_dec = ""

    ## On parcourt le texte
    for c in text:

        ## Si la lettre est une majuscule, on la met en minuscule
        c = c.lower()

        ## Si la lettre est une lettre de l'alphabet (a-z)
        if c in "abcdefghijklmnopqrstuvwxyz":

            ## On récupère la position de la lettre dans l'alphabet
            pos = ord(c) - 97 ## 97 car 97 correspond à la lettre a en ASCII

            ## On calcule la nouvelle position de la lettre
            new_pos = (pos + diff) % 26

            ## On calcule la nouvelle lettre
            new_c = chr(new_pos + 97) ## 97 car 97 correspond à la lettre a en ASCII

            ## On ajoute la nouvelle lettre au texte déchiffré
            text_dec += new_c

        ## Sinon, on ajoute la lettre au texte déchiffré
        else:
            text_dec += c

    return text_dec

## Interface graphique

## Configuration de la page
st.set_page_config(page_title="BreakCesar", page_icon="🔓", layout="centered", initial_sidebar_state="auto")

## Titre de la page et sous-titre
st.title("🔓 BreakCesar")
st.subheader("Déchiffrement automatique d'un code César")

## Démonstration du programme
st.write("## Démonstration")

## Choix de la langue et du fichier
lang = st.selectbox("Choisissez une langue", ("Français", "Anglais", "Allemand", "Espagnol", "Portugais", "Italien", "Turc", "Suédois", "Polonais", "Néerlandais", "Danois", "Islandais", "Finnois", "Tchèque", "Lituanien"))
cryptedFile = st.file_uploader("Choisissez un fichier texte chiffré (.txt)", type=["txt"])

## Si le fichier est bien un fichier texte
if cryptedFile is not None:

    ## On récupère le contenu du fichier
    bytes_data = cryptedFile.getvalue()

    ## On affiche le contenu du fichier
    st.write("## Texte chiffré")
    st.write(bytes_data.decode("utf-8"))

    ## On affiche le texte déchiffré
    st.write("## Texte déchiffré")
    st.write(break_cesar(bytes_data.decode("utf-8"), lang))

    ## On affiche des informations sur le texte
    st.write("## Informations")

    ## On affiche la fréquence des lettres du texte chiffré et du texte déchiffré
    st.write("### Fréquence des lettres du texte chiffré")
    st.bar_chart(freq_analyse(bytes_data.decode("utf-8")))
    st.write("### Fréquence des lettres du texte déchiffré")
    st.bar_chart(freq_analyse(break_cesar(bytes_data.decode("utf-8"), lang)))

    ## On affiche la clé de chiffrement (valeur estimée)
    diff = abs(diff_char(max_char(freq_analyse(bytes_data.decode('utf-8'))), freq_lang[lang]))
    st.write(f"### Clé de chiffrement (valeur estimée) : {diff}")
    st.write(f"La clé de chiffrement est une valeur estimée étant donné que, dès que l'on atteint le chiffre 26, l'alphabet recommence. Ainsi, plusieurs clés de chiffrement peuvent être générées.")
    st.write(f"D'autres clé de chiffrement sont possibles, telles que : **{diff+26}, {diff+52}, ...**")
    st.write(f'La valeur **{diff}** est la plus petite possible et représente le nombre de lettres à décaler pour chiffrer le texte.')