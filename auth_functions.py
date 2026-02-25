# auth_functions.py
import streamlit as st
import bcrypt
from db_operations import db_fetch, db_exec  # ← ovo mora postojati u projektu

# ────────────────────────────────────────────────
#     POMOĆNE FUNKCIJE ZA LOZINKE
# ────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Hashira lozinku koristeći bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def check_password(plain_password: str, hashed_password: str) -> bool:
    """Provjerava da li plain lozinka odgovara hashanoj."""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


# ────────────────────────────────────────────────
#     REGISTRACIJA KORISNIKA
# ────────────────────────────────────────────────

def registriraj_korisnika(korisnicko_ime: str, email: str, lozinka: str):
    """
    Registrira novog korisnika.
    Vraća tuple: (success: bool, poruka: str, user_data: dict | None)
    """
    try:
        # 1. Provjera postoji li već email (case-insensitive)
        postoji = db_fetch(
            "SELECT 1 FROM korisnici WHERE LOWER(email) = LOWER(%s)",
            (email,),
            one=True
        )
        if postoji:
            return False, "Email je već registriran.", None

        # 2. Hash lozinke
        hashed_pw = hash_password(lozinka)

        # 3. Spremanje i dohvaćanje novog ID-a
        user_id = db_exec(
            """
            INSERT INTO korisnici (korisnicko_ime, email, lozinka_hash)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (korisnicko_ime, email, hashed_pw),
            commit=True,
            returning=True
        )

        if user_id is None:
            return False, "Neuspješno spremanje korisnika (nema ID-a).", None

        # 4. Pripremi user_data u istom formatu kao provjeri_login
        user_data = {
            "id": user_id,
            "username": korisnicko_ime
        }

        # Opcionalno: možeš ovdje već postaviti session_state, ali bolje to raditi u app.py
        # st.session_state.authenticated = True
        # st.session_state.user = user_data

        return True, "Registracija uspješna! Dobrodošli.", user_data

    except Exception as e:
        # Možeš dodati logging ako imaš logger
        # logger.error(f"Registracija greška: {str(e)}")
        return False, f"Greška pri registraciji: {str(e)}", None

# ────────────────────────────────────────────────
#     PRIJAVA / PROVJERA LOGINA
# ────────────────────────────────────────────────

def provjeri_login(email, lozinka):
    try:
        row = db_fetch(
            """
            SELECT id, korisnicko_ime, lozinka_hash
            FROM korisnici
            WHERE LOWER(email) = LOWER(%s)
            """,
            (email,),
            one=True
        )
        if row:
            user_id, username, hashed = row
            if bcrypt.checkpw(lozinka.encode('utf-8'), hashed.encode('utf-8')):
                return {"id": user_id, "username": username}
        return None
    except Exception as e:
        st.error(f"Greška pri prijavi: {str(e)}")
        return None

# ────────────────────────────────────────────────
#     ODJAVA (logout) – korisno imati u auth modulu
# ────────────────────────────────────────────────

def odjavi_se():
    """Briše sve iz session_state i osvježava stranicu."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
