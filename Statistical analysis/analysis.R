# Statistical Analysis — LLM Replication of Software Estimation Bias Studies

library(jsonlite)
library(effsize)

output_file <- "output.md"
sink(output_file)

MODELS <- c(
  "google/gemini-3-flash-preview" = "Gemini",
  "anthropic/claude-opus-4.6"     = "Claude",
  "openai/gpt-5.2-codex"          = "GPT",
  "deepseek/deepseek-v3.2"        = "DeepSeek",
  "moonshotai/kimi-k2.5"          = "Kimi"
)

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

roms_correction <- function(p_vals, alpha = 0.05) {
  c_tests <- length(p_vals)
  if (c_tests == 1) return(setNames(p_vals < alpha, names(p_vals)))
  rom_alpha <- numeric(c_tests)
  rom_alpha[1] <- alpha
  if (c_tests >= 2) rom_alpha[2] <- 1 - (1 - alpha)^2
  if (c_tests >= 3) rom_alpha[3] <- 1 - (1 - alpha)^3 - 3 * alpha * (1 - alpha)^2
  if (c_tests >= 4) {
    for (k in 4:c_tests) {
      rom_alpha[k] <- alpha
      for (j in 1:(k-1))
        rom_alpha[k] <- rom_alpha[k] + ((-1)^(j+1)) * choose(k, j) * (1 - rom_alpha[j])^(k - j) * alpha^j
    }
  }
  ordered_idx <- order(p_vals, decreasing = TRUE)
  rejected <- logical(c_tests)
  for (i in seq_along(ordered_idx)) {
    if (p_vals[ordered_idx[i]] <= rom_alpha[c_tests - i + 1]) {
      rejected[ordered_idx[i:length(ordered_idx)]] <- TRUE
      break
    }
  }
  setNames(rejected, names(p_vals))
}

paired_test <- function(a, b, label_a, label_b, hypothesis = c("two.sided", "greater", "less")) {
  hypothesis <- match.arg(hypothesis)
  n <- length(a)
  if (n < 3) {
    cat(sprintf("    [UNDERPOWERED n=%d] %s vs %s\n", n, label_a, label_b))
    return(invisible(NULL))
  }
  w2 <- wilcox.test(a, b, paired = TRUE, alternative = "two.sided")
  w1 <- wilcox.test(a, b, paired = TRUE, alternative = hypothesis)
  cd <- cliff.delta(a, b)
  cat(sprintf("    %s vs %s  n=%d  W=%g  p=%.4f  p1=%.4f  d=%.3f (%s)\n",
              label_a, label_b, n, w2$statistic, w2$p.value, w1$p.value,
              cd$estimate, cd$magnitude))
  invisible(list(p = w2$p.value, d = cd$estimate))
}

onesample_test <- function(x, label, mu = 0, hypothesis = "greater") {
  x <- x[!is.na(x)]
  n <- length(x)
  if (n < 3) {
    cat(sprintf("    [UNDERPOWERED n=%d] %s\n", n, label))
    return(invisible(NULL))
  }
  w2 <- wilcox.test(x, mu = mu, alternative = "two.sided")
  w1 <- wilcox.test(x, mu = mu, alternative = hypothesis)
  d  <- (sum(x > mu) - sum(x < mu)) / n
  cat(sprintf("    %s  n=%d  V=%g  p=%.4f  p1=%.4f  d=%.3f\n",
              label, n, w2$statistic, w2$p.value, w1$p.value, d))
  invisible(list(p = w2$p.value, d = d))
}

print_roms <- function(results, alpha = 0.05) {
  p_vals <- sapply(results, function(r) if (is.null(r)) NA else r$p)
  p_vals <- p_vals[!is.na(p_vals)]
  if (length(p_vals) == 0) return(invisible(NULL))
  rejected <- roms_correction(p_vals, alpha)
  cat("    Rom's:\n")
  for (nm in names(rejected))
    cat(sprintf("      %s: %s\n", nm, if (rejected[nm]) "significant" else "not significant"))
}

match_pairs <- function(list_a, list_b) {
  shared <- intersect(names(list_a), names(list_b))
  a <- unlist(list_a[shared])
  b <- unlist(list_b[shared])
  keep <- !is.na(a) & !is.na(b)
  list(a = a[keep], b = b[keep])
}

