
# Aranda & Easterbrook (2005)

## Gemini
    low vs control  n=34  W=130.5  p=0.0360  p1=0.0180  d=-0.343 (medium)
    high vs control  n=34  W=520  p=0.0000  p1=0.0000  d=0.584 (large)
    Rom's:
      low: significant
      high: significant

## Claude
    low vs control  n=34  W=181.5  p=0.4416  p1=0.2208  d=-0.132 (negligible)
    high vs control  n=34  W=595  p=0.0000  p1=0.0000  d=0.849 (large)
    Rom's:
      low: not significant
      high: significant

## GPT
    low vs control  n=33  W=61.5  p=0.0067  p1=0.0033  d=-0.141 (negligible)
    high vs control  n=33  W=542  p=0.0000  p1=0.0000  d=0.499 (large)
    Rom's:
      low: significant
      high: significant

## DeepSeek
    low vs control  n=33  W=173  p=0.0901  p1=0.0450  d=-0.235 (small)
    high vs control  n=32  W=496  p=0.0000  p1=0.0000  d=0.751 (large)
    Rom's:
      low: significant
      high: significant

## Kimi
    low vs control  n=25  W=22  p=0.0004  p1=0.0002  d=-0.424 (medium)
    high vs control  n=23  W=276  p=0.0000  p1=0.0000  d=0.803 (large)
    Rom's:
      low: significant
      high: significant

# Løhre & Jørgensen (2014)

## exp1

### Gemini
    precise_single vs control  n=33  W=527  p=0.0000  p1=0.0000  d=0.591 (large)
    round_single vs control  n=34  W=562.5  p=0.0000  p1=0.0000  d=0.715 (large)
    precise_interval vs control  n=34  W=563  p=0.0000  p1=0.0000  d=0.687 (large)
    imprecise_interval vs control  n=34  W=560  p=0.0000  p1=0.0000  d=0.668 (large)
    precise_single vs round_single  n=33  W=110  p=0.0070  p1=0.0070  d=-0.188 (small)
    precise_interval vs imprecise_interval  n=34  W=311.5  p=0.5858  p1=0.5858  d=0.008 (negligible)
    Rom's:
      precise_single vs control: significant
      round_single vs control: significant
      precise_interval vs control: significant
      imprecise_interval vs control: significant
      precise_single vs round_single: significant
      precise_interval vs imprecise_interval: not significant

### Claude
    precise_single vs control  n=33  W=500  p=0.0001  p1=0.0000  d=0.335 (medium)
    round_single vs control  n=34  W=540.5  p=0.0000  p1=0.0000  d=0.449 (medium)
    precise_interval vs control  n=34  W=515.5  p=0.0002  p1=0.0001  d=0.420 (medium)
    imprecise_interval vs control  n=33  W=495  p=0.0000  p1=0.0000  d=0.376 (medium)
    precise_single vs round_single  n=33  W=96.5  p=0.0018  p1=0.0018  d=-0.202 (small)
    precise_interval vs imprecise_interval  n=33  W=228  p=0.9344  p1=0.9344  d=0.046 (negligible)
    Rom's:
      precise_single vs control: significant
      round_single vs control: significant
      precise_interval vs control: significant
      imprecise_interval vs control: significant
      precise_single vs round_single: significant
      precise_interval vs imprecise_interval: not significant

### GPT
    precise_single vs control  n=33  W=528  p=0.0000  p1=0.0000  d=0.554 (large)
    round_single vs control  n=32  W=527  p=0.0000  p1=0.0000  d=0.585 (large)
    precise_interval vs control  n=34  W=540  p=0.0000  p1=0.0000  d=0.693 (large)
    imprecise_interval vs control  n=33  W=522  p=0.0000  p1=0.0000  d=0.747 (large)
    precise_single vs round_single  n=32  W=135.5  p=0.0778  p1=0.0778  d=-0.079 (negligible)
    precise_interval vs imprecise_interval  n=33  W=231  p=0.3802  p1=0.3802  d=0.053 (negligible)
    Rom's:
      precise_single vs control: significant
      round_single vs control: significant
      precise_interval vs control: significant
      imprecise_interval vs control: significant
      precise_single vs round_single: significant
      precise_interval vs imprecise_interval: not significant

### DeepSeek
    precise_single vs control  n=34  W=518  p=0.0000  p1=0.0000  d=0.702 (large)
    round_single vs control  n=33  W=560  p=0.0000  p1=0.0000  d=0.818 (large)
    precise_interval vs control  n=33  W=529  p=0.0000  p1=0.0000  d=0.843 (large)
    imprecise_interval vs control  n=34  W=594  p=0.0000  p1=0.0000  d=0.895 (large)
    precise_single vs round_single  n=33  W=111.5  p=0.0077  p1=0.0077  d=-0.274 (small)
    precise_interval vs imprecise_interval  n=33  W=103.5  p=0.0239  p1=0.0239  d=-0.140 (negligible)
    Rom's:
      precise_single vs control: significant
      round_single vs control: significant
      precise_interval vs control: significant
      imprecise_interval vs control: significant
      precise_single vs round_single: significant
      precise_interval vs imprecise_interval: significant

