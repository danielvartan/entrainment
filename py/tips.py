import numpy as np

## How to convert 'dict' into 'np.array'

x = {"a": 1, "b": 2}
x
dict.items(x)
list(dict.items(x))
np.array(list(dict.items(x)))
np.array(list(dict.items(x)))[:, 0]
np.array(list(dict.items(x)))[:, 1]

## 

[i["tau"] for i in np.array(turtles[j])]
