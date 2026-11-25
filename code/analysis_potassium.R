# Potassium and markers of the cortisol-aldosterone response after spaceflight
# Inspiration4 crew, NASA OSDR metabolic panel (OSD-575). Exploratory, hypothesis-generating analysis.
suppressPackageStartupMessages({ library(lme4); library(lmerTest); library(pbkrtest) })
d <- read.csv("k_analysis.csv")
d$phase <- factor(d$phase, levels = c("1_pre", "2_return", "3_recovery"))

markers <- list(
  potassium   = list(var = "potassium_a", log = FALSE, role = "primary",   arm = "Aldosterone"),
  sodium      = list(var = "sodium",      log = FALSE, role = "secondary", arm = "Aldosterone"),
  chloride    = list(var = "chloride",    log = FALSE, role = "secondary", arm = "Aldosterone"),
  bicarbonate = list(var = "bicarbonate", log = FALSE, role = "secondary", arm = "Aldosterone"),
  glucose     = list(var = "glucose_a",   log = FALSE, role = "secondary", arm = "Stress"),
  creatinine  = list(var = "creatinine",  log = FALSE, role = "context",   arm = "Renal")
)

out <- list()
for (nm in names(markers)) {
  m <- markers[[nm]]
  f <- as.formula(paste(m$var, "~ phase + (1|crew)"))
  fit <- lmer(f, data = d, REML = TRUE)
  s <- summary(fit, ddf = "Kenward-Roger")$coefficients
  vc <- as.data.frame(VarCorr(fit))
  icc <- vc$vcov[1] / sum(vc$vcov)
  pre_mean <- mean(d[[m$var]][d$phase == "1_pre"], na.rm = TRUE)
  for (ct in c("phase2_return", "phase3_recovery")) {
    est <- s[ct, "Estimate"]; se <- s[ct, "Std. Error"]; df <- s[ct, "df"]; p <- s[ct, "Pr(>|t|)"]
    lo <- est - qt(0.975, df) * se; hi <- est + qt(0.975, df) * se
    out[[length(out) + 1]] <- data.frame(marker = nm, arm = m$arm, role = m$role, contrast = ct,
      n = nobs(fit), est = est, lo = lo, hi = hi, se = se, df = df, p = p, icc = icc,
      log_scale = m$log, pre_mean = pre_mean, singular = isSingular(fit))
  }
}
res <- do.call(rbind, out)
# Holm correction across the four secondary markers, return contrast only
sec <- res$role == "secondary" & res$contrast == "phase2_return"
res$p_holm <- NA
res$p_holm[sec] <- p.adjust(res$p[sec], method = "holm")
# Back-transform log-scale markers to ratios
res$ratio <- ifelse(res$log_scale, exp(res$est), NA)
res$ratio_lo <- ifelse(res$log_scale, exp(res$lo), NA)
res$ratio_hi <- ifelse(res$log_scale, exp(res$hi), NA)
write.csv(res, "results_models.csv", row.names = FALSE)
print(format(res[, c("marker","contrast","n","est","lo","hi","df","p","p_holm","icc","ratio","singular")], digits = 3), row.names = FALSE)

# Sensitivity: bicarbonate excluding R+45 (same delayed-processing samples)
fb <- lmer(bicarbonate ~ phase + (1|crew), data = subset(d, timepoint != "R+45"), REML = TRUE)
print(summary(fb, ddf = "Kenward-Roger")$coefficients)
# Per-crew change at R+1 versus own preflight mean
for (v in c("potassium_a", "glucose_a", "bicarbonate", "sodium", "chloride", "creatinine")) {
  pre <- tapply(d[[v]][d$phase == "1_pre"], d$crew[d$phase == "1_pre"], mean, na.rm = TRUE)
  r1 <- setNames(d[[v]][d$timepoint == "R+1"], d$crew[d$timepoint == "R+1"])
  cat(v, ":", paste(names(r1), round(r1 - pre[names(r1)], 2), collapse = "  "), "\n")
}