### Kimi
    precise_single vs control  n=31  W=454.5  p=0.0001  p1=0.0000  d=0.457 (medium)
    round_single vs control  n=28  W=383  p=0.0000  p1=0.0000  d=0.533 (large)
    precise_interval vs control  n=32  W=503.5  p=0.0000  p1=0.0000  d=0.615 (large)
    imprecise_interval vs control  n=32  W=494  p=0.0000  p1=0.0000  d=0.616 (large)
    precise_single vs round_single  n=30  W=125  p=0.0464  p1=0.0464  d=-0.133 (negligible)
    precise_interval vs imprecise_interval  n=34  W=291  p=0.0453  p1=0.0453  d=0.253 (small)
    Rom's:
      precise_single vs control: significant
      round_single vs control: significant
      precise_interval vs control: significant
      imprecise_interval vs control: significant
      precise_single vs round_single: significant
      precise_interval vs imprecise_interval: significant

## exp2

### Gemini
    precise_interval vs control  n=34  W=52.5  p=0.0000  p1=0.0000  d=-0.427 (medium)
    imprecise_interval vs control  n=34  W=42  p=0.0000  p1=0.0000  d=-0.429 (medium)
    precise vs imprecise  n=34  W=270.5  p=0.6662  p1=0.6662  d=-0.085 (negligible)
    Rom's:
      precise_interval vs control: significant
      imprecise_interval vs control: significant
      precise vs imprecise: not significant

### Claude
    precise_interval vs control  n=34  W=0  p=0.0000  p1=0.0000  d=-0.598 (large)
    imprecise_interval vs control  n=34  W=0  p=0.0000  p1=0.0000  d=-0.497 (large)
    precise vs imprecise  n=34  W=89.5  p=0.0020  p1=0.0020  d=-0.141 (negligible)
    Rom's:
      precise_interval vs control: significant
      imprecise_interval vs control: significant
      precise vs imprecise: significant

### GPT
    precise_interval vs control  n=34  W=33  p=0.0000  p1=0.0000  d=-0.580 (large)
    imprecise_interval vs control  n=34  W=0  p=0.0000  p1=0.0000  d=-0.497 (large)
    precise vs imprecise  n=34  W=227.5  p=0.6950  p1=0.6950  d=-0.038 (negligible)
    Rom's:
      precise_interval vs control: significant
      imprecise_interval vs control: significant
      precise vs imprecise: not significant

### DeepSeek
    precise_interval vs control  n=33  W=24  p=0.0000  p1=0.0000  d=-0.612 (large)
    imprecise_interval vs control  n=33  W=51  p=0.0002  p1=0.0001  d=-0.395 (medium)
    precise vs imprecise  n=34  W=100  p=0.0114  p1=0.0114  d=-0.240 (small)
    Rom's:
      precise_interval vs control: significant
      imprecise_interval vs control: significant
      precise vs imprecise: not significant

### Kimi
    precise_interval vs control  n=29  W=106.5  p=0.0168  p1=0.0084  d=-0.442 (medium)
    imprecise_interval vs control  n=27  W=75  p=0.0064  p1=0.0032  d=-0.471 (medium)
    precise vs imprecise  n=26  W=99  p=0.3805  p1=0.3805  d=-0.019 (negligible)
    Rom's:
      precise_interval vs control: significant
      imprecise_interval vs control: significant
      precise vs imprecise: not significant

## exp3

### Gemini
    low_credibility vs control  n=34  W=239  p=0.8677  p1=0.4338  d=-0.017 (negligible)
    neutral vs control  n=34  W=161.5  p=0.0564  p1=0.0282  d=-0.123 (negligible)
    high_credibility vs control  n=34  W=84.5  p=0.0008  p1=0.0004  d=-0.289 (small)
    low_cred vs neutral  n=34  W=246.5  p=0.1707  p1=0.1707  d=0.125 (negligible)
    neutral vs high_cred  n=34  W=235.5  p=0.0032  p1=0.0032  d=0.129 (negligible)
    low_cred vs high_cred  n=34  W=384.5  p=0.0018  p1=0.0018  d=0.267 (small)
    Rom's:
      low_credibility vs control: not significant
      neutral vs control: significant
      high_credibility vs control: significant
      low vs neutral: significant
      neutral vs high: significant
      low vs high: significant

