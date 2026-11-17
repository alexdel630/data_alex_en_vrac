"""Génère roadmap_simu_unreal.xlsx à partir du gabarit Gantt_lots.xlsx.

Seules les cellules de saisie sont remplacées ; formules et mises en forme du gabarit sont conservées.
Colonnes mois du Gantt : J = 09/2026 ... AA = 02/2028.
"""
from pathlib import Path

import openpyxl

ICI = Path(__file__).parent
GABARIT = ICI.parent.parent / "Gantt_lots.xlsx"
SORTIE = ICI / "roadmap_simu_unreal.xlsx"

PROJET = "Simu Unreal pilotable"
MOIS = {m: c for m, c in zip(
    ["2026-09", "2026-10", "2026-11", "2026-12", "2027-01", "2027-02", "2027-03", "2027-04",
     "2027-05", "2027-06", "2027-07", "2027-08", "2027-09", "2027-10", "2027-11", "2027-12",
     "2028-01", "2028-02"],
    ["J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA"])}

EQUIPE = [
    ("Personne A", "Chef de projet / architecte"),
    ("Personne B", "Développeur C++ Unreal"),
    ("Personne C", "Technical Artist / rendu"),
    ("Personne D", "Ingénieur physique (IR, dynamique)"),
    ("Personne E", "Ingénieur outils / CI / QA"),
]

PILOTAGE = {m: 30 for m in ["2027-01", "2027-02", "2027-03", "2027-04", "2027-05",
                            "2027-06", "2027-07", "2027-08", "2027-09"]}

# (lot, tâche, responsable, {mois: heures})
TACHES = [
    ("P0 Cadrage", "Spécification et définition du pilotage", "Personne A", {"2026-12": 100}),
    ("P0 Cadrage", "Architecture cible et registre des risques", "Personne B", {"2026-12": 60}),
    ("P1 Socle", "Projet UE 5.8 structuré en plugins", "Personne B", {"2027-01": 120, "2027-02": 60}),
    ("P1 Socle", "Gestion de configuration et CI GitLab", "Personne E", {"2027-01": 100, "2027-02": 80}),
    ("P1 Socle", "Terrain géoréférencé (Cesium / MNT)", "Personne C", {"2027-01": 100, "2027-02": 120}),
    ("P2 API", "API gRPC et client Python", "Personne B", {"2027-03": 140, "2027-04": 140}),
    ("P2 API", "Pilotage humain (Enhanced Input, HOTAS)", "Personne C", {"2027-04": 60}),
    ("P3 Scénarios", "Format de scénario et chargeur", "Personne B", {"2027-05": 120}),
    ("P3 Scénarios", "Enregistrement, rejeu et vérité terrain", "Personne E", {"2027-05": 80, "2027-06": 100}),
    ("P3 Scénarios", "Lancement en série et rapports", "Personne E", {"2027-06": 40}),
    ("P4 Capteur IR", "Matériaux IR (Physical Materials, stencil, audit)", "Personne C", {"2027-03": 120, "2027-04": 80}),
    ("P4 Capteur IR", "Fond atmosphérique (tables libRadtran)", "Personne D", {"2027-03": 80, "2027-04": 40}),
    ("P4 Capteur IR", "Injection subpixel (piste B puis hybride)", "Personne D", {"2027-04": 80, "2027-05": 100}),
    ("P4 Capteur IR", "Chaîne capteur (PSF, bruit, non-uniformité)", "Personne D", {"2027-05": 40, "2027-06": 120}),
    ("P5 Dynamique", "Modèles de mouvement et JSBSim", "Personne B", {"2027-06": 120, "2027-07": 60}),
    ("P5 Dynamique", "Capteurs portés (tourelle, jitter)", "Personne C", {"2027-06": 80}),
    ("P6 Performance", "Pas de temps fixe et déterminisme", "Personne E", {"2027-07": 120}),
    ("P6 Performance", "Profilage et optimisation", "Personne C", {"2027-07": 100, "2027-08": 40}),
    ("P7 Validation", "Tests automatisés et non-régression images", "Personne E", {"2027-08": 120, "2027-09": 60}),
    ("P7 Validation", "Validation radiométrique", "Personne D", {"2027-08": 100, "2027-09": 60}),
    ("P7 Validation", "Documentation, packaging et formation", "Personne A", {"2027-09": 100}),
    ("Transverse", "Pilotage et coordination", "Personne A", PILOTAGE),
    ("Transverse", "Contingence (≈ 15 %)", "Personne A", {"2027-10": 150, "2027-11": 150}),
]

wb = openpyxl.load_workbook(GABARIT)

# --- Gantt : lignes 4 à 33, saisie en A-E et J-AA
g = wb["Gantt"]
g["A1"] = "Roadmap — Simulation Unreal pilotable (charge en heures)"
for r in range(4, 34):
    for col in ["A", "B", "C", "D", "E", *MOIS.values()]:
        g[f"{col}{r}"].value = None
for r, (lot, tache, resp, charge) in enumerate(TACHES, start=4):
    g[f"A{r}"], g[f"B{r}"], g[f"C{r}"], g[f"D{r}"], g[f"E{r}"] = lot, PROJET, tache, resp, "Non commencé"
    for mois, h in charge.items():
        g[f"{MOIS[mois]}{r}"] = h

# --- Équipe : noms et rôles (les charges sont des formules)
e = wb["Équipe"]
for r in range(4, 28):
    if e[f"A{r}"].value is not None and not str(e[f"A{r}"].value).startswith("="):
        e[f"A{r}"].value = e[f"B{r}"].value = None
for r, (nom, role) in enumerate(EQUIPE, start=4):
    e[f"A{r}"], e[f"B{r}"] = nom, role

# --- Projets
p = wb["Projets"]
for r in range(4, 19):
    for col in "ABC":
        if not str(p[f"{col}{r}"].value or "").startswith("="):
            p[f"{col}{r}"].value = None
p["A4"], p["B4"], p["C4"] = PROJET, "Interne R&D", "Non commencé"

# --- Financement : une source interne couvrant toute la charge
total = sum(sum(c.values()) for *_, c in TACHES)
f = wb["Financement"]
for r in range(4, 19):
    for col in "ABCD":
        if not str(f[f"{col}{r}"].value or "").startswith("="):
            f[f"{col}{r}"].value = None
f["A4"], f["B4"], f["C4"], f["D4"] = "Interne", "Confirmé", "Budget R&D interne", total

# --- Répartition : chaque tâche financée à 100 % par la source interne
rep = wb["Répartition"]
for r in range(4, 104):
    for col in "ABC":
        rep[f"{col}{r}"].value = None
for r, (_, tache, _, charge) in enumerate(TACHES, start=4):
    rep[f"A{r}"], rep[f"B{r}"], rep[f"C{r}"] = tache, "Interne", sum(charge.values())

# --- Pointage : aucun réalisé à ce stade
pt = wb["Pointage"]
for r in range(4, 304):
    for col in ["A", "B", "C", "E", "F", "H"]:
        pt[f"{col}{r}"].value = None

wb.save(SORTIE)
print(f"{len(TACHES)} tâches, {total} h, écrit : {SORTIE.name}")