`%||%` <- function(x, y) if (is.null(x) || length(x) == 0) y else x


# -----------------------------------------------------------------------------
# 1. Aranda & Easterbrook (2005) — Anchoring
# -----------------------------------------------------------------------------
cat("\n# Aranda & Easterbrook (2005)\n")

aranda <- fromJSON("results/aranda2005_results.json", simplifyVector = FALSE)

for (mkey in names(MODELS)) {
  cat(sprintf("\n## %s\n", MODELS[mkey]))
  ctrl <- low <- high <- list()
  for (key in names(aranda[[mkey]])) {
    if (startsWith(key, "aranda_")) next
    v <- aranda[[mkey]][[key]][["months"]]
    if (is.null(v)) next
    if      (endsWith(key, "_control")) ctrl[[key]] <- v
    else if (endsWith(key, "_low"))     low[[key]]  <- v
    else if (endsWith(key, "_high"))    high[[key]] <- v
  }
  strip  <- function(lst, sfx) setNames(lst, sub(sfx, "", names(lst)))
  p_low  <- match_pairs(strip(low, "_low"),   strip(ctrl, "_control"))
  p_high <- match_pairs(strip(high, "_high"), strip(ctrl, "_control"))
  r <- list(
    low  = paired_test(p_low$a,  p_low$b,  "low",  "control", "less"),
    high = paired_test(p_high$a, p_high$b, "high", "control", "greater")
  )
  print_roms(r)
}


# -----------------------------------------------------------------------------
# 2. Løhre & Jørgensen (2014) — Numerical Anchors
# -----------------------------------------------------------------------------
cat("\n# Løhre & Jørgensen (2014)\n")

lohre <- fromJSON("results/lohre2014_results.json", simplifyVector = FALSE)

lohre_hypotheses <- list(
  exp1 = list(conditions = c("precise_single", "round_single", "precise_interval", "imprecise_interval"), direction = "greater"),
  exp2 = list(conditions = c("precise_interval", "imprecise_interval"), direction = "less"),
  exp3 = list(conditions = c("low_credibility", "neutral", "high_credibility"), direction = "less")
)

for (exp in names(lohre_hypotheses)) {
  cat(sprintf("\n## %s\n", exp))
  hyp      <- lohre_hypotheses[[exp]]
  exp_data <- lohre[[exp]]

  for (mkey in names(MODELS)) {
    cat(sprintf("\n### %s\n", MODELS[mkey]))
    model_data <- exp_data[[mkey]]

    cond_vals <- list()
    for (doc in names(model_data))
      for (cond in names(model_data[[doc]])) {
        v <- model_data[[doc]][[cond]][["most_likely"]]
        if (!is.null(v)) cond_vals[[cond]][[doc]] <- v
      }

    results <- list()
    for (cond in hyp$conditions) {
      p <- match_pairs(cond_vals[[cond]], cond_vals[["control"]])
      results[[paste(cond, "vs control")]] <- paired_test(p$a, p$b, cond, "control", hyp$direction)
    }

    if (exp == "exp1") {
      p <- match_pairs(cond_vals[["precise_single"]], cond_vals[["round_single"]])
      results[["precise_single vs round_single"]] <- paired_test(p$a, p$b, "precise_single", "round_single", "two.sided")
      p <- match_pairs(cond_vals[["precise_interval"]], cond_vals[["imprecise_interval"]])
      results[["precise_interval vs imprecise_interval"]] <- paired_test(p$a, p$b, "precise_interval", "imprecise_interval", "two.sided")
    }

    if (exp == "exp2") {
      p <- match_pairs(cond_vals[["precise_interval"]], cond_vals[["imprecise_interval"]])
      results[["precise vs imprecise"]] <- paired_test(p$a, p$b, "precise", "imprecise", "two.sided")
    }

    if (exp == "exp3") {
      p <- match_pairs(cond_vals[["low_credibility"]], cond_vals[["neutral"]])
      results[["low vs neutral"]] <- paired_test(p$a, p$b, "low_cred", "neutral", "two.sided")
      p <- match_pairs(cond_vals[["neutral"]], cond_vals[["high_credibility"]])
      results[["neutral vs high"]] <- paired_test(p$a, p$b, "neutral", "high_cred", "two.sided")
      p <- match_pairs(cond_vals[["low_credibility"]], cond_vals[["high_credibility"]])
      results[["low vs high"]] <- paired_test(p$a, p$b, "low_cred", "high_cred", "two.sided")
    }

    print_roms(results)
  }
}


