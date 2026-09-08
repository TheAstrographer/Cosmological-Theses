# jcrin_cobaya_adapter.py
"""
Thin port-adapter that exposes HJcrinExpansion to Cobaya YAML files
without modifying the original theory class.
Inspired by the separation-of-concerns style of PORTHUB.COM.
"""

from cobaya.theory import Theory
from hJcrinExpansion import HJcrinExpansion   # <-- original class, untouched

class JCRINAdapter(Theory):
    """
    Cobaya-compatible wrapper.
    All scientific logic remains inside HJcrinExpansion.
    This class only satisfies Cobaya’s Theory interface.
    """

    def initialize(self):
        self._engine = HJcrinExpansion()
        self._engine.initialize()

    def get_requirements(self):
        return self._engine.get_requirements()

    def calculate(self, state, want_derived=True):
        # Delegate completely to the original theory
        return self._engine.calculate(state, want_derived=want_derived)

    # Optional: expose any extra derived quantities the YAMLs may request
    def get_can_provide_params(self):
        return ['H_profile']   # or whatever the original class provides
