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

def analyse_frequence(texte):
    """
    Fonction qui analyse la fréquence des lettres dans un texte
    :entrée -> texte (str)
    :sortie -> freq (dict)
    """

    ## Initialisation du dictionnaire de fréquence
    freq = {}

    ## Parcours du texte
    for caractere in texte:

        ## Si le caractère est une majuscule, on le met en minuscule
        caractere = caractere.lower()

        ## Vérification que le caractère est bien une lettre de l'alphabet (a-z)
        if not caractere.isalpha():

            ## Si ce n'est pas le cas, on passe au caractère suivant
            continue

        ## Si le caractère est déjà dans le dictionnaire, on ajoute 1 à sa fréquence
        if caractere in freq:
            freq[caractere] += 1

        ## Sinon, on l'ajoute au dictionnaire avec une fréquence de 1
        else:
            freq[caractere] = 1
    return freq

def pourcentage_frequence(freq):
    """
    Fonction qui calcule la fréquence en pourcentage
    :entrée -> freq (dict)
    :sortie -> freq (dict)
    """

    total = sum(freq[caractere] for caractere in freq)
    ## Parcours du dictionnaire de fréquence
    for caractere in freq:

        ## Calcul de la fréquence en pourcentage
        freq[caractere] = (freq[caractere] / total) * 100

    return freq

def caractere_plus_frequent(freq):
    """
    Fonction qui renvoie la lettre la plus fréquente dans un texte
    :entrée -> freq (dict)
    :sortie -> max (str)
    """

    ## Initialisation de la lettre la plus fréquente
    max_caractere = ""

    ## Parcours du dictionnaire de fréquence
    for caractere in freq:

        ## Si le caractère est plus fréquent que le caractère max, on le remplace
        if max_caractere == "" or freq[caractere] > freq[max_caractere]:
            max_caractere = caractere

    return max_caractere

def difference_caracteres(caractere1, caractere2):
    """
    Fonction qui calcule la différence entre deux lettres
    :entrée -> caractere1 (str), caractere2 (str)
    :sortie -> diff (int)
    """

    ## On récupère la position du caractère caractere1 dans l'alphabet
    pos1 = ord(caractere1) - 97 ## 97 car 97 correspond à la lettre a en ASCII

    ## On récupère la position du caractère caractere2 dans l'alphabet
    pos2 = ord(caractere2) - 97 ## 97 car 97 correspond à la lettre a en ASCII

    return pos2 - pos1

def dechiffrer_cesar(texte, lang="Français"):
    """
    Fonction qui casse un code César
    :entrée -> texte (str)
    :sortie -> texte (str)
    """

    ## On analyse la fréquence des lettres dans le texte
    freq = analyse_frequence(texte)

    ## On calcule la fréquence en pourcentage
    freq = pourcentage_frequence(freq)

    ## On récupère la lettre la plus fréquente
    max_caractere = caractere_plus_frequent(freq)

    ## On calcule la différence entre la lettre la plus fréquente et la lettre la plus fréquente de chaque langage
    diff = difference_caracteres(max_caractere, freq_lang[lang])

    ## On initialise le texte déchiffré
    texte_dechiffre = ""

    ## On parcourt le texte
    for caractere in texte:

        ## Si le caractère est une majuscule, on le met en minuscule
        caractere = caractere.lower()

        ## Si le caractère est une lettre de l'alphabet (a-z)
        if caractere in "abcdefghijklmnopqrstuvwxyz":

            ## On récupère la position du caractère dans l'alphabet
            pos = ord(caractere) - 97 ## 97 car 97 correspond à la lettre a en ASCII

            ## On calcule la nouvelle position du caractère
            nouvelle_pos = (pos + diff) % 26

            ## On calcule le nouveau caractère
            nouveau_caractere = chr(nouvelle_pos + 97) ## 97 car 97 correspond à la lettre a en ASCII

            ## On ajoute le nouveau caractère au texte déchiffré
            texte_dechiffre += nouveau_caractere

        ## Sinon, on ajoute le caractère au texte déchiffré
        else:
            texte_dechiffre += caractere

    return texte_dechiffre

## Interface graphique

## Configuration de la page
st.set_page_config(page_title="BreakCesar", page_icon="🔓", layout="centered", initial_sidebar_state="auto")

## Titre de la page et sous-titre
st.title("🔓 BreakCesar")
st.subheader("Déchiffrement automatique d'un code César")

## Démonstration du programme
st.write("## Démonstration")