### Claude
    low_credibility vs control  n=34  W=91  p=0.0004  p1=0.0002  d=-0.240 (small)
    neutral vs control  n=33  W=0  p=0.0000  p1=0.0000  d=-0.683 (large)
    high_credibility vs control  n=34  W=0  p=0.0000  p1=0.0000  d=-0.589 (large)
    low_cred vs neutral  n=33  W=527  p=0.0000  p1=0.0000  d=0.439 (medium)
    neutral vs high_cred  n=33  W=195  p=0.3034  p1=0.3034  d=-0.031 (negligible)
    low_cred vs high_cred  n=34  W=592  p=0.0000  p1=0.0000  d=0.382 (medium)
    Rom's:
      low_credibility vs control: significant
      neutral vs control: significant
      high_credibility vs control: significant
      low vs neutral: significant
      neutral vs high: not significant
      low vs high: significant

### GPT
    low_credibility vs control  n=33  W=107  p=0.0059  p1=0.0029  d=-0.265 (small)
    neutral vs control  n=34  W=17.5  p=0.0000  p1=0.0000  d=-0.418 (medium)
    high_credibility vs control  n=34  W=27  p=0.0000  p1=0.0000  d=-0.484 (large)
    low_cred vs neutral  n=33  W=359.5  p=0.0296  p1=0.0296  d=0.140 (negligible)
    neutral vs high_cred  n=34  W=296  p=0.3518  p1=0.3518  d=0.112 (negligible)
    low_cred vs high_cred  n=33  W=351  p=0.0008  p1=0.0008  d=0.199 (small)
    Rom's:
      low_credibility vs control: significant
      neutral vs control: significant
      high_credibility vs control: significant
      low vs neutral: significant
      neutral vs high: not significant
      low vs high: significant

### DeepSeek
    low_credibility vs control  n=33  W=247  p=0.5306  p1=0.7418  d=0.051 (negligible)
    neutral vs control  n=30  W=175  p=0.7457  p1=0.3728  d=-0.088 (negligible)
    high_credibility vs control  n=29  W=122.5  p=0.0410  p1=0.0205  d=-0.287 (small)
    low_cred vs neutral  n=31  W=303.5  p=0.0061  p1=0.0061  d=0.191 (small)
    neutral vs high_cred  n=27  W=137.5  p=0.4548  p1=0.4548  d=0.139 (negligible)
    low_cred vs high_cred  n=30  W=286  p=0.0203  p1=0.0203  d=0.321 (small)
    Rom's:
      low_credibility vs control: not significant
      neutral vs control: not significant
      high_credibility vs control: not significant
      low vs neutral: significant
      neutral vs high: not significant
      low vs high: significant

### Kimi
    low_credibility vs control  n=31  W=22.5  p=0.0000  p1=0.0000  d=-0.373 (medium)
    neutral vs control  n=30  W=0  p=0.0000  p1=0.0000  d=-0.432 (medium)
    high_credibility vs control  n=29  W=28  p=0.0000  p1=0.0000  d=-0.522 (large)
    low_cred vs neutral  n=30  W=240.5  p=0.3991  p1=0.3991  d=0.052 (negligible)
    neutral vs high_cred  n=28  W=234  p=0.0037  p1=0.0037  d=0.199 (small)
    low_cred vs high_cred  n=31  W=336.5  p=0.0844  p1=0.0844  d=0.212 (small)
    Rom's:
      low_credibility vs control: significant
      neutral vs control: significant
      high_credibility vs control: significant
      low vs neutral: not significant
      neutral vs high: significant
      low vs high: significant

# Connolly & Dean (1997)

## Gemini

### H3a: gap vs zero
    cond A  n=94  V=131.5  p=0.6062  p1=0.7068  d=-0.043
    cond B  n=94  V=0  p=0.0058  p1=0.9979  d=-0.106
    cond C  n=89  V=1206.5  p=0.1849  p1=0.9084  d=-0.135
    cond D  n=94  V=675  p=0.9021  p1=0.5525  d=-0.021
    Rom's:
      cond A: not significant
      cond B: significant
      cond C: not significant
      cond D: not significant

### H3b: subtask-first vs whole-first
    B vs A  n=94  W=217  p=0.2591  p1=0.8742  d=-0.054 (negligible)
    D vs C  n=89  W=1788.5  p=0.5483  p1=0.2741  d=0.089 (negligible)
    Rom's:
      B vs A: not significant
      D vs C: not significant

### H3c: less-than vs greater-than wording
    C vs A  n=89  W=1313  p=0.2581  p1=0.2581  d=-0.113 (negligible)
    D vs B  n=94  W=741  p=0.9931  p1=0.9931  d=0.040 (negligible)
    Rom's:
      C vs A: not significant
      D vs B: not significant

### H3d: Study 2 vs Study 1 PI width
    S2A median=1.789  S1A median=1.625
    S2A vs S1A  n=89  W=2910  p=0.0002  p1=0.0001  d=0.129 (negligible)
    S2B median=2.025  S1B median=1.309
    S2B vs S1B  n=83  W=2930  p=0.0000  p1=0.0000  d=0.401 (medium)

## Claude

