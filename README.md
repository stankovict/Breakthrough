# Breakthrough

## Opis projekta
Ovaj projekat implementira igru **Breakthrough** u programskom jeziku Python, u okviru predmeta *Algoritmi i strukture podataka*.  
Cilj igre je da jedan od igrača dovede svoju figuru na početni red protivnika. Igra se na tabli dimenzija 8x8.  

Projekat demonstrira primenu algoritama i struktura podataka kroz:  
- Reprezentaciju table pomoću matrica/lista  
- Manipulaciju figurama pomoću metoda za validaciju i izvršavanje poteza  
- Pretragu stanja igre za AI protivnika (minimax, alfa-beta rezovi, heurističke procene)  
- Upotrebu struktura podataka (liste, nizovi, hash-maps)  

---

## Funkcionalnosti
- Igra protiv računara (AI)  
- Provera validnosti poteza 
- Detekcija kraja igre (pobeda kada figura stigne na protivnički kraj table)  
- Tekstualni prikaz table u konzoli

---

## Pravila igre (ukratko)
1. Igra se na tabli sa dva reda figura po igraču.  
2. Figure se pomeraju samo unapred; jedno polje dijagonalno ili pravo napred.  
3. Dijagonalno igrači takođe mogu uzeti protivničku figuru.
4. Pobednik je onaj igrač koji prvi prebaci figuru na početni red protivnika, ili protivnik ostane bez poteza.  

---

## Tehnologije
- Python 3.x  
- Standardne biblioteke (`random`, `copy`,...)  
