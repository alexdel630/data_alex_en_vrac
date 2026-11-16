"""Analyse des sorties libRadtran : luminance du fond de ciel MWIR (3-5 µm) par altitude.

Sorties uvspec (output_user lambda zout uu, output_process per_nm) :
- solaire.out  : mW/(m² nm sr), unité du spectre solaire Kurucz fourni ;
- thermique.out : W/(m² nm sr).
"""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ICI = Path(__file__).parent
integrer = getattr(np, "trapezoid", None) or np.trapz   # numpy < 2 : trapz
H, C, K = 6.62607015e-34, 2.99792458e8, 1.380649e-23


def lire(nom, facteur):
    d = np.loadtxt(ICI / nom)
    return {z: (d[d[:, 1] == z, 0], d[d[:, 1] == z, 2] * facteur) for z in np.unique(d[:, 1])}


def planck_nm(lam_nm, t):
    """Luminance du corps noir en W/(m² nm sr)."""
    lam = lam_nm * 1e-9
    return 2 * H * C**2 / lam**5 / np.expm1(H * C / (lam * K * t)) * 1e-9


solaire = lire("solaire.out", 1e-3)    # mW -> W
thermique = lire("thermique.out", 1.0)

# Contrôle d'unité : au centre de la bande CO2 (4,25-4,35 µm) le trajet est opaque,
# la luminance thermique doit valoir environ B(T de l'air local).
T_US76 = {0.5: 284.9, 1: 281.7, 2: 275.2, 5: 255.7, 8: 236.2, 10: 223.3, 12: 216.7, 15: 216.7}
print("Contrôle bande CO2 4,3 µm : L_thermique / B(T_air)")
for z, (lam, l) in thermique.items():
    m = (lam >= 4250) & (lam <= 4350)
    print(f"  {z:5.1f} km : {l[m].mean() / planck_nm(lam[m], T_US76[z]).mean():.2f}")

lignes = ["| Altitude (km) | Solaire diffusé | Thermique | **Total** | Part thermique |",
          "|---|---|---|---|---|"]
fig, ax = plt.subplots(figsize=(9, 5.5))
for z in sorted(solaire):
    lam, ls = solaire[z]
    _, lt = thermique[z]
    tot = ls + lt
    i_s, i_t = integrer(ls, lam), integrer(lt, lam)   # W/(m² sr)
    lignes.append(f"| {z:g} | {i_s:.3g} | {i_t:.3g} | **{i_s + i_t:.3g}** | {100 * i_t / (i_s + i_t):.0f} % |")
    ax.plot(lam / 1000, tot * 1000, label=f"{z:g} km")   # W/(m² sr µm)

ax.set_yscale("log")
ax.set_xlabel("Longueur d'onde (µm)")
ax.set_ylabel("Luminance spectrale (W·m⁻²·sr⁻¹·µm⁻¹)")
ax.set_title("Fond de ciel MWIR — visée 1° au-dessus de l'horizon\n"
             "US Standard 1976, aérosols par défaut, soleil à 45°, azimut relatif 90°")
ax.grid(True, which="both", alpha=0.3)
ax.legend(title="Altitude", ncol=2)
fig.tight_layout()
fig.savefig(ICI / "luminance_mwir.png", dpi=150)

tableau = "\n".join(lignes)
print("\nLuminance intégrée 3-5 µm, W/(m² sr)\n" + tableau)
(ICI / "resultats.md").write_text(tableau + "\n", encoding="utf-8")
