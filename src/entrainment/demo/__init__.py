"""Tools to explore the entrainment dynamics."""
from .demo import f_exact
from .demo import exact
from .demo import plot_exact

__all__ = ["f_exact", "exact", "plot_exact"]

# # Test
# 
# entrainment.demo.f_exact(lam = 1, lam_c = 5, k = 2, tau = 22)
# entrainment.demo.exact(lam_c = 5, k = 2, tau = 22, lam_0 = 0, lam_n = 10)
# entrainment.demo.plot_exact(lam_c = 5, k = 2, tau = 22, lam_0 = 0, lam_n = 10)
# entrainment.demo.plot_exact(lam_c = 5, k = 2, tau = 26, lam_0 = 0, lam_n = 10)
