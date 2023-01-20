
<!-- model-formulas.md is generated from model-formulas.Rmd. Please edit that file -->

``` {toctree}
:maxdepth: 2
:hidden:

model-formulas
```

# Model formulas

- Logistic function

$$
f(x) = \cfrac{L}{1 + e^{-k (x - x_{0})}}
$$

- Entrainment function

$$
\text{Entrain}(\lambda, \lambda_{c}, k, \tau) = \tau +  \cfrac{24 - \tau}{1 + e^{-k (\lambda - \lambda_{c})}} \pm E
$$

- Unentrainment function

$$
\text{Unentrain}(\lambda, \lambda_{c}, k, \tau, \tau_{0}) = \tau +  \cfrac{\tau_{0} - \tau}{1 + e^{-k (\lambda - \lambda_{c})}} \pm E
$$

- General (un)entrainment function

$$
\text{(un)Entrain}(\lambda, \lambda_{c}, k, \tau, \tau_{\text{ref}}) = \tau +  \cfrac{\tau_{\text{ref}} - \tau}{1 + e^{-k (\lambda - \lambda_{c})}} \pm E
$$

$$
\text{Entrain}(\lambda, \lambda_{c}, k, \tau, \tau_{\text{ref}}) = 
\overbrace{\tau + \cfrac{\tau_{\text{ref}} - \tau}{1 + e^{-k (\lambda - \lambda_{c})}}}^{F_{- E}} \pm E
$$

- Error term

$$
E = P_{unifom}(0, 1) \times |F_{- E} - \tau|
$$