### H3a: gap vs zero
    cond A  n=94  V=254.5  p=0.0001  p1=1.0000  d=-0.383
    cond B  n=94  V=191  p=0.0004  p1=0.9998  d=-0.298
    cond C  n=94  V=1948.5  p=0.5974  p1=0.2987  d=0.011
    cond D  n=94  V=1110  p=0.3368  p1=0.8330  d=-0.138
    Rom's:
      cond A: significant
      cond B: significant
      cond C: not significant
      cond D: not significant

### H3b: subtask-first vs whole-first
    B vs A  n=94  W=1157  p=0.5824  p1=0.2912  d=0.054 (negligible)
    D vs C  n=94  W=1760  p=0.4111  p1=0.7956  d=-0.075 (negligible)
    Rom's:
      B vs A: not significant
      D vs C: not significant

### H3c: less-than vs greater-than wording
    C vs A  n=94  W=2319.5  p=0.1330  p1=0.1330  d=0.151 (small)
    D vs B  n=94  W=1746  p=0.4183  p1=0.4183  d=0.067 (negligible)
    Rom's:
      C vs A: not significant
      D vs B: not significant

### H3d: Study 2 vs Study 1 PI width
    S2A median=2.050  S1A median=1.667
    S2A vs S1A  n=93  W=3521  p=0.0000  p1=0.0000  d=0.322 (small)
    S2B median=2.000  S1B median=1.656
    S2B vs S1B  n=91  W=3260  p=0.0000  p1=0.0000  d=0.308 (small)

## GPT

### H3a: gap vs zero
    cond A  n=93  V=259  p=0.0000  p1=1.0000  d=-0.505
    cond B  n=92  V=49  p=0.0001  p1=0.9999  d=-0.283
    cond C  n=94  V=842.5  p=0.0005  p1=0.9998  d=-0.404
    cond D  n=94  V=595.5  p=0.5297  p1=0.7382  d=-0.181
    Rom's:
      cond A: significant
      cond B: significant
      cond C: significant
      cond D: not significant

### H3b: subtask-first vs whole-first
    B vs A  n=92  W=1774  p=0.0007  p1=0.0003  d=0.314 (small)
    D vs C  n=94  W=2284.5  p=0.0260  p1=0.0130  d=0.255 (small)
    Rom's:
      B vs A: significant
      D vs C: significant

### H3c: less-than vs greater-than wording
    C vs A  n=93  W=1685  p=0.6570  p1=0.6570  d=-0.062 (negligible)
    D vs B  n=92  W=932  p=0.9031  p1=0.9031  d=-0.000 (negligible)
    Rom's:
      C vs A: not significant
      D vs B: not significant

### H3d: Study 2 vs Study 1 PI width
    S2A median=1.722  S1A median=1.308
    S2A vs S1A  n=94  W=3846.5  p=0.0000  p1=0.0000  d=0.584 (large)
    S2B median=1.716  S1B median=1.388
    S2B vs S1B  n=93  W=3170  p=0.0002  p1=0.0001  d=0.328 (small)

## DeepSeek

### H3a: gap vs zero
    cond A  n=93  V=1833.5  p=0.1451  p1=0.0725  d=0.086
    cond B  n=94  V=795  p=0.0000  p1=1.0000  d=-0.436
    cond C  n=94  V=2436  p=0.2482  p1=0.1241  d=0.128
    cond D  n=94  V=2530.5  p=0.0837  p1=0.0418  d=0.074
    Rom's:
      cond A: not significant
      cond B: significant
      cond C: not significant
      cond D: significant

### H3b: subtask-first vs whole-first
    B vs A  n=93  W=1071  p=0.0002  p1=0.9999  d=-0.336 (medium)
    D vs C  n=94  W=2370  p=0.4808  p1=0.2404  d=0.054 (negligible)
    Rom's:
      B vs A: significant
      D vs C: not significant

### H3c: less-than vs greater-than wording
    C vs A  n=93  W=2153.5  p=0.9565  p1=0.9565  d=0.017 (negligible)
    D vs B  n=94  W=2821  p=0.0150  p1=0.0150  d=0.192 (small)
    Rom's:
      C vs A: not significant
      D vs B: significant

### H3d: Study 2 vs Study 1 PI width
    S2A median=2.286  S1A median=1.667
    S2A vs S1A  n=91  W=3685.5  p=0.0000  p1=0.0000  d=0.540 (large)
    S2B median=2.143  S1B median=1.500
    S2B vs S1B  n=93  W=3766.5  p=0.0000  p1=0.0000  d=0.521 (large)

## Kimi

### H3a: gap vs zero
    cond A  n=91  V=1107  p=0.0039  p1=0.9981  d=-0.363
    cond B  n=94  V=2575.5  p=0.0000  p1=0.0000  d=0.266
    cond C  n=89  V=1913  p=0.7095  p1=0.3547  d=-0.124
    cond D  n=94  V=2720  p=0.0003  p1=0.0001  d=0.383
    Rom's:
      cond A: significant
      cond B: significant
      cond C: not significant
      cond D: significant

