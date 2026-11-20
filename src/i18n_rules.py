"""Pattern rules for the desk translations: team names, dates and the repeating page phrases.
Anything a rule does not cover is looked up word for word in src/i18n/<lang>.json."""
import re

COUNTRIES = {
 "fr": {"Algeria": "Algérie", "Argentina": "Argentine", "Australia": "Australie", "Belgium": "Belgique", "Brazil": "Brésil", "Cameroon": "Cameroun", "Chile": "Chili", "China PR": "RP Chine", "Colombia": "Colombie", "Costa Rica": "Costa Rica", "Croatia": "Croatie", "Cuba": "Cuba", "Côte d'Ivoire": "Côte d'Ivoire", "Denmark": "Danemark", "Dominican Republic": "République dominicaine", "Ecuador": "Équateur", "Egypt": "Égypte", "Fiji": "Fidji", "France": "France", "Greece": "Grèce", "Haiti": "Haïti", "Honduras": "Honduras", "Italy": "Italie", "Jamaica": "Jamaïque", "Japan": "Japon", "Korea Republic": "République de Corée", "Mali": "Mali", "Mexico": "Mexique", "Montenegro": "Monténégro", "Morocco": "Maroc", "Mozambique": "Mozambique", "New Caledonia": "Nouvelle-Calédonie", "New Zealand": "Nouvelle-Zélande", "Panama": "Panama", "Qatar": "Qatar", "Republic of Ireland": "République d'Irlande", "Romania": "Roumanie", "Saudi Arabia": "Arabie saoudite", "Senegal": "Sénégal", "Serbia": "Serbie", "Spain": "Espagne", "Tajikistan": "Tadjikistan", "Tanzania": "Tanzanie", "Uganda": "Ouganda", "Uruguay": "Uruguay", "Uzbekistan": "Ouzbékistan", "Venezuela": "Venezuela", "Vietnam": "Viêt Nam", "Greece's": "de la Grèce"},
 "sw": {"Algeria": "Algeria", "Argentina": "Argentina", "Australia": "Australia", "Belgium": "Ubelgiji", "Brazil": "Brazil", "Cameroon": "Kamerun", "Chile": "Chile", "China PR": "China", "Colombia": "Kolombia", "Costa Rica": "Kosta Rika", "Croatia": "Kroatia", "Cuba": "Kuba", "Côte d'Ivoire": "Côte d'Ivoire", "Denmark": "Denmaki", "Dominican Republic": "Jamhuri ya Dominika", "Ecuador": "Ekwado", "Egypt": "Misri", "Fiji": "Fiji", "France": "Ufaransa", "Greece": "Ugiriki", "Haiti": "Haiti", "Honduras": "Honduras", "Italy": "Italia", "Jamaica": "Jamaika", "Japan": "Japani", "Korea Republic": "Jamhuri ya Korea", "Mali": "Mali", "Mexico": "Meksiko", "Montenegro": "Montenegro", "Morocco": "Morocco", "Mozambique": "Msumbiji", "New Caledonia": "Kaledonia Mpya", "New Zealand": "New Zealand", "Panama": "Panama", "Qatar": "Qatar", "Republic of Ireland": "Jamhuri ya Ireland", "Romania": "Romania", "Saudi Arabia": "Saudi Arabia", "Senegal": "Senegal", "Serbia": "Serbia", "Spain": "Hispania", "Tajikistan": "Tajikistan", "Tanzania": "Tanzania", "Uganda": "Uganda", "Uruguay": "Uruguay", "Uzbekistan": "Uzbekistan", "Venezuela": "Venezuela", "Vietnam": "Vietnam"},
 "pt": {"Algeria": "Argélia", "Argentina": "Argentina", "Australia": "Austrália", "Belgium": "Bélgica", "Brazil": "Brasil", "Cameroon": "Camarões", "Chile": "Chile", "China PR": "China", "Colombia": "Colômbia", "Costa Rica": "Costa Rica", "Croatia": "Croácia", "Cuba": "Cuba", "Côte d'Ivoire": "Costa do Marfim", "Denmark": "Dinamarca", "Dominican Republic": "República Dominicana", "Ecuador": "Equador", "Egypt": "Egito", "Fiji": "Fiji", "France": "França", "Greece": "Grécia", "Haiti": "Haiti", "Honduras": "Honduras", "Italy": "Itália", "Jamaica": "Jamaica", "Japan": "Japão", "Korea Republic": "Coreia do Sul", "Mali": "Mali", "Mexico": "México", "Montenegro": "Montenegro", "Morocco": "Marrocos", "Mozambique": "Moçambique", "New Caledonia": "Nova Caledônia", "New Zealand": "Nova Zelândia", "Panama": "Panamá", "Qatar": "Catar", "Republic of Ireland": "Irlanda", "Romania": "Romênia", "Saudi Arabia": "Arábia Saudita", "Senegal": "Senegal", "Serbia": "Sérvia", "Spain": "Espanha", "Tajikistan": "Tajiquistão", "Tanzania": "Tanzânia", "Uganda": "Uganda", "Uruguay": "Uruguai", "Uzbekistan": "Uzbequistão", "Venezuela": "Venezuela", "Vietnam": "Vietnã"},
}
FR_ART = {"Algérie": "l'", "Argentine": "l'", "Australie": "l'", "Belgique": "la ", "Brésil": "le ", "Cameroun": "le ", "Chili": "le ", "RP Chine": "la ", "Colombie": "la ", "Costa Rica": "le ", "Croatie": "la ", "Cuba": "", "Côte d'Ivoire": "la ", "Danemark": "le ", "République dominicaine": "la ", "Équateur": "l'", "Égypte": "l'", "Fidji": "les ", "France": "la ", "Grèce": "la ", "Haïti": "", "Honduras": "le ", "Italie": "l'", "Jamaïque": "la ", "Japon": "le ", "République de Corée": "la ", "Mali": "le ", "Mexique": "le ", "Monténégro": "le ", "Maroc": "le ", "Mozambique": "le ", "Nouvelle-Calédonie": "la ", "Nouvelle-Zélande": "la ", "Panama": "le ", "Qatar": "le ", "République d'Irlande": "la ", "Roumanie": "la ", "Arabie saoudite": "l'", "Sénégal": "le ", "Serbie": "la ", "Espagne": "l'", "Tadjikistan": "le ", "Tanzanie": "la ", "Ouganda": "l'", "Uruguay": "l'", "Ouzbékistan": "l'", "Venezuela": "le ", "Viêt Nam": "le "}
PT_ART = {"Argélia": "a", "Argentina": "a", "Austrália": "a", "Bélgica": "a", "Brasil": "o", "Camarões": "", "Chile": "o", "China": "a", "Colômbia": "a", "Costa Rica": "a", "Croácia": "a", "Cuba": "", "Costa do Marfim": "a", "Dinamarca": "a", "República Dominicana": "a", "Equador": "o", "Egito": "o", "Fiji": "", "França": "a", "Grécia": "a", "Haiti": "o", "Honduras": "", "Itália": "a", "Jamaica": "a", "Japão": "o", "Coreia do Sul": "a", "Mali": "o", "México": "o", "Montenegro": "", "Marrocos": "o", "Moçambique": "", "Nova Caledônia": "a", "Nova Zelândia": "a", "Panamá": "o", "Catar": "o", "Irlanda": "a", "Romênia": "a", "Arábia Saudita": "a", "Senegal": "o", "Sérvia": "a", "Espanha": "a", "Tajiquistão": "o", "Tanzânia": "a", "Uganda": "", "Uruguai": "o", "Uzbequistão": "o", "Venezuela": "a", "Vietnã": "o"}

