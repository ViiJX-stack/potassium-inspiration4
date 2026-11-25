import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
INK, NAVY, TEAL, ORANGE, GREY, BLUE = "#1E2A38", "#1F3A5F", "#0F7C80", "#D9822B", "#7A8B99", "#3A6EA5"
CREW_COL = {"C001": "#1F3A5F", "C002": "#0F7C80", "C003": "#D9822B", "C004": "#7A5C99"}
d = pd.read_csv("k_analysis.csv")
r = pd.read_csv("results_models.csv")
ORDER = ["L-92", "L-44", "L-3", "R+1", "R+45", "R+82", "R+194"]
X = {t: i for i, t in enumerate(ORDER)}

def save(fig, name):
    for ext in ("png", "tif"):
        kw = {"pil_kwargs": {"compression": "tiff_lzw"}} if ext == "tif" else {}
        fig.savefig(f"{name}.{ext}", dpi=400, facecolor="white", bbox_inches="tight", **kw)
    plt.close(fig)

# ---------- Figure 1: hypothesis schematic ----------
def fig1(lang):
    T = {"en": dict(stress="Acute flight\nstress\n(launch, re-entry,\nreadaptation\nto gravity)", ald="Aldosterone", cor="Cortisol", cat="Catecholamines",
                    k="Serum potassium\n(primary outcome)", na="Sodium, chloride,\nbicarbonate", glu="Glucose",
                    note="Hormones were not measured in the open dataset: each arm is assessed through its laboratory markers.",
                    a1="renal K⁺ excretion", a2="β2 shift of K⁺ into cells"),
         "es": dict(stress="Estrés agudo\ndel vuelo\n(lanzamiento,\nreentrada,\nreadaptación\na la gravedad)", ald="Aldosterona", cor="Cortisol", cat="Catecolaminas",
                    k="Potasio sérico\n(desenlace\nprincipal)", na="Sodio, cloro,\nbicarbonato", glu="Glucosa",
                    note="Las hormonas no se midieron en los datos abiertos: cada vía se evalúa con sus marcadores de laboratorio.",
                    a1="excreción renal de K⁺", a2="paso de K⁺ a las células (β2)")}[lang]
    fig, ax = plt.subplots(figsize=(7.2, 3.9)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 5.4)
    def box(x, y, w, h, txt, fc, tc="white", fs=9, bold=True):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15", fc=fc, ec=fc))
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", color=tc, fontsize=fs, fontweight="bold" if bold else "normal")
    def arr(x1, y1, x2, y2, c=GREY):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=c, lw=1.4))
    box(0.05, 1.95, 2.55, 1.5, T["stress"], NAVY, fs=7.6)
    box(3.3, 3.9, 2.0, 0.8, T["ald"], TEAL); box(3.3, 2.3, 2.0, 0.8, T["cor"], ORANGE); box(3.3, 0.7, 2.0, 0.8, T["cat"], GREY)
    for y in (4.3, 2.7, 1.1): arr(2.6, 2.7, 3.3, y)
    box(6.6, 2.0, 2.3, 1.35, T["k"], "#EEF3F7", tc=NAVY, fs=8.5)
    ax.add_patch(FancyBboxPatch((6.6, 2.0), 2.3, 1.35, boxstyle="round,pad=0.02,rounding_size=0.15", fc="none", ec=NAVY, lw=1.6))
    arr(5.3, 4.05, 6.7, 3.15, TEAL); ax.text(6.02, 3.42, T["a1"], fontsize=6.8, color=TEAL, ha="center", rotation=-33, bbox=dict(fc="white", ec="none", pad=0.5))
    arr(5.3, 1.1, 6.7, 2.25, GREY); ax.text(5.85, 1.45, T["a2"], fontsize=6.8, color=GREY, ha="center", rotation=38, bbox=dict(fc="white", ec="none", pad=0.5))
    box(6.6, 4.05, 2.3, 0.75, T["na"], "white", tc=TEAL, fs=8, bold=False); ax.add_patch(FancyBboxPatch((6.6, 4.05), 2.3, 0.75, boxstyle="round,pad=0.02,rounding_size=0.15", fc="none", ec=TEAL))
    arr(5.3, 4.4, 6.6, 4.4, TEAL)
    box(6.6, 0.45, 1.05, 0.75, T["glu"], "white", tc=ORANGE, fs=8, bold=False); ax.add_patch(FancyBboxPatch((6.6, 0.45), 1.05, 0.75, boxstyle="round,pad=0.02,rounding_size=0.15", fc="none", ec=ORANGE))
    arr(5.3, 2.5, 6.9, 1.2, ORANGE)
    ax.text(5.0, 0.02, T["note"], ha="center", fontsize=7, color=GREY, style="italic")
    save(fig, f"Fig1_hypothesis_{lang}")

