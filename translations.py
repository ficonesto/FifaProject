# translations.py
# Sve tekstualne konstante za Athos League aplikaciju
# All text constants for the Athos League application
# -----------------------------------------------------------
# Korištenje / Usage:
#   from translations import t, set_language
#   t("welcome")  →  "Dobrodošli u Athos League" (HR) or "Welcome to Athos League" (EN)
# -----------------------------------------------------------

import streamlit as st

TRANSLATIONS = {

    # ── OPĆE / GENERAL ──────────────────────────────────────────────────────────
    "app_title":            {"hr": "ATHOS LEAGUE",              "en": "ATHOS LEAGUE"},
    "language_button_hr":   {"hr": "🇭🇷 HR",                    "en": "🇭🇷 HR"},
    "language_button_en":   {"hr": "🇬🇧 EN",                    "en": "🇬🇧 EN"},

    # ── AUTH ────────────────────────────────────────────────────────────────────
    "welcome":              {"hr": "Dobrodošli u Athos League", "en": "Welcome to Athos League"},
    "login_tab":            {"hr": "Prijava",                   "en": "Login"},
    "register_tab":         {"hr": "Registracija",              "en": "Register"},

    # Login forma
    "email":                {"hr": "Email",                     "en": "Email"},
    "password":             {"hr": "Lozinka",                   "en": "Password"},
    "login_btn":            {"hr": "Prijavi se",                "en": "Sign in"},
    "login_empty":          {"hr": "Molimo unesite email i lozinku.", "en": "Please enter email and password."},
    "login_success":        {"hr": "Dobrodošao, {}!",           "en": "Welcome, {}!"},
    "login_fail":           {"hr": "Neispravni podaci za prijavu.", "en": "Invalid login credentials."},

    # Registracija forma
    "username_placeholder": {"hr": "npr. Athos Varaždin",       "en": "e.g. Athos Varaždin"},
    "username_label":       {"hr": "Ime lige / korisničko ime", "en": "League name / username"},
    "password_repeat":      {"hr": "Ponovi lozinku",            "en": "Repeat password"},
    "register_btn":         {"hr": "Registriraj se",            "en": "Register"},
    "reg_fields_required":  {"hr": "Sva polja su obavezna.",    "en": "All fields are required."},
    "reg_pw_mismatch":      {"hr": "Lozinke se ne podudaraju.", "en": "Passwords do not match."},
    "reg_pw_short":         {"hr": "Lozinka mora imati barem 6 znakova.", "en": "Password must be at least 6 characters."},

    # ── SIDEBAR ─────────────────────────────────────────────────────────────────
    "sidebar_id":           {"hr": "ID Lige: #{}",              "en": "League ID: #{}"},
    "logout_btn":           {"hr": "Odjavi se",                 "en": "Log out"},

    # ── TABOVI NAVIGACIJE / MAIN NAV TABS ───────────────────────────────────────
    "tab_players":          {"hr": "👤 Igrači",                 "en": "👤 Players"},
    "tab_clubs":            {"hr": "⚽ Klubovi",                "en": "⚽ Clubs"},
    "tab_teams":            {"hr": "👥 Timovi",                 "en": "👥 Teams"},
    "tab_tournaments":      {"hr": "🏆 Turniri",                "en": "🏆 Tournaments"},
    "tab_settings":         {"hr": "⚙️ Postavke & Stil",        "en": "⚙️ Settings & Style"},

    # ── TAB 1: IGRAČI / PLAYERS ──────────────────────────────────────────────────
    "players_subheader":    {"hr": "🏃 Upravljanje ljudstvom",  "en": "🏃 Player Management"},
    "add_player":           {"hr": "### Dodaj igrača",          "en": "### Add player"},
    "player_name":          {"hr": "Ime i prezime",             "en": "Full name"},
    "player_active_chk":    {"hr": "Igrač je aktivan",         "en": "Player is active"},
    "save_to_db":           {"hr": "Spremi u bazu",             "en": "Save to database"},
    "player_exists":        {"hr": "❌ Igrač '{}' već postoji!", "en": "❌ Player '{}' already exists!"},
    "player_saved":         {"hr": "✅ Igrač {} spremljen!",    "en": "✅ Player {} saved!"},
    "db_error":             {"hr": "Greška baze: {}",           "en": "Database error: {}"},
    "name_empty":           {"hr": "⚠️ Ime ne može biti prazno!", "en": "⚠️ Name cannot be empty!"},
    "player_list":          {"hr": "### Popis igrača",          "en": "### Player list"},
    "no_players":           {"hr": "Još nemaš dodanih igrača.", "en": "No players added yet."},
    "player_tip":           {"hr": "💡 Klikni na kvačicu za aktivaciju/deaktivaciju igrača.",
                             "en": "💡 Click the checkbox to activate/deactivate a player."},

    # ── TAB 2: KLUBOVI / CLUBS ───────────────────────────────────────────────────
    "clubs_subheader":      {"hr": "🛡️ Upravljanje klubovima",  "en": "🛡️ Club Management"},
    "add_club":             {"hr": "### Dodaj klub",            "en": "### Add club"},
    "club_name":            {"hr": "Naziv kluba",               "en": "Club name"},
    "club_active_chk":      {"hr": "Klub je aktivan",           "en": "Club is active"},
    "save_club_btn":        {"hr": "Spremi klub",               "en": "Save club"},
    "club_exists":          {"hr": "❌ Klub '{}' već postoji!", "en": "❌ Club '{}' already exists!"},
    "club_saved":           {"hr": "✅ Klub {} dodan!",         "en": "✅ Club {} added!"},
    "club_list":            {"hr": "### Popis klubova",         "en": "### Club list"},
    "no_clubs":             {"hr": "Nema registriranih klubova.", "en": "No clubs registered."},
    "club_tip":             {"hr": "💡 Isključeni klubovi neće se nuditi pri kreiranju turnira.",
                             "en": "💡 Inactive clubs won't appear when creating a tournament."},

    # ── TAB 3: TIMOVI / TEAMS ────────────────────────────────────────────────────
    "teams_header":         {"hr": "👥 Generator Athos Ekipa",  "en": "👥 Athos Team Generator"},
    "team_mode_radio":      {"hr": "Odaberi način kreiranja:",  "en": "Choose creation mode:"},
    "team_mode_auto":       {"hr": "Automatski (Random)",       "en": "Automatic (Random)"},
    "team_mode_manual":     {"hr": "Ručno uparivanje",          "en": "Manual pairing"},

    # Automatski
    "auto_subheader":       {"hr": "🎲 Automatsko miješanje",   "en": "🎲 Automatic shuffle"},
    "who_plays_today":      {"hr": "Tko sve igra danas?",       "en": "Who's playing today?"},
    "players_per_team":     {"hr": "Broj igrača po jednom timu:", "en": "Players per team:"},
    "generate_teams_btn":   {"hr": "🔀 Generiraj i dodijeli klubove", "en": "🔀 Generate and assign clubs"},
    "not_enough_players":   {"hr": "Nedovoljno igrača za turnir!", "en": "Not enough players for a tournament!"},
    "not_enough_clubs":     {"hr": "Nemaš dovoljno aktivnih klubova u bazi za ovaj broj timova!",
                             "en": "Not enough active clubs for this number of teams!"},
    "leftover_players":     {"hr": "Igrači koji su ostali bez tima (višak): {}",
                             "en": "Players without a team (surplus): {}"},
    "teams_generated":      {"hr": "Generirano {} timova!",     "en": "{} teams generated!"},

    # Ručno
    "manual_subheader":     {"hr": "✍️ Ručno kreiranje tima",   "en": "✍️ Manual team creation"},
    "select_players":       {"hr": "Odaberi igrače za ovaj tim:", "en": "Select players for this team:"},
    "select_club":          {"hr": "Odaberi klub:",             "en": "Select club:"},
    "save_team_btn":        {"hr": "Spremi ovaj tim",           "en": "Save this team"},

    # Prikaz
    "registered_teams":     {"hr": "📋 Prijavljeni timovi",     "en": "📋 Registered teams"},
    "col_players_in_team":  {"hr": "Igrači u timu",             "en": "Players in team"},
    "col_club":             {"hr": "Klub",                      "en": "Club"},
    "delete_all_btn":       {"hr": "🗑️ Obriši sve",            "en": "🗑️ Delete all"},

    # ── TAB 4: TURNIRI / TOURNAMENTS ────────────────────────────────────────────
    "arena_header":         {"hr": "🏆 Athos Arena",            "en": "🏆 Athos Arena"},
    "tournament_mgmt":      {"hr": "Upravljanje turnirima:",    "en": "Tournament management:"},
    "active_competition":   {"hr": "⚽ Aktivno natjecanje",     "en": "⚽ Active competition"},
    "new_season":           {"hr": "➕ Nova sezona",             "en": "➕ New season"},

    # Nova sezona
    "tournament_settings":  {"hr": "Postavke turnira",         "en": "Tournament settings"},
    "preview_participants": {"hr": "🔍 Pregledaj sudionike prije početka",
                             "en": "🔍 Preview participants before starting"},
    "league_name_input":    {"hr": "Naziv lige:",               "en": "League name:"},
    "league_name_default":  {"hr": "Athos Liga",                "en": "Athos League"},
    "vs":                   {"hr": "vs",                        "en": "vs"},
    "format_select":        {"hr": "Format:",                   "en": "Format:"},
    "format_single":        {"hr": "Jednokružno",               "en": "Single round-robin"},
    "format_double":        {"hr": "Dvokružno",                 "en": "Double round-robin"},
    "start_league_btn":     {"hr": "🚀 POKRENI LIGU",          "en": "🚀 START LEAGUE"},
    "league_created":       {"hr": "⚽ Liga je uspješno kreirana!", "en": "⚽ League successfully created!"},
    "no_teams_warning":     {"hr": "⚠️ Prvo moraš generirati timove u tabu 'Timovi'!",
                             "en": "⚠️ You must first generate teams in the 'Teams' tab!"},

    # Aktivno natjecanje
    "select_competition":   {"hr": "Odaberi aktivno natjecanje:", "en": "Select active competition:"},
    "standings_tab":        {"hr": "📊 Tablica Poretka",        "en": "📊 Standings"},
    "results_tab":          {"hr": "🏟️ Unos Rezultata",         "en": "🏟️ Enter Results"},

    # Ljestvica stupci
    "col_player":           {"hr": "Igrač",                     "en": "Player"},
    "col_played":           {"hr": "Odigrano",                  "en": "Played"},
    "col_won":              {"hr": "Pobjede",                   "en": "Won"},
    "col_drawn":            {"hr": "Neriješeno",                "en": "Drawn"},
    "col_lost":             {"hr": "Izgubljeno",                "en": "Lost"},
    "col_gf":               {"hr": "Postignuti",                "en": "Goals For"},
    "col_ga":               {"hr": "Primljeni",                 "en": "Goals Against"},
    "col_gd":               {"hr": "Gol Razlika",               "en": "Goal Difference"},
    "col_pts":              {"hr": "Bodovi",                    "en": "Points"},

    # Unos rezultata
    "goals_home":           {"hr": "Golovi D",                  "en": "Home Goals"},
    "goals_away":           {"hr": "Golovi G",                  "en": "Away Goals"},
    "save_result_btn":      {"hr": "Spremi",                    "en": "Save"},
    "all_played":           {"hr": "🎉 Sve utakmice su odigrane!", "en": "🎉 All matches have been played!"},
    "match_history":        {"hr": "📜 Povijest odigranih susreta", "en": "📜 Match history"},
    "no_active_tournament": {"hr": "Nema aktivnih turnira. Kreni na opciju 'Nova sezona'!",
                             "en": "No active tournaments. Go to 'New season'!"},

    # Stupci utakmica
    "col_home":             {"hr": "Domaćin",                   "en": "Home"},
    "col_away":             {"hr": "Gost",                      "en": "Away"},
    "col_home_short":       {"hr": "D",                         "en": "H"},
    "col_away_short":       {"hr": "G",                         "en": "A"},

    # ── TAB 5: POSTAVKE / SETTINGS ───────────────────────────────────────────────
    "settings_header":      {"hr": "🎨 Postavke Sučelja",       "en": "🎨 Interface Settings"},
    "theme_select":         {"hr": "Izaberi temu:",             "en": "Choose theme:"},

    # Gumbi za reset
    "reset_tab3_btn":       {"hr": "🗑️ Resetiraj samo Tab 3 (Priprema)",
                             "en": "🗑️ Reset only Tab 3 (Preparation)"},
    "reset_tab3_success":   {"hr": "Priprema timova je očišćena.", "en": "Team preparation cleared."},
    "delete_history_btn":   {"hr": "🚨 OBRIŠI SVU POVIJEST TURNIRA",
                             "en": "🚨 DELETE ALL TOURNAMENT HISTORY"},
    "confirm_delete":       {"hr": "⚠️ Jeste li sigurni?",     "en": "⚠️ Are you sure?"},
    "confirm_yes":          {"hr": "✅ DA, BRIŠI SVE",          "en": "✅ YES, DELETE ALL"},
    "confirm_no":           {"hr": "❌ ODUSTANI",               "en": "❌ CANCEL"},
    "delete_success":       {"hr": "Sve obrisano!",             "en": "Everything deleted!"},
}


