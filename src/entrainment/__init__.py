r"""Main {entrainment} package."""
from . import data
from .run_model import run_model, plot_model_line, plot_model_violin
from .run_model import plot_model_line_1_2, plot_model_violin_1_2
from .analyze_data import analyze_data, plot_hist, plot_qq
from .test_hypothesis import test_hypothesis
from .labren import labren, plot_labren
from .plot_dynamics import plot_dynamics

__all__ = [
    "data", "run_model", "analyze_data", "test_hypothesis", "labren", 
    "plot_labren", "plot_dynamics", "plot_model_1_2"
    ]

__version__ = "0.0.0.9000"