# -----------------------------------------------------------------------------
# 3. Connolly & Dean (1997) — Decomposed vs Holistic Estimates
# -----------------------------------------------------------------------------
cat("\n# Connolly & Dean (1997)\n")

s1 <- fromJSON("results/connolly1997_study1_results.json", simplifyVector = FALSE)
s2 <- fromJSON("results/connolly1997_study2_results.json", simplifyVector = FALSE)

extract_s1 <- function(data, cond, model, field) {
  vals <- c()
  for (pair in names(data[[cond]][[model]]))
    for (doc in names(data[[cond]][[model]][[pair]])) {
      v <- data[[cond]][[model]][[pair]][[doc]][[field]]
      if (!is.null(v)) vals <- c(vals, v)
    }
  vals
}

extract_pi_width <- function(data, cond, model) {
  vals <- c()
  for (pair in names(data[[cond]][[model]]))
    for (doc in names(data[[cond]][[model]][[pair]])) {
      f <- data[[cond]][[model]][[pair]][[doc]][["whole_fractiles"]]
      p50 <- f[["p50"]]; p01 <- f[["p01"]]; p99 <- f[["p99"]]
      if (!is.null(p50) && !is.null(p01) && !is.null(p99) && p50 > 0)
        vals <- c(vals, (p99 - p01) / p50)
    }
  vals
}

for (mkey in names(MODELS)) {
  cat(sprintf("\n## %s\n", MODELS[mkey]))

  cat("\n### H3a: gap vs zero\n")
  h3a <- list()
  for (cond in c("A", "B", "C", "D")) {
    gaps <- extract_s1(s1, cond, mkey, "gap")
    h3a[[paste("cond", cond)]] <- onesample_test(gaps, paste("cond", cond), mu = 0, hypothesis = "greater")
  }
  print_roms(h3a)

  cat("\n### H3b: subtask-first vs whole-first\n")
  h3b <- list()
  for (pair in list(c("B","A"), c("D","C"))) {
    g1  <- extract_s1(s1, pair[1], mkey, "gap")
    g2  <- extract_s1(s1, pair[2], mkey, "gap")
    n   <- min(length(g1), length(g2))
    lbl <- paste(pair[1], "vs", pair[2])
    h3b[[lbl]] <- paired_test(g1[1:n], g2[1:n], pair[1], pair[2], "greater")
  }
  print_roms(h3b)

  cat("\n### H3c: less-than vs greater-than wording\n")
  h3c <- list()
  for (pair in list(c("C","A"), c("D","B"))) {
    g1  <- extract_s1(s1, pair[1], mkey, "gap")
    g2  <- extract_s1(s1, pair[2], mkey, "gap")
    n   <- min(length(g1), length(g2))
    lbl <- paste(pair[1], "vs", pair[2])
    h3c[[lbl]] <- paired_test(g1[1:n], g2[1:n], pair[1], pair[2], "two.sided")
  }
  print_roms(h3c)

  cat("\n### H3d: Study 2 vs Study 1 PI width\n")
  for (cond in c("A", "B")) {
    w2 <- extract_pi_width(s2, cond, mkey)
    w1 <- extract_pi_width(s1, cond, mkey)
    n  <- min(length(w2), length(w1))
    cat(sprintf("    S2%s median=%.3f  S1%s median=%.3f\n", cond, median(w2), cond, median(w1)))
    paired_test(w2[1:n], w1[1:n], paste0("S2",cond), paste0("S1",cond), "greater")
  }
}


# -----------------------------------------------------------------------------
# 4. Jørgensen et al. (2002) — Overconfidence in Prediction Intervals
# -----------------------------------------------------------------------------
cat("\n# Jørgensen et al. (2002)\n")

j02a <- fromJSON("results/jorgensen2002_study_a_results.json", simplifyVector = FALSE)
j02b <- fromJSON("results/jorgensen2002_study_b_results.json", simplifyVector = FALSE)
j02c <- fromJSON("results/jorgensen2002_study_c_results.json", simplifyVector = FALSE)
j02d <- fromJSON("results/jorgensen2002_study_d_results.json", simplifyVector = FALSE)

