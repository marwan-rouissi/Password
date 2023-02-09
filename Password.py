import hashlib
import tkinter as tk
from tkinter import messagebox
import json
from os.path import exists

root = tk.Tk()
root.geometry("500x400")
root.title("Password")


# Demmander à l'utilisateur de choisir un mdp

# Vérifier les exigeances de sécurité:
## Doit contenir:
### au moins 8 caractères
def check_len(passwd):
    passwd = passwd_entry.get()
    len_state = False
    if len(passwd) >= 8:
        len_state = True
    return len_state

### vérifier si le mdp contient au moins une lettre MAJUSCULE
def check_upercase(passwd):
    passwd = passwd_entry.get()
    uppercase="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    uper_state = False
    for char in passwd:
        if(char in uppercase):
            uper_state = True
    return uper_state

### vérifier si le mdp contient au moins une lettre minuscule
def check_lowercase(passwd):
    passwd = passwd_entry.get()
    lowercase="abcdefghijklmnopqrstuvwxyz"
    lower_state = False
    for char in passwd:
        if(char in lowercase):
            lower_state = True
    return lower_state

### vérifier si le mdp contient au moins un chiffre
def check_digit(passwd):
    passwd = passwd_entry.get()
    digit="01234566789"
    digit_state = False
    for char in passwd:
        if(char in digit):
            digit_state = True
    return digit_state

### vérifier si le mdp contient au moins un caractère spécial (!, @, #, $, %, ^, &, *)
def check_special_char(passwd):
    passwd = passwd_entry.get()
    special_char="!@#$%^&*"
    special_char_state = False
    for char in passwd:
        if(char in special_char):
            special_char_state = True
    return special_char_state

# fonction pour reset l'entry
def clear():
    passwd_entry.delete(0, tk.END)

# afficher un message d'alerte si mdp déjà utilisé/enregistré 
def already_used():
    messagebox.showwarning(title="Attention", message="Mot de passe déjà utilisé")

# fonction pour enregistrer les mdp vadilés en format .json
def save_json(crypted_passwd):
    # ficher json
    history_file="History.json"
    # variable de verification si le fichier existe déjà ou non
    file_exist = exists(history_file)
    # variable dans laquelle stocker les mdp
    passwd_dictio = {}
    # le mdp validé à enregistrer
    data = {"crypted_pwd" : crypted_passwd}
    
    # si le fichier .json existe déjà
    if file_exist:
        # ouvrir le fichier en question
        with open(history_file, 'r') as file:
            file_data = json.load(file)
            # print(file_data["Passwords:"])

            # pour pour les éléments récupérer depuis le fichier
            for element in file_data["Passwords:"]:
        
                # si l'élément en question est identique au mdp valide que l'on souhaite ajouter
                if element["crypted_pwd"] == data["crypted_pwd"]:
                    
                    # afficher un message d'avertissement
                    already_used()
                    # arrêter là
                    break

            # sinon ajouter le mdp à la liste d'éléments récupérés depuis le fichier .json    
            else:
                passwd_dictio["Passwords:"] = [data]
                file_data["Passwords:"] += passwd_dictio["Passwords:"]

            # réécrire par dessus le fichier .json en le remplacant par la nouvelle variable incluants les éléments récupérés + le mdp à ajouter    
            with open(history_file, "w") as file:
                json.dump(file_data, file, indent=4)
            
    #si le fichier .json n'existe pas                
    else:
        # le créer avec pour object le 1er mdp valide à ajouter
        with open(history_file, 'w') as file:
            passwd_dictio["Passwords:"] = [data]
            json.dump(passwd_dictio, file, indent=4)
            

# Chiffrer/Crypter le mot de passe valide
def crypt(passwd):
    # récupérer le mdp depuis l'Entry de l'interface graphique
    passwd = passwd_entry.get()
    # chiffrer le mdp en sha256 à l'aide du module hashlib en l'encodant avant de le traduire en en hash (64 caractères)
    crypted_passwd = hashlib.sha256(passwd.encode()).hexdigest()
    
    # sauvegarder le mdp chiffré
    save_json(crypted_passwd)
    # print("Le mot de passe crypté est: " + crypted_passwd)

# Fonction pour afficher l'historique dans une fenêtre sur l'interface graphique mais aussi sur le terminal
def history():
    # définition d'une nouvelle fenêtre à afficher au clique sur "Historique"
    history = tk.Toplevel(root)
    history.title("Passwords")
    # Label pour l'affichage avec texte par defaut si pas d'historique
    history_label = tk.Label(history, text="Pas d'historique.")
    history_label.pack()
    history.geometry("600x300")
    # récupération du json 
    with open("History.json", 'r') as file:
        # récupération des données dans une variable 
        txt = json.load(file)
        # affichage des mdp présents dans l'historique sur le terminal
        for e in txt["Passwords:"]:
            print(e)
    # récupération de l'historique 
    file = open("History.json", "r")
    # lecture du ficher
    txt = file.read()
    # affichache du ficher dans le label dédié
    history_label.config(text=txt)
    
    file.close()
    history.mainloop()


###vérifier si toute les exigeances de sécurité sont valides
def check_valid():
    passwd = passwd_entry.get()
    # si toutes les conditions bonne, mdp validé
    if check_len(passwd) == True and check_upercase(passwd) == True and check_lowercase(passwd) == True and check_digit(passwd) == True and check_special_char(passwd) == True:
        # message de validation
        messagebox.showinfo(title="Valid", message="Mot de passe valide")
        # message alors crypté
        crypt(passwd)
        clear()
        # exit()

    # sinon, message d'erreur avec rappel des conditons de valitation
    else:
        messagebox.showerror(title="Erreur", message="Mot de passe invalide. \n \n Doit contenir: \n - au moins 8 caractères \n - au moins une lettre MAJUSCULE \n - au moins une lettre minuscule \n - au moins un chiffre \n - au moins un caractère spécial (!, @, #, $, %, ^, &, *)")
        clear()

# fonction pour afficher ou masquer le mdp selon si la case dédiée est selectionnée ou pas 
def readable():
    if var.get() == 1 :
        passwd_entry.config(show="")
    else:
        passwd_entry.config(show="*")


# Txt de saisie

passwd_label = tk.Label(root, text="Entrer un mot de passe. \n \n Doit contenir, au minimum: \n - 8 caractères \n - une lettre MAJUSCULE \n - une lettre minuscule \n - un chiffre \n - un caractère spécial (!, @, #, $, %, ^, &, *)",foreground="blue", font=1)
passwd_label.pack()

# barre de saisie du mdp

passwd_var = tk.StringVar()
passwd_entry = tk.Entry(root, borderwidth=5, font=10, textvariable=passwd_var, justify="center", show="*")
passwd_entry.pack(pady=30)
passwd = passwd_entry.get()

# checkbox lisibilité mdp

var = tk.IntVar()
readable_checkbox = tk.Checkbutton(root, text="Afficher mdp", variable=var, onvalue=1, offvalue=0, command=readable)
readable_checkbox.pack()

# bouton de confirmation

passwd_btn = tk.Button(root, text="Confirmer", borderwidth=10, command=check_valid)
passwd_btn.pack()

# bouton historique

history_btn = tk.Button(root, text="Historique", borderwidth=10, command=history)
history_btn.pack()

root.mainloop()