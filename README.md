# Potassium after a 3-day orbital flight · Potasio tras un vuelo orbital de 3 días

**English** · [Español](#español)

Data and code for the exploratory secondary analysis *"Serum potassium and laboratory markers of the cortisol–aldosterone response after a 3-day orbital flight: an exploratory secondary analysis of NASA open data from the Inspiration4 civilian crew"*.

**Hypothesis.** Acute flight stress may alter cortisol and aldosterone secretion, and serum potassium would express that change. Hormones are not in the open dataset, so each arm is assessed through its laboratory markers: potassium, sodium, chloride and bicarbonate (aldosterone) and glucose, neutrophil-to-lymphocyte ratio and eosinophils (cortisol).

**Data.** NASA Open Science Data Repository: OSD-575 (comprehensive metabolic panel) and OSD-569 (complete blood count). Four civilian crew members, seven timepoints, 28 samples.

| Folder | Content |
|---|---|
| `code/build_dataset.py` | Builds `k_analysis.csv` from the two OSDR transformed files and applies the quality rules |
| `code/analysis_potassium.R` | Linear mixed models (random intercept per crew member, Kenward–Roger), Holm correction |
| `code/figures.py` | Figures 1–4 in English and Spanish |
| `data/k_analysis.csv` | Analysis dataset |
| `data/qc_log.csv` | Data-quality findings and actions |
| `results/results_models.csv` | Model estimates |

**Reproduce.**
```
python code/build_dataset.py LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv LSDS-7_Complete_Blood_Count_CBC_TRANSFORMED.csv
Rscript code/analysis_potassium.R
python code/figures.py
```
Requires R ≥ 4.3 with lme4, lmerTest and pbkrtest; Python 3 with pandas, numpy and matplotlib.

**Data-quality findings.** (1) R+45 samples show delayed serum separation (glucose < 55 mg/dL in 3 of 4 crew; potassium 5.9 mmol/L in one): glucose and potassium at R+45 are excluded. (2) In OSD-569, the absolute leukocyte counts of C003 at L-92 are shifted between columns; all absolute counts are recalculated as total leukocytes × differential %.

**Scope.** Exploratory and hypothesis-generating; not preregistered; n = 4. It does not establish causation.

**Related work.** Preregistered NLR analysis of the same crew: medRxiv, doi:10.64898/2026.10.16.26365757.

**Licence.** Code: MIT. Text, figures and derived data: CC BY 4.0.

---

## Español

Datos y código del análisis secundario exploratorio *"Potasio sérico y marcadores de laboratorio de la respuesta cortisol–aldosterona tras un vuelo orbital de 3 días"*.

**Hipótesis.** El estrés agudo del vuelo puede alterar la secreción de cortisol y aldosterona, y el potasio sérico sería la expresión de ese cambio. Las hormonas no están en los datos abiertos, por lo que cada vía se evalúa con sus marcadores de laboratorio: potasio, sodio, cloro y bicarbonato (aldosterona) y glucosa, índice neutrófilo-linfocito y eosinófilos (cortisol).

**Datos.** Open Science Data Repository de la NASA: OSD-575 (panel metabólico completo) y OSD-569 (biometría hemática). Cuatro tripulantes civiles, siete momentos, 28 muestras.

| Carpeta | Contenido |
|---|---|
| `code/build_dataset.py` | Construye `k_analysis.csv` a partir de los dos archivos transformados del OSDR y aplica las reglas de calidad |
| `code/analysis_potassium.R` | Modelos lineales mixtos (intercepto aleatorio por tripulante, Kenward–Roger), corrección de Holm |
| `code/figures.py` | Figuras 1–4 en inglés y español |
| `data/k_analysis.csv` | Conjunto de datos de análisis |
| `data/qc_log.csv` | Hallazgos de calidad de datos y acciones |
| `results/results_models.csv` | Estimaciones de los modelos |

**Reproducir.** Mismos comandos que en la sección en inglés.

**Hallazgos de calidad.** (1) Las muestras de R+45 muestran separación tardía del suero (glucosa < 55 mg/dL en 3 de 4 tripulantes; potasio de 5.9 mmol/L en uno): se excluyen glucosa y potasio en R+45. (2) En OSD-569, los recuentos absolutos de leucocitos de C003 en L-92 están desplazados entre columnas; todos los recuentos absolutos se recalculan como leucocitos totales × porcentaje.

**Alcance.** Exploratorio y generador de hipótesis; no prerregistrado; n = 4. No establece causalidad.

**Trabajo relacionado.** Análisis prerregistrado del INL en la misma tripulación: medRxiv, doi:10.64898/2026.10.16.26365757.

**Licencia.** Código: MIT. Texto, figuras y datos derivados: CC BY 4.0.

**Autor.** Víctor Junior Godínez-Vázquez · ORCID 0000-0003-0644-801X
