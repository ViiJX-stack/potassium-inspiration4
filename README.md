# Serum potassium after a 3-day orbital flight
# Potasio sérico tras un vuelo orbital de 3 días

**English** · [Español](#español)

Data and code for the exploratory secondary analysis *"Serum potassium after a 3-day orbital flight: an exploratory secondary analysis of NASA open data from the Inspiration4 civilian crew"*.

**Hypothesis.** Flight stress may modulate the renin–angiotensin–aldosterone system, so that serum potassium varies through its renal handling. Hormones are not in the open dataset, so this hypothesis cannot be tested directly; the metabolic panel provides indirect markers: sodium, chloride and bicarbonate (aldosterone pathway) and glucose (non-specific marker of the acute stress response). Creatinine is analysed as renal context.

**Data.** NASA Open Science Data Repository: OSD-575 (comprehensive metabolic panel). Four civilian crew members, seven timepoints, 28 samples.

| Folder | Content |
|---|---|
| `code/build_dataset.py` | Builds `k_analysis.csv` from the OSDR transformed file and applies the quality rule |
| `code/analysis_potassium.R` | Linear mixed models (random intercept per crew member, Kenward–Roger), Holm correction |
| `code/figures.py` | Figures 1–4 in English and Spanish |
| `data/k_analysis.csv` | Analysis dataset |
| `data/qc_log.csv` | Data-quality findings and actions |
| `results/results_models.csv` | Model estimates |

**Reproduce.**
```
python code/build_dataset.py LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv
Rscript code/analysis_potassium.R
python code/figures.py
```
Requires R ≥ 4.3 with lme4, lmerTest and pbkrtest; Python 3 with pandas, numpy and matplotlib.

**Data-quality finding.** R+45 samples show delayed serum separation (glucose < 55 mg/dL in 3 of 4 crew; potassium 5.9 mmol/L in one): glucose and potassium at R+45 are excluded.

**Scope.** Exploratory and hypothesis-generating; not preregistered; n = 4. It does not establish causation.

**Licence.** Code: MIT. Text, figures and derived data: CC BY 4.0.

---

## Español

Datos y código del análisis secundario exploratorio *"Potasio sérico tras un vuelo orbital de 3 días: análisis secundario exploratorio de datos abiertos de la NASA de la tripulación civil de Inspiration4"*.

**Hipótesis.** El estrés del vuelo podría modular el sistema renina–angiotensina–aldosterona, de modo que el potasio sérico varíe a través de su manejo renal. Las hormonas no están en los datos abiertos, por lo que esta hipótesis no puede probarse directamente; el panel metabólico ofrece marcadores indirectos: sodio, cloro y bicarbonato (vía de la aldosterona) y glucosa (marcador no específico de la respuesta aguda al estrés). La creatinina se analiza como contexto renal.

**Datos.** Open Science Data Repository de la NASA: OSD-575 (panel metabólico completo). Cuatro tripulantes civiles, siete momentos, 28 muestras.

| Carpeta | Contenido |
|---|---|
| `code/build_dataset.py` | Construye `k_analysis.csv` a partir del archivo transformado del OSDR y aplica la regla de calidad |
| `code/analysis_potassium.R` | Modelos lineales mixtos (intercepto aleatorio por tripulante, Kenward–Roger), corrección de Holm |
| `code/figures.py` | Figuras 1–4 en inglés y español |
| `data/k_analysis.csv` | Conjunto de datos de análisis |
| `data/qc_log.csv` | Hallazgos de calidad de datos y acciones |
| `results/results_models.csv` | Estimaciones de los modelos |

**Reproducir.** Mismos comandos que en la sección en inglés.

**Hallazgo de calidad.** Las muestras de R+45 muestran separación tardía del suero (glucosa < 55 mg/dL en 3 de 4 tripulantes; potasio de 5.9 mmol/L en uno): se excluyen glucosa y potasio en R+45.

**Alcance.** Exploratorio y generador de hipótesis; no prerregistrado; n = 4. No establece causalidad.

**Licencia.** Código: MIT. Texto, figuras y datos derivados: CC BY 4.0.

**Autor.** Víctor Junior Godínez-Vázquez · ORCID 0000-0003-0644-801X