def le(c):  # French: le Danemark, l'Argentine, Cuba
    return FR_ART.get(c, "") + c
def du(c):  # French: du Mozambique, de la Croatie, de l'Égypte, des Fidji, de Cuba
    a = FR_ART.get(c, "")
    return {"le ": "du ", "la ": "de la ", "l'": "de l'", "les ": "des ", "": "de "}[a] + c
def o(c):  # Portuguese: a Dinamarca, o Egito, Moçambique
    a = PT_ART.get(c, "")
    return (a + " " if a else "") + c
def do(c):  # Portuguese: da Dinamarca, do Egito, de Moçambique
    return {"a": "da ", "o": "do ", "": "de "}[PT_ART.get(c, "")] + c

def played(lang, n, w, dr, l):
    n, w, dr, l = int(n), int(w), int(dr), int(l)
    if lang == "fr":
        p = lambda k, one, many: f"{k} {one if k < 2 else many}"
        return (f"{p(n, 'match disputé', 'matchs disputés')} : {p(w, 'victoire', 'victoires')}, {p(dr, 'nul', 'nuls')} et {p(l, 'défaite', 'défaites')}. "
                "Retrouvez chaque but en extrait vidéo, puis notre analyse de ce que chaque match apprend aux clubs, agents et fédérations.")
    if lang == "pt":
        p = lambda k, one, many: f"{k} {one if k == 1 else many}"
        return (f"{p(n, 'jogo disputado', 'jogos disputados')}: {p(w, 'vitória', 'vitórias')}, {p(dr, 'empate', 'empates')} e {p(l, 'derrota', 'derrotas')}. "
                "Assista a cada gol em seu próprio clipe e depois leia nossa análise do que cada partida mostra a clubes, agentes e federações.")
    return (f"Mechi {n} {'iliyochezwa' if n == 1 else 'zilizochezwa'}: ushindi {w}, sare {dr}, {'kipigo' if l == 1 else 'vipigo'} {l}. "
            "Tazama kila bao kama video yake, kisha soma tathmini yetu ya kile kila mechi inachoonyesha vilabu, mawakala na mashirikisho.")

