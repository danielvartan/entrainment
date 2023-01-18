from .hypothesis import analyze_data
from .hypothesis import plot_hypothesis
from .hypothesis import test_hypothesis

__all__ = ["analyze_data", "plot_hypothesis", "test_hypothesis"]

# # Test
# 
# # labren(72272)
# north = run_model(
#     n = 10 ** 3, labren_id = 72272, by = "season", n_cycles = 3,
#     repetitions = 100, plot = False
#     )
# 
# # labren(1)
# south = run_model(
#     n = 10 ** 3, labren_id = 1, by = "season", n_cycles = 3,
#     repetitions = 100, plot = False
#     )
# 
# for i in list(north): analyze_data(north, i, "Nascente do rio Ailã")
# for i in list(south): analyze_data(south, i, "Arroio Chuí")
# for i in list(north): test_hypothesis(i, north, south)
