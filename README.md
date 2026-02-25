# ⚽ FifaTurnir

Web aplikacija za upravljanje FIFA turnirima s podrškom za više korisnika.  
A multi-user web application for managing FIFA tournaments.

---

## 🇭🇷 Funkcionalnosti

- Registracija i login korisnika (hashirane lozinke)
- Multi-user model (svaki korisnik vidi svoje podatke)
- Kreiranje igrača, klubova, timova i turnira
- Automatska raspodjela timova bez ponavljanja
- Generiranje kola i utakmica
- Unos rezultata uz validaciju
- Automatsko računanje bodova i poretka
- Povijest turnira
- Connection pooling za PostgreSQL bazu

---

## 🇬🇧 Features

- User registration and login (password hashing)
- Multi-user architecture (data isolation per user)
- Creation of players, clubs, teams and tournaments
- Automatic team distribution without repetition
- Match and round generation
- Result input with validation
- Automatic standings calculation
- Tournament history
- PostgreSQL connection pooling

---

## ⚙️ Pokretanje / Running locally

1. Kloniraj repozitorij / Clone the repository:

```bash
git clone https://github.com/tvoj-username/fifaturnir.git
cd fifaturnir
```

2. Kreiraj virtualno okruženje / Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

3. Instaliraj ovisnosti / Install dependencies:

```bash
pip install -r requirements.txt
```

4. Postavi environment varijablu za bazu / Set database environment variable:

```bash
export DATABASE_URL="postgresql://..."
```

5. Pokreni aplikaciju / Run the app:

```bash
streamlit run app2.py
```

---

## 🗄 Baza podataka / Database

Aplikacija koristi PostgreSQL bazu (npr. Supabase).  
Potrebno je postaviti vlastiti `DATABASE_URL` prije pokretanja.

The application uses a PostgreSQL database (e.g. Supabase).  
You must configure your own `DATABASE_URL` before running.
