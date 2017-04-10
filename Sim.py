import tkinter as tk
import math

#################################################################################
# Igra

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
    def __init__(self,gui):
        self.gui=gui
        self.na_potezi = IGRALEC_MODER
        self.moder = []
        self.rdec = []

    def kopija(self):
        #skopiramo celotno igro
        kopija = Igra(self)
        kopija.na_potezi = self.na_potezi
        kopija.moder = self.moder
        kopija.rdec = self.rdec
        return kopija

    def razveljavi(self):
        #iz seznama igralca, ki je zadnji igral, odstranimo zadnjo potezo in spremenimo, kdo je na vrsti za igrati
        if self.na_potezi == IGRALEC_MODER:
            if self.rdec == []: pass
            else:
                self.rdec.pop()
                self.na_potezi = nasprotnik(self.na_potezi)
        elif self.na_potezi == IGRALEC_RDEC:
            if self.moder == []: pass
            else:
                self.moder.pop()
                self.na_potezi = nasprotnik(self.na_potezi)
        else:pass

    def je_veljavna(self, p):
        #pogledamo, ce je poteza ze bila povlecena
        if (p in self.moder) or (p in self.rdec):
            return False
        else:
            self.preveri_trojke(p)
            return True

    def veljavne_poteze(self):
        #pogledamo, katere poteze so se veljavne
        poteze = {}
        for i in self.gui.seznam_pik:
            for j in self.gui.seznam_pik:
                if self.je_veljavna({i,j}):
                    poteze.append({i,j})
        return poteze

    def povleci(self, i, j):
        if (self.je_veljavna({i,j}) == False) or (self.na_potezi == None):
            return None #neveljavna poteza
        else:
            (vrednost, k) = self.preveri_trojke({i,j})
            if vrednost == True:
                self.gui.koncaj_igro([{i,j},{j,k},{k,i}])
            else:
                if self.na_potezi == IGRALEC_MODER: #dodamo potezo igralcu v seznam
                    self.moder.append({i, j})
                else:
                    self.rdec.append({i, j})
                self.na_potezi = nasprotnik(self.na_potezi) #spremenimo, kdo je na potezi
                return True

    def mozni_trikotniki(self):
        TRIKOTNIKI = []
        # zgeneriramo vse možne trikotnike
        for i in self.gui.seznam_pik:
            for j in self.gui.seznam_pik:
                for k in self.gui.seznam_pik:
                    if (i != j) and (i!=k) and (j!=k):
                        TRIKOTNIKI.append([{i,j},{i,k},{j,k}])
                    else: pass
        return TRIKOTNIKI

    def preveri_trojke(self, p):
        igralec = self.na_potezi
        vrednost = False
        i, j = list(p)[0], list(p)[1]
        if igralec == IGRALEC_MODER:
            for k in self.gui.seznam_pik:
                if ({i,k} in self.moder) and ({k,j} in self.moder):
                    vrednost = True
                    break
                else: vrednost = False
        else:
            for k in self.gui.seznam_pik:
                if ({i,k} in self.rdec) and ({k,j} in self.rdec):
                    vrednost = True
                    break
                else: vrednost = False
        return (vrednost, k)


#################################################################################
# Igralec človek

class Clovek():
    def __init__(self, gui):
        self.gui = gui

    def igraj(self):
        pass

    def prekini(self):
        pass

    def klik(self, p):
        self.gui.povleci_potezo(p)

#################################################################################
# Igralec računalnik

class Racunalnik():
    def __init__(self, gui):
        self.gui = gui

    def igraj(self):
        #TODO
        pass

    def preveri_potezo(self):
        #TODO
        pass

    def prekini(self):
        #TODO
        pass

    def klik(self, p):
        pass

#################################################################################
# Uporabniski umesnik

def sredisce(koord):
    (x1, y1, x2, y2) = koord
    return ((x1 + x2)/2, (y1 + y2)/2)

