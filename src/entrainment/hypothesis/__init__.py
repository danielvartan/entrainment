"""Tools for hypothesis testing."""
from .analyze_data import analyze_data
from .plot_hypothesis import plot_hypothesis
from .test_hypothesis import test_hypothesis

__all__ = ["analyze_data", "plot_hypothesis", "test_hypothesis"]

# # Test
# 
# entrainment.labren.labren(72272)
# north = entrainment.model.run(
#     n = 10 ** 3, labren_id = 72272, by = "season", n_cycles = 3,
#     repetitions = 100, plot = False
#     )
# 
# entrainment.labren.labren(1)
# south = entrainment.model.run(
#     n = 10 ** 3, labren_id = 1, by = "season", n_cycles = 3,
#     repetitions = 100, plot = False
#     )
# 
# for i in list(north):
#     entrainment.hypothesis.analyze_data(north, i, "Nascente do rio Ailã")
#
# for i in list(south):
#     entrainment.hypothesis.analyze_data(south, i, "Arroio Chuí")
#
# import numpy as np
# entrainment.hypothesis.plot_hypothesis(
#     key = "winter", p_value = "0.0000",
#     x = [i["tau"] for i in np.array(north["winter"])],
#     y = [i["tau"] for i in np.array(south["winter"])],
#     )
#
# for i in list(north):
#     entrainment.hypothesis.test_hypothesis(i, north, south)
