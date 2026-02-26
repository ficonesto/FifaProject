import psycopg2
import pandas as pd
import streamlit as st


DATABASE_URL = st.secrets["DATABASE_URL"]


# ────────────────────────────────────────────────
#    CACHE + SIGLETON VEZA
# ────────────────────────────────────────────────

@st.cache_resource
def get_db_connection():
    """Jedna veza za cijelu app, refresh ako pukne"""
    return psycopg2.connect(DATABASE_URL)


def get_cursor():
    conn = get_db_connection()
    # Provjera je li veza živa (Postgres način)
    if conn.closed != 0:
        st.cache_resource.clear()
        conn = get_db_connection()
    return conn, conn.cursor()


# ────────────────────────────────────────────────
#    HELPERI ZA DB OPERACIJE
# ────────────────────────────────────────────────

def db_exec(query, params=(), commit=False, returning=False):
    """Izvrši INSERT/UPDATE/DELETE, opciono vraća RETURNING"""
    conn = None
    cur = None
    try:
        conn, cur = get_cursor()
        cur.execute(query, params)
        if commit:
            conn.commit()
        if returning:
            return cur.fetchone()[0]
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        st.error(f"DB greška: {query[:80]}... → {str(e)}")
        return False
    finally:
        if cur:
            cur.close()


def db_fetch(query, params=(), one=False):
    """SELECT → vraća tuple/listu ili None"""
    conn = None
    cur = None
    try:
        conn, cur = get_cursor()
        cur.execute(query, params)
        if one:
            return cur.fetchone()
        return cur.fetchall()
    except Exception as e:
        st.error(f"DB fetch greška: {str(e)}")
        return None
    finally:
        if cur:
            cur.close()


def db_fetch_df(query, params=()):
    """SELECT → direktno pandas DataFrame"""
    try:
        conn, cur = get_cursor()           # osigurava validnu vezu
        df = pd.read_sql(query, conn, params=params)
        return df
    except Exception as e:
        st.error(f"Greška pri čitanju u DataFrame: {str(e)}")
        return pd.DataFrame()
    finally:
        if 'cur' in locals() and cur:
            cur.close()


# ────────────────────────────────────────────────
#    IGRAČI
# ────────────────────────────────────────────────

def dodaj_igraca(ime, korisnik_id, aktivan=True):
    success = db_exec(
        "INSERT INTO igraci (ime, korisnik_id, aktivan) VALUES (%s, %s, %s)",
        (ime, int(korisnik_id), aktivan),
        commit=True
    )
    return success, "Igrač dodan!"


def dohvati_sve_igrace(korisnik_id):
    df = db_fetch_df(
        "SELECT id, ime, aktivan FROM igraci WHERE korisnik_id = %s ORDER BY id",
        (int(korisnik_id),)
    )
    return df if not df.empty else None


def promjeni_status_igraca(igrac_id, novi_status):
    return db_exec(
        "UPDATE igraci SET aktivan = %s WHERE id = %s",
        (bool(novi_status), int(igrac_id)),
        commit=True
    )


# ────────────────────────────────────────────────
#    KLUBOVI
# ────────────────────────────────────────────────

def dodaj_klub(naziv, korisnik_id, aktivan=True):
    success = db_exec(
        "INSERT INTO klubovi (naziv, korisnik_id, aktivan) VALUES (%s, %s, %s)",
        (naziv, int(korisnik_id), aktivan),
        commit=True
    )
    return success, "Klub dodan!"


def dohvati_sve_klubove(korisnik_id):
    df = db_fetch_df(
        "SELECT id, naziv, aktivan FROM klubovi WHERE korisnik_id = %s ORDER BY id",
        (int(korisnik_id),)
    )
    return df if not df.empty else None


def promjeni_status_kluba(klub_id, novi_status):
    return db_exec(
        "UPDATE klubovi SET aktivan = %s WHERE id = %s",
        (bool(novi_status), int(klub_id)),
        commit=True
    )


# ────────────────────────────────────────────────
#    TIMOVI
# ────────────────────────────────────────────────

def sacuvaj_tim(naziv_tima, lista_igraca, korisnik_id):
    igraci_str = ", ".join(str(x) for x in lista_igraca)
    success = db_exec(
        "INSERT INTO sacuvani_timovi (naziv_tima, igraci, korisnik_id) VALUES (%s, %s, %s)",
        (naziv_tima, igraci_str, int(korisnik_id)),
        commit=True
    )
    if not success:
        st.error("Neuspješno spremanje tima")
    return success


def dohvati_sacuvane_timove(korisnik_id):
    return db_fetch_df(
        "SELECT naziv_tima, igraci FROM sacuvani_timovi WHERE korisnik_id = %s ORDER BY id DESC",
        (int(korisnik_id),)
    )


# ────────────────────────────────────────────────
#    TURNIRI + RASPORED
# ────────────────────────────────────────────────

