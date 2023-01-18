
<!-- README.md is generated from README.Rmd. Please edit that file -->

# entrainment

<!-- badges: start -->

[![Project Status: WIP – Initial development is in progress, but there
has not yet been a stable, usable release suitable for the
public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)
[![License:
MIT](https://img.shields.io/badge/license-MIT-green)](https://choosealicense.com/licenses/mit/)
[![Contributor
Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](https://www.contributor-covenant.org/version/2/1/code_of_conduct/)
<!-- badges: end -->

## Overview

`entrainment` is a rule-based model created on Python to test and to
demonstrate the 24h light/dark cycle [entrainment
phenomenon](https://en.wikipedia.org/wiki/Entrainment_(chronobiology)).

## Prerequisites

You need to have some familiarity with the [Python programming
language](https://www.python.org/) to use `entrainment` main functions.

In case you don’t feel comfortable with Python, we strongly recommend
checking Jake VanderPlas free and online book [Python Data Science
Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) and the
Coursera course from Google [Crash Course on
Python](https://www.coursera.org/learn/python-crash-course) (free for
audit students).

## Installation

You can install `entrainment` from GitHub with:

``` eval
py -m pip install git+https://github.com/danielvartan/entrainment.git#egg=entrainment
```

We don’t intend to publish this package to [PyPI](https://pypi.org/).

## Usage

The `entrainment` package comes with 5 subpackages:

- `demo`: A subpackage to plot the entrainment dynamics.
- `hypothesis`: A subpackage with tools for hypothesis testing.
- `labren`: A subpackage to access LABREN’s global horizontal solar
  irradiation model.
- `model`: A subpackage with the entrainment model.
- `utils`: A subpackage with some utility tools.

<!-- You can learn more about each subpackage and its functions on the package documentation website. -->

The following example illustrates how to run the model.

Please note in this example all of the model arguments are assigned. You
don’t need to assign values to all arguments, you can just use the
default values. Check `run()` documentation to learn more.

``` python
import entrainment.model as model

turtles = model.run(
    n = 10 ** 3, # Number of turtles/subjects to create
    tau_range = (23.5, 24.6), # Limits for assigning Tau values
    tau_mean = 24.15, # Mean value for the Tau distribution
    tau_sd = 0.2, # Standard deviation value for the Tau distribution
    k_range = (0.001, 0.01), # Limits for assigning the k values
    k_mean = 0.001, # Mean value for the k distribution
    k_sd = 0.005, # Standard deviation value for the k distribution
    lam_c = 4727.833, # Critical lambda value
    lam_c_tol = 1000, # Critical lambda tolerance
    labren_id = 1, # LABREN id of the global horizontal irradiation means
    by = "season", # Series resolution (choices: "month", "season")
    n_cycles = 2, # Number of cycles to run
    start_at = 0, # Index number indicating the start of the series
    repetitions = 100, # Number of repetitions
    plot = True # Boolean value indicating if the function must plot the results
    )
```

<img src="doc/source/_static/README-unnamed-chunk-2-1.png" width="100%" />

## Citation

If you use `entrainment` in your research, please consider citing it. We
put a lot of work to build and maintain a free and open-source Python
package. You can find the `entrainment` citation below.

    Vartanian, D. (2023). {entrainment}: A rule-based model of the 24h light/dark cycle entrainment phenomenon. (v. 0.0.0.9000). https://github.com/danielvartan/entrainment

A BibTeX entry for LaTeX users is

    @Unpublished{,
        title = {{entrainment}: A rule-based model of the 24h light/dark cycle entrainment phenomenon},
        author = {Daniel Vartanian},
        year = {2023},
        url = {https://github.com/danielvartan/entrainment},
        note = {(v. 0.0.0.9000). Lifecycle: experimental},
    }

## Contributing

We welcome contributions, including bug reports.

Please note that this package is released with a [Contributor Code of
Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
By contributing to this project, you agree to abide by its terms.

## Acknowledgments

The initial development of `entrainment` was supported by a scholarship
provided by the [University of Sao Paulo (USP)](http://usp.br/) (❤️).

This model was initially created for the [SCX5002 - Complex System
I](https://uspdigital.usp.br/janus/Disciplina?tipo=D&sgldis=SCX5002&nomdis=&origem=C)
class of the [Graduate Program in Modeling Complex Systems
(PPG-SCX)](https://www.prpg.usp.br/pt-br/faca-pos-na-usp/programas-de-pos-graduacao/621-modelagem-de-sistemas-complexos)
of the [University of Sao Paulo (USP)](https://www5.usp.br/), under the
guidance of [Prof. Dr. Camilo Rodrigues
Neto](https://orcid.org/0000-0001-6783-6695).
