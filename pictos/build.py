"""Génère la bibliothèque de pictos (SVG 24x24, trait, couleur = currentColor).

Chaque catégorie est un module dans icones/ exposant ICONS = {nom: contenu SVG}.
Sortie : svg/<categorie>/<nom>.svg + apercu.html.
"""
import runpy
import shutil
from pathlib import Path

CATEGORIES = {
    "strategie": "Pilotage & stratégie",
    "finance-donnees": "Données & finance",
    "commerce-client": "Commerce & client",
    "equipe-rh": "Équipe & RH",
    "planning-suivi": "Planning & suivi",
    "formation-recherche": "Formation & recherche",
    "communication": "Communication",
    "numerique-it": "Numérique & IT",
    "securite-juridique": "Sécurité & juridique",
    "ingenierie": "Projet ingénierie",
    "industrie-energie": "Industrie & énergie",
    "transport-logistique": "Transport & logistique",
    "environnement-rse": "Environnement & RSE",
    "interface-fleches": "Interface & flèches",
}

HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" '
        'fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">')

root = Path(__file__).parent
out = root / "svg"
shutil.rmtree(out, ignore_errors=True)

library = {}
for cat in CATEGORIES:
    module = root / "icones" / f"{cat}.py"
    library[cat] = runpy.run_path(str(module))["ICONS"] if module.exists() else {}
    (out / cat).mkdir(parents=True, exist_ok=True)
    for name, body in library[cat].items():
        (out / cat / f"{name}.svg").write_text(f"{HEAD}{body}</svg>\n", encoding="utf-8")

total = sum(len(icons) for icons in library.values())
sections = "\n".join(
    f'<h2>{CATEGORIES[cat]} <small>{len(icons)}</small></h2><div class="grid">'
    + "".join(f'<figure title="{cat}/{n}.svg"><div class="ic">{HEAD}{b}</svg></div>'
              f'<figcaption>{n}</figcaption></figure>' for n, b in icons.items())
    + "</div>"
    for cat, icons in library.items() if icons)
(root / "apercu.html").write_text(f"""<!doctype html><html lang="fr"><meta charset="utf-8">
<title>Pictos présentation</title>
<style>
body{{font-family:Segoe UI,sans-serif;margin:32px;background:#fff;color:#1f2a44}}
h1{{font-weight:600;font-size:22px}} h2{{font-size:16px;margin:28px 0 10px}} small{{color:#99a;font-weight:400}}
p{{color:#667}} label{{margin-right:16px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:12px}}
figure{{margin:0;border:1px solid #e3e6ee;border-radius:10px;padding:16px 8px;text-align:center}}
.ic svg{{width:var(--s,40px);height:var(--s,40px);color:var(--c,#1f2a44)}}
figcaption{{font-size:12px;color:#667;margin-top:8px;word-break:break-word}}
</style>
<h1>Bibliothèque de pictos — {total} icônes</h1>
<p>SVG 24×24, trait 1,75, couleur pilotée par <code>currentColor</code>. Fichiers dans <code>svg/&lt;catégorie&gt;/</code>.</p>
<label>Couleur <input type="color" value="#1f2a44" oninput="document.body.style.setProperty('--c',this.value)"></label>
<label>Taille <input type="range" min="24" max="96" value="40" oninput="document.body.style.setProperty('--s',this.value+'px')"></label>
{sections}
</html>
""", encoding="utf-8")
print(total, "icônes générées")