def kreiraj_turnir(naziv, tip, format_t, sudionici, klubovi_mapa, korisnik_id):
    conn = None
    cur = None
    try:
        conn, cur = get_cursor()

        # 1. Kreiraj turnir i dohvati ID
        cur.execute(
            "INSERT INTO turniri (naziv, tip, format, korisnik_id) VALUES (%s, %s, %s, %s) RETURNING id",
            (naziv, tip, format_t, int(korisnik_id))
        )
        turnir_id = cur.fetchone()[0]

        # 2. Round-robin logika
        sudionici = sudionici[:]  # kopija da ne mijenjamo original
        if len(sudionici) % 2 != 0:
            sudionici.append("SLOBODAN")
            klubovi_mapa["SLOBODAN"] = "N/A"

        n = len(sudionici)
        utakmice = []
        for r in range(n - 1):
            for i in range(n // 2):
                domacin = sudionici[i]
                gost = sudionici[n - 1 - i]
                if domacin != "SLOBODAN" and gost != "SLOBODAN":
                    kd = klubovi_mapa.get(domacin, "Nepoznat klub")
                    kg = klubovi_mapa.get(gost, "Nepoznat klub")
                    utakmice.append((turnir_id, domacin, gost, kd, kg))

            # rotacija
            sudionici = [sudionici[0]] + sudionici[2:] + [sudionici[1]]

        # 3. Dvokružno → dupliraj uzvratne
        if format_t == "Dvokružno":
            uzvrat = [(tid, g, d, kg, kd) for tid, d, g, kd, kg in utakmice]
            utakmice.extend(uzvrat)

        # 4. Ubaci utakmice
        cur.executemany(
            """
            INSERT INTO utakmice
            (turnir_id, domacin, gost, klub_domacin, klub_gost)
            VALUES (%s, %s, %s, %s, %s)
            """,
            utakmice
        )

        # 5. Očisti pripremljene timove
        cur.execute("DELETE FROM sacuvani_timovi WHERE korisnik_id = %s", (int(korisnik_id),))

        conn.commit()
        return True, "Turnir kreiran!"

    except Exception as e:
        if conn:
            conn.rollback()
        st.error(f"Greška pri kreiranju turnira: {str(e)}")
        return False, str(e)
    finally:
        if cur:
            cur.close()


# ────────────────────────────────────────────────
#    OSTALE FUNKCIJE
# ────────────────────────────────────────────────

def dohvati_ljestvicu(turnir_id):
    query = """
        SELECT
            igrac AS "Igrač",
            O AS "Odigrano",
            P AS "Pobjede",
            N AS "Neriješeno",
            I AS "Izgubljeno",
            GZ AS "Postignuti",
            GP AS "Primljeni",
            GR AS "Gol Razlika",
            B AS "Bodovi"
        FROM ljestvica_pogled
        WHERE turnir_id = %s
    """
    return db_fetch_df(query, (int(turnir_id),))


def unesi_rezultat(utakmica_id, g_domacin, g_gost):
    return db_exec(
        """
        UPDATE utakmice
        SET golovi_domacin = %s, golovi_gost = %s, odigrano = TRUE
        WHERE id = %s
        """,
        (int(g_domacin), int(g_gost), int(utakmica_id)),
        commit=True
    )


def dohvati_turnire(korisnik_id):
    rows = db_fetch(
        "SELECT id, naziv FROM turniri WHERE korisnik_id = %s ORDER BY id DESC",
        (int(korisnik_id),)
    )
    return rows or []


def dohvati_utakmice_turnira(turnir_id):
    return db_fetch_df(
        """
        SELECT id, domacin, gost, klub_domacin, klub_gost,
               golovi_domacin, golovi_gost, odigrano
        FROM utakmice
        WHERE turnir_id = %s
        """,
        (int(turnir_id),)
    )


def obrisi_sve_timove(korisnik_id):
    return db_exec(
        "DELETE FROM sacuvani_timovi WHERE korisnik_id = %s",
        (int(korisnik_id),),
        commit=True
    )


def obrisi_povijest_turnira(korisnik_id):
    conn = None
    cur = None
    try:
        conn, cur = get_cursor()
        korisnik_id = int(korisnik_id)

        cur.execute("""
            DELETE FROM utakmice
            WHERE turnir_id IN (SELECT id FROM turniri WHERE korisnik_id = %s)
        """, (korisnik_id,))

        cur.execute("DELETE FROM turniri WHERE korisnik_id = %s", (korisnik_id,))

        cur.execute("DELETE FROM sacuvani_timovi WHERE korisnik_id = %s", (korisnik_id,))

        conn.commit()
        return True, "Povijest obrisana"
    except Exception as e:
        if conn:
            conn.rollback()
        st.error(f"Greška pri brisanju povijesti: {str(e)}")
        return False, str(e)
    finally:
        if cur:
            cur.close()