cat("\n## Study A: PI width (descriptive)\n")
for (mkey in names(MODELS)) {
  widths <- sapply(j02a[[mkey]], function(d) d[["pi_width"]] %||% NA)
  widths <- widths[!is.na(widths)]
  cat(sprintf("    %-10s n=%d  median=%.3f  IQR=%.3f\n",
              MODELS[mkey], length(widths), median(widths), IQR(widths)))
}

cat("\n## Study B: GROUP vs mean-of-individuals\n")
roles <- c("EM", "PM", "UD", "DEV")
for (mkey in names(MODELS)) {
  cat(sprintf("\n### %s\n", MODELS[mkey]))
  group_w <- c(); indiv_w <- c()
  for (doc in names(j02b[[mkey]])) {
    d  <- j02b[[mkey]][[doc]]
    gw <- d[["GROUP"]][["pi_width"]]
    iw <- mean(sapply(roles, function(r) d[[r]][["pi_width"]] %||% NA), na.rm = TRUE)
    if (!is.null(gw) && !is.na(iw)) { group_w <- c(group_w, gw); indiv_w <- c(indiv_w, iw) }
  }
  paired_test(group_w, indiv_w, "GROUP", "mean-indiv", "less")
}

cat("\n## Study C: PI width by confidence level\n")
conf_pairs <- list(c("50","75"), c("75","90"), c("90","99"))
for (mkey in names(MODELS)) {
  cat(sprintf("\n### %s\n", MODELS[mkey]))
  results <- list()
  for (pair in conf_pairs) {
    lo   <- sapply(j02c[[mkey]], function(d) d[[pair[1]]][["pi_width"]] %||% NA)
    hi   <- sapply(j02c[[mkey]], function(d) d[[pair[2]]][["pi_width"]] %||% NA)
    keep <- !is.na(lo) & !is.na(hi)
    lbl  <- paste(pair[1], "vs", pair[2])
    results[[lbl]] <- paired_test(hi[keep], lo[keep], pair[2], pair[1], "greater")
  }
  print_roms(results)
}

cat("\n## Study D: ego-free vs Study A\n")
for (mkey in names(MODELS)) {
  cat(sprintf("\n### %s\n", MODELS[mkey]))
  shared <- intersect(names(j02d[[mkey]]), names(j02a[[mkey]]))
  wd   <- sapply(shared, function(k) j02d[[mkey]][[k]][["pi_width"]] %||% NA)
  wa   <- sapply(shared, function(k) j02a[[mkey]][[k]][["pi_width"]] %||% NA)
  keep <- !is.na(wd) & !is.na(wa)
  paired_test(wd[keep], wa[keep], "Study D", "Study A", "greater")
}


# -----------------------------------------------------------------------------
# 5. Jørgensen (2009) — Risk Identification and Over-Optimism
# -----------------------------------------------------------------------------
cat("\n# Jørgensen (2009)\n")

j09 <- fromJSON("results/jorgensen2009_results.json", simplifyVector = FALSE)

for (exp in c("exp_a", "exp_b", "exp_c", "exp_d")) {
  cat(sprintf("\n## %s\n", exp))
  for (mkey in names(MODELS)) {
    cat(sprintf("\n### %s\n", MODELS[mkey]))

    get_field <- function(cond, field) {
      docs <- j09[[exp]][[cond]][[mkey]]
      vals <- sapply(names(docs), function(k) { v <- docs[[k]][[field]]; if (is.null(v)) NA else v })
      list(vals = vals, names = names(docs))
    }

    less_r <- get_field("LESS", "num_risks")
    more_r <- get_field("MORE", "num_risks")
    shared <- intersect(less_r$names, more_r$names)

    cat("    Manipulation check:\n")
    mc <- paired_test(more_r$vals[shared], less_r$vals[shared], "MORE", "LESS", "greater")
    if (!is.null(mc) && mc$p > 0.05)
      cat("    [WARNING: manipulation check failed]\n")

    results <- list()
    for (field in c("effort", "success")) {
      less_f   <- get_field("LESS", field)
      more_f   <- get_field("MORE", field)
      shared_f <- intersect(less_f$names, more_f$names)
      direction <- if (field == "effort") "less" else "greater"
      results[[field]] <- paired_test(more_f$vals[shared_f], less_f$vals[shared_f], "MORE", "LESS", direction)
    }
    print_roms(results)
  }
}


