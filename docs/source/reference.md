# Function reference

The `entrainment` package comes with 4 subpackages. Use the pattern  `entrainment.<subpackage>.<function>` to access the API from each subpackage.

If you are only interested in one subpackage, you can import it directly using a command like:

``` python
import entrainment.model as model
```

## Model (`entrainment.model`)

The entrainment model.

```{eval-rst}
.. autofunction:: entrainment.model.run_model
.. autofunction:: entrainment.model.plot_model
.. autofunction:: entrainment.model.create_turtles
.. autofunction:: entrainment.model.entrain
.. autofunction:: entrainment.model.entrain_turtles
.. autofunction:: entrainment.model.average_turtles
```

## LABREN (`entrainment.labren`)

Tools for accessing [LABREN's global horizontal solar irradiation model](http://labren.ccst.inpe.br/atlas_2017.html).

```{eval-rst}
.. autofunction:: entrainment.labren.labren
.. autofunction:: entrainment.labren.plot_labren
```

## Hypothesis (`entrainment.hypothesis`)

Tools for hypothesis testing.

```{eval-rst}
.. autofunction:: entrainment.hypothesis.analyze_data
.. autofunction:: entrainment.hypothesis.test_hypothesis
.. autofunction:: entrainment.hypothesis.plot_hypothesis
```

## Demo (`entrainment.demo`)

Tools to explore the entrainment dynamics.

```{eval-rst}
.. autofunction:: entrainment.demo.f_exact
.. autofunction:: entrainment.demo.exact
.. autofunction:: entrainment.demo.plot_exact
```

## Utils (`entrainment.utils`)

Utility tools.

```{eval-rst}
.. autofunction:: entrainment.utils.reorder
```