# ---------- Figure 2: potassium trajectories ----------
def fig2(lang):
    L = {"en": dict(y="Serum potassium (mmol/L)", x="Timepoint (days relative to flight)", excl="R+45 excluded\n(delayed processing)", flight="Flight", pre="Preflight", ret="Return"),
         "es": dict(y="Potasio sérico (mmol/L)", x="Momento (días respecto al vuelo)", excl="R+45 excluido\n(procesamiento tardío)", flight="Vuelo", pre="Prevuelo", ret="Regreso")}[lang]
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.axvspan(3.5, 4.5, color="#F3E3D0", alpha=0.6, lw=0); ax.text(4.0, 6.05, L["excl"], ha="center", fontsize=7, color=ORANGE)
    ax.axvline(2.5, color=GREY, ls="--", lw=1); ax.text(2.5, 6.15, L["flight"], ha="center", fontsize=8, color=GREY)
    ax.axhspan(3.5, 5.3, color="#EEF3F7", lw=0, zorder=0)
    for c, g in d.groupby("crew"):
        g = g.set_index("timepoint").reindex(ORDER)
        xs = [X[t] for t in ORDER]; ys = g["potassium"].values
        ok = [t != "R+45" for t in ORDER]
        ax.plot([x for x, k in zip(xs, ok) if k], [y for y, k in zip(ys, ok) if k], "-o", color=CREW_COL[c], lw=1.6, ms=5, label=c)
        ax.plot(X["R+45"], g.loc["R+45", "potassium"], "o", mfc="white", mec=CREW_COL[c], ms=5)
    ax.set_xticks(range(7)); ax.set_xticklabels(ORDER); ax.set_ylabel(L["y"]); ax.set_xlabel(L["x"]); ax.set_ylim(2.8, 6.45)
    ax.legend(frameon=False, ncol=4, loc="lower center", bbox_to_anchor=(0.5, -0.38), fontsize=8)
    save(fig, f"Fig2_potassium_{lang}")

