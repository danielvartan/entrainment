
<!-- hypothesis-test.md is generated from hypothesis-test.Rmd. Please edit that file -->

``` {toctree}
:maxdepth: 2
:hidden:

hypothesis-test
```

# Latitude hypothesis test

The following topics show the basic steps for testing the latitude
hypothesis using the `entrainment` model.

> Hypothesis statement: Populations residing close to the equator
> (latitude 0°) (i.e., with greater average insolation) have, on
> average, a shorter duration/morning circadian phenotype when compared
> to populations residing near the planet’s poles (i.e., with lower
> average insolation) ([Leocadio-Miguel et al.,
> 2017](https://doi.org/10.1038/s41598-017-05797-w); [Roenneberg et al.,
> 2003](https://doi.org/10.1177/0748730402239679)).

The latitude hypothesis is based on the idea that regions located at
latitudes close to the poles have, on average, a lower incidence of
annual sunlight when compared to regions close to the equator (latitude
0°).

<img src="_static/pidwirny_2019_figure-6i-3.png" alt="Monthly values of available insolation in Wm-2 for the equator (0°), 30°, 60°, and 90° North." width="100%" />

> Figure source: Pidwirny
> ([2019](http://www.physicalgeography.net/fundamentals/6i.html)).

Thus, it is understood by deduction that the regions close to the
equator have a stronger solar
[zeitgeber](https://en.wikipedia.org/wiki/Zeitgeber), which, according
to theory, should generate a greater propensity for synchronizing the
circadian rhythms of these populations to the light-dark cycle, reducing
the amplitude and the diversity of circadian phenotypes. This would also
give these populations a morning characteristic when compared to
populations living far from the equator, in which the opposite would
occur, i.e., a greater amplitude and diversity of circadian phenotypes
and an evening characteristic when compared to populations living near
the equator. ([Roenneberg et al.,
2003](https://doi.org/10.1177/0748730402239679)).

<img src="_static/roenneberg_2003_figure-7.png" alt="Hypothetical distribution of chronotypes (circadian phenotypes) for populations exposed to a strong (black) solar zeitgeber and a weak (striped) zeitgeber based on mid-sleep phase." width="100%" />

> Figure source: Roenneberg et
> al. ([2003](https://doi.org/10.1177/0748730402239679)).

## 1. Do the initial setup

``` python
import entrainment.hypothesis as hypothesis
import entrainment.labren as labren
import entrainment.model as model
```

## 2. Run the model for both groups

### By season

``` python
n = 10**3
lam_c = 3750
n_cycles = 3
repetitions = 10**2
x_name = "Nascente do rio Ailã"
y_name = "Arroio Chuí"
```

- North group (Location: Nascente do Rio Ailã) (Latitude: 5.272)

``` python
north_by_season = model.run_model(
    n = n, labren_id = 72272, by = "season", lam_c = lam_c, n_cycles = n_cycles,
    repetitions = repetitions
    )
```

<img src="_static/hypothesis-test_run_north_by_season-2.png" width="100%" />

- South group (Location: Arroio Chuí) (Latitude: -33.752)

``` python
south_by_season = model.run_model(
    n = n, labren_id = 1, by = "season", lam_c = lam_c, n_cycles = n_cycles,
    repetitions = repetitions
    )
```

<img src="_static/hypothesis-test_run_south_by_season-4.png" width="100%" />

### By year

- North group (Location: Nascente do Rio Ailã) (Latitude: 5.272)

``` python
north_by_year = model.run_model(
    n = n, labren_id = 72272, by = "year", lam_c = lam_c, n_cycles = n_cycles,
    repetitions = repetitions
    )
```

<img src="_static/hypothesis-test_run_north_by_year-6.png" width="100%" />

- South group (Location: Arroio Chuí) (Latitude: -33.752)

``` python
south_by_year = model.run_model(
    n = n, labren_id = 1, by = "year", lam_c = lam_c, n_cycles = n_cycles,
    repetitions = repetitions
    )
```

<img src="_static/hypothesis-test_run_south_by_year-8.png" width="100%" />

## 3. Analyze the distributions of both groups

For more information about the values presented, see
[`scipy.stats.kstest()`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kstest.html)
and
[`scipy.stats.shapiro()`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html).

### North group (Location: Nascente do Rio Ailã) (Latitude: 5.272)

- Unentrained (Control)

``` python
stats = hypothesis.analyze_data(
    x = north_by_season, key = "unentrain", name = x_name
    )
#> ---------------------------------------------------------
#> 
#> [Group: Nascente do rio Ailã | Key: Unentrain]
#> 
#> Mean = 24.153981670614982
#> Var. = 0.04000840916939309
#> SD = 0.20002102181869058
#> 
#> Min. = 23.5
#> 1st Qu. = 24.021067505316942
#> Median = 24.15733603650458
#> 3rd Qu. = 24.288490825112614
#> Max. = 24.599999999999955
#> 
#> Kurtosis = -0.08172287299030812
#> Skewness = -0.136452174143951
#> 
#> Kolmogorov-Smirnov test p-value = 0.0
#> Shapiro-Wilks test p-value = 0.0055746519938111305
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_analyze_north_unentrain-10.png" width="100%" /><img src="_static/hypothesis-test_analyze_north_unentrain-11.png" width="100%" />

- Summer

``` python
stats = hypothesis.analyze_data(
    x = north_by_season, key = "summer", name = x_name
    )
#> ---------------------------------------------------------
#> 
#> [Group: Nascente do rio Ailã | Key: Summer]
#> 
#> Mean = 24.007500312316605
#> Var. = 0.00012585853411413927
#> SD = 0.011218668999223538
#> 
#> Min. = 23.977287694332063
#> 1st Qu. = 24.000826098073816
#> Median = 24.00519609190592
#> 3rd Qu. = 24.01298838211254
#> Max. = 24.04644822430907
#> 
#> Kurtosis = 0.8722262867546493
#> Skewness = 0.6676912664760524
#> 
#> Kolmogorov-Smirnov test p-value = 0.0
#> Shapiro-Wilks test p-value = 4.803230029325558e-16
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_analyze_north_summer-14.png" width="100%" /><img src="_static/hypothesis-test_analyze_north_summer-15.png" width="100%" />

- Autumn

``` python
stats = hypothesis.analyze_data(
    x = north_by_season, key = "autumn", name = x_name
    )
#> ---------------------------------------------------------
#> 
#> [Group: Nascente do rio Ailã | Key: Autumn]
#> 
#> Mean = 24.006856334442748
#> Var. = 0.00010645358765508953
#> SD = 0.010317634789770838
#> 
#> Min. = 23.97791790830482
#> 1st Qu. = 24.00079848808784
#> Median = 24.0047458976943
#> 3rd Qu. = 24.011905188763823
#> Max. = 24.043516338968434
#> 
#> Kurtosis = 0.9117777510798715
#> Skewness = 0.6732870943381821
#> 
#> Kolmogorov-Smirnov test p-value = 0.0
#> Shapiro-Wilks test p-value = 2.9245956556102457e-16
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_analyze_north_autumn-18.png" width="100%" /><img src="_static/hypothesis-test_analyze_north_autumn-19.png" width="100%" />

- Winter

``` python
stats = hypothesis.analyze_data(
    x = north_by_season, key = "winter", name = x_name
    )
#> ---------------------------------------------------------
#> 
#> [Group: Nascente do rio Ailã | Key: Winter]
#> 
#> Mean = 24.006590091086064
#> Var. = 9.863818302093738e-05
#> SD = 0.009931675740827295
#> 
#> Min. = 23.979219672121413
#> 1st Qu. = 24.000763566277733
#> Median = 24.00450047874636
#> 3rd Qu. = 24.011691424261343
#> Max. = 24.04108842893429
#> 
#> Kurtosis = 0.9405910729668365
#> Skewness = 0.6712386816505003
#> 
#> Kolmogorov-Smirnov test p-value = 0.0
#> Shapiro-Wilks test p-value = 2.8456333913826277e-16
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_analyze_north_winter-22.png" width="100%" /><img src="_static/hypothesis-test_analyze_north_winter-23.png" width="100%" />

- Spring

``` python
stats = hypothesis.analyze_data(
    x = north_by_season, key = "spring", name = x_name
    )
#> ---------------------------------------------------------
#> 
#> [Group: Nascente do rio Ailã | Key: Spring]
#> 
#> Mean = 24.00625564689865
#> Var. = 8.775140305459706e-05
#> SD = 0.009367571886812347
#> 
#> Min. = 23.980384388706703
#> 1st Qu. = 24.00075660862617
#> Median = 24.004485956033015
#> 3rd Qu. = 24.010771574105473
#> Max. = 24.03903734232796
#> 
#> Kurtosis = 0.979661292972605
#> Skewness = 0.676784519420967
#> 
#> Kolmogorov-Smirnov test p-value = 0.0
#> Shapiro-Wilks test p-value = 5.692209106919076e-16
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_analyze_north_spring-26.png" width="100%" /><img src="_static/hypothesis-test_analyze_north_spring-27.png" width="100%" />

- Annual

``` python
stats = hypothesis.analyze_data(
    x = north_by_year, key = "annual", name = x_name
    )
#> ---------------------------------------------------------
#> 
#> [Group: Nascente do rio Ailã | Key: Annual]
#> 
#> Mean = 24.03066549913019
#> Var. = 0.0018223900810283458
#> SD = 0.04268946100653352
#> 
#> Min. = 23.869030864822204
#> 1st Qu. = 24.00292882323987
#> Median = 24.027693837460998
#> 3rd Qu. = 24.05679725065423
#> Max. = 24.177573330151247
#> 
#> Kurtosis = 0.6537250433010837
#> Skewness = 0.1862739442112428
#> 
#> Kolmogorov-Smirnov test p-value = 0.0
#> Shapiro-Wilks test p-value = 6.248676072573289e-05
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_analyze_north_annual-30.png" width="100%" /><img src="_static/hypothesis-test_analyze_north_annual-31.png" width="100%" />

### South group (Location: Arroio Chuí) (Latitude: -33.752)

- Unentrained (Control)

``` python
stats = hypothesis.analyze_data(
    x = south_by_season, key = "unentrain", name = y_name
    )
#> ---------------------------------------------------------
#> 
#> [Group: Arroio Chuí | Key: Unentrain]
#> 
#> Mean = 24.14259647182555
#> Var. = 0.03833415116583862
#> SD = 0.19579109061915614
#> 
#> Min. = 23.59889796814711
#> 1st Qu. = 24.00092648300528
#> Median = 24.147089034601475
#> 3rd Qu. = 24.28134547126313
#> Max. = 24.599999999999955
#> 
#> Kurtosis = -0.36765394167136556
#> Skewness = -0.03998138805016263
#> 
#> Kolmogorov-Smirnov test p-value = 0.0
#> Shapiro-Wilks test p-value = 0.01260786410421133
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_analyze_south_unentrain-34.png" width="100%" /><img src="_static/hypothesis-test_analyze_south_unentrain-35.png" width="100%" />

- Summer

``` python
stats = hypothesis.analyze_data(
    x = south_by_season, key = "summer", name = y_name
    )
#> ---------------------------------------------------------
#> 
#> [Group: Arroio Chuí | Key: Summer]
#> 
#> Mean = 24.015055988742
#> Var. = 0.00047774930369823477
#> SD = 0.021857477066171995
#> 
#> Min. = 23.94689481244995
#> 1st Qu. = 24.000069424333212
#> Median = 24.01383224081763
#> 3rd Qu. = 24.0284856850586
#> Max. = 24.090212433867755
#> 
#> Kurtosis = 0.4201331042213785
#> Skewness = 0.1950542748300403
#> 
#> Kolmogorov-Smirnov test p-value = 0.0
#> Shapiro-Wilks test p-value = 0.0018138405866920948
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_analyze_south_summer-38.png" width="100%" /><img src="_static/hypothesis-test_analyze_south_summer-39.png" width="100%" />

- Autumn

``` python
stats = hypothesis.analyze_data(
    x = south_by_season, key = "autumn", name = y_name
    )
#> ---------------------------------------------------------
#> 
#> [Group: Arroio Chuí | Key: Autumn]
#> 
#> Mean = 24.05581234504408
#> Var. = 0.005985737583467895
#> SD = 0.07736754864584953
#> 
#> Min. = 23.823639401510707
#> 1st Qu. = 24.000318510357793
#> Median = 24.055776570039903
#> 3rd Qu. = 24.10873105435103
#> Max. = 24.270393898412973
#> 
#> Kurtosis = -0.22692293012138354
#> Skewness = 0.0032568906872570713
#> 
#> Kolmogorov-Smirnov test p-value = 0.0
#> Shapiro-Wilks test p-value = 0.37971231341362
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_analyze_south_autumn-42.png" width="100%" /><img src="_static/hypothesis-test_analyze_south_autumn-43.png" width="100%" />

- Winter

``` python
stats = hypothesis.analyze_data(
    x = south_by_season, key = "winter", name = y_name
    )
#> ---------------------------------------------------------
#> 
#> [Group: Arroio Chuí | Key: Winter]
#> 
#> Mean = 24.035481644001106
#> Var. = 0.002732255494023046
#> SD = 0.05227098137612346
#> 
#> Min. = 23.874895984242002
#> 1st Qu. = 24.00014006033675
#> Median = 24.031261556362864
#> 3rd Qu. = 24.067366044287475
#> Max. = 24.20134513199081
#> 
#> Kurtosis = 0.42536579535968855
#> Skewness = 0.27724846510199297
#> 
#> Kolmogorov-Smirnov test p-value = 0.0
#> Shapiro-Wilks test p-value = 6.818345354986377e-06
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_analyze_south_winter-46.png" width="100%" /><img src="_static/hypothesis-test_analyze_south_winter-47.png" width="100%" />

- Spring

``` python
stats = hypothesis.analyze_data(
    x = south_by_season, key = "spring", name = y_name
    )
#> ---------------------------------------------------------
#> 
#> [Group: Arroio Chuí | Key: Spring]
#> 
#> Mean = 24.01635858475334
#> Var. = 0.0005693646255408013
#> SD = 0.02386136260863577
#> 
#> Min. = 23.944042931072087
#> 1st Qu. = 24.000071337712775
#> Median = 24.01454060012173
#> 3rd Qu. = 24.03049973925903
#> Max. = 24.095389819113567
#> 
#> Kurtosis = 0.3973141526025534
#> Skewness = 0.23959697256459048
#> 
#> Kolmogorov-Smirnov test p-value = 0.0
#> Shapiro-Wilks test p-value = 0.00013035570736974478
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_analyze_south_spring-50.png" width="100%" /><img src="_static/hypothesis-test_analyze_south_spring-51.png" width="100%" />

- Annual

``` python
stats = hypothesis.analyze_data(
    x = south_by_year, key = "annual", name = y_name
    )
#> ---------------------------------------------------------
#> 
#> [Group: Arroio Chuí | Key: Annual]
#> 
#> Mean = 24.032487884365004
#> Var. = 0.002328148390157346
#> SD = 0.048250890045234876
#> 
#> Min. = 23.860244673126147
#> 1st Qu. = 24.003788111712588
#> Median = 24.030157197713002
#> 3rd Qu. = 24.06169110598058
#> Max. = 24.181616067677282
#> 
#> Kurtosis = 0.5256828733320953
#> Skewness = 0.025520497579107744
#> 
#> Kolmogorov-Smirnov test p-value = 0.0
#> Shapiro-Wilks test p-value = 0.0016869448591023684
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_analyze_south_annual-54.png" width="100%" /><img src="_static/hypothesis-test_analyze_south_annual-55.png" width="100%" />

## 4. Test the hypothesis

For more information about the values presented, see
[`scipy.stats.ttest_ind`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html).

> Hypothesis statement: Populations residing close to the equator
> (latitude 0°) (i.e., with greater average insolation) have, on
> average, a shorter duration/morning circadian phenotype when compared
> to populations residing near the planet’s poles (i.e., with lower
> average insolation) ([Leocadio-Miguel et al.,
> 2017](https://doi.org/10.1038/s41598-017-05797-w); [Roenneberg et al.,
> 2003](https://doi.org/10.1177/0748730402239679)).

- Unentrained (Control)

``` python
test = hypothesis.test_hypothesis(
    key = "unentrain", x = north_by_season, y = south_by_season,
    x_name = x_name, y_name = y_name, lam_c = lam_c, n_cycles = n_cycles,
    repetitions = repetitions
    )
#> ---------------------------------------------------------
#> 
#> [Group: Nascente do rio Ailã | Key: Unentrain]
#> 
#> Mean = 24.153981670614982
#> Var. = 0.04000840916939309
#> SD = 0.20002102181869058
#> 
#> ---------------------------------------------------------
#> 
#> [Group: Arroio Chuí | Key: Unentrain]
#> 
#> Mean = 24.14259647182555
#> Var. = 0.03833415116583862
#> SD = 0.19579109061915614
#> 
#> ---------------------------------------------------------
#> 
#> [Groups: Nascente do rio Ailã & Arroio Chuí | Key: Unentrain]
#> 
#> Variance ratio: 0.04000840916939309 / 0.03833415116583862 = 1.0436753639414478
#> Ratio test: 1.0436753639414478 < 2: TRUE
#> 
#> Standard t-test statistic = 1.285655114047359
#> Standard t-test p-value = 0.19871244016050682
#> Welch’s t-test statistic = 1.2856551140473593
#> Welch’s t-test p-value = 0.19871250819685377
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_test_unentrain-58.png" width="100%" />

- Summer

``` python
test = hypothesis.test_hypothesis(
    key = "summer", x = north_by_season, y = south_by_season,
    x_name = x_name, y_name = y_name, lam_c = lam_c, n_cycles = n_cycles,
    repetitions = repetitions
    )
#> ---------------------------------------------------------
#> 
#> [Group: Nascente do rio Ailã | Key: Summer]
#> 
#> Mean = 24.007500312316605
#> Var. = 0.00012585853411413927
#> SD = 0.011218668999223538
#> 
#> ---------------------------------------------------------
#> 
#> [Group: Arroio Chuí | Key: Summer]
#> 
#> Mean = 24.015055988742
#> Var. = 0.00047774930369823477
#> SD = 0.021857477066171995
#> 
#> ---------------------------------------------------------
#> 
#> [Groups: Nascente do rio Ailã & Arroio Chuí | Key: Summer]
#> 
#> Variance ratio: 0.00047774930369823477 / 0.00012585853411413927 = 3.7959229945024697
#> Ratio test: 3.7959229945024697 < 2: FALSE
#> 
#> Standard t-test statistic = -9.720277413563368
#> Standard t-test p-value = 7.468122221975087e-22
#> Welch’s t-test statistic = -9.720277413563368
#> Welch’s t-test p-value = 1.0713503317880253e-21
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_test_summer-60.png" width="100%" />

> - (R1) Mean Tau North != Mean Tau South (p-value \< 0.05) (Welch’s
>   t-test): **TRUE**
> - (R2) Mean Tau North \< Mean Tau South: **TRUE**
> - Hypothesis: R1 & R2: **TRUE** (**CONFIRMED**)

- Autumn

``` python
test = hypothesis.test_hypothesis(
    key = "autumn", x = north_by_season, y = south_by_season,
    x_name = x_name, y_name = y_name, lam_c = lam_c, n_cycles = n_cycles,
    repetitions = repetitions
    )
#> ---------------------------------------------------------
#> 
#> [Group: Nascente do rio Ailã | Key: Autumn]
#> 
#> Mean = 24.006856334442748
#> Var. = 0.00010645358765508953
#> SD = 0.010317634789770838
#> 
#> ---------------------------------------------------------
#> 
#> [Group: Arroio Chuí | Key: Autumn]
#> 
#> Mean = 24.05581234504408
#> Var. = 0.005985737583467895
#> SD = 0.07736754864584953
#> 
#> ---------------------------------------------------------
#> 
#> [Groups: Nascente do rio Ailã & Arroio Chuí | Key: Autumn]
#> 
#> Variance ratio: 0.005985737583467895 / 0.00010645358765508953 = 56.228613007029246
#> Ratio test: 56.228613007029246 < 2: FALSE
#> 
#> Standard t-test statistic = -19.824489052272124
#> Standard t-test p-value = 5.427384051266498e-80
#> Welch’s t-test statistic = -19.824489052272124
#> Welch’s t-test p-value = 2.1699768354697642e-74
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_test_autumn-62.png" width="100%" />

> - (R1) Mean Tau North != Mean Tau South (p-value \< 0.05) (Welch’s
>   t-test): **TRUE**
> - (R2) Mean Tau North \< Mean Tau South: **TRUE**
> - Hypothesis: R1 & R2: **TRUE** (**CONFIRMED**)

- Winter

``` python
test = hypothesis.test_hypothesis(
    key = "winter", x = north_by_season, y = south_by_season,
    x_name = x_name, y_name = y_name, lam_c = lam_c, n_cycles = n_cycles,
    repetitions = repetitions
    )
#> ---------------------------------------------------------
#> 
#> [Group: Nascente do rio Ailã | Key: Winter]
#> 
#> Mean = 24.006590091086064
#> Var. = 9.863818302093738e-05
#> SD = 0.009931675740827295
#> 
#> ---------------------------------------------------------
#> 
#> [Group: Arroio Chuí | Key: Winter]
#> 
#> Mean = 24.035481644001106
#> Var. = 0.002732255494023046
#> SD = 0.05227098137612346
#> 
#> ---------------------------------------------------------
#> 
#> [Groups: Nascente do rio Ailã & Arroio Chuí | Key: Winter]
#> 
#> Variance ratio: 0.002732255494023046 / 9.863818302093738e-05 = 27.699775181818637
#> Ratio test: 27.699775181818637 < 2: FALSE
#> 
#> Standard t-test statistic = -17.162946575493436
#> Standard t-test p-value = 1.068858822974819e-61
#> Welch’s t-test statistic = -17.162946575493436
#> Welch’s t-test p-value = 1.623748310466898e-58
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_test_winter-64.png" width="100%" />

> - (R1) Mean Tau North != Mean Tau South (p-value \< 0.05) (Welch’s
>   t-test): **TRUE**
> - (R2) Mean Tau North \< Mean Tau South: **TRUE**
> - Hypothesis: R1 & R2: **TRUE** (**CONFIRMED**)

- Spring

``` python
test = hypothesis.test_hypothesis(
    key = "spring", x = north_by_season, y = south_by_season,
    x_name = x_name, y_name = y_name, lam_c = lam_c, n_cycles = n_cycles,
    repetitions = repetitions
    )
#> ---------------------------------------------------------
#> 
#> [Group: Nascente do rio Ailã | Key: Spring]
#> 
#> Mean = 24.00625564689865
#> Var. = 8.775140305459706e-05
#> SD = 0.009367571886812347
#> 
#> ---------------------------------------------------------
#> 
#> [Group: Arroio Chuí | Key: Spring]
#> 
#> Mean = 24.01635858475334
#> Var. = 0.0005693646255408013
#> SD = 0.02386136260863577
#> 
#> ---------------------------------------------------------
#> 
#> [Groups: Nascente do rio Ailã & Arroio Chuí | Key: Spring]
#> 
#> Variance ratio: 0.0005693646255408013 / 8.775140305459706e-05 = 6.488382016941139
#> Ratio test: 6.488382016941139 < 2: FALSE
#> 
#> Standard t-test statistic = -12.4568832834903
#> Standard t-test p-value = 2.3378582424830284e-34
#> Welch’s t-test statistic = -12.456883283490297
#> Welch’s t-test p-value = 9.930085962170789e-34
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_test_spring-66.png" width="100%" />

> - (R1) Mean Tau North != Mean Tau South (p-value \< 0.05) (Welch’s
>   t-test): **TRUE**
> - (R2) Mean Tau North \< Mean Tau South: **TRUE**
> - Hypothesis: R1 & R2: **TRUE** (**CONFIRMED**)

- Annual

``` python
test = hypothesis.test_hypothesis(
    key = "annual", x = north_by_year, y = south_by_year,
    x_name = x_name, y_name = y_name, lam_c = lam_c, n_cycles = n_cycles,
    repetitions = repetitions
    )
#> ---------------------------------------------------------
#> 
#> [Group: Nascente do rio Ailã | Key: Annual]
#> 
#> Mean = 24.03066549913019
#> Var. = 0.0018223900810283458
#> SD = 0.04268946100653352
#> 
#> ---------------------------------------------------------
#> 
#> [Group: Arroio Chuí | Key: Annual]
#> 
#> Mean = 24.032487884365004
#> Var. = 0.002328148390157346
#> SD = 0.048250890045234876
#> 
#> ---------------------------------------------------------
#> 
#> [Groups: Nascente do rio Ailã & Arroio Chuí | Key: Annual]
#> 
#> Variance ratio: 0.002328148390157346 / 0.0018223900810283458 = 1.277524726673012
#> Ratio test: 1.277524726673012 < 2: TRUE
#> 
#> Standard t-test statistic = -0.894068327727477
#> Standard t-test p-value = 0.37139301638141087
#> Welch’s t-test statistic = -0.8940683277274772
#> Welch’s t-test p-value = 0.3713946150956766
#> 
#> ---------------------------------------------------------
```

<img src="_static/hypothesis-test_test_annual-68.png" width="100%" />

> - (R1) Mean Tau North != Mean Tau South (p-value \< 0.05) (Standard
>   t-test): **FALSE**
> - (R2) Mean Tau North \< Mean Tau South: **TRUE**
> - Hypothesis: R1 & R2: **FALSE** (**REJECTED**)
