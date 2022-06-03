import PySimpleGUI as sg

saldo = 1000

def uttag(användarnamn, lösenord1, saldo):
    sg.theme("DarkGrey7")

    layout = [
        [sg.Text("Hur mycket vill du ta ut?")],
        [sg.Input()],
        [sg.Button("Ok"), sg.Button("Cancel")]
    ]

    window = sg.Window("Form", layout)

    while True:
        event, values = window.read()
        skillnad = values[0]
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if event == "Ok":
            #Räknar ut nya saldot
            res = checkSaldo(användarnamn, lösenord1)
            #Ser till så man har tillräkligt med pengar
            if int(res) >= int(skillnad):
                amount = int(res) - int(skillnad)
                updtSaldo(användarnamn, lösenord1, amount)
                break
            else:
                sg.Popup("Du har inte så mycket pengar.")
    window.close()
    bank(användarnamn, lösenord1, saldo)

def inmatning(användarnamn, lösenord1, saldo):
    sg.theme("DarkGrey7")

    layout = [
        [sg.Text("Hur mycket vill du mata in?")],
        [sg.Input()],
        [sg.Button("Ok"), sg.Button("Cancel")]
    ]

    window = sg.Window("Form", layout)

    while True:
        event, values = window.read()
        skillnad = values[0]
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        #räknar ut det nya saldot
        if event == "Ok":
            res = checkSaldo(användarnamn, lösenord1)
            amount = int(res) + int(skillnad)
            updtSaldo(användarnamn, lösenord1, amount)
            break

    window.close()
    bank(användarnamn, lösenord1, saldo)

def bank(användarnamn, lösenord1, saldo):

    sg.theme("DarkGrey7")

    layout = [
        [sg.Text("Bank.")],
        [sg.Button("Saldo")],
        [sg.Button("Inmatning")],
        [sg.Button("Uttag")],
        [sg.Button("Ok"), sg.Button("Cancel")]
    ]

    window = sg.Window("Form", layout)

    while True:
        event, values = window.read()
        if event == "Cancel" or event == "Ok" or event == sg.WIN_CLOSED:
            break
        if event == "Saldo":
            res = checkSaldo(användarnamn, lösenord1)
            sg.Popup(res)
        if event == "Inmatning":
            window.close()
            inmatning(användarnamn, lösenord1, saldo)
        if event == "Uttag":
            window.close()
            uttag(användarnamn, lösenord1, saldo)
    window.close()

def regiseter(saldo):
    sg.theme("DarkGrey7")

    layout = [
        [sg.Text("Skriv in användar namn:")],
        [sg.Input()],
        [sg.Text("Skriv in lösenord:")],
        [sg.Input()],
        [sg.Text("bekräfta lösenord:")],
        [sg.Input()],
        [sg.Button("Ok"), sg.Button("Cancel")]
    ]

    window = sg.Window("Form", layout)

    while True:
        bi = open("bank_inlogg.txt", "r")
        d = []
        f = []
        s = []
        for i in bi:
            a,b,c = i.split(", ")
            b = b.strip()
            d.append(a)
            f.append(b)
            s.append(c)
        event, values = window.read()
        användarnamn = values[0]
        lösenord1 = values[1]
        lösenord2 = values[2]
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if lösenord1 != lösenord2:
            sg.Popup("lösenorden matchar inte.")
        else:
            #Lägger till konto och saldoom kreterierna stämmer
            if len(lösenord1) < 5:
                sg.Popup("Lösenordet är för kort.")
            elif användarnamn in d:
                sg.Popup("användar namn finns redan.")
            else:
                bi = open("bank_inlogg.txt", "a")
                bi.write(användarnamn+ ", " +lösenord1+ ", " +str(saldo)+ "\n")
                bi.close()
                break
    window.close()
    start(saldo)

#Log in funktion
def login(saldo):
    sg.theme("DarkGrey7")
    layout = [
        [sg.Text("Skriv in användar namn:")],
        [sg.Input()],
        [sg.Text("Skriv in lösenord:")],
        [sg.Input()],
        [sg.Button("Ok"), sg.Button("Cancel")]
    ]

    window = sg.Window("Form", layout)

    while True:
        bi = open("bank_inlogg.txt", "r")
        event, values = window.read()
        användarnamn = values[0]
        lösenord1 = values[1]
        

        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        #Ser till att rutorna inte är tomma
        if not len (användarnamn or lösenord1)<1:
            d = []
            f = []
            s = []
            for i in bi:
                a,b,c = i.split(", ")
                b = b.strip()
                d.append(a)
                f.append(b)
                s.append(c)
                data = dict(zip(d, f))
            #Kollar så lösenord och användarnamn stämmer 
            try:
                if data[användarnamn]:
                    try:
                        if lösenord1 == data[användarnamn]:
                            window.close()
                            bank(användarnamn, lösenord1, saldo)
                            break
                        else:
                            sg.Popup("Lösenord eller användarnamn är fel.")
                    except:
                        sg.Popup("Lösenord eller användarnamn är fel.")
                else:
                    sg.Popup("Lösenord eller användarnamn finns inte.")
            except:
                sg.Popup("Lösenord eller användarnamn finns inte.")
        else:
            sg.Popup("Skriv in dina uppgifter.")
    window.close()

#Start meny för använadre
def start(saldo):

    sg.theme("DarkGrey7")

    layout = [
        [sg.Text("Hej!")],
        [sg.Button("Regiseter"), sg.Button("Log in")],
        [sg.Button("Ok"), sg.Button("Cancel")]
    ]

    window = sg.Window("Form", layout)
    #Läser av användarens inputs
    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if event == "Regiseter":
            window.close()
            regiseter(saldo)
        if event == "Log in":
            window.close()
            login(saldo)
    window.close()

#Uppdaterar saldo på det konto man är inloggad på
def updtSaldo(användarnamn, lösenord1, amount):
    search_word = användarnamn + ", " + lösenord1
    file = open("bank_inlogg.txt", "r")
    lines = file.readlines()
    lineNumber = 0
    for line in lines:
        if(line.find(search_word) == 0):
            lines[lineNumber] = (användarnamn + ", " + lösenord1 + ", " + str(amount) + "\n")
            file.close()
            file = open("bank_inlogg.txt", "w")
            file.writelines(lines)
            file.close()
            return True
        lineNumber = lineNumber + 1
    return False

#Tar reda på saldot på det konto man är inloggad på
def checkSaldo(användarnamn, lösenord1):
    search_word = användarnamn + ", " + lösenord1
    file = open("bank_inlogg.txt")
    lines = file.readlines()
    for line in lines:
        if(line.find(search_word) == 0):
            res = line.split(", ")[2]
            file.close()
            return res
    file.close()
    return False


start(saldo)
