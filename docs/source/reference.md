```{toctree}
:maxdepth: 2
:hidden:

reference
```

# Function reference

The `entrainment` package comes with 5 subpackages. Use the pattern  `entrainment.<subpackage>.<function>` to access the API from each subpackage.

You are only interested in one subpackage, you can import it directly using a command like:

``` python
import entrainment.model as model
```

## Model (`entrainment.model`)

The entrainment model.

```{eval-rst}
.. autofunction:: model.run
.. autofunction:: model.plot_model
.. autofunction:: model.create_turtles
.. autofunction:: model.entrain
.. autofunction:: model.entrain_turtles
.. autofunction:: model.average_turtles
```

## Hypothesis (`entrainment.hypothesis`)

Tools for hypothesis testing.

```{eval-rst}
.. autofunction:: hypothesis.analyze_data
.. autofunction:: hypothesis.test_hypothesis
.. autofunction:: hypothesis.plot_hypothesis
```

## LABREN (`entrainment.labren`)

Tools for accessing [LABREN's global horizontal solar irradiation model](http://labren.ccst.inpe.br/atlas_2017.html).

```{eval-rst}
.. autofunction:: labren.labren
.. autofunction:: labren.plot_labren
```

## Demo (`entrainment.demo`)

Tools to explore the entrainment dynamics.

```{eval-rst}
.. autofunction:: demo.f_exact
.. autofunction:: demo.exact
.. autofunction:: demo.plot_exact
```

## Utils (`entrainment.utils`)

Utilitary tools.

```{eval-rst}
.. autofunction:: utils.reorder
```