# ---------- Figure 3: forest plot of return effects (% of preflight mean) ----------
def fig3(lang):
    names = {"en": {"potassium": "Potassium (primary)", "sodium": "Sodium", "chloride": "Chloride", "bicarbonate": "Bicarbonate",
                    "glucose": "Glucose"},
             "es": {"potassium": "Potasio (principal)", "sodium": "Sodio", "chloride": "Cloro", "bicarbonate": "Bicarbonato",
                    "glucose": "Glucosa"}}[lang]
    L = {"en": dict(x="Change at return (R+1) vs preflight, % of preflight mean (95% CI)", ald="Aldosterone pathway (indirect markers)", cor="Acute stress response (non-specific)"),
         "es": dict(x="Cambio al regreso (R+1) vs prevuelo, % de la media prevuelo (IC 95 %)", ald="Vía de la aldosterona (marcadores indirectos)", cor="Respuesta aguda al estrés (no específico)")}[lang]
    rr = r[r.contrast == "phase2_return"].set_index("marker")
    order = ["potassium", "sodium", "chloride", "bicarbonate", "glucose"]
    rows = []
    for m in order:
        x = rr.loc[m]
        if x.log_scale:
            e, lo, hi = (np.exp(x.est) - 1) * 100, (np.exp(x.lo) - 1) * 100, (np.exp(x.hi) - 1) * 100
        else:
            e, lo, hi = x.est / x.pre_mean * 100, x.lo / x.pre_mean * 100, x.hi / x.pre_mean * 100
        pdisp = x.p if m == "potassium" else x.p_holm
        rows.append((m, e, lo, hi, pdisp, x.arm))
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    for i, (m, e, lo, hi, p, arm) in enumerate(rows):
        y = len(rows) - 1 - i
        col = TEAL if arm == "Aldosterone" else ORANGE
        ax.plot([lo, hi], [y, y], color=col, lw=2)
        ax.plot(e, y, "D" if m == "potassium" else "o", color=col, ms=7 if m == "potassium" else 6)
        lab = ("p" if m == "potassium" else "p (Holm)") + (" = %.3f" % p if p >= 0.001 else " < 0.001")
        ax.text(66, y, lab, va="center", fontsize=7.5, color=INK)
    ax.axvline(0, color=GREY, lw=1)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([names[m] for m, *_ in rows][::-1])
    ax.set_xlim(-45, 95); ax.set_xlabel(L["x"])
    ax.text(-44, 4.45, L["ald"], color=TEAL, fontsize=8, fontweight="bold", va="bottom", bbox=dict(fc="white", ec="none", pad=1), zorder=5); ax.text(-44, 0.52, L["cor"], color=ORANGE, fontsize=8, fontweight="bold", va="bottom", bbox=dict(fc="white", ec="none", pad=1), zorder=5)
    ax.axhline(0.5, color="#DDE3E8", lw=0.8); ax.set_ylim(-0.6, 4.95)
    save(fig, f"Fig3_forest_{lang}")

# ---------- Figure 4: per-crew change heatmap ----------
def fig4(lang):
    names = {"en": ["Potassium", "Sodium", "Chloride", "Bicarbonate", "Glucose"],
             "es": ["Potasio", "Sodio", "Cloro", "Bicarbonato", "Glucosa"]}[lang]
    L = {"en": dict(cb="Change at R+1 vs own preflight mean (% )", exp="Expected"), "es": dict(cb="Cambio en R+1 vs media prevuelo propia (%)", exp="Esperado")}[lang]
    vars_ = ["potassium_a", "sodium", "chloride", "bicarbonate", "glucose_a"]
    expected = ["?", "↑", "↓", "↑", "↑"]
    crews = ["C001", "C002", "C003", "C004"]
    M = np.zeros((len(vars_), 4))
    for i, v in enumerate(vars_):
        for j, c in enumerate(crews):
            g = d[d.crew == c]
            pre = g[g.phase == "1_pre"][v].mean(); r1 = g[g.timepoint == "R+1"][v].iloc[0]
            M[i, j] = (r1 - pre) / pre * 100
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    lim = 45
    im = ax.imshow(np.clip(M, -lim, lim), cmap="BrBG_r", vmin=-lim, vmax=lim, aspect="auto")
    for i in range(M.shape[0]):
        for j in range(4):
            ax.text(j, i, f"{(round(M[i, j]) + 0):+.0f}", ha="center", va="center", fontsize=8, color="white" if abs(M[i, j]) > 28 else INK)
        ax.text(4.0, i, expected[i], ha="center", va="center", fontsize=9, color=NAVY, fontweight="bold")
    ax.set_xticks(list(range(4)) + [4.0]); ax.set_xticklabels(crews + [L["exp"]], fontsize=8)
    ax.set_yticks(range(len(vars_))); ax.set_yticklabels(names)
    ax.set_xlim(-0.5, 4.5)
    for s in ax.spines.values(): s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02); cb.set_label(L["cb"], fontsize=7.5); cb.ax.tick_params(labelsize=7)
    save(fig, f"Fig4_heatmap_{lang}")

for lang in ("en", "es"):
    fig1(lang); fig2(lang); fig3(lang); fig4(lang)
print("ok")
