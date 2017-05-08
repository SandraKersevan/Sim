# Sim
projekt pri predmetu Programiranje 2  
avtorici Sandra Kerševan in Sara Močnik

Za projekt sva si izbrali igrico [Sim](https://en.wikipedia.org/wiki/Sim_(pencil_game)).

## Načrt
1. izdelava GUI  [22.3.2017]
2. logika igre  [29.3.2017]
3. igra med dvema človekoma  [5.4.2017]
4. računalnik kot igralec  [19.4.2017]
5. testiranje in odprava napak  [26.4.2017]

## Opis igre
Igra Sim je igra za dva igralca. Igro se igra na igralni plošči, na kateri je šest oglišč postavljenih v obliko šestkotnika. Igralca izmenično vsak s svojo barvo povezujeta po dve različni, še ne povezani oglišči. Cilj igre je prisiliti nasprotnika, da tri oglišča s svojo barvo poveže v trikotnik. Igralec, ki prvi povleče trikotnik, je izgubil igro.

## Opis programa
V datoteki Sim.py je program, ki je sestavljen iz:
* **Glavni program** program poskrbi, da se igra zažene.  

* **Igra** ima v sebi shranjeno logiko igre. Ta nazoruje potek igre, stanje na igralni plošči...  

BLA
* **Igralec človek** se zažene, če je vsaj eden od igralcev človek.  

Človek igra tako, da si na igralni plošči izbere dve piki, ki ju želi povezati. S klikom na piko, se ta obarva sivo, kar pomeni, da za potezo potrebujemo še eno piko. Če igralec ponovno klikne na isto piko, je poteza neveljavna in je ponovno na vrsti. Če s povlečeno potezo ni zadovoljen, jo lahko razveljavi s klikom na ukaz Razveljavi v meniju.
* **Igralec računalnik** zažene, če je vsaj eden od igralcev računalnik.  

Računalnik igra s pomočjo izbranega algoritma. Vse klike na igralno ploščo, ki jih v času, ko je na potezi računalnik, naredi drugi igralec ignoriramo.
* **Algoritem minimax** izračunava poteze, če je eden od igralcev računalnik.  

Algoritem minimax je nastavljen na globino (`PRIVZETA_GLOBINA`) 3. Uporabnik jo lahko skozi igro spreminja, a večja kot je, počasneje bo igral računalnik. Cenilka pregleda vse možne trikotnike, a upošteva le tiste, ki jih ima zasedene le en igralec s svojo bravo. Največ so vredni trikotniki, kjer sta možni še dve potezi, najmanj pa tisti, v katerem so že vse poteze povlečene. Algoritem si enakovredne poteze shranjuje v seznam in naključno potegne eno izmed teh potez (tako se izognemo monotonemu in predvidljivemu igranju računalnika).
* **Algoritem alfabeta** izračunava poteze, če je eden od igralcev računalnik.  

Enako kot algoritem minimax.
* **Uporabniški vmesnik** nam nariše igralno ploščo, menu, začne igro.  

Uporabniški vmesnik je sprogramiran s pomočjo Pythonove knjižnice TkInter. 
Igralna plošča je na začetku nastavljena na velikost (`VELIKOST_POLJA`) 400x400 (sprogramirano je tudi aktivno prilagajanje velikosti igralne plošče, ki si jo igralec nastavlja med igranjem igre), na njej pa se nariše 6 pik (uporabnik lahko število poljubno prilagodi pri `ST_PIK`; smiselno število pik je vsaj 4, zgornje omejitve ni, a zaradi preglednosti priporočamo največ 18). Ob zagonu programa, sta kot nasprotnika nastavljena dva človeka. V glavnem meniju sta dva podmenija:
  * Igra, kjer si igralec lahko izbere ukaz:
    * nova igra, ki začne novo igro z dvema človekoma,
    * razveljavi, ki razveljavi potezo igralca, a le, če ta poteza ni pomenila konec igre,
    * navodila, ki igralcu izpiše navodila igre in
    * zapri, ki ugasne program.
  * Igralec, kjer si izberemo možnost nasprotnika in algoritem, po katerem bo igral računalnik, če je ta eden od igralcev.