# -----------------------------------------------------------------------------
# 6. Moløkken & Jørgensen (2003) — Group Discussion Effects
# -----------------------------------------------------------------------------
cat("\n# Moløkken & Jørgensen (2003)\n")

mol <- fromJSON("results/molokken2003_results.json", simplifyVector = FALSE)

for (mkey in names(MODELS)) {
  cat(sprintf("\n## %s\n", MODELS[mkey]))
  before <- c(); group <- c(); after <- c()
  before_dist <- c(); after_dist <- c()

  for (doc in names(mol[[mkey]])) {
    d  <- mol[[mkey]][[doc]]
    ab <- d[["avg_before"]]; g <- d[["group"]]; aa <- d[["avg_after"]]
    if (!is.null(ab) && !is.null(g) && !is.null(aa) && ab > 0 && g > 0 && aa > 0) {
      before <- c(before, ab); group <- c(group, g); after <- c(after, aa)
      before_dist <- c(before_dist, abs(ab - g))
      after_dist  <- c(after_dist,  abs(aa - g))
    }
  }

  cat("    H6a: group vs avg_before\n")
  cat("    H6b: convergence\n")
  h6 <- list(
    H6a = paired_test(group, before, "group", "avg_before", "less"),
    H6b = paired_test(after_dist, before_dist, "after_dist", "before_dist", "less")
  )
  print_roms(h6)
}


# -----------------------------------------------------------------------------
# 7. Haugen (2006) — Planning Poker vs Unstructured
# -----------------------------------------------------------------------------
cat("\n# Haugen (2006)\n")

hau <- fromJSON("results/haugen2006_results.json", simplifyVector = FALSE)

for (mkey in names(MODELS)) {
  cat(sprintf("\n## %s\n", MODELS[mkey]))
  unstruct_sd <- c(); poker_sd <- c()
  unstruct_grp <- c(); poker_grp <- c()
  unstruct_indiv <- c(); poker_indiv <- c()

  for (pair in names(hau[[mkey]])) {
    for (method in c("unstructured", "planning_poker")) {
      rows        <- hau[[mkey]][[pair]][[method]]
      devs        <- unlist(lapply(rows, function(r) unlist(r[["individual"]])))
      grp_vals    <- sapply(rows, function(r) r[["group"]])
      indiv_means <- sapply(rows, function(r) mean(unlist(r[["individual"]]), na.rm = TRUE))

      if (method == "unstructured") {
        unstruct_sd    <- c(unstruct_sd,    sd(devs, na.rm = TRUE))
        unstruct_grp   <- c(unstruct_grp,   grp_vals)
        unstruct_indiv <- c(unstruct_indiv, indiv_means)
      } else {
        poker_sd    <- c(poker_sd,    sd(devs, na.rm = TRUE))
        poker_grp   <- c(poker_grp,   grp_vals)
        poker_indiv <- c(poker_indiv, indiv_means)
      }
    }
  }

  cat(sprintf("    Descriptive — unstruct: SD median=%.2f  group median=%.2f\n",
              median(unstruct_sd, na.rm=TRUE), median(unstruct_grp, na.rm=TRUE)))
  cat(sprintf("    Descriptive — poker:    SD median=%.2f  group median=%.2f\n",
              median(poker_sd, na.rm=TRUE), median(poker_grp, na.rm=TRUE)))
  h7 <- list(
    "SD poker vs unstruct"         = paired_test(poker_sd,    unstruct_sd,    "poker SD",    "unstruct SD",    "two.sided"),
    "group poker vs unstruct"      = paired_test(poker_grp,   unstruct_grp,   "poker group", "unstruct group", "two.sided"),
    "group vs mean-indiv (unstruct)" = paired_test(unstruct_grp, unstruct_indiv, "group",    "mean-indiv",     "two.sided"),
    "group vs mean-indiv (poker)"  = paired_test(poker_grp,   poker_indiv,    "group",       "mean-indiv",     "two.sided")
  )
  print_roms(h7)
}

sink()