DAYS = {
 "fr": {"Monday": "lundi", "Tuesday": "mardi", "Wednesday": "mercredi", "Thursday": "jeudi", "Friday": "vendredi", "Saturday": "samedi", "Sunday": "dimanche"},
 "sw": {"Monday": "Jumatatu", "Tuesday": "Jumanne", "Wednesday": "Jumatano", "Thursday": "Alhamisi", "Friday": "Ijumaa", "Saturday": "Jumamosi", "Sunday": "Jumapili"},
 "pt": {"Monday": "segunda-feira", "Tuesday": "terça-feira", "Wednesday": "quarta-feira", "Thursday": "quinta-feira", "Friday": "sexta-feira", "Saturday": "sábado", "Sunday": "domingo"},
}
MONTHS = {
 "fr": {"November": "novembre", "December": "décembre", "Nov": "nov.", "Dec": "déc.", "May": "mai", "June": "juin"},
 "sw": {"November": "Novemba", "December": "Desemba", "Nov": "Nov", "Dec": "Des", "May": "Mei", "June": "Juni"},
 "pt": {"November": "de novembro", "December": "de dezembro", "Nov": "de nov.", "Dec": "de dez.", "May": "de maio", "June": "de junho"},
}
ROLES = {
 "fr": {"Striker": "Attaquant", "Winger": "Ailier", "Midfielder": "Milieu de terrain", "Central midfielder": "Milieu central", "Attacking midfielder": "Milieu offensif", "Forward": "Attaquant", "Goalkeeper": "Gardien", "Centre back": "Défenseur central", "Full back": "Latéral"},
 "sw": {"Striker": "Mshambuliaji", "Winger": "Winga", "Midfielder": "Kiungo", "Central midfielder": "Kiungo wa kati", "Attacking midfielder": "Kiungo mshambuliaji", "Forward": "Mshambuliaji", "Goalkeeper": "Kipa", "Centre back": "Beki wa kati", "Full back": "Beki wa pembeni"},
 "pt": {"Striker": "Centroavante", "Winger": "Ponta", "Midfielder": "Meio-campista", "Central midfielder": "Meio-campista central", "Attacking midfielder": "Meia ofensivo", "Forward": "Atacante", "Goalkeeper": "Goleiro", "Centre back": "Zagueiro", "Full back": "Lateral"},
}

