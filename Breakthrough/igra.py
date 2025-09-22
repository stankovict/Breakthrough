import time
import json
import os
import ast

def napravi_tablu():

    tabla = []
    for i in range(8):
        tabla.append(['.'] * 8)

    for red in range(0, 2):
        for kolona in range(8):
            tabla[red][kolona] = 'B'

    for red in range(6, 8):
        for kolona in range(8):
            tabla[red][kolona] = 'W'

    return tabla


def oznaka_u_indeks(oznaka):

    kolone_slova = ["A", "B", "C", "D", "E", "F", "G", "H"]
    kol = kolone_slova.index(oznaka[0])
    red = 8 - int(oznaka[1])
    return red, kol

def prikazi_tablu(tabla, poslednji_potez=None, oznacena=None):

    kolone_slova = ["A", "B", "C", "D", "E", "F", "G", "H"]
    oznacena_polja = set()

    if poslednji_potez:
        start_red, start_kol = oznaka_u_indeks(poslednji_potez[0])
        kraj_red, kraj_kol = oznaka_u_indeks(poslednji_potez[1])
        oznacena_polja = {(start_red, start_kol), (kraj_red, kraj_kol)}

    print("    A  B  C  D  E  F  G  H")

    for red in range(8):
        print(8 - red, end="  ")

        for kolona in range(8):
            if (red, kolona) in oznacena_polja:
                print(f"[{tabla[red][kolona]}]", end="")
            elif oznacena and (red, kolona) in oznacena:
                print(" * ", end="")
            else:
                print(f" {tabla[red][kolona]} ", end="")
        print()

    print("    A  B  C  D  E  F  G  H")


def generisi_poteze(tabla, igrac):

    potezi = []

    kolone_slova = ["A", "B", "C", "D", "E", "F", "G", "H"]
    protivnik = "W" if igrac == "B" else "B"
    smer = 1 if igrac == "B" else -1

    for red in range(8):
        for kolona in range(8):
            if tabla[red][kolona] == igrac:
                novi_red = red + smer
                if 0 <= novi_red < 8:

                    if tabla[novi_red][kolona] == ".":
                        potezi.append((
                            f"{kolone_slova[kolona]}{8 - red}",
                            f"{kolone_slova[kolona]}{8 - novi_red}"
                        ))
                    if kolona - 1 >= 0 and (tabla[novi_red][kolona-1] == "." or tabla[novi_red][kolona-1] == protivnik):
                        potezi.append((
                            f"{kolone_slova[kolona]}{8 - red}",
                            f"{kolone_slova[kolona-1]}{8 - novi_red}"
                        ))
                    if kolona + 1 <= 7 and (tabla[novi_red][kolona+1] == "." or tabla[novi_red][kolona+1] == protivnik):
                        potezi.append((
                            f"{kolone_slova[kolona]}{8 - red}",
                            f"{kolone_slova[kolona+1]}{8 - novi_red}"
                        ))
    return potezi


def odigraj_potez(tabla, potez):
    nova_tabla = [red.copy() for red in tabla]
    (red1, kol1) = oznaka_u_indeks(potez[0])
    (red2, kol2) = oznaka_u_indeks(potez[1])
    nova_tabla[red2][kol2] = nova_tabla[red1][kol1]
    nova_tabla[red1][kol1] = '.'
    return nova_tabla

def proveri_pobednika(tabla):
    for kol in range(8):
        if tabla[7][kol] == 'B':
            return 'B'
        if tabla[0][kol] == 'W':
            return 'W'
    return None


