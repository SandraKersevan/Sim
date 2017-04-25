import tkinter as tk
import threading
import argparse
import logging
import math
import random

#################################################################################
# Igra

IGRALEC_MODER = 'M'
IGRALEC_RDEC = 'R'
NEODLOCENO = 'neodloceno'
NI_KONEC = 'ni konec'

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
        self.gui = gui
        self.na_potezi = IGRALEC_MODER
        self.moder = []
        self.rdec = []
        self.stanje_igre = NI_KONEC
        self.koncen_seznam = []

    def kopija(self):
        ''' Vrne kopijo celotne igre.'''
        kopija = Igra(self.gui)
        kopija.na_potezi = self.na_potezi
        kopija.moder = self.moder
        kopija.rdec = self.rdec
        kopija.stanje_igre = self.stanje_igre
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
        elif len(p) != 2:
            return False
        else:
            return True

    def veljavne_poteze(self):
        #pogledamo, katere poteze so se veljavne
        poteze = []
        for i in self.gui.seznam_pik:
            for j in self.gui.seznam_pik:
                if (self.je_veljavna({i,j})) and ({i,j} not in poteze):
                    poteze.append({i,j})
        return poteze

    def povleci(self, i, j):
        if (self.je_veljavna({i,j}) == False) or (self.na_potezi == None):
            if self.veljavne_poteze == []:
                self.stanje_igre = NEODLOCENO
                self.koncen_seznam = []
                self.na_potezi = None
            return None
        else:
            vrednost= self.preveri_trojke({i,j})
            if vrednost == True:
                self.stanje_igre = nasprotnik(self.na_potezi)
            else:
                self.stanje_igre = NI_KONEC

            def dodaj_v_seznam(igralec):
                if igralec == IGRALEC_MODER: #dodamo potezo igralcu v seznam
                    self.moder.append({i, j})
                elif igralec == IGRALEC_RDEC:
                    self.rdec.append({i, j})

            dodaj_v_seznam(self.na_potezi)
            self.na_potezi = nasprotnik(self.na_potezi) #spremenimo, kdo je na potezi
            return True

    def koncaj_igro(self):
        [crta_1, crta_2, crta_3] = self.koncen_seznam
        if self.na_potezi == IGRALEC_MODER:
            self.moder.append(crta_1)
        else:
            self.rdec.append(crta_1)
        self.na_potezi = None

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
            seznam = self.moder
        else:
            seznam = self.rdec
        for k in self.gui.seznam_pik:
            if ({i,k} in seznam) and ({k,j} in seznam):
                vrednost = True
                self.koncen_seznam.append({i,j})
                self.koncen_seznam.append({j,k})
                self.koncen_seznam.append({k,i})
                break
        return vrednost


############################################################################
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

############################################################################
# Igralec računalnik

class Racunalnik():
    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem #Algoritem, ki izračuna potezo
        self.mislec = None #Vlakno, ki razmišlja

    def igraj(self):
        """Igra potezo, ki jo vrne algoritem"""
        self.mislec = threading.Thread(target=lambda : self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))
        self.mislec.start()
        self.gui.plosca.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        if self.algoritem.poteza is not None:
            self.gui.aktivne_pike.append(list(self.algoritem.poteza)[0])
            self.gui.povleci_potezo(list(self.algoritem.poteza)[1])
            self.mislec = None
        else:
            self.gui.plosca.after(100, self.preveri_potezo)

    def prekini(self):
        if self.mislec:
            logging.debug("Prekinjamo{0}".format(self.mislec))
            self.algoritem.prekini()
            self.mislec.join()
            self.mislec = None

    def klik(self, p):
        pass

############################################################################
# Algoritem minimax

ALFABETA_GLOBINA = 3

