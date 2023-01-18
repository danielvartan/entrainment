from .model import average_turtles
from .model import create_turtles
from .model import entrain
from .model import entrain_turtles
from .model import plot_model
from .model import run_model

__all__ = ["average_turtles", "create_turtles", "entrain", "entrain_turtles",
           "plot_model", "run_model"]

# # Test
#
# labren(72272)
# x = run_model(
#     labren_id = 72272, by = "season", n_cycles = 2, repetitions = 100
#     )
# 
# labren(1)
# x = run_model(labren_id = 1, by = "season", n_cycles = 2, repetitions = 100)
