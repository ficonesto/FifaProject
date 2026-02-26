import streamlit as st
import pandas as pd
import bcrypt
from db_operations import (
    dohvati_sve_igrace, dohvati_sve_klubove, sacuvaj_tim,
    dohvati_sacuvane_timove, kreiraj_turnir, dohvati_turnire,
    dohvati_utakmice_turnira, unesi_rezultat, dohvati_ljestvicu,
    obrisi_sve_timove, dodaj_klub, dodaj_igraca, promjeni_status_igraca,
    promjeni_status_kluba, obrisi_povijest_turnira,
    db_fetch
)
from auth_functions import registriraj_korisnika, provjeri_login, odjavi_se
from translations import t, language_toggle_buttons
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

    # Gumbi za jezik i na login ekranu (sidebar)
    language_toggle_buttons()

    st.title(t("welcome"))

    tab1, tab2 = st.tabs([t("login_tab"), t("register_tab")])

    with tab1:
        with st.form(key="login_form"):
            email = st.text_input(t("email"))
            lozinka = st.text_input(t("password"), type="password")
            submit_login = st.form_submit_button(t("login_btn"))

            if submit_login:
                if not email.strip() or not lozinka.strip():
                    st.error(t("login_empty"))
                else:
                    user_data = provjeri_login(email, lozinka)
                    if user_data:
                        st.session_state.authenticated = True
                        st.session_state.user = user_data
                        st.success(t("login_success", user_data['username']))
                        st.rerun()
                    else:
                        st.error(t("login_fail"))

    with tab2:
        with st.form(key="registracija_form", clear_on_submit=True):
            korisnicko_ime = st.text_input(t("username_label"), placeholder=t("username_placeholder"))
            email_reg      = st.text_input(t("email"))
            lozinka_reg    = st.text_input(t("password"), type="password")
            lozinka_potvrda = st.text_input(t("password_repeat"), type="password")
            submit_reg     = st.form_submit_button(t("register_btn"), use_container_width=True)

            if submit_reg:
                if not all([korisnicko_ime.strip(), email_reg.strip(), lozinka_reg.strip()]):
                    st.error(t("reg_fields_required"))
                elif lozinka_reg != lozinka_potvrda:
                    st.error(t("reg_pw_mismatch"))
                elif len(lozinka_reg) < 6:
                    st.error(t("reg_pw_short"))
                else:
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
    st.sidebar.caption(t("sidebar_id", kid))
    if st.sidebar.button(t("logout_btn")):
        odjavi_se()

    # Gumbi za promjenu jezika u sidebaru
    language_toggle_buttons()

    # ── TEMA: čitamo iz session_state i primjenjujemo CSS globalno na svakom rerunu ──
    # Koristimo zasebni ključ "active_tema" koji nije vezan uz widget,
    # tako da st.rerun() ne može resetirati temu.
    if "active_tema" not in st.session_state:
        st.session_state["active_tema"] = "Dark Sport (Athos)"
    _tema = st.session_state["active_tema"]

    if _tema == "Ice Pitch (Svijetla)":
        _bg, _text, _accent, _card_bg, _btn_text = "#F0F2F6", "#1E293B", "#0EA5E9", "#FFFFFF", "#FFFFFF"
    elif _tema == "Athos Gold":
        _bg, _text, _accent, _card_bg, _btn_text = "#0A0A0A", "#D4AF37", "#D4AF37", "#151515", "#000000"
    elif _tema == "Dark Sport (Athos)":
        _bg, _text, _accent, _card_bg, _btn_text = "#050A0E", "#FFFFFF", "#00FF66", "#0B161E", "#000000"
    elif _tema == "Red Devils":
        _bg, _text, _accent, _card_bg, _btn_text = "#0E0E0E", "#FFFFFF", "#E31B23", "#1A1A1A", "#FFFFFF"
    else:  # Sofascore Night
        _bg, _text, _accent, _card_bg, _btn_text = "#121921", "#FFFFFF", "#0073E6", "#1A242D", "#FFFFFF"

    st.markdown(f"""
<style>
.stApp {{ background-color: {_bg} !important; }}
section.main, section.main p, section.main span, section.main div {{ color: {_text} !important; opacity: 1 !important; }}
div.stButton > button, div.stDownloadButton > button, div[data-testid="stFormSubmitButton"] > button {{ background-color: {_accent} !important; color: {_btn_text} !important; border: 2px solid {_accent} !important; border-radius: 8px !important; font-weight: 800 !important; padding: 0.5rem 1rem !important; }}
div.stButton > button:hover, div.stDownloadButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {{ opacity: 0.9 !important; transform: scale(1.02); transition: 0.15s ease-in-out; }}
input[type="text"], input[type="number"], textarea {{ background-color: {_card_bg} !important; color: {_text} !important; -webkit-text-fill-color: {_text} !important; border: 1px solid {_accent} !important; border-radius: 6px !important; }}
div[data-baseweb="select"] > div {{ background-color: white !important; color: {_accent} !important; border: 1px solid {_accent} !important; border-radius: 6px !important; font-weight: 600 !important; }}
div[data-baseweb="popover"] {{ background-color: white !important; }}
li[role="option"] {{ color: {_accent} !important; font-weight: 500 !important; }}
li[role="option"]:hover {{ background-color: {_accent} !important; color: {_btn_text} !important; }}
[data-testid="stVerticalBlockBorderWrapper"] {{ background-color: {_card_bg} !important; border: 1px solid {_accent} !important; border-radius: 12px !important; padding: 1rem !important; }}
.stTabs [data-baseweb="tab"] p {{ color: {_text} !important; opacity: 0.6 !important; font-weight: 600; }}
.stTabs [aria-selected="true"] p {{ color: {_accent} !important; opacity: 1 !important; }}
.stTabs [aria-selected="true"] {{ border-bottom: 3px solid {_accent} !important; }}
[data-testid="stHeader"] {{ background: transparent !important; }}
section.main * {{ color: {_text} !important; }}
section.main p, section.main span, section.main label, section.main div {{ color: {_text} !important; opacity: 1 !important; }}
:root {{ --text-color: {_text} !important; }}
[data-testid="stMarkdownContainer"] * {{ color: {_text} !important; opacity: 1 !important; }}
div.stButton > button p, div.stButton > button div, div.stButton > button span {{ color: {_btn_text} !important; }}
div[data-testid="stFormSubmitButton"] > button p, div[data-testid="stFormSubmitButton"] > button span {{ color: {_btn_text} !important; }}
</style>
""", unsafe_allow_html=True)

    tab_igraci, tab_klubovi, tab_timovi, tab_turniri, tab_postavke = st.tabs([
        t("tab_players"),
        t("tab_clubs"),
        t("tab_teams"),
        t("tab_tournaments"),
        t("tab_settings"),
    ])

    # ── TAB 1: IGRAČI / PLAYERS ────────────────────────────────────────────────
    with tab_igraci:
        st.subheader(t("players_subheader"))

        df_i = dohvati_sve_igrace(kid)
        c1, c2 = st.columns([1, 1])

        with c1:
            st.markdown(t("add_player"))
            with st.form("forma_novi_igrac", clear_on_submit=True):
                n_ime = st.text_input(t("player_name")).strip()
                n_aktivan = st.checkbox(t("player_active_chk"), value=True)

                if st.form_submit_button(t("save_to_db")):
                    if n_ime:
                        moze_upis = True
                        if df_i is not None and not df_i.empty:
                            postojeca_imena = [ime.lower() for ime in df_i['ime'].tolist()]
                            if n_ime.lower() in postojeca_imena:
                                st.error(t("player_exists", n_ime))
                                moze_upis = False

                        if moze_upis:
                            uspjeh, poruka = dodaj_igraca(n_ime, kid, n_aktivan)
                            if uspjeh:
                                st.success(t("player_saved", n_ime))
                                st.rerun()
                            else:
                                st.error(t("db_error", poruka))
                    else:
                        st.warning(t("name_empty"))

        with c2:
            st.markdown(t("player_list"))
            if df_i is not None and not df_i.empty:
                uredjeni_df = st.data_editor(
                    df_i[['id', 'ime', 'aktivan']],
                    width="stretch",
                    hide_index=True,
                    disabled=["id", "ime"],
                    key="editor_igraci"
                )

                if st.session_state.editor_igraci["edited_rows"]:
                    for row_idx, changes in st.session_state.editor_igraci["edited_rows"].items():
                        if "aktivan" in changes:
                            pravi_id = int(df_i.iloc[row_idx]['id'])
                            novi_status = changes["aktivan"]
                            promjeni_status_igraca(pravi_id, novi_status)
                            st.rerun()

                st.caption(t("player_tip"))
            else:
                st.info(t("no_players"))

    # ── TAB 2: KLUBOVI / CLUBS ─────────────────────────────────────────────────
    with tab_klubovi:
        st.subheader(t("clubs_subheader"))
        df_k = dohvati_sve_klubove(kid)

        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown(t("add_club"))
            with st.form("forma_novi_klub", clear_on_submit=True):
                n_naziv = st.text_input(t("club_name")).strip()
                n_aktivan_k = st.checkbox(t("club_active_chk"), value=True)

                if st.form_submit_button(t("save_club_btn")):
                    if n_naziv:
                        moze_upis_k = True
                        if df_k is not None and not df_k.empty:
                            postojeci_klubovi = [k.lower() for k in df_k['naziv'].tolist()]
                            if n_naziv.lower() in postojeci_klubovi:
                                st.error(t("club_exists", n_naziv))
                                moze_upis_k = False

                        if moze_upis_k:
                            uspjeh, poruka = dodaj_klub(n_naziv, kid, n_aktivan_k)
                            if uspjeh:
                                st.success(t("club_saved", n_naziv))
                                st.rerun()
                            else:
                                st.error(t("db_error", poruka))
                    else:
                        st.warning(t("name_empty"))

        with c2:
            st.markdown(t("club_list"))
            if df_k is not None and not df_k.empty:
                uredjeni_k = st.data_editor(
                    df_k[['id', 'naziv', 'aktivan']],
                    width="stretch", hide_index=True,
                    disabled=["id", "naziv"], key="editor_klubovi"
                )

                if st.session_state.editor_klubovi["edited_rows"]:
                    for row_idx, changes in st.session_state.editor_klubovi["edited_rows"].items():
                        if "aktivan" in changes:
                            pravi_id_k = int(df_k.iloc[row_idx]['id'])
                            novi_status_k = changes["aktivan"]
                            promjeni_status_kluba(pravi_id_k, novi_status_k)
                            st.rerun()

                st.caption(t("club_tip"))
            else:
                st.info(t("no_clubs"))

    # ── TAB 3: TIMOVI / TEAMS ──────────────────────────────────────────────────
    with tab_timovi:
        st.header(t("teams_header"))

        df_i = dohvati_sve_igrace(kid)
        df_k = dohvati_sve_klubove(kid)

        if df_i is not None and df_k is not None:
            aktivni_imena = df_i[df_i['aktivan'] == True]['ime'].tolist()
            aktivni_klubovi = df_k[df_k['aktivan'] == True]['naziv'].tolist()

            izbor_nacina = st.radio(
                t("team_mode_radio"),
                [t("team_mode_auto"), t("team_mode_manual")]
            )

            if izbor_nacina == t("team_mode_auto"):
                st.subheader(t("auto_subheader"))
                col1, col2 = st.columns(2)
                with col1:
                    sudionici = st.multiselect(t("who_plays_today"), aktivni_imena)
                with col2:
                    broj_ljudi_u_timu = st.number_input(t("players_per_team"), 1, 5, 2)

                if st.button(t("generate_teams_btn"), use_container_width=True):
                    if len(sudionici) < 2:
                        st.error(t("not_enough_players"))
                    elif len(aktivni_klubovi) < (len(sudionici) // broj_ljudi_u_timu):
                        st.error(t("not_enough_clubs"))
                    else:
                        obrisi_sve_timove(kid)
                        random.shuffle(sudionici)
                        random.shuffle(aktivni_klubovi)

                        broj_timova = len(sudionici) // broj_ljudi_u_timu

                        for t_idx in range(broj_timova):
                            start = t_idx * broj_ljudi_u_timu
                            end = start + broj_ljudi_u_timu
                            grupa_igraca = sudionici[start:end]
                            imena_str = ", ".join(grupa_igraca)
                            odabrani_klub = aktivni_klubovi[t_idx]
                            sacuvaj_tim(imena_str, [odabrani_klub], kid)

                        visak = sudionici[broj_timova * broj_ljudi_u_timu:]
                        if visak:
                            st.warning(t("leftover_players", ", ".join(visak)))

                        st.success(t("teams_generated", broj_timova))
                        st.rerun()

            else:
                st.subheader(t("manual_subheader"))
                with st.form("rucna_forma"):
                    c1, c2 = st.columns(2)
                    with c1:
                        m_igraci = st.multiselect(t("select_players"), aktivni_imena)
                    with c2:
                        m_klub = st.selectbox(t("select_club"), aktivni_klubovi)

                    if st.form_submit_button(t("save_team_btn")):
                        if m_igraci and m_klub:
                            sacuvaj_tim(", ".join(m_igraci), [m_klub], kid)
                            st.rerun()

        st.divider()
        df_st = dohvati_sacuvane_timove(kid)
        if not df_st.empty:
            st.subheader(t("registered_teams"))
            st.dataframe(
                df_st[['naziv_tima', 'igraci']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "naziv_tima": t("col_players_in_team"),
                    "igraci": t("col_club")
                }
            )
            if st.button(t("delete_all_btn"), type="secondary"):
                obrisi_sve_timove(kid)
                st.rerun()

    # ── TAB 4: TURNIRI / TOURNAMENTS ──────────────────────────────────────────
    with tab_turniri:
        st.markdown(f"<h2 style='text-align: center;'>{t('arena_header')}</h2>", unsafe_allow_html=True)

        turniri_lista = dohvati_turnire(kid)

        izbor = st.radio(
            t("tournament_mgmt"),
            [t("active_competition"), t("new_season")],
            horizontal=True
        )

        if izbor == t("new_season"):
            st.subheader(t("tournament_settings"))
            df_priprema = dohvati_sacuvane_timove(kid)

            if df_priprema is not None and not df_priprema.empty:
                with st.expander(t("preview_participants")):
                    st.dataframe(df_priprema[['naziv_tima', 'igraci']], use_container_width=True, hide_index=True)

                with st.form("forma_novi_turnir"):
                    naziv_t = st.text_input(
                        t("league_name_input"),
                        value=f"{t('league_name_default')} {pd.Timestamp.now().strftime('%d.%m.')}"
                    )
                    format_options = [t("format_single"), t("format_double")]
                    format_display = st.selectbox(t("format_select"), format_options)
                    # Map display value back to internal Croatian value expected by kreiraj_turnir
                    format_t = "Dvokružno" if format_display == t("format_double") else "Jednokružno"

                    if st.form_submit_button(t("start_league_btn"), use_container_width=True):
                        sudionici = df_priprema['naziv_tima'].tolist()
                        klubovi_mapa = dict(zip(df_priprema['naziv_tima'], df_priprema['igraci']))

                        uspjeh, poruka = kreiraj_turnir(naziv_t, "Liga", format_t, sudionici, klubovi_mapa, kid)
                        if uspjeh:
                            st.success(t("league_created"))
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(poruka)
            else:
                st.warning(t("no_teams_warning"))

        else:
            if turniri_lista:
                imena_turnira = {t_item[1]: t_item[0] for t_item in turniri_lista}
                odabrani_naziv = st.selectbox(t("select_competition"), list(imena_turnira.keys()))
                t_id = imena_turnira[odabrani_naziv]

                s_tab1, s_tab2 = st.tabs([t("standings_tab"), t("results_tab")])

                with s_tab1:
                    df_ljestvica = dohvati_ljestvicu(t_id)
                    if df_ljestvica is not None and not df_ljestvica.empty:
                        df_ljestvica.index = range(1, len(df_ljestvica) + 1)
                        st.dataframe(
                            df_ljestvica,
                            use_container_width=True,
                            column_config={
                                "Igrač":        t("col_player"),
                                "Odigrano":     t("col_played"),
                                "Pobjede":      t("col_won"),
                                "Neriješeno":   t("col_drawn"),
                                "Izgubljeno":   t("col_lost"),
                                "Postignuti":   t("col_gf"),
                                "Primljeni":    t("col_ga"),
                                "Gol Razlika":  t("col_gd"),
                                "Bodovi":       t("col_pts"),
                            }
                        )

                with s_tab2:
                    df_utakmice = dohvati_utakmice_turnira(t_id)
                    if df_utakmice is not None and not df_utakmice.empty:
                        neodigrano = df_utakmice[df_utakmice['odigrano'] == False]

                        if not neodigrano.empty:
                            for idx, row in neodigrano.iterrows():
                                with st.container(border=True):
                                    st.markdown(f"**{row['domacin']}** {t('vs')} **{row['gost']}**")
                                    st.caption(f"🎮 {row['klub_domacin']} 🆚 {row['klub_gost']}")

                                    c1, c2, c3 = st.columns([1, 1, 1])
                                    with c1:
                                        g_d = st.number_input(t("goals_home"), 0, 20, key=f"d_{row['id']}")
                                    with c2:
                                        g_g = st.number_input(t("goals_away"), 0, 20, key=f"g_{row['id']}")
                                    with c3:
                                        st.write("")
                                        if st.button(t("save_result_btn"), key=f"b_{row['id']}", use_container_width=True, type="primary"):
                                            if unesi_rezultat(row['id'], g_d, g_g):
                                                st.rerun()
                        else:
                            st.success(t("all_played"))

                        with st.expander(t("match_history")):
                            odigrane = df_utakmice[df_utakmice['odigrano'] == True]
                            if not odigrane.empty:
                                prikaz_povijest = odigrane[['domacin', 'golovi_domacin', 'golovi_gost', 'gost']].copy()
                                prikaz_povijest.index = range(1, len(prikaz_povijest) + 1)
                                st.dataframe(
                                    prikaz_povijest,
                                    use_container_width=True,
                                    column_config={
                                        "domacin":        t("col_home"),
                                        "golovi_domacin": t("col_home_short"),
                                        "golovi_gost":    t("col_away_short"),
                                        "gost":           t("col_away"),
                                    }
                                )
            else:
                st.info(t("no_active_tournament"))

    # ── TAB 5: POSTAVKE / SETTINGS ────────────────────────────────────────────
    with tab_postavke:
        st.markdown(f"<h3 style='text-align: center;'>{t('settings_header')}</h3>", unsafe_allow_html=True)

        opcije_tema = [
            "Dark Sport (Athos)",
            "Athos Gold",
            "Sofascore Night",
            "Red Devils",
            "Ice Pitch (Svijetla)"
        ]

        def _on_tema_change():
            st.session_state["active_tema"] = st.session_state["tema_izbor"]

        st.selectbox(
            t("theme_select"),
            opcije_tema,
            index=opcije_tema.index(st.session_state["active_tema"]),
            key="tema_izbor",
            on_change=_on_tema_change
        )

        st.markdown("---")
        if st.button(t("reset_tab3_btn"), use_container_width=True):
            obrisi_sve_timove(kid)
            st.success(t("reset_tab3_success"))
            st.rerun()

        st.write("")

        if st.button(t("delete_history_btn"), use_container_width=True):
            st.session_state.confirm_nuke = True

        if st.session_state.get('confirm_nuke', False):
            st.error(t("confirm_delete"))
            c1, c2 = st.columns(2)

            with c1:
                if st.button(t("confirm_yes"), key="nuke_confirm_btn"):
                    uspjeh, poruka = obrisi_povijest_turnira(kid)
                    if uspjeh:
                        st.session_state.confirm_nuke = False
                        st.success(t("delete_success"))
                        st.rerun()
                    else:
                        st.error(poruka)

            with c2:
                if st.button(t("confirm_no"), key="nuke_cancel_btn"):
                    st.session_state.confirm_nuke = False
                    st.rerun()