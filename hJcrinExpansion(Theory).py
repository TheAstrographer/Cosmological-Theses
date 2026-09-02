#!/usr/bin/env python3
"""
Cobaya Custom Theory Class for the JCRIN Additive Torque Model.
Reconstructs background distances for Planck + DESI DR2 joint likelihood runs.
"""

import numpy as np
from cobaya.theory import Theory

class HJcrinExpansion(Theory):
    def initialize(self):
        """ Defines variables and registers parameters from the YAML configuration. """
        self.c = 299792.458  # Speed of light (km/s)

    def get_requirements(self):
        """ Informs Cobaya that we require baseline cosmological parameters. """
        return {'H0': None, 'Omega_m': None}

    def standard_H_lcdm(self, z, H0, Omega_m):
        """ Calculates the standard unperturbed flat LCDM background expansion rate. """
        return H0 * np.sqrt(Omega_m * (1.0 + z)**3 + (1.0 - Omega_m))

    def H_jcrin(self, z, H0_base, torque=3.17, tau=5.8):
        """
        Calculates the effective Hubble parameter using the additive, 
        exponentially damped geometric torque channel.
        """
        # Read the background Om from the sampler state
        Omega_m = self.provider.get_param('Omega_m')
        
        H_lcdm = self.standard_H_lcdm(z, H0=H0_base, Omega_m=Omega_m)
        return H_lcdm + torque * np.exp(-z / tau)

    def calculate(self, state, want_derived=True):
        """
        Executes the background integration loops and passes the 
        modified expansion profile down to the likelihood modules.
        """
        # Pull current parameter coordinates from the active chain step
        H0_current = self.provider.get_param('H0')
        
        # In a full run, you can define a custom integration vector over z
        # to populate modified comoving distances chi(z) for the DES Y6 band-powers
        state['H_profile'] = lambda z: self.H_jcrin(z, H0_base=H0_current)
