import tkinter as tk
import math

############################################################################
# Uporabniski umesnik

class Gui():

    VELIKOST_POLJA = 400

    TAG_PIKE = 'pika'

    ST_PIK = 6

    def __init__(self, master):
        self.igralec_modri = None
        self.igralec_rdeci = None
        self.igra = None
        self.seznam_pik = []
        
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Menu
        menu = tk.Menu(master)
        master.config(menu=menu)

        # Podmenu za izbiro igre
        menu_igra = tk.Menu(menu)
        menu.add_cascade(label='Igra', menu=menu_igra)
        menu_igra.add_command(label='Nova igra', command=self.zacni_igro)
        menu_igra.add_command(label='Razveljavi', command=self.razveljavi)
        menu_igra.add_command(label='Navodila', command=self.navodila)
        menu_igra.add_command(label='Zapri', command=master.destroy)

        # Podmenu - ostali(igralci, stevila oglisc
        #TODO

        # Napis, ki prikazuje stanje igre
        self.napis = tk.StringVar(master, value='Dobrodošli!')
        tk.Label(master, textvariable=self.napis).grid(row=0, column=0)

        # Igralno območje
        self.plosca = tk.Canvas(master, width=Gui.VELIKOST_POLJA, height=Gui.VELIKOST_POLJA)
        self.plosca.grid(row=1, column=0)

        # Naročimo se na dogodek Button-1 na self.plosca,
        self.plosca.bind("<Button-1>", self.pika_klik)

        # Prični igro
        self.zacni_igro()
        self.narisi_pike()

    def zapri_okno(self, master):
        master.destroy()

    def zacni_igro(self):
        #self.plosca.delete(Gui.TAG_FIGURA)
        pass

    def koncaj_igro(self):
        self.napis.set("Konec igre.")

    def narisi_pike(self):
        self.plosca.delete(Gui.TAG_PIKE)
        for i in range(1, Gui.ST_PIK + 1):
            p = self.plosca.create_oval(Gui.VELIKOST_POLJA / 2 + ((Gui.VELIKOST_POLJA / 2) - 50) * math.cos(2*(i-1)*math.pi/Gui.ST_PIK) + 5,
                                    Gui.VELIKOST_POLJA / 2 + ((Gui.VELIKOST_POLJA / 2) - 50) * math.sin(2*(i-1)*math.pi/Gui.ST_PIK) + 5,
                                    Gui.VELIKOST_POLJA / 2 + ((Gui.VELIKOST_POLJA / 2) - 50) * math.cos(2*(i-1)*math.pi/Gui.ST_PIK) - 5,
                                    Gui.VELIKOST_POLJA / 2 + ((Gui.VELIKOST_POLJA / 2) - 50) * math.sin(2*(i-1)*math.pi/Gui.ST_PIK) - 5,
                                    fill='black', tag=Gui.TAG_PIKE)
            self.seznam_pik.append(p)
        self.plosca.tag_bind(Gui.TAG_PIKE, "<Button-1>", func=self.pika_klik)

    def narisi_crto(self):
        #TODO
        pass
    
    def razveljavi(self):
        #TODO
        pass

    def navodila(self):
        window = tk.Toplevel(root)
        string = 'To so navodila za igro'
        #TODO
        tk.Label(window, text=string).pack()

    def pika_klik(self, event):
        #TODO
        pass

    def povleci_potezo(self, event):
        #TODO
        pass


###########################################################################
#Igra

IGRALEC_MODER = 'M'
IGRALEC_RDEC = 'R'
PRAZNO = '_'

def nasprotnik(igralec):
    """Vrni nasprotnika od igralca."""
    if igralec == IGRALEC_MODER:
        return IGRALEC_RDEC
    elif igralec == IGRALEC_RDEC:
        return IGRALEC_MODER
    else:
        assert False, 'neveljaven igralec'

class Igra():
    def __init__(self):
        self.na_potezi = IGRALEC_MODER
        self.zgodovina = []
        self.moder = []
        self.rdec = []

    def shrani_pozicijo(self):
        pass
    


##############################################################################
# Glavni program

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sim")

    aplikacija = Gui(root)

    root.mainloop()
