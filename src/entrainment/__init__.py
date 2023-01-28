r"""Main {entrainment} package."""
from . import data
from .run_model import run_model
from .analyze_data import analyze_data
from .test_hypothesis import test_hypothesis
from .labren import labren, plot_labren
from .plot_dynamics import plot_dynamics

__all__ = [
    "data", "run_model", "analyze_data", "test_hypothesis", "labren", 
    "plot_labren", "plot_dynamics"
    ]

__version__ = "0.0.0.9000"