T = {  # phrase templates; {c}/{c2} = team, {n}/{m} = numbers or minutes, {x} = kept as is
 "fr": {
  "flag": "Drapeau : {c}", "at": "{c} à la Coupe du monde U-17 de la FIFA, Qatar 2026",
  "atdesc": "{c} à la Coupe du monde U-17 de la FIFA, Qatar 2026 : chaque résultat, chaque but avec le résumé officiel, les prochains matchs et les joueurs à suivre, par Afritech Sports.",
  "attitle": "{c} à la Coupe du monde U-17 2026 : résultats, buts et joueurs | Afritech Tournament Desk",
  "fixtures": "{c} : calendrier et comptes rendus ›", "results": "{c} : résultats, buts et prochains matchs ›", "cards": "{c} : comptes rendus et toutes les fiches ›",
  "brief": "Réserver un échange sur {le}", "coming": "Prochains matchs {du}",
  "every": "Chaque joueur {du} avec un but ou une passe décisive, plus les joueurs suivis avant le tournoi. Chaque fiche donne notre recommandation, ses chiffres, ses buts en extraits et ce qui le ferait monter ou descendre.",
  "ourcards": "Nos fiches d'observation pour {le} se construisent avec les matchs de groupe : chaque buteur et chaque joueur qui se distingue est ajouté ici après chaque journée.",
  "want": "Vous souhaitez consulter le tableau complet des joueurs {du} ?", "timeline": "Chronologie des buts : buts {du} au-dessus de la ligne, buts adverses en dessous",
  "goal": "But contre {le}, {m}", "assist": "Passe décisive contre {le}, {m}", "coach": "Entraîneur : {x}", "radar": "{x} : radar {r}, en attente des premières notes",
  "first": "Premier match : {c} – {c2}, {d}, {t} heure de Doha. Le compte rendu, les buts et notre analyse arrivent ici après le coup de sifflet final.",
  "played": "{n} joué : {w} victoire(s), {dr} nul(s), {l} défaite(s). Regardez chaque but en extrait, puis lisez notre analyse de ce que chaque match apprend aux clubs, agents et fédérations.",
  "doha": "{t} Doha", "pitch": "Aspire Zone, terrain {n}", "all": "Tous ({n})", "africa": "Afrique ({n})", "world": "Reste du monde ({n})",
  "playall": "Voir les {n} buts : chaque but est un extrait vidéo qui s'arrête puis enchaîne sur le suivant.", "playallbtn": "▶ Voir les {n} buts", "assistby": "Passe décisive : {x}.",
  "group": "Groupe {x}", "updated": "Mis à jour le {d}", "date": "{wd} {n} {mo}", "dm": "{n} {mo}", "dmy": "{n} {mo} {y}",
 },
 "sw": {
  "flag": "Bendera ya {c}", "at": "{c} kwenye Kombe la Dunia la FIFA U-17, Qatar 2026",
  "atdesc": "{c} kwenye Kombe la Dunia la FIFA U-17, Qatar 2026: kila matokeo, kila bao pamoja na video rasmi, mechi zijazo na wachezaji wa kufuatilia, kutoka Afritech Sports.",
  "attitle": "{c} kwenye Kombe la Dunia U-17 2026: matokeo, mabao na wachezaji | Afritech Tournament Desk",
  "fixtures": "{c}: ratiba na ripoti za mechi ›", "results": "{c}: matokeo, mabao na mechi zijazo ›", "cards": "{c}: ripoti za mechi na kadi zote za wachezaji ›",
  "brief": "Panga mazungumzo kuhusu {c}", "coming": "Mechi zijazo za {c}",
  "every": "Kila mchezaji wa {c} aliyefunga au kutoa pasi ya bao, pamoja na wachezaji tuliowafuatilia kabla ya mashindano. Kila kadi ina pendekezo letu, takwimu zake, mabao yake kwa video na kinachoweza kumpandisha au kumshusha.",
  "ourcards": "Kadi zetu za wachezaji wa {c} zinajengwa kutoka mechi za makundi: kila mfungaji na mchezaji anayeng'aa huongezwa hapa baada ya kila raundi.",
  "want": "Unataka picha kamili ya wachezaji wa {c}?", "timeline": "Mfuatano wa mabao: mabao ya {c} juu ya mstari, ya mpinzani chini",
  "goal": "Bao dhidi ya {c}, {m}", "assist": "Pasi ya bao dhidi ya {c}, {m}", "coach": "Kocha: {x}", "radar": "{x}: rada ya {r}, inasubiri alama za kwanza",
  "first": "Mechi ya kwanza: {c} – {c2}, {d}, saa {t} kwa saa za Doha. Ripoti ya mechi, mabao na tathmini yetu vitawekwa hapa baada ya filimbi ya mwisho.",
  "played": "Mechi {n}: ushindi {w}, sare {dr}, kupoteza {l}. Tazama kila bao kama kipande chake, kisha soma tathmini yetu ya kile kila mechi inachoonyesha vilabu, mawakala na mashirikisho.",
  "doha": "{t} Doha", "pitch": "Aspire Zone, Uwanja {n}", "all": "Wote ({n})", "africa": "Afrika ({n})", "world": "Nje ya Afrika ({n})",
  "playall": "Tazama mabao yote {n}: kila bao ni video yake, inasimama kisha inaendelea na bao linalofuata.", "playallbtn": "▶ Tazama mabao yote {n}", "assistby": "Pasi ya bao: {x}.",
  "group": "Kundi {x}", "updated": "Imesasishwa {d}", "date": "{wd} {n} {mo}", "dm": "{n} {mo}", "dmy": "{n} {mo} {y}",
 },
 "pt": {
  "flag": "Bandeira: {c}", "at": "{c} na Copa do Mundo Sub-17 da FIFA, Catar 2026",
  "atdesc": "{c} na Copa do Mundo Sub-17 da FIFA, Catar 2026: todos os resultados, cada gol com o vídeo oficial, os próximos jogos e os jogadores para acompanhar, pela Afritech Sports.",
  "attitle": "{c} na Copa do Mundo Sub-17 2026: resultados, gols e jogadores | Afritech Tournament Desk",
  "fixtures": "{c}: jogos e relatórios das partidas ›", "results": "{c}: resultados, gols e próximos jogos ›", "cards": "{c}: relatórios das partidas e todas as fichas ›",
  "brief": "Agende um briefing sobre {o}", "coming": "Próximos jogos {do}",
  "every": "Todo jogador {do} com gol ou assistência, mais os jogadores que acompanhamos antes do torneio. Cada ficha traz nossa recomendação, seus números, seus gols em vídeo e o que faria ele subir ou descer.",
  "ourcards": "Nossos relatórios de observação {do} são montadas a partir dos jogos da fase de grupos: cada goleador e cada destaque entra aqui depois de cada rodada.",
  "want": "Quer o quadro completo dos jogadores {do}?", "timeline": "Linha do tempo dos gols: gols {do} acima da linha, do adversário abaixo",
  "goal": "Gol contra {o}, {m}", "assist": "Assistência contra {o}, {m}", "coach": "Técnico: {x}", "radar": "{x}: radar de {r}, aguardando as primeiras notas",
  "first": "Primeiro jogo: {c} x {c2}, {d}, {t} no horário de Doha. O relatório da partida, os gols e nossa análise entram aqui depois do apito final.",
  "played": "{n} jogo: {w} vitória(s), {dr} empate(s), {l} derrota(s). Veja cada gol em seu próprio clipe e depois leia nossa análise do que cada partida mostra a clubes, agentes e federações.",
  "doha": "{t} Doha", "pitch": "Aspire Zone, Campo {n}", "all": "Todos ({n})", "africa": "África ({n})", "world": "Resto do mundo ({n})",
  "playall": "Assista aos {n} gols: cada lance é reproduzido separadamente e, ao terminar, o próximo começa.", "playallbtn": "▶ Assistir aos {n} gols", "assistby": "Assistência de {x}.",
  "group": "Grupo {x}", "updated": "Atualizado em {d}", "date": "{wd}, {n} {mo}", "dm": "{n} {mo}", "dmy": "{n} {mo} de {y}",
 },
}