### H3b: subtask-first vs whole-first
    B vs A  n=91  W=2970.5  p=0.0000  p1=0.0000  d=0.455 (medium)
    D vs C  n=89  W=2351  p=0.1024  p1=0.0512  d=0.220 (small)
    Rom's:
      B vs A: significant
      D vs C: not significant

### H3c: less-than vs greater-than wording
    C vs A  n=89  W=2372  p=0.0171  p1=0.0171  d=0.230 (small)
    D vs B  n=94  W=2089.5  p=0.7234  p1=0.7234  d=0.069 (negligible)
    Rom's:
      C vs A: significant
      D vs B: not significant

### H3d: Study 2 vs Study 1 PI width
    S2A median=2.300  S1A median=1.507
    S2A vs S1A  n=82  W=2888  p=0.0000  p1=0.0000  d=0.574 (large)
    S2B median=2.333  S1B median=1.746
    S2B vs S1B  n=89  W=3335.5  p=0.0000  p1=0.0000  d=0.403 (medium)

# Jørgensen et al. (2002)

## Study A: PI width (descriptive)
    Gemini     n=34  median=0.772  IQR=0.201
    Claude     n=34  median=1.014  IQR=0.258
    GPT        n=34  median=1.000  IQR=0.122
    DeepSeek   n=34  median=0.720  IQR=0.185
    Kimi       n=32  median=1.050  IQR=0.204

## Study B: GROUP vs mean-of-individuals

### Gemini
    GROUP vs mean-indiv  n=34  W=578  p=0.0000  p1=1.0000  d=0.709 (large)

### Claude
    GROUP vs mean-indiv  n=34  W=594  p=0.0000  p1=1.0000  d=0.600 (large)

### GPT
    GROUP vs mean-indiv  n=34  W=431.5  p=0.0225  p1=0.9893  d=0.200 (small)

### DeepSeek
    GROUP vs mean-indiv  n=31  W=416  p=0.0006  p1=0.9997  d=0.469 (medium)

### Kimi
    GROUP vs mean-indiv  n=33  W=441  p=0.0010  p1=0.9995  d=0.345 (medium)

## Study C: PI width by confidence level

### Gemini
    75 vs 50  n=34  W=505  p=0.0004  p1=0.0002  d=0.490 (large)
    90 vs 75  n=33  W=490  p=0.0000  p1=0.0000  d=0.614 (large)
    99 vs 90  n=31  W=466  p=0.0000  p1=0.0000  d=0.769 (large)
    Rom's:
      50 vs 75: significant
      75 vs 90: significant
      90 vs 99: significant

### Claude
    75 vs 50  n=32  W=481  p=0.0000  p1=0.0000  d=0.646 (large)
    90 vs 75  n=33  W=557  p=0.0000  p1=0.0000  d=0.776 (large)
    99 vs 90  n=32  W=528  p=0.0000  p1=0.0000  d=0.996 (large)
    Rom's:
      50 vs 75: significant
      75 vs 90: significant
      90 vs 99: significant

### GPT
    75 vs 50  n=32  W=429  p=0.0004  p1=0.0002  d=0.523 (large)
    90 vs 75  n=33  W=453  p=0.0004  p1=0.0002  d=0.559 (large)
    99 vs 90  n=30  W=459  p=0.0000  p1=0.0000  d=0.826 (large)
    Rom's:
      50 vs 75: significant
      75 vs 90: significant
      90 vs 99: significant

### DeepSeek
    75 vs 50  n=33  W=306  p=0.2597  p1=0.1299  d=0.150 (small)
    90 vs 75  n=32  W=331  p=0.1059  p1=0.0530  d=0.173 (small)
    99 vs 90  n=31  W=248  p=0.3108  p1=0.1554  d=0.108 (negligible)
    Rom's:
      50 vs 75: not significant
      75 vs 90: not significant
      90 vs 99: not significant

### Kimi
    75 vs 50  n=29  W=272  p=0.0474  p1=0.0237  d=0.289 (small)
    90 vs 75  n=30  W=372.5  p=0.0001  p1=0.0001  d=0.641 (large)
    99 vs 90  n=33  W=478  p=0.0000  p1=0.0000  d=0.748 (large)
    Rom's:
      50 vs 75: not significant
      75 vs 90: significant
      90 vs 99: significant

## Study D: ego-free vs Study A

### Gemini
    Study D vs Study A  n=34  W=495  p=0.0004  p1=0.0002  d=0.583 (large)

### Claude
    Study D vs Study A  n=34  W=594  p=0.0000  p1=0.0000  d=0.863 (large)

### GPT
    Study D vs Study A  n=34  W=507  p=0.0000  p1=0.0000  d=0.697 (large)

### DeepSeek
    Study D vs Study A  n=31  W=279  p=0.0315  p1=0.0158  d=0.259 (small)