def evaluacija(tabla, igrac):
    protivnik = "W" if igrac == "B" else "B"
    pobednik = proveri_pobednika(tabla)

    if pobednik == igrac:
        return 100000
    if pobednik == protivnik:
        return -100000

    broj_figura = 0
    napredak = 0
    centar = 0
    pretnje = 0
    blokade = 0
    protivnicki_napredak = 0
    moguce_jedenje = 0

    for red in range(8):
        for kolona in range(8):
            if tabla[red][kolona] == igrac:
                broj_figura += 1
                smer = 1 if igrac == "B" else -1
                red_ispred = red + smer

                napredak += red_ispred if igrac == "B" else (7 - red_ispred)

                if 2 <= red <= 5 and 2 <= kolona <= 5:
                    centar += 1

                for promena_kolone in [-1, 1]:
                    nova_kolona = kolona + promena_kolone
                    if 0 <= red_ispred < 8 and 0 <= nova_kolona < 8:
                        if tabla[red_ispred][nova_kolona] == protivnik:
                            moguce_jedenje += 1
                        elif tabla[red_ispred][nova_kolona] == '.':
                            napredak += 1

                if 0 <= red_ispred < 8:
                    if tabla[red_ispred][kolona] == '.':
                        napredak += 2
                    elif tabla[red_ispred][kolona] == protivnik:
                        blokade += 1

                for promena_kolone in [-1, 1]:
                    nova_kolona = kolona + promena_kolone
                    protivnik_red = red - smer
                    if 0 <= protivnik_red < 8 and 0 <= nova_kolona < 8:
                        if tabla[protivnik_red][nova_kolona] == protivnik:
                            pretnje += 1

            elif tabla[red][kolona] == protivnik:
                broj_figura -= 1
                smer_p = -1 if igrac == "B" else 1
                red_ispred = red + smer_p
                for promena_kolone in [-1, 0, 1]:
                    nova_kolona = kolona + promena_kolone
                    if 0 <= red_ispred < 8 and 0 <= nova_kolona < 8:
                        if tabla[red_ispred][nova_kolona] == '.':
                            protivnicki_napredak += 1
                        elif (igrac == "B" and red_ispred == 7) or (igrac == "W" and red_ispred == 0):
                            protivnicki_napredak += 10

    score = (
        broj_figura * 10 +
        napredak * 6 +
        centar * 3 +
        moguce_jedenje * 12 -
        pretnje * 15 -
        blokade * 8 -
        protivnicki_napredak * 10
    )

    return score

def sortiraj_poteze(tabla, potezi, igrac):

    def vrednost_poteza(potez):
        nova_tabla = odigraj_potez(tabla, potez)
        return evaluacija(nova_tabla, igrac)

    return sorted(
        potezi,
        key=lambda potez: (vrednost_poteza(potez), potez[0], potez[1]),
        reverse=True
    )


def tabla_kljuc(tabla, igrac):
    return (tuple(tuple(red) for red in tabla), igrac)


def sacuvaj_hashmapu(hash_mapa, ime_fajla="hash.json"):

    with open(ime_fajla, "w") as fajl:
        json.dump({str(kljuc): vrednost for kljuc, vrednost in hash_mapa.items()}, fajl)

def ucitaj_hashmapu(ime_fajla="hash.json"):
    if not os.path.exists(ime_fajla) or os.path.getsize(ime_fajla) == 0:
        return {}
    with open(ime_fajla, "r") as f:
        json_map = json.load(f)

    return {ast.literal_eval(kljuc): tuple(vrednost) if isinstance(vrednost, list) else vrednost for kljuc, vrednost in json_map.items()}


def minimax(tabla, dubina, alfa, beta, max_igrac, igrac, hash_mapa, end_time=None):

    if end_time and time.time() > end_time:
        return evaluacija(tabla, max_igrac)

    kljuc = tabla_kljuc(tabla, igrac)
    if kljuc in hash_mapa:
        return evaluacija(tabla, max_igrac)

    pobednik = proveri_pobednika(tabla)

    if dubina == 0 or pobednik:
        vrednost = evaluacija(tabla, max_igrac)
        return vrednost

    potezi = generisi_poteze(tabla, igrac)
    if not potezi:
        vrednost = -10000 if igrac == max_igrac else 10000
        return vrednost

    protivnik = "W" if igrac == "B" else "B"

    if igrac == max_igrac:
        najbolja = -10000
        for potez in potezi:
            nova = odigraj_potez(tabla, potez)
            val = minimax(nova, dubina - 1, alfa, beta, max_igrac, protivnik, hash_mapa, end_time)
            najbolja = max(najbolja, val)
            alfa = max(alfa, val)
            if beta <= alfa:
                break
    else:
        najbolja = 10000
        for potez in potezi:
            nova = odigraj_potez(tabla, potez)
            val = minimax(nova, dubina - 1, alfa, beta, max_igrac, protivnik, hash_mapa, end_time)
            najbolja = min(najbolja, val)
            beta = min(beta, val)
            if beta <= alfa:
                break

    return najbolja