## Choix de la langue et du fichier
langue = st.selectbox("Choisissez une langue", ("Français", "Anglais", "Allemand", "Espagnol", "Portugais", "Italien", "Turc", "Suédois", "Polonais", "Néerlandais", "Danois", "Islandais", "Finnois", "Tchèque", "Lituanien"))
fichier_chiffre = st.file_uploader("Choisissez un fichier texte chiffré (.txt)", type=["txt"])
demo_frLong = st.button("Test en Français [925 caractères] > Clé de chiffrement : 5")
demo_trLong = st.button("Test en Turc [710 caractères] > Clé de chiffrement : 18")
demo_enCourt = st.button("Test en Anglais [29 caractères] > Clé de chiffrement : 1")
demo_frAsLt = st.button("Test d'un texte en Français déchiffré en Lituanien [925 caractères] > Clé de chiffrement : 5")

## Si le fichier est bien un fichier texte
if fichier_chiffre is not None or demo_frLong or demo_trLong or demo_enCourt or demo_frAsLt:

    ## On récupère le contenu du fichier en fonction du choix de l'utilisateur
    if demo_frLong:
        donnees_crypter = "Jqqj jsatnj qj rfszxhwny à Xnrtsj ij Gjfzatnw vzn xtzynjsy xf uzgqnhfynts fzc Éinyntsx Lfqqnrfwi. Zsj htwwjxutsifshj x'éyfgqny jsywj jqqjx à qf kns ijx fsséjx 1960. Jqqj qzn jcuwnrj fnsxn xjx jxuéwfshjx jy xjx fyyjsyjx anx-à-anx i'zsj uzgqnhfynts ufw Lfqqnrfwi, zsj rfnxts i'éinynts à qf stytwnéyé nsyjwsfyntsfqj : « Xn atzx xfanje hj vzj o'fyyjsix ij hjyyj uzgqnhfynts ! Qf wzuyzwj fajh zsj anj ij wtzynsj jy ij wéxnlsfynts, qf kznyj js ufdx éywfsljw, q'nsiéujsifshj ufw qj ywfafnq. Atzx atdje vz'nq sj x'flny ufx xnruqjrjsy utzw rtn i'zsj xnruqj vzjxynts ij afsnyé. Utzw tgyjsnw q'fzytwnxfynts ij xtwynj, nq stzx kfzy i'fgtwi zsj fzytwnxfynts rfwnyfqj, uznx zsj fzywj tkknhnjqqj. », éhwny-jqqj ifsx zs htzwwnjw ifyé iz 23 iéhjrgwj 196722. Uznx ifsx zs fzywj htzwwnjw, ifyé hjyyj ktnx iz 5 ofsanjw 1968, jqqj éhwny jshtwj : « Oj hwfnsx gjfzhtzu ij s'fatnw ufx fxxje i'fwljsy inxutsngqj utzw atdfljw ozxvz'à Ufwnx. Oj htruyfnx ozxyjrjsy xzw zsj fafshj ij Lfqqnrfwi utzw qj kfnwj. Rts rfwn utzwwfny r'fnijw rfnx oj sj qj ajzc ufx. Stzx sj xtrrjx ufx js ywèx gtsx yjwrjx jy oj anx à xjx hwthmjyx ijuznx ansly fsx"
        langue = "Français"
    elif demo_trLong:
        donnees_crypter = "Ewjzsts twf Sda. Tmjskı twfae gvse. Gvsevs rsesf ywçajewqa çgc kwnwjae. Karw gvseı sfdslesc aklaqgjme. Gvseı csjvwşaedw hsqdsşıjıe. Vmnsjdsjıfıf jwfya esnavaj. Esna twfae wf kwnvağae jwfclaj. Çsdışes eskse hwfuwjwfaf qsfıfvsvıj. Kstsz mqsfıj mqsfesr hwfuwjwqa sçsjıe nw tajsr lwear zsns sdıjıe. Tadyaksqsjıe çsdışes eskseıf üklüfvwvaj. Csjvwşae tskcwltgd gqfsesqı çgc kwnwj. Tm qürvwf qslsğıfıf sdlıfvs taj tskcwltgd lghm nsjvıj. Vmnsjvs vs tskcwltgd gqmfumdsjıfıf jwkaedwja nsjvıj. Csjvwşae tadyaksqsj gqmfdsjıfı kwnewr ses twf çgc kwnwjae. Wf kwnvağae tadyaksqsj gqmfm sjsts qsjışıvıj. Övwndwjaea qshlıclsf kgfjs tajsr tadyaksqsj gqmfm gqfsj tajsr vs calsh gcmjme. Yüfüf tüqüc cıkeıfı gvsevs ywçajajae. Tm qürvwf gvseıf lwear nw vürwfda gdeskıfs çgc öfwe nwjajae. Fw vwjdwj tadajkafar: Skdsf qsllığı qwjvwf twdda gdmj."
        langue = "Turc"
    elif demo_enCourt:
        donnees_crypter = "Ifmmp Xpsme! J'n Cpoe, Kbnft Cpoe."
        langue = "Anglais"
    elif demo_frAsLt:
        donnees_crypter = "Jqqj jsatnj qj rfszxhwny à Xnrtsj ij Gjfzatnw vzn xtzynjsy xf uzgqnhfynts fzc Éinyntsx Lfqqnrfwi. Zsj htwwjxutsifshj x'éyfgqny jsywj jqqjx à qf kns ijx fsséjx 1960. Jqqj qzn jcuwnrj fnsxn xjx jxuéwfshjx jy xjx fyyjsyjx anx-à-anx i'zsj uzgqnhfynts ufw Lfqqnrfwi, zsj rfnxts i'éinynts à qf stytwnéyé nsyjwsfyntsfqj : « Xn atzx xfanje hj vzj o'fyyjsix ij hjyyj uzgqnhfynts ! Qf wzuyzwj fajh zsj anj ij wtzynsj jy ij wéxnlsfynts, qf kznyj js ufdx éywfsljw, q'nsiéujsifshj ufw qj ywfafnq. Atzx atdje vz'nq sj x'flny ufx xnruqjrjsy utzw rtn i'zsj xnruqj vzjxynts ij afsnyé. Utzw tgyjsnw q'fzytwnxfynts ij xtwynj, nq stzx kfzy i'fgtwi zsj fzytwnxfynts rfwnyfqj, uznx zsj fzywj tkknhnjqqj. », éhwny-jqqj ifsx zs htzwwnjw ifyé iz 23 iéhjrgwj 196722. Uznx ifsx zs fzywj htzwwnjw, ifyé hjyyj ktnx iz 5 ofsanjw 1968, jqqj éhwny jshtwj : « Oj hwfnsx gjfzhtzu ij s'fatnw ufx fxxje i'fwljsy inxutsngqj utzw atdfljw ozxvz'à Ufwnx. Oj htruyfnx ozxyjrjsy xzw zsj fafshj ij Lfqqnrfwi utzw qj kfnwj. Rts rfwn utzwwfny r'fnijw rfnx oj sj qj ajzc ufx. Stzx sj xtrrjx ufx js ywèx gtsx yjwrjx jy oj anx à xjx hwthmjyx ijuznx ansly fsx"
        langue = "Lituanien"
    elif fichier_chiffre:

        ## On récupère le contenu du fichier et on le décode en UTF-8
        donnees_crypter = fichier_chiffre.read().decode("utf-8")

    ## On affiche le contenu du fichier
    st.write("## Texte chiffré")
    st.write(donnees_crypter)

    ## On affiche le texte déchiffré
    st.write("## Texte déchiffré")
    st.write(dechiffrer_cesar(donnees_crypter, langue))

    ## On affiche des informations sur le texte
    st.write("## Informations")
    diff = abs(difference_caracteres(caractere_plus_frequent(analyse_frequence(donnees_crypter)), freq_lang[langue]))

    ## On affiche la lettre la plus fréquente de la langue choisie et la transformation de la lettre la plus fréquente de la langue choisie après chiffrement
    st.info(f"La lettre la plus fréquente en **{langue}** est **{freq_lang[langue].upper()}**")
    st.info(f"Avec une clé de **{diff}**, la lettre **{freq_lang[langue].upper()}** devient **{caractere_plus_frequent(analyse_frequence(donnees_crypter)).upper()}** après chiffrement")

    ## On affiche la fréquence des lettres du texte chiffré et du texte déchiffré
    st.write("### Fréquence des lettres du texte chiffré")
    st.bar_chart(analyse_frequence(donnees_crypter))
    st.write("### Fréquence des lettres du texte déchiffré")
    st.bar_chart(analyse_frequence(dechiffrer_cesar(donnees_crypter, langue)))

    ## On affiche la clé de chiffrement (valeur estimée)
    st.write(f"### Clé de chiffrement (valeur estimée) : {diff}")
    st.write(
        "La clé de chiffrement est une valeur estimée étant donné que, dès que l'on atteint le chiffre 26, l'alphabet recommence. Ainsi, plusieurs clés de chiffrement peuvent être générées."
    )
    st.write(f"D'autres clés de chiffrement sont possibles, telles que : **{diff+26}, {diff+52}, ...**")
    st.write(f'La valeur **{diff}** est la plus petite possible et représente le nombre de lettres à décaler pour chiffrer le texte.')