class Gui():

    VELIKOST_POLJA = 400

    TAG_PIKE = 'pika'

    ST_PIK = 6

    TAG_CRTE = 'crta'

    def __init__(self, master):
        self.igralec_moder = None
        self.igralec_rdec = None
        self.igra = None
        self.seznam_pik = []
        self.aktivne_pike = []
        self.seznam_crt = []
        self.stanje = 'normal'
        
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Menu
        menu = tk.Menu(master)
        master.config(menu=menu)

        # Podmenu za izbiro igre
        menu_igra = tk.Menu(menu)
        menu.add_cascade(label='Igra', menu=menu_igra)
        menu_igra.add_command(label='Nova igra', command=lambda: self.zacni_igro(Clovek(self), Clovek(self), 'Na potezi je modri igralec.'))
        menu_igra.add_command(label='Razveljavi', command=self.razveljavi, state=self.stanje)
        menu_igra.add_command(label='Navodila', command=self.navodila)
        menu_igra.add_command(label='Zapri', command=master.destroy)

        menu_igralci = tk.Menu(menu)
        menu.add_cascade(label='Igralci', menu=menu_igralci)
        menu_igralci.add_command(label='Človek/Človek', command=lambda: self.zacni_igro(Clovek(self), Clovek(self), 'Na potezi je modri igralec.'))
        menu_igralci.add_command(label='Človek/Računalnik', command=lambda: self.zacni_igro(Clovek(self), Racunalnik(self), 'Na potezi je modri igralec.'))
        menu_igralci.add_command(label='Računalnik/Človek', command=lambda: self.zacni_igro(Racunalnik(self), Clovek(self), 'Na potezi je modri igralec.'))
        menu_igralci.add_command(label='Računalnik/Računalnik', command=lambda: self.zacni_igro(Racunalnik(self), Racunalnik(self), 'Na potezi je modri igralec.'))
        
        # Napis, ki prikazuje stanje igre
        self.napis = tk.StringVar(master, value='Dobrodošli! \n Na potezi je modri igralec.')
        tk.Label(master, textvariable=self.napis).grid(row=0, column=0)

        # Igralno območje
        self.plosca = tk.Canvas(master, width=Gui.VELIKOST_POLJA, height=Gui.VELIKOST_POLJA)
        self.plosca.grid(row=1, column=0)

        # Naročimo se na dogodek Button-1 na self.plosca,
        self.plosca.bind("<Button-1>", self.pika_klik)

        # Prični igro
        self.zacni_igro(Clovek(self), Clovek(self), 'Dobrodošli! \n Na potezi je modri igralec.')
        self.narisi_pike()

    def zapri_okno(self, master):
        self.prekini_igralce()
        master.destroy()

    def zacni_igro(self, igralec_moder, igralec_rdec, napis):
        self.stanje='normal'
        self.napis.set(napis)
        self.plosca.delete(Gui.TAG_CRTE)
        self.barva = 'blue'
        self.prekini_igralce()
        self.igra = Igra(self)
        if (igralec_moder, igralec_rdec) == (None, None):
            self.igralec_moder = Clovek(self)
            self.igralec_rdec = Clovek(self)
        else:
            self.igralec_moder = igralec_moder
            self.igralec_rdec = igralec_rdec
        self.igralec_moder.igraj()

    def koncaj_igro(self, sez):
        [crta_1, crta_2, crta_3] = sez
        if self.igra.na_potezi == IGRALEC_MODER:
            barva = 'blue'
            vrednost = 'Konec igre. \n Zmagal je rdeč igralec.'
            self.igra.moder.append(crta_1)
        else:
            barva = 'red'
            vrednost = 'Konec igre. \n Zmagal je moder igralec.'
            self.igra.rdec.append(crta_1)
        self.narisi_trikotnik(sez, barva)
        self.igra.na_potezi = None
        self.napis.set(vrednost)
        self.stanje='disabled'
        
    def narisi_trikotnik(self, sez, barva):
        [crta_1, crta_2, crta_3] = sez
        prve_koord_0, prve_koord_1 = list(crta_1)[0], list(crta_1)[1]
        l1 = self.plosca.create_line(sredisce(self.plosca.coords(prve_koord_0))[0],sredisce(self.plosca.coords(prve_koord_0))[1],
                                    sredisce(self.plosca.coords(prve_koord_1))[0],sredisce(self.plosca.coords(prve_koord_1))[1],
                                    fill=barva, tag=Gui.TAG_CRTE, width = 10)
        self.plosca.tag_lower(l1)
        druge_koord_0, druge_koord_1 = list(crta_2)[0], list(crta_2)[1]
        l2 = self.plosca.create_line(sredisce(self.plosca.coords(druge_koord_0))[0],sredisce(self.plosca.coords(druge_koord_0))[1],
                                    sredisce(self.plosca.coords(druge_koord_1))[0],sredisce(self.plosca.coords(druge_koord_1))[1],
                                    fill=barva, tag=Gui.TAG_CRTE, width = 10)
        self.plosca.tag_lower(l2)
        tretje_koord_0, tretje_koord_1 = list(crta_3)[0], list(crta_3)[1]
        l3 = self.plosca.create_line(sredisce(self.plosca.coords(tretje_koord_0))[0],sredisce(self.plosca.coords(tretje_koord_0))[1],
                                    sredisce(self.plosca.coords(tretje_koord_1))[0],sredisce(self.plosca.coords(tretje_koord_1))[1],
                                    fill=barva, tag=Gui.TAG_CRTE, width = 10)
        self.plosca.tag_lower(l3)

    def prekini_igralce(self):
        if self.igralec_moder: self.igralec_moder.prekini()
        if self.igralec_rdec: self.igralec_rdec.prekini()

    def narisi_pike(self):
        self.plosca.delete(Gui.TAG_PIKE)
        for i in range(1, Gui.ST_PIK + 1):
            p = self.plosca.create_oval(Gui.VELIKOST_POLJA / 2 + ((Gui.VELIKOST_POLJA / 2) - 50) * math.cos(2*(i-1)*math.pi/Gui.ST_PIK) + 10,
                                    Gui.VELIKOST_POLJA / 2 + ((Gui.VELIKOST_POLJA / 2) - 50) * math.sin(2*(i-1)*math.pi/Gui.ST_PIK) + 10,
                                    Gui.VELIKOST_POLJA / 2 + ((Gui.VELIKOST_POLJA / 2) - 50) * math.cos(2*(i-1)*math.pi/Gui.ST_PIK) - 10,
                                    Gui.VELIKOST_POLJA / 2 + ((Gui.VELIKOST_POLJA / 2) - 50) * math.sin(2*(i-1)*math.pi/Gui.ST_PIK) - 10,
                                    fill='black', tag=Gui.TAG_PIKE)
            self.seznam_pik.append(p)
        for p in self.seznam_pik:
            self.plosca.tag_raise(p)

    def narisi_crto(self, barva):
        [pika_1, pika_2] = self.aktivne_pike
        (sredisceX_1, sredisceY_1) = sredisce(self.plosca.coords(pika_1))
        (sredisceX_2, sredisceY_2) = sredisce(self.plosca.coords(pika_2))
        l = self.plosca.create_line(sredisceX_1, sredisceY_1, sredisceX_2, sredisceY_2,
                                fill=barva, tag=Gui.TAG_CRTE, width = 5)
        self.plosca.tag_lower(l)
        self.seznam_crt.append(l)
 
    def razveljavi(self):
        if self.stanje == 'disabled': pass
        elif self.seznam_crt == []: pass
        else:
            self.igra.razveljavi()
            self.plosca.delete(self.seznam_crt[-1])
            self.seznam_crt.pop()
            if self.igra.na_potezi == IGRALEC_MODER:
                self.napis.set('Na potezi je modri igralec.')
            elif self.igra.na_potezi == IGRALEC_RDEC:
                self.napis.set('Na potezi je rdeč igralec.')
            else: pass

    def navodila(self):
        window = tk.Toplevel(root)
        string = '''Na igralnem polju so narisane pike. Igralca izmenjajoč povezujeta
pike s črtami, vsak s svojo barvo. Cilj igre je nasprotnika prisiliti,
da s svojo barvo tri pike poveže v trikotnik. Ko se to zgodi, je igre
konec in igralec s trikotnikom v svoji barvi je igro izgubil.'''
        tk.Label(window, text=string).pack()

    def pika_klik(self, event):
        if self.igra.na_potezi == IGRALEC_MODER:
            self.igralec_moder.klik(event)
        elif self.igra.na_potezi == IGRALEC_RDEC:
            self.igralec_rdec.klik(event)        

    def povleci_potezo(self, event):
        igralec = self.igra.na_potezi
        for pika in self.seznam_pik:
            (x1, y1, x2, y2) = self.plosca.coords(pika)
            if (x1 <= event.x <= x2) and (y1 <= event.y <= y2):
                if pika in self.aktivne_pike:
                    self.plosca.itemconfig(pika, fill='black')
                    self.aktivne_pike.remove(pika)
                else:
                    self.plosca.itemconfig(pika, fill='grey')
                    self.aktivne_pike.append(pika)
            else:
                pass
        if len(self.aktivne_pike) == 2:
            if self.igra.povleci(self.aktivne_pike[0],self.aktivne_pike[1]) == True:
                if igralec == IGRALEC_MODER:
                    self.barva = 'blue'
                    vrednost = 'Na potezi je rdeč igralec.'
                else:
                    self.barva = 'red'
                    vrednost = 'Na potezi je modri igralec.'
                self.narisi_crto(self.barva)
                self.napis.set(vrednost)
            else: pass
            for pika in self.aktivne_pike: 
                self.plosca.itemconfig(pika, fill='black')
            self.aktivne_pike = []
        else:
            pass

##############################################################################
# Glavni program

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sim")

    aplikacija = Gui(root)

    root.mainloop()