def odaberi_ai_potez(tabla, igrac, max_vreme=3.0):

    hash_mapa = ucitaj_hashmapu()
    kljuc = tabla_kljuc(tabla, igrac)

    if kljuc in hash_mapa:
        return hash_mapa[kljuc]

    potezi = generisi_poteze(tabla, igrac)
    if not potezi:
        return None

    potezi = sortiraj_poteze(tabla, potezi, igrac)
    najbolji = potezi[0]
    end_time = time.time() + max_vreme

    dubina = 1

    while time.time() < end_time:

        trenutni_najbolji = None
        najbolja_v = -10000
        protivnik = "W" if igrac == "B" else "B"

        for potez in potezi:
            if time.time() > end_time:
                break
            nova_tabla = odigraj_potez(tabla, potez)

            vrednost = minimax(
                nova_tabla,
                dubina,
                alfa=-10000,
                beta=10000,
                max_igrac=igrac,
                igrac=protivnik,
                hash_mapa=hash_mapa,
                end_time=end_time
            )

            if vrednost > najbolja_v:
                najbolja_v = vrednost
                trenutni_najbolji = potez

        if trenutni_najbolji:
            najbolji = trenutni_najbolji

        dubina += 1

    hash_mapa[kljuc] = najbolji
    sacuvaj_hashmapu(hash_mapa)

    return najbolji


def igra():

    tabla = napravi_tablu()
    igrac = "W"
    poslednji = None

    sirina = 26

    print("\n  " + "=" * sirina)
    print("BREAKTHROUGH".center(sirina+3))
    print("  "+"=" * sirina)
    print()

    while True:

        prikazi_tablu(tabla, poslednji)
        pobednik = proveri_pobednika(tabla)
        if pobednik:
            if pobednik == "W":
                print("\nCONGRATULATIONS! YOU ARE A WINNER!")
            else:
                print("\nGAME OVER. AI WON. BETTER LUCK NEXT TIME.")
            break

        potezi = generisi_poteze(tabla, igrac)
        if not potezi:
            if igrac == "W":
                pobednik = "B"
            else:
                pobednik = "W"
            if pobednik == "W":
                print("\nCONGRATULATIONS! YOU ARE A WINNER!")
                print("No valid moves for AI.")
            else:
                print("\nGAME OVER. BETTER LUCK NEXT TIME.")
                print("No valid moves for you.")
            break

        if igrac == "W":

            figure_sa_potezima = {}
            for potez in potezi:
                start, kraj = potez
                if start not in figure_sa_potezima:
                    figure_sa_potezima[start] = []
                figure_sa_potezima[start].append(potez)

            print("\nAVAILABLE TO MOVE: ")
            for i, figura in enumerate(figure_sa_potezima.keys()):
                print(f"{i+1}. {figura}")

            while True:

                izbor = input("\nCHOICE (NUMBER): ")
                if izbor.isdigit():
                    broj = int(izbor) - 1
                    if 0 <= broj < len(figure_sa_potezima):
                        izabrana_figura = list(figure_sa_potezima.keys())[broj]
                        break
                print("\nINVALID CHOICE")


            moguci_potezi = figure_sa_potezima[izabrana_figura]
            oznacena = set()

            for start, kraj in moguci_potezi:
                oznacena.add(oznaka_u_indeks(kraj))

            prikazi_tablu(tabla, poslednji, oznacena)

            print(f"\nAVAILABLE MOVES FOR FIGURE {izabrana_figura} :")
            for i, potez in enumerate(moguci_potezi):
                print(f"{i+1}. {potez[0]} -> {potez[1]}")

            while True:
                izbor = input("\nCHOICE (NUMBER): ")
                if izbor.isdigit():
                    broj = int(izbor) - 1
                    if 0 <= broj < len(moguci_potezi):
                        potez = moguci_potezi[broj]
                        break
                print("\nINVALID CHOICE")

        else:

            print("\nAI IS THINKING. BE PATIENT.")
            start = time.time()
            potez = odaberi_ai_potez(tabla, igrac, max_vreme=3.0)
            kraj = time.time()
            if potez:
                print(f"\nAI MOVE: {potez[0]} -> {potez[1]}")
                print(f"\nAI THINKING TIME: {kraj - start:.2f} SECONDS\n")
            else:
                print("NO AI MOVES AVAILABLE.")
                break

        tabla = odigraj_potez(tabla, potez)
        poslednji = potez
        igrac = "B" if igrac == "W" else "W"

if __name__ == "__main__":
    igra()