### Kimi
    Study D vs Study A  n=30  W=387  p=0.0003  p1=0.0001  d=0.594 (large)

# Jørgensen (2009)

## exp_a

### Gemini
    Manipulation check:
    MORE vs LESS  n=34  W=595  p=0.0000  p1=0.0000  d=1.000 (large)
    MORE vs LESS  n=34  W=95  p=0.0083  p1=0.0042  d=-0.092 (negligible)
    MORE vs LESS  n=34  W=21  p=0.0844  p1=0.9639  d=-0.151 (small)
    Rom's:
      effort: significant
      success: significant

### Claude
    Manipulation check:
    MORE vs LESS  n=34  W=595  p=0.0000  p1=0.0000  d=1.000 (large)
    MORE vs LESS  n=34  W=158.5  p=0.0299  p1=0.0150  d=-0.032 (negligible)
    MORE vs LESS  n=34  W=9  p=0.0000  p1=1.0000  d=-0.245 (small)
    Rom's:
      effort: significant
      success: significant

### GPT
    Manipulation check:
    MORE vs LESS  n=34  W=595  p=0.0000  p1=0.0000  d=1.000 (large)
    MORE vs LESS  n=34  W=200.5  p=0.9637  p1=0.4818  d=0.005 (negligible)
    MORE vs LESS  n=34  W=57  p=0.0074  p1=0.9966  d=-0.214 (small)
    Rom's:
      effort: not significant
      success: significant

### DeepSeek
    Manipulation check:
    MORE vs LESS  n=34  W=490  p=0.0009  p1=0.0004  d=0.176 (small)
    MORE vs LESS  n=34  W=186.5  p=0.5267  p1=0.7454  d=0.034 (negligible)
    MORE vs LESS  n=34  W=67.5  p=1.0000  p1=0.5224  d=0.000 (negligible)
    Rom's:
      effort: not significant
      success: not significant

### Kimi
    Manipulation check:
    MORE vs LESS  n=34  W=528  p=0.0000  p1=0.0000  d=1.000 (large)
    MORE vs LESS  n=34  W=287.5  p=0.6671  p1=0.6732  d=0.062 (negligible)
    MORE vs LESS  n=34  W=81  p=0.3700  p1=0.8250  d=-0.117 (negligible)
    Rom's:
      effort: not significant
      success: not significant

## exp_b

### Gemini
    Manipulation check:
    MORE vs LESS  n=34  W=595  p=0.0000  p1=0.0000  d=0.927 (large)
    MORE vs LESS  n=34  W=90.5  p=0.0004  p1=0.0002  d=-0.135 (negligible)
    MORE vs LESS  n=34  W=10.5  p=0.3185  p1=0.8728  d=-0.069 (negligible)
    Rom's:
      effort: significant
      success: not significant

### Claude
    Manipulation check:
    MORE vs LESS  n=34  W=595  p=0.0000  p1=0.0000  d=1.000 (large)
    MORE vs LESS  n=34  W=91  p=0.0007  p1=0.0004  d=-0.150 (small)
    MORE vs LESS  n=34  W=35.5  p=0.0006  p1=0.9997  d=-0.228 (small)
    Rom's:
      effort: significant
      success: significant

### GPT
    Manipulation check:
    MORE vs LESS  n=34  W=595  p=0.0000  p1=0.0000  d=1.000 (large)
    MORE vs LESS  n=34  W=85  p=0.0074  p1=0.0037  d=-0.102 (negligible)
    MORE vs LESS  n=34  W=81  p=0.0134  p1=0.9938  d=-0.171 (small)
    Rom's:
      effort: significant
      success: significant

### DeepSeek
    Manipulation check:
    MORE vs LESS  n=34  W=473  p=0.0001  p1=0.0000  d=0.706 (large)
    MORE vs LESS  n=34  W=10  p=0.0000  p1=0.0000  d=-0.366 (medium)
    MORE vs LESS  n=34  W=85  p=0.6738  p1=0.3369  d=0.036 (negligible)
    Rom's:
      effort: significant
      success: not significant

### Kimi
    Manipulation check:
    MORE vs LESS  n=34  W=496  p=0.0000  p1=0.0000  d=0.991 (large)
    MORE vs LESS  n=34  W=200  p=0.9546  p1=0.4773  d=-0.025 (negligible)
    MORE vs LESS  n=34  W=59.5  p=0.4229  p1=0.8023  d=-0.066 (negligible)
    Rom's:
      effort: not significant
      success: not significant

## exp_c

### Gemini
    Manipulation check:
    MORE vs LESS  n=55  W=1326  p=0.0000  p1=0.0000  d=0.871 (large)
    MORE vs LESS  n=55  W=544  p=0.3691  p1=0.1845  d=-0.039 (negligible)
    MORE vs LESS  n=55  W=366  p=0.0421  p1=0.0210  d=0.119 (negligible)
    Rom's:
      effort: not significant
      success: significant

