#!/usr/bin/env python3
"""
five_slice_full_report.py
-------------------------
Full diagnostic report for the five empirical slices of the Dual-Gate model.
Reports for every slice:
  • mean ± std of H0_base, H0_local, Omega_m, sigma8, S8
  • best-fit -lnL (and Δχ² vs corresponding ΛCDM if available)
  • posterior mean ± std of A_IA and logT_AGN
"""

import numpy as np
from getdist import loadMCSamples
import os
import argparse

TORQUE = 3.17

SLICES = [
    "01_Planck_only",
    "02_Planck_DESI",
    "03_Planck_DESI_Pantheon",
    "04_Planck_DESI_Pantheon_DESY6",
    "05_Full_Five_Pillar",
]

PARAMS = ["H0", "Omega_m", "sigma8", "S8", "A_IA", "logT_AGN"]

def load_samples(root, name):
    path = os.path.join(root, name)
    if not (os.path.exists(path + ".txt") or os.path.exists(path + "_1.txt")):
        return None
    return loadMCSamples(path, settings={"ignore_rows": 0.3})

def get_best_fit(samples):
    """Return best-fit -lnL if available."""
    try:
        return samples.getBestFit().loglike
    except Exception:
        # fallback: minimum of -loglike in the chain
        if "chi2" in samples.paramNames.list():
            return 0.5 * samples.samples[:, samples.paramNames.list().index("chi2")].min()
        return np.nan

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="chains/jcrin_dual_gate")
    parser.add_argument("--lcdm-root", default=None,
                        help="Optional root of corresponding pure-ΛCDM chains for Δχ²")
    args = parser.parse_args()

    print("\n" + "="*80)
    print("JCRIN Dual-Gate — Full Five-Slice Empirical Report")
    print(f"Torque = {TORQUE} km s⁻¹ Mpc⁻¹")
    print("="*80)

    for name in SLICES:
        samples = load_samples(args.root, name)
        if samples is None:
            print(f"\n[{name}]  -->  chain not found")
            continue

        print(f"\n\nSLICE: {name}")
        print("-"*80)

        # Main cosmological parameters
        for p in ["H0", "Omega_m", "sigma8", "S8"]:
            if p in samples.paramNames.list():
                mean, std = samples.mean(p), samples.std(p)
                print(f"  {p:12s} : {mean:8.4f}  ±  {std:7.4f}")
            else:
                print(f"  {p:12s} : not present")

        # Derived local Hubble
        if "H0" in samples.paramNames.list():
            H0_base = samples.mean("H0")
            print(f"  {'H0_local':12s} : {H0_base + TORQUE:8.4f}   (base + {TORQUE})")

        # Nuisance parameters (IA + baryons)
        print()
        for p in ["A_IA", "logT_AGN"]:
            if p in samples.paramNames.list():
                mean, std = samples.mean(p), samples.std(p)
                print(f"  {p:12s} : {mean:8.4f}  ±  {std:7.4f}")
            else:
                print(f"  {p:12s} : not present")

        # Best-fit likelihood
        bf = get_best_fit(samples)
        print(f"\n  best-fit -lnL     : {bf:10.3f}")

        # Optional Δχ² vs ΛCDM
        if args.lcdm_root:
            lcdm = load_samples(args.lcdm_root, name)
            if lcdm is not None:
                bf_lcdm = get_best_fit(lcdm)
                delta = 2.0 * (bf - bf_lcdm)          # Δχ² ≈ 2Δ(-lnL)
                print(f"  ΛCDM best-fit -lnL: {bf_lcdm:10.3f}")
                print(f"  Δχ² (DualGate - ΛCDM) : {delta:10.2f}")

        print("-"*80)

    print("\nReport complete.\n")

if __name__ == "__main__":
    main()
