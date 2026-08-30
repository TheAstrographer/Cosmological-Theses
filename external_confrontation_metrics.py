import numpy as np
import scipy.integrate as integrate
from typing import Dict, Tuple

class JCRCosmoClock:
    """
    Core Mathematical Core for JCR Cosmological Clock.
    """
    def __init__(self, H_wind=70.0, tau_decay=5.8, chi_scale=4500.0):
        self.H_wind = H_wind
        self.tau_decay = tau_decay
        self.chi_scale = chi_scale
        self.Omega_m = 0.3
        self.Omega_L = 0.7
        self.sin_torque = 0.9882  # Fixed phase invariant from your document
        self.c = 299792.458       # Speed of light in km/s

    def H_eff(self, z: float, chi: float) -> float:
        H_base = self.H_wind * np.sqrt(self.Omega_m * (1 + z)**3 + self.Omega_L)
        f_mod = 1.0 + 5.0 * np.exp(-z / 2.0)
        f_damp = np.exp(-z / self.tau_decay)
        S_spatial = np.exp(-chi / self.chi_scale)
        
        delta_H = 3.170 * (1.0 / (1.0 + z)) * self.sin_torque * f_mod * f_damp * S_spatial * 0.528
        return H_base + delta_H

    def integrate_distance_grid(self, z_arr: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Integrates your effective Hubble parameter across a target redshift array.
        """
        chi_arr = np.zeros_like(z_arr)
        # Iterative step since H depend on chi
        for i in range(1, len(z_arr)):
            dz = z_arr[i] - z_arr[i-1]
            z_mid = 0.5 * (z_arr[i] + z_arr[i-1])
            chi_pred = chi_arr[i-1] + (self.c / self.H_eff(z_arr[i-1], chi_arr[i-1])) * dz
            H_mid = self.H_eff(z_mid, 0.5 * (chi_arr[i-1] + chi_pred))
            chi_arr[i] = chi_arr[i-1] + (self.c / H_mid) * dz
            
        dL_arr = (1.0 + z_arr) * chi_arr
        return chi_arr, dL_arr

class ExternalStatisticalValidator:
    """
    Confronts the JCR framework with external statistics via standard Chi-Square tests.
    """
    def __init__(self, model: JCRCosmoClock):
        self.model = model
        
        # Mock Real-World Observatory Datasets for Demonstration
        # In a raw MCMC chain, these are replaced by the true covariance matrices
        self.data_pantheon = {
            'z': np.array([0.01, 0.05, 0.15, 0.50, 1.00, 1.50]),
            'dL_obs': np.array([43.1, 218.4, 695.1, 2810.3, 6610.5, 11210.2]),
            'error': np.array([0.5, 2.1, 7.5, 31.2, 75.4, 150.1])
        }
        
        self.data_desi_bao = {
            'z': np.array([0.57, 2.33]),
            'chi_obs': np.array([2215.0, 5620.0]),
            'error': np.array([15.0, 45.0])
        }

    def compute_pantheon_chi2(self, dL_pred: np.ndarray) -> float:
        return float(np.sum(((self.data_pantheon['dL_obs'] - dL_pred) / self.data_pantheon['error'])**2))

    def compute_desi_chi2(self, chi_pred: np.ndarray) -> float:
        return float(np.sum(((self.data_desi_bao['chi_obs'] - chi_pred) / self.data_desi_bao['error'])**2))

    def run_confrontation(self) -> Dict:
        # Evaluate Pantheon Grid
        _, dL_calc = self.model.integrate_distance_grid(self.data_pantheon['z'])
        chi2_pantheon = self.compute_pantheon_chi2(dL_calc)
        
        # Evaluate DESI Grid
        chi_calc, _ = self.model.integrate_distance_grid(self.data_desi_bao['z'])
        chi2_desi = self.compute_desi_chi2(chi_calc)
        
        total_chi2 = chi2_pantheon + chi2_desi
        dof = len(self.data_pantheon['z']) + len(self.data_desi_bao['z']) - 3 # 3 free params
        reduced_chi2 = total_chi2 / dof
        
        return {
            'Chi2_Pantheon': chi2_pantheon,
            'Chi2_DESI': chi2_desi,
            'Total_Chi2': total_chi2,
            'Reduced_Chi2': reduced_chi2,
            'Degrees_of_Freedom': dof
        }

# --- Execution ---
if __name__ == "__main__":
    jcr_universe = JCRCosmoClock(H_wind=70.0, tau_decay=5.8)
    tester = ExternalStatisticalValidator(jcr_universe)
    stats = tester.run_confrontation()
    
    print("="*60)
    print("EXTERNAL CONFRONTATION METRICS FOR JCR COSMOLOGICAL CLOCK")
    print("="*60)
    print(f"Pantheon+ Supernova Chi2 Error Vector : {stats['Chi2_Pantheon']:.4f}")
    print(f"DESI BAO Standard Ruler Chi2 Vector   : {stats['Chi2_DESI']:.4f}")
    print(f"Unified Total Framework Chi2          : {stats['Total_Chi2']:.4f}")
    print(f"Reduced Chi2 Value (Goodness of Fit)   : {stats['Reduced_Chi2']:.4f} (Target ~1.0)")
    print(f"Total Model Free Parameter Space DoF  : {stats['Degrees_of_Freedom']}")
    print("="*60)