### Claude
    Manipulation check:
    MORE vs LESS  n=55  W=1485  p=0.0000  p1=0.0000  d=1.000 (large)
    MORE vs LESS  n=55  W=1069  p=0.0005  p1=0.9997  d=0.141 (negligible)
    MORE vs LESS  n=55  W=308  p=0.0177  p1=0.9914  d=-0.291 (small)
    Rom's:
      effort: significant
      success: significant

### GPT
    Manipulation check:
    MORE vs LESS  n=55  W=1540  p=0.0000  p1=0.0000  d=1.000 (large)
    MORE vs LESS  n=55  W=951.5  p=0.0369  p1=0.9819  d=0.097 (negligible)
    MORE vs LESS  n=55  W=186  p=0.0224  p1=0.9893  d=-0.184 (small)
    Rom's:
      effort: significant
      success: significant

### DeepSeek
    Manipulation check:
    MORE vs LESS  n=55  W=1431  p=0.0000  p1=0.0000  d=0.966 (large)
    MORE vs LESS  n=55  W=539.5  p=0.9956  p1=0.4978  d=0.004 (negligible)
    MORE vs LESS  n=55  W=254  p=0.0358  p1=0.9827  d=-0.209 (small)
    Rom's:
      effort: not significant
      success: significant

### Kimi
    Manipulation check:
    MORE vs LESS  n=55  W=1326  p=0.0000  p1=0.0000  d=0.997 (large)
    MORE vs LESS  n=55  W=577  p=0.3412  p1=0.8324  d=0.100 (negligible)
    MORE vs LESS  n=55  W=264  p=0.1174  p1=0.9430  d=-0.170 (small)
    Rom's:
      effort: not significant
      success: not significant

## exp_d

### Gemini
    Manipulation check:
    MORE vs LESS  n=34  W=595  p=0.0000  p1=0.0000  d=1.000 (large)
    MORE vs LESS  n=34  W=90  p=0.0012  p1=0.0006  d=-0.088 (negligible)
    MORE vs LESS  n=34  W=35.5  p=0.4927  p1=0.7759  d=-0.099 (negligible)
    Rom's:
      effort: significant
      success: not significant

### Claude
    Manipulation check:
    MORE vs LESS  n=34  W=528  p=0.0000  p1=0.0000  d=1.000 (large)
    MORE vs LESS  n=34  W=272.5  p=0.8810  p1=0.5669  d=-0.011 (negligible)
    MORE vs LESS  n=34  W=42.5  p=0.0013  p1=0.9994  d=-0.209 (small)
    Rom's:
      effort: not significant
      success: significant

### GPT
    Manipulation check:
    MORE vs LESS  n=34  W=528  p=0.0000  p1=0.0000  d=1.000 (large)
    MORE vs LESS  n=34  W=220  p=0.9655  p1=0.5259  d=0.017 (negligible)
    MORE vs LESS  n=34  W=61  p=0.0577  p1=0.9734  d=-0.189 (small)
    Rom's:
      effort: not significant
      success: not significant

### DeepSeek
    Manipulation check:
    MORE vs LESS  n=34  W=468  p=0.0000  p1=0.0000  d=0.562 (large)
    MORE vs LESS  n=34  W=144  p=0.3302  p1=0.8434  d=-0.024 (negligible)
    MORE vs LESS  n=34  W=35  p=0.7781  p1=0.6414  d=0.051 (negligible)
    Rom's:
      effort: not significant
      success: not significant

### Kimi
    Manipulation check:
    MORE vs LESS  n=34  W=561  p=0.0000  p1=0.0000  d=1.000 (large)
    MORE vs LESS  n=34  W=358  p=0.0802  p1=0.9615  d=0.112 (negligible)
    MORE vs LESS  n=34  W=79.5  p=0.0241  p1=0.9888  d=-0.258 (small)
    Rom's:
      effort: significant
      success: significant

# Moløkken & Jørgensen (2003)

## Gemini
    H6a: group vs avg_before
    H6b: convergence
    group vs avg_before  n=34  W=465  p=0.0000  p1=1.0000  d=0.294 (small)
    after_dist vs before_dist  n=34  W=36  p=0.0000  p1=0.0000  d=-0.494 (large)
    Rom's:
      H6a: significant
      H6b: significant

## Claude
    H6a: group vs avg_before
    H6b: convergence
    group vs avg_before  n=34  W=486  p=0.0002  p1=0.9999  d=0.084 (negligible)
    after_dist vs before_dist  n=34  W=129  p=0.0032  p1=0.0016  d=-0.253 (small)
    Rom's:
      H6a: significant
      H6b: significant

## GPT
    H6a: group vs avg_before
    H6b: convergence
    group vs avg_before  n=34  W=594  p=0.0000  p1=1.0000  d=0.111 (negligible)
    after_dist vs before_dist  n=34  W=30  p=0.0000  p1=0.0000  d=-0.436 (medium)
    Rom's:
      H6a: significant
      H6b: significant

