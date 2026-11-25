"""Build the analysis dataset from the NASA OSDR Inspiration4 metabolic panel.
Input (download from the OSDR study page OSD-575):
  LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv
Output: k_analysis.csv
"""
import sys
import numpy as np
import pandas as pd

cmp_file = sys.argv[1] if len(sys.argv) > 1 else "LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv"
cmp = pd.read_csv(cmp_file, encoding="utf-8-sig")
cmp["crew"] = cmp["Sample Name"].str.split("_").str[0]
cmp["timepoint"] = cmp["Sample Name"].str.split("_").str[2]

d = cmp[["crew", "timepoint"]].copy()
cols = {"potassium": "potassium_value_millimol_per_liter", "sodium": "sodium_value_millimol_per_liter",
        "chloride": "chloride_value_millimol_per_liter", "bicarbonate": "carbon_dioxide_value_millimol_per_liter",
        "glucose": "glucose_value_milligram_per_deciliter", "creatinine": "creatinine_value_milligram_per_deciliter"}
for k, v in cols.items():
    d[k] = pd.to_numeric(cmp[v], errors="coerce")

d["day"] = d.timepoint.map({"L-92": -92, "L-44": -44, "L-3": -3, "R+1": 1, "R+45": 45, "R+82": 82, "R+194": 194})
d["phase"] = np.where(d.timepoint.str.startswith("L"), "1_pre", np.where(d.timepoint == "R+1", "2_return", "3_recovery"))
# R+45: delayed serum separation (glucose < 55 mg/dL in 3 of 4 crew, potassium 5.9 mmol/L in one)
d["qc_r45"] = d.timepoint.eq("R+45")
d["potassium_a"] = d.potassium.where(~d.qc_r45)
d["glucose_a"] = d.glucose.where(~d.qc_r45)
d.sort_values(["crew", "day"]).to_csv("k_analysis.csv", index=False)
print("k_analysis.csv written:", len(d), "rows")
