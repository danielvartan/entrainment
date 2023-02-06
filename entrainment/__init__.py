r"""Main {entrainment} package."""
from . import data
from .run_model import run_model
from .analyze_model import analyze_model
from .test_hypothesis import test_hypothesis
from .plot_model import plot_model_line, plot_model_line_1_2
from .plot_model import plot_model_violin, plot_model_violin_1_2
from .plot_model import plot_model_dynamics
from .get_labren_data import get_labren_data, plot_labren_data

__all__ = [
    "data", "run_model", "analyze_model", "test_hypothesis", 
    "plot_model_line", "plot_model_line_1_2", "plot_model_violin",
    "plot_model_violin_1_2", "plot_model_dynamics",
    "get_labren_data", "plot_labren_data"
    ]

__version__ = "0.0.0.9000"
