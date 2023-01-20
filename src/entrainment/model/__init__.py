"""The entrainment model."""
from .average_turtles import average_turtles
from .create_turtles import create_turtles
from .entrain import entrain
from .entrain import entrain_turtles
from .plot_model import plot_model
from .run_model import run_model

__all__ = ["average_turtles", "create_turtles", "entrain", "entrain_turtles",
           "plot_model", "run_model"]

# # Test
# 
# entrainment.model.create_turtles(1)
# entrainment.model.average_turtles(entrainment.model.create_turtles(5))
# entrainment.model.entrain(lam = 10, lam_c = 4, k = 10, tau = 19)
#
# entrainment.model.entrain_turtles(
#     turtles = entrainment.model.create_turtles(5),
#     turtles_0 = entrainment.model.create_turtles(5),
#     lam = 10, lam_c = 4, lam_c_tol = 1
#     )
# 
# entrainment.model.plot_model(
#     turtles = entrainment.model.run_model(labren_id = 1000, plot = False,
#                                     repetitions = 10),
#     lam_c = 4727.833, labren_id = 1000, n_cycles = 3, repetitions = 10
# )
# 
# entrainment.labren.labren(72272)
# x = entrainment.model.run_model(
#     labren_id = 72272, by = "season", n_cycles = 2, repetitions = 100
#     )
# 
# entrainment.labren.labren(1)
# x = entrainment.model.run_model(
#     labren_id = 1, by = "season", n_cycles = 2, repetitions = 100
#     )