DAYRE = "(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"
MONRE = "(November|December|Nov|Dec|May|June)"


def date(lang, s):
    m = re.fullmatch(DAYRE + r" (\d+) " + MONRE, s)
    if m:
        return T[lang]["date"].format(wd=DAYS[lang][m[1]], n=m[2], mo=MONTHS[lang][m[3]])
    m = re.fullmatch(r"(\d+) " + MONRE + r" (\d{4})", s)
    if m:
        return T[lang]["dmy"].format(n=m[1], mo=MONTHS[lang][m[2]], y=m[3])
    m = re.fullmatch(r"(\d+) " + MONRE, s)
    if m:
        return T[lang]["dm"].format(n=m[1], mo=MONTHS[lang][m[2]])
    return None


def rule(lang, s, names, tr):
    """Translate s by rule, or return None. tr(x) translates a sub-phrase (dictionary first)."""
    C, t = COUNTRIES[lang], T[lang]
    c = lambda x: C.get(x)
    k = lambda x: {"c": c(x), "le": le(c(x)), "du": du(c(x)), "o": o(c(x)), "do": do(c(x))}
    if s in C:
        return C[s]
    if s in names or re.fullmatch(r"[A-Z]{3}", s) or re.fullmatch(r".+ \([A-Z]{3}\)", s):
        return s
    if s in ROLES[lang]:
        return ROLES[lang][s]
    d = date(lang, s)
    if d:
        return d
    pats = [
        (r"(.+) flag", lambda m: c(m[1]) and t["flag"].format(**k(m[1]))),
        (r"\((.+)\)", lambda m: c(m[1]) and f"({c(m[1])})"),
        (r"(.+) at the FIFA U-17 World Cup Qatar 2026", lambda m: c(m[1]) and t["at"].format(**k(m[1]))),
        (r"(.+) at the FIFA U-17 World Cup Qatar 2026: every result, every goal with the official highlight, next matches and the players to watch, from Afritech Sports\.", lambda m: c(m[1]) and t["atdesc"].format(**k(m[1]))),
        (r"(.+) at the U-17 World Cup 2026: results, goals and players \| Afritech Tournament Desk", lambda m: c(m[1]) and t["attitle"].format(**k(m[1]))),
        (r"(.+): Fixtures and match reports ›", lambda m: c(m[1]) and t["fixtures"].format(**k(m[1]))),
        (r"(.+): Results, goals and next matches ›", lambda m: c(m[1]) and t["results"].format(**k(m[1]))),
        (r"(.+): match reports and all scout cards ›", lambda m: c(m[1]) and t["cards"].format(**k(m[1]))),
        (r"Book a briefing on (.+)", lambda m: c(m[1]) and t["brief"].format(**k(m[1]))),
        (r"Coming up for (.+)", lambda m: c(m[1]) and t["coming"].format(**k(m[1]))),
        (r"Every (.+) player with a goal or assist, plus the players we tracked before the tournament\. .*", lambda m: c(m[1]) and t["every"].format(**k(m[1]))),
        (r"Our scout cards for (.+) are built from the group matches: every goal scorer and standout is added here after each matchday\.", lambda m: c(m[1]) and t["ourcards"].format(**k(m[1]))),
        (r"Want the full picture on (.+)'s players\?", lambda m: c(m[1]) and t["want"].format(**k(m[1]))),
        (r"Goal timeline: (.+) goals above the line, opponent goals below", lambda m: c(m[1]) and t["timeline"].format(**k(m[1]))),
        (r"(?:▶ )?(Goal|Assist) v (.+), (\d+(?:\+\d+)?')( ›)?", lambda m: c(m[2]) and (("▶ " if s.startswith("▶") else "") + t["goal" if m[1] == "Goal" else "assist"].format(m=m[3], **k(m[2])) + (m[4] or ""))),
        (r"› (.+)", lambda m: c(m[1]) and "› " + c(m[1])),
        (r"(.+) v", lambda m: c(m[1]) and c(m[1]) + (" x" if lang == "pt" else " –")),
        (r"v (.+)", lambda m: c(m[1]) and ("x " if lang == "pt" else "– ") + c(m[1])),
        (r"(.+) \((.+)\)", lambda m: c(m[2]) and (m[1] in names or re.fullmatch(r"[A-ZÀ-Ý][\w'’.-]*(?: [A-ZÀ-Ý\w][\w'’.-]*)*", m[1])) and f"{m[1]} ({c(m[2])})"),
        (r"(\d+-\d+) (.+)", lambda m: c(m[2]) and f"{m[1]} {c(m[2])}"),
        (r"(.+) (\d+-\d+)", lambda m: c(m[1]) and f"{c(m[1])} {m[2]}"),
        (r"Coach: (.+)", lambda m: t["coach"].format(x=m[1])),
        (r"(.+): (.+) radar, awaiting first scores", lambda m: m[2] in ROLES[lang] and t["radar"].format(x=m[1], r=ROLES[lang][m[2]].lower() if lang != "sw" else ROLES[lang][m[2]].lower())),
        (r"First match: (.+) v (.+), (\w+ \d+ \w+), (\d\d:\d\d) Doha time\. The match report, goals and our read go up here after the final whistle\.", lambda m: c(m[1]) and c(m[2]) and t["first"].format(c=c(m[1]), c2=c(m[2]), d=date(lang, m[3]), t=m[4])),
        (r"(\d+) played: (\d+) won, (\d+) drawn, (\d+) lost\. Watch every goal as its own clip, then read our analysis of what each match tells clubs, agents and federations\.", lambda m: played(lang, m[1], m[2], m[3], m[4])),
        (r"(\d\d:\d\d) Doha", lambda m: t["doha"].format(t=m[1])),
        (r"Aspire Zone, Pitch (\d+)", lambda m: t["pitch"].format(n=m[1])),
        (r"All \((\d+)\)", lambda m: t["all"].format(n=m[1])),
        (r"Africa \((\d+)\)", lambda m: t["africa"].format(n=m[1])),
        (r"Rest of the world \((\d+)\)", lambda m: t["world"].format(n=m[1])),
        (r"Play all (\d+) goals: each goal plays as its own clip, stops, and moves to the next\.", lambda m: t["playall"].format(n=m[1])),
        (r"▶ Play all (\d+) goals", lambda m: t["playallbtn"].format(n=m[1])),
        (r"Assist ([A-ZÀ-Ý][^ ]+(?: [A-ZÀ-Ý][^ ]+)+)\.", lambda m: t["assistby"].format(x=m[1])),
        (r"Age (\d+)", lambda m: {"fr": "{n} ans", "sw": "Miaka {n}", "pt": "{n} anos"}[lang].format(n=m[1])),
        (r"No\. (\d+)", lambda m: {"fr": "N° {n}", "sw": "Na. {n}", "pt": "Nº {n}"}[lang].format(n=m[1])),
        (r"Aspire Zone|Doha|[\w.+-]+@[\w.-]+", lambda m: s),
        (r"Built from public sources up to (\d+ \w+ \d{4})", lambda m: {"fr": "Construit à partir de sources publiques jusqu'au {d}", "sw": "Imetokana na vyanzo vya umma hadi {d}", "pt": "Feito com fontes públicas até {d}"}[lang].format(d=date(lang, m[1]))),
        (r"Group ([A-L])", lambda m: t["group"].format(x=m[1])),
        (r"Updated (\d+ \w+ \d{4})", lambda m: date(lang, m[1]) and t["updated"].format(d=date(lang, m[1]))),
    ]
    for p, f in pats:
        m = re.fullmatch(p, s)
        if m:
            r = f(m)
            if r:
                return r
    if " · " in s:
        parts = [tr(x) for x in s.split(" · ")]
        if all(p is not None for p in parts):
            return " · ".join(parts)
    return None