# ── HELPER FUNKCIJE / HELPER FUNCTIONS ──────────────────────────────────────────

def set_language(lang: str):
    """Postavi jezik u session_state. / Set language in session_state."""
    st.session_state["lang"] = lang


def get_language() -> str:
    """Vrati trenutni jezik (default: hr). / Return current language (default: hr)."""
    return st.session_state.get("lang", "hr")


def t(key: str, *args) -> str:
    """
    Vrati prevedeni string za zadani ključ.
    Return translated string for the given key.
    Podržava .format() argumente putem *args.
    Supports .format() arguments via *args.
    """
    lang = get_language()
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return f"[MISSING: {key}]"
    text = entry.get(lang, entry.get("hr", f"[MISSING: {key}]"))
    if args:
        text = text.format(*args)
    return text


def language_toggle_buttons():
    """
    Prikazuje gumbe za promjenu jezika u sidebaru.
    Displays language toggle buttons in the sidebar.
    """
    st.sidebar.markdown("---")
    lang = get_language()
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🇭🇷 HR", key="lang_hr",
                     type="primary" if lang == "hr" else "secondary",
                     use_container_width=True):
            set_language("hr")
            st.rerun()
    with col2:
        if st.button("🇬🇧 EN", key="lang_en",
                     type="primary" if lang == "en" else "secondary",
                     use_container_width=True):
            set_language("en")
            st.rerun()