## DeepSeek
    H6a: group vs avg_before
    H6b: convergence
    group vs avg_before  n=34  W=438  p=0.0153  p1=0.9927  d=0.038 (negligible)
    after_dist vs before_dist  n=34  W=29  p=0.0000  p1=0.0000  d=-0.410 (medium)
    Rom's:
      H6a: significant
      H6b: significant

## Kimi
    H6a: group vs avg_before
    H6b: convergence
    group vs avg_before  n=31  W=296  p=0.3519  p1=0.8291  d=0.004 (negligible)
    after_dist vs before_dist  n=31  W=185  p=0.2206  p1=0.1103  d=-0.163 (small)
    Rom's:
      H6a: not significant
      H6b: not significant

# Haugen (2006)

## Gemini
    Descriptive — unstruct: SD median=4.14  group median=11.00
    Descriptive — poker:    SD median=4.10  group median=12.00
    poker SD vs unstruct SD  n=5  W=9  p=0.8125  p1=0.8125  d=0.040 (negligible)
    poker group vs unstruct group  n=10  W=41  p=0.1840  p1=0.1840  d=0.100 (negligible)
    group vs mean-indiv  n=10  W=45  p=0.0090  p1=0.0090  d=0.190 (small)
    group vs mean-indiv  n=10  W=32.5  p=0.0497  p1=0.0497  d=0.130 (negligible)
    Rom's:
      SD poker vs unstruct: not significant
      group poker vs unstruct: not significant
      group vs mean-indiv (unstruct): significant
      group vs mean-indiv (poker): significant

## Claude
    Descriptive — unstruct: SD median=6.09  group median=17.25
    Descriptive — poker:    SD median=10.09  group median=19.00
    poker SD vs unstruct SD  n=5  W=15  p=0.0625  p1=0.0625  d=0.840 (large)
    poker group vs unstruct group  n=10  W=31.5  p=0.3131  p1=0.3131  d=0.140 (negligible)
    group vs mean-indiv  n=10  W=7  p=0.5248  p1=0.5248  d=-0.000 (negligible)
    group vs mean-indiv  n=10  W=12.5  p=0.8655  p1=0.8655  d=-0.040 (negligible)
    Rom's:
      SD poker vs unstruct: not significant
      group poker vs unstruct: not significant
      group vs mean-indiv (unstruct): not significant
      group vs mean-indiv (poker): not significant

## GPT
    Descriptive — unstruct: SD median=5.73  group median=20.75
    Descriptive — poker:    SD median=16.54  group median=29.50
    poker SD vs unstruct SD  n=5  W=15  p=0.0625  p1=0.0625  d=0.760 (large)
    poker group vs unstruct group  n=10  W=52  p=0.0143  p1=0.0143  d=0.370 (medium)
    group vs mean-indiv  n=10  W=9  p=0.2012  p1=0.2012  d=0.020 (negligible)
    group vs mean-indiv  n=10  W=44.5  p=0.0907  p1=0.0907  d=0.120 (negligible)
    Rom's:
      SD poker vs unstruct: significant
      group poker vs unstruct: significant
      group vs mean-indiv (unstruct): significant
      group vs mean-indiv (poker): significant

## DeepSeek
    Descriptive — unstruct: SD median=2.85  group median=12.00
    Descriptive — poker:    SD median=5.96  group median=12.50
    poker SD vs unstruct SD  n=5  W=12  p=0.3125  p1=0.3125  d=0.360 (medium)
    poker group vs unstruct group  n=10  W=32  p=0.6831  p1=0.6831  d=0.120 (negligible)
    group vs mean-indiv  n=10  W=51.5  p=0.0165  p1=0.0165  d=0.140 (negligible)
    group vs mean-indiv  n=10  W=37.5  p=0.3319  p1=0.3319  d=0.160 (small)
    Rom's:
      SD poker vs unstruct: not significant
      group poker vs unstruct: not significant
      group vs mean-indiv (unstruct): significant
      group vs mean-indiv (poker): not significant

## Kimi
    Descriptive — unstruct: SD median=13.77  group median=25.00
    Descriptive — poker:    SD median=14.70  group median=34.00
    poker SD vs unstruct SD  n=5  W=10  p=0.6250  p1=0.6250  d=0.200 (small)
    poker group vs unstruct group  n=10  W=36  p=0.1235  p1=0.1235  d=0.220 (small)
    group vs mean-indiv  n=10  W=24.5  p=0.0898  p1=0.0898  d=0.110 (negligible)
    group vs mean-indiv  n=10  W=30.5  p=0.7985  p1=0.7985  d=0.060 (negligible)
    Rom's:
      SD poker vs unstruct: not significant
      group poker vs unstruct: not significant
      group vs mean-indiv (unstruct): not significant
      group vs mean-indiv (poker): not significant