class Minimax():
    def __init__(self, globina):
        self.globina = globina
        self.prekinitev = False 
        self.igra = None 
        self.jaz = None 
        self.poteza = None

    def prekini(self):
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        """Izračunaj potezo za trenutno stanje dane igre."""
        self.igra = igra
        self.prekinitev = False
        self.jaz = self.igra.na_potezi
        self.poteza = None
        # Poženemo minimax
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza

    # Vrednosti igre
    ZMAGA = 100000
    NESKONCNO = ZMAGA + 1

    def vrednost_pozicije(self):
        """Ocena vrednosti pozicije: sešteje vrednosti vseh trojk na plošči."""
        vrednost_trikotnika = {
            (0,3) : Minimax.ZMAGA,
            (3,0) : -Minimax.ZMAGA//10,
            (0,2) : Minimax.ZMAGA//100,
            (2,0) : -Minimax.ZMAGA//1000,
            (0,1) : Minimax.ZMAGA//10000,
            (1,0) : -Minimax.ZMAGA//100000
        }
        vrednost = 0
        for t in self.igra.mozni_trikotniki():
            x = 0
            y = 0
            for par in t:
                if par in self.igra.moder:
                    x += 1
                elif par in self.igra.rdec:
                    y += 1
            vrednost += vrednost_trikotnika.get((x,y), 0)
        return vrednost

    def minimax(self, globina, maksimiziramo):
        """Glavna metoda minimax."""
        if self.prekinitev:
            logging.debug ("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)
        zmagovalec = self.igra.stanje_igre
        if zmagovalec in (IGRALEC_MODER, IGRALEC_RDEC, NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, Minimax.ZMAGA)
            elif zmagovalec == nasprotnik(self.jaz):
                return (None, -Minimax.ZMAGA)
            else:
                assert False, "Konec igre brez zmagovalca."
        elif zmagovalec == NI_KONEC:
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    najboljse_poteze = []
                    for p in self.igra.veljavne_poteze():
                        pika_1, pika_2 = list(p)[0], list(p)[1]
                        r = self.igra.povleci(pika_1, pika_2)
                        if r == True:
                            vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                            self.igra.razveljavi()
                            if vrednost > vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = p
                                najboljse_poteze = [p]
                            elif vrednost == vrednost_najboljse:
                                najboljse_poteze.append(p)
                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    najboljse_poteze = []
                    for p in self.igra.veljavne_poteze():
                        pika_1, pika_2 = list(p)[0], list(p)[1]
                        r = self.igra.povleci(pika_1, pika_2)
                        if r == True:
                            vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                            self.igra.razveljavi()
                            if vrednost < vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = p
                                najboljse_poteze = [p]
                            elif vrednost == vrednost_najboljse:
                                najboljse_poteze.append(p)
                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                najboljsa_poteza = random.choice(najboljse_poteze)
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"


############################################################################
# Algoritem alfabeta

class Alfabeta():
    def __init__(self, globina):
        self.globina = globina
        self.prekinitev = False 
        self.igra = None 
        self.jaz = None 
        self.poteza = None

    def prekini(self):
        self.prekinitev = True

    # Vrednosti igre
    ZMAGA = 100000
    NESKONCNO = ZMAGA + 1

    def vrednost_pozicije(self):
        """Ocena vrednosti pozicije: sešteje vrednosti vseh trojk na plošči."""
        vrednost_trikotnika = {
            (0,3) : Minimax.ZMAGA,
            (3,0) : -Minimax.ZMAGA//10,
            (0,2) : Minimax.ZMAGA//100,
            (2,0) : -Minimax.ZMAGA//1000,
            (0,1) : Minimax.ZMAGA//10000,
            (1,0) : -Minimax.ZMAGA//100000
        }
        vrednost = 0
        for t in self.igra.mozni_trikotniki():
            x = 0
            y = 0
            for par in t:
                if par in self.igra.moder:
                    x += 1
                elif par in self.igra.rdec:
                    y += 1
            vrednost += vrednost_trikotnika.get((x,y), 0)
        return vrednost

    def izracunaj_potezo(self, igra):
        """Izračunaj potezo za trenutno stanje dane igre."""
        self.igra = igra
        self.prekinitev = False
        self.jaz = self.igra.na_potezi
        self.poteza = None
        (poteza, vrednost) = self.alfabeta(self.globina, True, - Alfabeta.NESKONCNO, Alfabeta.NESKONCNO)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("alfabeta: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza
            
    def alfabeta(self, globina, maksimiziramo, alfa, beta):
        """Glavna metoda alfabeta."""
        if self.prekinitev:
            logging.debug ("Alfabeta prekinja, globina = {0}".format(globina))
            return (None, 0)
        zmagovalec = self.igra.stanje_igre
        if zmagovalec in (IGRALEC_MODER, IGRALEC_RDEC, NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, Alfabeta.ZMAGA)
            elif zmagovalec == nasprotnik(self.jaz):
                return (None, -Alfabeta.ZMAGA)
            else:
                assert False, "Konec igre brez zmagovalca."
        elif zmagovalec == NI_KONEC:
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                if maksimiziramo:
                    a = alfa
                    b = beta
                    najboljsa_poteza = None
                    vrednost_najboljse = -Alfabeta.NESKONCNO
                    najboljse_poteze = []
                    for p in self.igra.veljavne_poteze():
                        pika_1, pika_2 = list(p)[0], list(p)[1]
                        r = self.igra.povleci(pika_1, pika_2)
                        if r == True:
                            vrednost = self.alfabeta(globina-1, not maksimiziramo, alfa, beta)[1]
                            self.igra.razveljavi()
                            if vrednost > vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = p
                                najboljse_poteze = [p]
                            elif vrednost == vrednost_najboljse:
                                najboljse_poteze.append(p)
                            else: pass

                            if vrednost > a:
                                a = vrednost
                            elif  b <= a: break
                else:
                    a = alfa
                    b = beta
                    najboljsa_poteza = None
                    vrednost_najboljse = Alfabeta.NESKONCNO
                    najboljse_poteze = []
                    for p in self.igra.veljavne_poteze():
                        pika_1, pika_2 = list(p)[0], list(p)[1]
                        r = self.igra.povleci(pika_1, pika_2)
                        if r == True:
                            vrednost = self.alfabeta(globina-1, not maksimiziramo, alfa, beta)[1]
                            self.igra.razveljavi()
                            if vrednost < vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = p
                                najboljse_poteze = [p]
                            elif vrednost == vrednost_najboljse:
                                najboljse_poteze.append(p)
                            else: pass

                            if vrednost < b:
                                b = vrednost
                            elif b < a: break
                assert (najboljsa_poteza is not None), "alfabeta: izračunana poteza je None"
                najboljsa_poteza = random.choice(najboljse_poteze)
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "alfabeta: nedefinirano stanje igre"

            
############################################################################
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
        menu_igra = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='Igra', menu=menu_igra)
        menu_igra.add_command(label='Nova igra', command=lambda: self.zacni_igro(Clovek(self), Clovek(self), 'Na potezi je modri igralec.'))
        menu_igra.add_command(label='Razveljavi', command=self.razveljavi, state=self.stanje)
        menu_igra.add_command(label='Navodila', command=self.navodila)
        menu_igra.add_command(label='Zapri', command=master.destroy)

        menu_igralci = tk.Menu(menu, tearoff=False)
        menu_clovek_racunalnik = tk.Menu(menu_igralci)
        menu_racunalnik_clovek = tk.Menu(menu_igralci)
        menu_racunalnik_racunalnik = tk.Menu(menu_igralci)

        podmenu1 = tk.Menu(menu, tearoff=False)
        podmenu2 = tk.Menu(menu, tearoff=False)
        podmenu3 = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='Igralci', menu=menu_igralci)
        menu_igralci.add_command(label='Človek/Človek', command=lambda: self.zacni_igro(Clovek(self), Clovek(self), 'Na potezi je modri igralec.'))
        menu_igralci.add_cascade(label='Človek/Računalnik', menu=podmenu1)
        menu_igralci.add_cascade(label='Računalnik/Človek', menu=podmenu2)
        menu_igralci.add_cascade(label='Računalnik/Računalnik', menu=podmenu3)

        podmenu1.add_command(label='Minimax', command=lambda: self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(ALFABETA_GLOBINA)), 'Na potezi je modri igralec.'))
        podmenu1.add_command(label='Alfabeta', command=lambda: self.zacni_igro(Clovek(self), Racunalnik(self, Alfabeta(ALFABETA_GLOBINA)), 'Na potezi je modri igralec.'))
        podmenu2.add_command(label='Minimax', command=lambda: self.zacni_igro(Racunalnik(self, Minimax(ALFABETA_GLOBINA)), Clovek(self), 'Na potezi je modri igralec.'))
        podmenu2.add_command(label='Alfabeta', command=lambda: self.zacni_igro(Racunalnik(self, Alfabeta(ALFABETA_GLOBINA)), Clovek(self), 'Na potezi je modri igralec.'))
        podmenu3.add_command(label='Minimax', command=lambda: self.zacni_igro(Racunalnik(self, Minimax(ALFABETA_GLOBINA)), Racunalnik(self, Minimax(ALFABETA_GLOBINA)), 'Na potezi je modri igralec.'))
        podmenu3.add_command(label='Alfabeta', command=lambda: self.zacni_igro(Racunalnik(self, Alfabeta(ALFABETA_GLOBINA)), Racunalnik(self, Alfabeta(ALFABETA_GLOBINA)), 'Na potezi je modri igralec.'))
        
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

    def navodila(self):
        window = tk.Toplevel(root)
        string = '''Na igralnem polju so narisane pike. Igralca izmenjajoč povezujeta
pike s črtami, vsak s svojo barvo. Cilj igre je nasprotnika prisiliti,
da s svojo barvo tri pike poveže v trikotnik. Ko se to zgodi, je igre
konec in igralec s trikotnikom v svoji barvi je igro izgubil.'''
        tk.Label(window, text=string, font=(14)).pack()

    def zacni_igro(self, igralec_moder, igralec_rdec, napis):
        self.stanje='normal'
        self.napis.set(napis)
        self.plosca.delete(Gui.TAG_CRTE)
        self.seznam_crt = []
        self.barva = 'blue'
        self.prekini_igralce()
        self.igra = Igra(self)
        for p in self.aktivne_pike:
            self.plosca.itemconfig(p, fill='black')
        self.aktivne_pike = []
        if (igralec_moder, igralec_rdec) == (None, None):
            self.igralec_moder = Clovek(self)
            self.igralec_rdec = Clovek(self)
        else:
            self.igralec_moder = igralec_moder
            self.igralec_rdec = igralec_rdec
        self.igralec_moder.igraj()

    def koncaj_igro(self):
        if len(self.igra.koncen_seznam) != 3:
            assert False, 'nekje je slo nekaj narobe'
        if self.igra.stanje_igre == IGRALEC_MODER:
            barva = 'red'
            vrednost = 'Konec igre. \n Zmagal je moder igralec.'
        else:
            barva = 'blue'
            vrednost = 'Konec igre. \n Zmagal je rdec igralec.'
        self.narisi_trikotnik(barva)
        self.napis.set(vrednost)
        self.stanje='disabled'
        
    def narisi_trikotnik(self, barva):
        [crta_1, crta_2, crta_3] = self.igra.koncen_seznam
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

    def pika_klik(self, event):
        for pika in self.seznam_pik:
            (x1, y1, x2, y2) = self.plosca.coords(pika)
            if (x1 <= event.x <= x2) and (y1 <= event.y <= y2):
                if self.igra.na_potezi == IGRALEC_MODER:
                    self.igralec_moder.klik(pika)
                elif self.igra.na_potezi == IGRALEC_RDEC:
                    self.igralec_rdec.klik(pika)
                else:pass
            else:pass

    def povleci_potezo(self, p):
        igralec = self.igra.na_potezi
        if len(self.igra.moder + self.igra.rdec) != len(self.seznam_crt):
            assert False, 'neskladje crt v seznamih'
        if p in self.aktivne_pike:
            self.plosca.itemconfig(p, fill='black')
            self.aktivne_pike.remove(p)
        else:
            self.plosca.itemconfig(p, fill='grey')
            self.aktivne_pike.append(p)
        if len(self.aktivne_pike) == 2:
            if self.igra.povleci(self.aktivne_pike[0],self.aktivne_pike[1]) == True:
                if igralec == IGRALEC_MODER:
                    self.barva = 'blue'
                    vrednost = 'Na potezi je rdeč igralec.'
                    self.igralec_rdec.igraj()
                else:
                    self.barva = 'red'
                    vrednost = 'Na potezi je modri igralec.'
                    self.igralec_moder.igraj()
                self.narisi_crto(self.barva)
                self.napis.set(vrednost)
            else: pass
            for pika in self.aktivne_pike: 
                self.plosca.itemconfig(pika, fill='black')
            self.aktivne_pike = []
        elif len(self.aktivne_pike) > 2:
            assert False, 'napaka'
        else:
            pass
        if (self.igra.stanje_igre == IGRALEC_MODER) or (self.igra.stanje_igre == IGRALEC_RDEC):
            self.igra.koncaj_igro()
            self.koncaj_igro()

############################################################################
# Glavni program

if __name__ == "__main__":
    # Opišemo argumente, ki jih sprejmemo iz ukazne vrstice
    parser = argparse.ArgumentParser(description="Igrica Sim")
    # Argument --globina n, s privzeto vrednostjo PRIVZETA_GLOBINA
    parser.add_argument("--globina",
                        default=ALFABETA_GLOBINA,
                        type=int,
                        help="globina iskanja za minimax algoritem")
    # Argument --debug, ki vklopi sporočila o tem, kaj se dogaja
    parser.add_argument("--debug",
                        action="store_true",
                        help="vklopi sporočila o dogajanju")

    # Obdelamo argumente iz ukazne vrstice
    args = parser.parse_args()

    # Vklopimo sporočila, če je uporabnik podal --debug
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        
    root = tk.Tk()
    root.title("Sim")

    aplikacija = Gui(root)

    root.mainloop()
