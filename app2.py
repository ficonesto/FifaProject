import streamlit as st
import pandas as pd
import bcrypt
from db_operations import (
    dohvati_sve_igrace, dohvati_sve_klubove, sacuvaj_tim,
    dohvati_sacuvane_timove, kreiraj_turnir, dohvati_turnire,
    dohvati_utakmice_turnira, unesi_rezultat, dohvati_ljestvicu,
    obrisi_sve_timove, dodaj_klub, dodaj_igraca, promjeni_status_igraca,
    promjeni_status_kluba, obrisi_povijest_turnira,
    db_fetch   # ← DODAJ OVO
)
from auth_functions import registriraj_korisnika, provjeri_login, odjavi_se
import random
# --- KONFIGURACIJA ---
st.set_page_config(page_title="Athos League", page_icon="🏛️", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #FFD700; font-family: "Arial Black", sans-serif; text-shadow: 2px 2px #000000;'>
        🏆 ATHOS LEAGUE 🏆
    </h1>
    <hr style="border: 1px solid #FFD700;">
""", unsafe_allow_html=True)

# --- INICIJALIZACIJA SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

# --- LOGIN / REGISTRACIJA EKRAN ---
if not st.session_state.authenticated:

    st.title("Dobrodošli u Athos League")

    tab1, tab2 = st.tabs(["Prijava", "Registracija"])

    with tab1:
        with st.form(key="login_form"):
            email = st.text_input("Email")
            lozinka = st.text_input("Lozinka", type="password")
            submit_login = st.form_submit_button("Prijavi se")

            if submit_login:
                if not email.strip() or not lozinka.strip():
                    st.error("Molimo unesite email i lozinku.")
                else:
                    user_data = provjeri_login(email, lozinka)
                    if user_data:
                        st.session_state.authenticated = True
                        st.session_state.user = user_data                   # ← dict sa "id" i "username"
                        st.success(f"Dobrodošao, {user_data['username']}!")
                        st.rerun()
                    else:
                        st.error("Neispravni podaci za prijavu.")

    with tab2:
        with st.form(key="registracija_form", clear_on_submit=True):
            korisnicko_ime = st.text_input("Ime lige / korisničko ime", placeholder="npr. Athos Varaždin")
            email_reg     = st.text_input("Email")
            lozinka_reg   = st.text_input("Lozinka", type="password")
            lozinka_potvrda = st.text_input("Ponovi lozinku", type="password")
            submit_reg    = st.form_submit_button("Registriraj se", use_container_width=True)

            if submit_reg:
                if not all([korisnicko_ime.strip(), email_reg.strip(), lozinka_reg.strip()]):
                    st.error("Sva polja su obavezna.")
                elif lozinka_reg != lozinka_potvrda:
                    st.error("Lozinke se ne podudaraju.")
                elif len(lozinka_reg) < 6:
                    st.error("Lozinka mora imati barem 6 znakova.")
                else:
                # OVDJE IDE TAJ KOD
                    success, msg, user_data = registriraj_korisnika(
                        korisnicko_ime.strip(),
                        email_reg.strip(),
                        lozinka_reg
                    )
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user = user_data
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            

else:
    # --- DASHBOARD (ULOGIRAN KORISNIK) ---
    kid = st.session_state.user['id']
    st.sidebar.title(f"🏛️ {st.session_state.user['username']}")
    st.sidebar.caption(f"ID Lige: #{kid}")
    if st.sidebar.button("Odjavi se"):
        odjavi_se()

    # app.py - Pronađi ovaj dio na početku prikaza (poslije prijave)
    # app2.py - Linija sa tvoje slike
    tab_igraci, tab_klubovi, tab_timovi, tab_turniri, tab_postavke = st.tabs([
    "👤 Igrači", 
    "⚽ Klubovi", 
    "👥 Timovi", 
    "🏆 Turniri",
    "⚙️ Postavke & Stil"
    ])

    # --- TAB 1: UPRAVLJANJE IGRAČIMA ---

# --- TAB 1: UPRAVLJANJE IGRAČIMA ---
    # --- TAB 1: UPRAVLJANJE IGRAČIMA ---
    with tab_igraci:
        st.subheader("🏃 Upravljanje ljudstvom")
        
        df_i = dohvati_sve_igrace(kid)
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.markdown("### Dodaj igrača")
            with st.form("forma_novi_igrac", clear_on_submit=True):
                n_ime = st.text_input("Ime i prezime").strip()
                n_aktivan = st.checkbox("Igrač je aktivan", value=True)
                
                if st.form_submit_button("Spremi u bazu"):
                    if n_ime:
                        # Inicijaliziramo zastavicu za prolaz
                        moze_upis = True
                        
                        # Provjera duplikata
                        if df_i is not None and not df_i.empty:
                            postojeca_imena = [ime.lower() for ime in df_i['ime'].tolist()]
                            if n_ime.lower() in postojeca_imena:
                                st.error(f"❌ Igrač '{n_ime}' već postoji!")
                                moze_upis = False # Ne prekidamo skriptu, samo blokiramo upis
                        
                        if moze_upis:
                            uspjeh, poruka = dodaj_igraca(n_ime, kid, n_aktivan)
                            if uspjeh:
                                st.success(f"✅ Igrač {n_ime} spremljen!")
                                st.rerun()
                            else:
                                st.error(f"Greška baze: {poruka}")
                    else:
                        st.warning("⚠️ Ime ne može biti prazno!")
        
        with c2:
            st.markdown("### Popis igrača")
            # Čak i ako gore izađe error, ovaj dio koda se sada izvršava
            if df_i is not None and not df_i.empty:
                uredjeni_df = st.data_editor(
                    df_i[['id', 'ime', 'aktivan']], 
                    width="stretch", 
                    hide_index=True,
                    disabled=["id", "ime"],
                    key="editor_igraci"
                )
                
                # ... ostatak logike za editor ...
                # Hvatanje promjena u kvačicama
                if st.session_state.editor_igraci["edited_rows"]:
                    for row_idx, changes in st.session_state.editor_igraci["edited_rows"].items():
                        if "aktivan" in changes:
                            pravi_id = int(df_i.iloc[row_idx]['id']) 
                            novi_status = changes["aktivan"]
                            promjeni_status_igraca(pravi_id, novi_status)
                            st.rerun()
                
                st.caption("💡 Klikni na kvačicu za aktivaciju/deaktivaciju igrača.")
            else:
                st.info("Još nemaš dodanih igrača.")

    # --- TAB 2: UPRAVLJANJE KLUBOVIMA ---
    with tab_klubovi:
        st.subheader("🛡️ Upravljanje klubovima")
        df_k = dohvati_sve_klubove(kid)
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("### Dodaj klub")
            with st.form("forma_novi_klub", clear_on_submit=True):
                n_naziv = st.text_input("Naziv kluba").strip()
                n_aktivan_k = st.checkbox("Klub je aktivan", value=True)
                
                if st.form_submit_button("Spremi klub"):
                    if n_naziv:
                        moze_upis_k = True
                        if df_k is not None and not df_k.empty:
                            postojeci_klubovi = [k.lower() for k in df_k['naziv'].tolist()]
                            if n_naziv.lower() in postojeci_klubovi:
                                st.error(f"❌ Klub '{n_naziv}' već postoji!")
                                moze_upis_k = False
                        
                        if moze_upis_k:
                            uspjeh, poruka = dodaj_klub(n_naziv, kid, n_aktivan_k)
                            if uspjeh:
                                st.success(f"✅ Klub {n_naziv} dodan!")
                                st.rerun()
                            else:
                                st.error(f"Greška: {poruka}")
                    else:
                        st.warning("⚠️ Naziv kluba ne može biti prazan!")
        
        with c2:
            st.markdown("### Popis klubova")
            if df_k is not None and not df_k.empty:
                # Koristimo data_editor za brzu aktivaciju/deaktivaciju
                uredjeni_k = st.data_editor(
                    df_k[['id', 'naziv', 'aktivan']], 
                    width="stretch", hide_index=True,
                    disabled=["id", "naziv"], key="editor_klubovi"
                )
                
                # Update statusa bez prekidanja teme
                if st.session_state.editor_klubovi["edited_rows"]:
                    for row_idx, changes in st.session_state.editor_klubovi["edited_rows"].items():
                        if "aktivan" in changes:
                            pravi_id = int(df_k.iloc[row_idx]['id'])
                            novi_status = changes["aktivan"]
                            promjeni_status_kluba(pravi_id, novi_status)
                            st.rerun()
                
                # Hvatanje promjena za klubove
                if st.session_state.editor_klubovi["edited_rows"]:
                    for row_idx, changes in st.session_state.editor_klubovi["edited_rows"].items():
                        if "aktivan" in changes:
                            # KLJUČNO: int() rješava numpy.int64 grešku
                            pravi_id_k = int(df_k.iloc[row_idx]['id'])
                            novi_status_k = changes["aktivan"]
                            promjeni_status_kluba(pravi_id_k, novi_status_k)
                            st.rerun()
                
                st.caption("💡 Isključeni klubovi neće se nuditi pri kreiranju turnira.")
            else:
                st.info("Nema registriranih klubova.")
# --- TAB 3: KREIRANJE TIMOVA ---
    # --- TAB 3: TIMOVI ---
    with tab_timovi:
        st.header("👥 Generator Athos Ekipa")
    
    # Dohvat podataka
        df_i = dohvati_sve_igrace(kid)
        df_k = dohvati_sve_klubove(kid)
    
        if df_i is not None and df_k is not None:
            aktivni_imena = df_i[df_i['aktivan'] == True]['ime'].tolist()
            aktivni_klubovi = df_k[df_k['aktivan'] == True]['naziv'].tolist()

            izbor_nacina = st.radio("Odaberi način kreiranja:", ["Automatski (Random)", "Ručno uparivanje"])

            if izbor_nacina == "Automatski (Random)":
                st.subheader("🎲 Automatsko miješanje")
                col1, col2 = st.columns(2)
                with col1:
                    sudionici = st.multiselect("Tko sve igra danas?", aktivni_imena)
                with col2:
                    broj_ljudi_u_timu = st.number_input("Broj igrača po jednom timu:", 1, 5, 2)

                if st.button("🔀 Generiraj i dodijeli klubove", use_container_width=True):
                    if len(sudionici) < 2:
                        st.error("Nedovoljno igrača za turnir!")
                    elif len(aktivni_klubovi) < (len(sudionici) // broj_ljudi_u_timu):
                        st.error("Nemaš dovoljno aktivnih klubova u bazi za ovaj broj timova!")
                    else:
                        obrisi_sve_timove(kid) # Čistimo staro
                        random.shuffle(sudionici) # Miješamo ljude
                        random.shuffle(aktivni_klubovi) # Miješamo klubove
                    
                        broj_timova = len(sudionici) // broj_ljudi_u_timu
                    
                        for t in range(broj_timova):
                        # Uzimamo grupu ljudi
                            start = t * broj_ljudi_u_timu
                            end = start + broj_ljudi_u_timu
                            grupa_igraca = sudionici[start:end]
                        
                        # Spajamo ih u string "Igrač 1, Igrač 2"
                            imena_str = ", ".join(grupa_igraca)
                            odabrani_klub = aktivni_klubovi[t] # Uzimamo t-ti klub iz promiješane liste
                        
                            sacuvaj_tim(imena_str, [odabrani_klub], kid)
                    
                    # Provjera ako je ostao netko "viška" (npr. 5 igrača, a timovi su po 2)
                        visak = sudionici[broj_timova * broj_ljudi_u_timu:]
                        if visak:
                            st.warning(f"Igrači koji su ostali bez tima (višak): {', '.join(visak)}")
                    
                        st.success(f"Generirano {broj_timova} timova!")
                        st.rerun()

            else:
                st.subheader("✍️ Ručno kreiranje tima")
                with st.form("rucna_forma"):
                    c1, c2 = st.columns(2)
                    with c1:
                        m_igraci = st.multiselect("Odaberi igrače za ovaj tim:", aktivni_imena)
                    with c2:
                        m_klub = st.selectbox("Odaberi klub:", aktivni_klubovi)
                
                    if st.form_submit_button("Spremi ovaj tim"):
                        if m_igraci and m_klub:
                            sacuvaj_tim(", ".join(m_igraci), [m_klub], kid)
                            st.rerun()

    # --- PRIKAZ I BRISANJE ---
        st.divider()
        df_st = dohvati_sacuvane_timove(kid)
        if not df_st.empty:
            st.subheader("📋 Prijavljeni timovi")
            st.dataframe(df_st[['naziv_tima', 'igraci']], use_container_width=True, hide_index=True,
                         column_config={"naziv_tima": "Igrači u timu", "igraci": "Klub"})
            if st.button("🗑️ Obriši sve", type="secondary"):
                obrisi_sve_timove(kid)
                st.rerun()

    # --- TAB 4: TURNIRI ---
    with tab_turniri:
        st.markdown(f"<h2 style='text-align: center;'>🏆 Athos Arena</h2>", unsafe_allow_html=True)

        # 1. Dohvaćanje turnira
        turniri_lista = dohvati_turnire(kid)

        # Navigacija: Novi turnir ili Pregled aktivnog
        izbor = st.radio("Upravljanje turnirima:", ["⚽ Aktivno natjecanje", "➕ Nova sezona"], horizontal=True)

        if izbor == "➕ Nova sezona":
            st.subheader("Postavke turnira")
            df_priprema = dohvati_sacuvane_timove(kid)
            
            if df_priprema is not None and not df_priprema.empty:
                with st.expander("🔍 Pregledaj sudionike prije početka"):
                    st.dataframe(df_priprema[['naziv_tima', 'igraci']], use_container_width=True, hide_index=True)
                
                with st.form("forma_novi_turnir"):
                    naziv_t = st.text_input("Naziv lige:", value=f"Athos Liga {pd.Timestamp.now().strftime('%d.%m.')}")
                    format_t = st.selectbox("Format:", ["Jednokružno", "Dvokružno"])
                    
                    if st.form_submit_button("🚀 POKRENI LIGU", use_container_width=True):
                        sudionici = df_priprema['naziv_tima'].tolist()
                        klubovi_mapa = dict(zip(df_priprema['naziv_tima'], df_priprema['igraci']))
                        
                        uspjeh, poruka = kreiraj_turnir(naziv_t, "Liga", format_t, sudionici, klubovi_mapa, kid)
                        if uspjeh:
                            st.success("⚽ Liga je uspješno kreirana!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(poruka)
            else:
                st.warning("⚠️ Prvo moraš generirati timove u tabu 'Timovi'!")

        else:
            # --- UŠMINKANI PRIKAZ AKTIVNOG TURNIRA ---
            if turniri_lista:
                imena_turnira = {t[1]: t[0] for t in turniri_lista}
                odabrani_naziv = st.selectbox("Odaberi aktivno natjecanje:", list(imena_turnira.keys()))
                t_id = imena_turnira[odabrani_naziv]

                s_tab1, s_tab2 = st.tabs(["📊 Tablica Poretka", "🏟️ Unos Rezultata"])

                with s_tab1:
                    df_ljestvica = dohvati_ljestvicu(t_id)
                    if df_ljestvica is not None and not df_ljestvica.empty:
                        # Ovim brišemo nulu i stavljamo da kreće od 1
                        df_ljestvica.index = range(1, len(df_ljestvica) + 1)
                        
                        st.dataframe(
                            df_ljestvica,
                            use_container_width=True,
                            column_config={
                                "sudionik": "Igrač",
                                "utakmica": "OU",
                                "bodovi": "Bod",
                                "postignuti": "G+",
                                "primljeni": "G-",
                                "gol_razlika": "GR"
                            }
                        )
                with s_tab2:
                    df_utakmice = dohvati_utakmice_turnira(t_id)
                    if df_utakmice is not None and not df_utakmice.empty:
                        neodigrano = df_utakmice[df_utakmice['odigrano'] == False]
                        
                        if not neodigrano.empty:
                            for idx, row in neodigrano.iterrows():
                                # Ušminkani red za svaku utakmicu
                                with st.container(border=True):
                                    st.markdown(f"**{row['domacin']}** vs **{row['gost']}**")
                                    st.caption(f"🎮 {row['klub_domacin']} 🆚 {row['klub_gost']}")
                                    
                                    c1, c2, c3 = st.columns([1, 1, 1])
                                    with c1:
                                        g_d = st.number_input(f"Golovi D", 0, 20, key=f"d_{row['id']}")
                                    with c2:
                                        g_g = st.number_input(f"Golovi G", 0, 20, key=f"g_{row['id']}")
                                    with c3:
                                        st.write("") # Spacer
                                        if st.button("Spremi", key=f"b_{row['id']}", use_container_width=True, type="primary"):
                                            if unesi_rezultat(row['id'], g_d, g_g):
                                                st.rerun()
                        else:
                            st.success("🎉 Sve utakmice su odigrane!")

                        # Pregled povijesti (zadnjih par rezultata)
                        with st.expander("📜 Povijest odigranih susreta"):
                            odigrane = df_utakmice[df_utakmice['odigrano'] == True]
                            if not odigrane.empty:
                                prikaz_povijest = odigrane[['domacin', 'golovi_domacin', 'golovi_gost', 'gost']].copy()
                                prikaz_povijest.index = range(1, len(prikaz_povijest) + 1)
                                
                                st.dataframe(
                                    prikaz_povijest,
                                    use_container_width=True,
                                    column_config={
                                        "domacin": "Domaćin",
                                        "golovi_domacin": "D",
                                        "golovi_gost": "G",
                                        "gost": "Gost"
                                    }
                                )
            else:
                st.info("Nema aktivnih turnira. Kreni na opciju 'Nova sezona'!")

    #---Tab 5: Postavke---
    with tab_postavke:
        st.markdown("<h3 style='text-align: center;'>🎨 Postavke Sučelja</h3>", unsafe_allow_html=True)

        opcije_tema = [
            "Dark Sport (Athos)", 
            "Athos Gold", 
            "Sofascore Night", 
            "Red Devils", 
            "Ice Pitch (Svijetla)"
    ]

        tema = st.selectbox("Izaberi temu:", opcije_tema, key="tema_izbor")

    # ---------------- BOJE ----------------
        if tema == "Ice Pitch (Svijetla)":
            bg, text, accent, card_bg = "#F0F2F6", "#1E293B", "#0EA5E9", "#FFFFFF"
            btn_text = "#FFFFFF"

        elif tema == "Athos Gold":
            bg, text, accent, card_bg = "#0A0A0A", "#D4AF37", "#D4AF37", "#151515"
            btn_text = "#000000"

        elif tema == "Dark Sport (Athos)":
            bg, text, accent, card_bg = "#050A0E", "#FFFFFF", "#00FF66", "#0B161E"
            btn_text = "#000000"

        elif tema == "Red Devils":
            bg, text, accent, card_bg = "#0E0E0E", "#FFFFFF", "#E31B23", "#1A1A1A"
            btn_text = "#FFFFFF"

        else:  # Sofascore Night
            bg, text, accent, card_bg = "#121921", "#FFFFFF", "#0073E6", "#1A242D"
            btn_text = "#FFFFFF"

    # ---------------- GLOBALNI CSS FIX ----------------
        st.markdown(f"""
<style>

/* ================= BACKGROUND ================= */

.stApp {{
    background-color: {bg} !important;
}}

/* ================= BODY TEXT FIX (uklanja sivilo) ================= */

section.main, 
section.main p, 
section.main span, 
section.main div {{
    color: {text} !important;
    opacity: 1 !important;
}}

/* ================= BUTTONS ================= */

div.stButton > button,
div.stDownloadButton > button,
div[data-testid="stFormSubmitButton"] > button {{
    background-color: {accent} !important;
    color: {btn_text} !important;
    border: 2px solid {accent} !important;
    border-radius: 8px !important;
    font-weight: 800 !important;
    padding: 0.5rem 1rem !important;
}}

div.stButton > button:hover,
div.stDownloadButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {{
    opacity: 0.9 !important;
    transform: scale(1.02);
    transition: 0.15s ease-in-out;
}}

/* ================= INPUT POLJA ================= */

input[type="text"],
input[type="number"],
textarea {{
    background-color: {card_bg} !important;
    color: {text} !important;
    -webkit-text-fill-color: {text} !important;
    border: 1px solid {accent} !important;
    border-radius: 6px !important;
}}

/* ================= DROPDOWN (white clean style) ================= */

div[data-baseweb="select"] > div {{
    background-color: white !important;
    color: {accent} !important;
    border: 1px solid {accent} !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
}}

div[data-baseweb="popover"] {{
    background-color: white !important;
}}

li[role="option"] {{
    color: {accent} !important;
    font-weight: 500 !important;
}}

li[role="option"]:hover {{
    background-color: {accent} !important;
    color: {btn_text} !important;
}}

/* ================= KARTICE ================= */

[data-testid="stVerticalBlockBorderWrapper"] {{
    background-color: {card_bg} !important;
    border: 1px solid {accent} !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}}

/* ================= TABOVI ================= */

.stTabs [data-baseweb="tab"] p {{
    color: {text} !important;
    opacity: 0.6 !important;
    font-weight: 600;
}}

.stTabs [aria-selected="true"] p {{
    color: {accent} !important;
    opacity: 1 !important;
}}

.stTabs [aria-selected="true"] {{
    border-bottom: 3px solid {accent} !important;
}}

/* ================= HEADER ================= */

[data-testid="stHeader"] {{
    background: transparent !important;
}}
/* ===== ULTRA BODY TEXT FIX ===== */

section.main * {{
    color: {text} !important;
}}

section.main p,
section.main span,
section.main label,
section.main div {{
    color: {text} !important;
    opacity: 1 !important;
}}

/* ubijanje rgba varijabli */
:root {{
    --text-color: {text} !important;
}}

/* BaseWeb override */
[data-testid="stMarkdownContainer"] * {{
    color: {text} !important;
    opacity: 1 !important;
}}
/* SPECIFIČAN FIX ZA TEXT U GUMBIMA - POBJEĐUJE ULTRA FIX */
div.stButton > button p, 
div.stButton > button div, 
div.stButton > button span {{
    color: {btn_text} !important;
}}

/* Fix za Form gumbe */
div[data-testid="stFormSubmitButton"] > button p,
div[data-testid="stFormSubmitButton"] > button span {{
    color: {btn_text} !important;
}}
</style>
""", unsafe_allow_html=True)
        # 1. Postojeći gumb za Tab 3
        st.markdown("---")
        if st.button("🗑️ Resetiraj samo Tab 3 (Priprema)", use_container_width=True):
            obrisi_sve_timove(kid)
            st.success("Priprema timova je očišćena.")
            st.rerun()

        st.write("") # Malo razmaka

        # 2. NOVI GUMB: Resetiranje cijele povijesti turnira
        if st.button("🚨 OBRIŠI SVU POVIJEST TURNIRA", use_container_width=True):
            st.session_state.confirm_nuke = True

        if st.session_state.get('confirm_nuke', False):
            st.error("⚠️ Jeste li sigurni?")
            c1, c2 = st.columns(2)
        
            with c1:
                # Dodajemo mali trik: gumb direktno poziva funkciju
                if st.button("✅ DA, BRIŠI SVE", key="nuke_confirm_btn"):
                    uspjeh, poruka = obrisi_povijest_turnira(kid)
                    if uspjeh:
                        st.session_state.confirm_nuke = False # Resetiramo stanje
                        st.success("Sve obrisano!")
                        st.rerun() # Prisilno osvježavanje da dropdown nestane
                    else:
                        st.error(poruka)
        
            with c2:
                if st.button("❌ ODUSTANI", key="nuke_cancel_btn"):
                    st.session_state.confirm_nuke = False
                    st.rerun()
