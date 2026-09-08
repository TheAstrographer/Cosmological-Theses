#!/usr/bin/env python3
"""
five_slice_diagnostics.py
-------------------------
Empirical five-slice analysis for the JCRIN Dual-Gate / lattice-torque model.

Assumes Cobaya chains have been run with the parameters:
  H0          (base)
  H0_local    (derived = H0 + 3.17)
  Omega_m
  sigma8
  S8
  A_IA
  alpha_IA / eta_IA
  logT_AGN

Usage:
  python five_slice_diagnostics.py --root chains/jcrin_dual_gate
"""

import argparse
import numpy as np
from getdist import loadMCSamples, plots
import os

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
TORQUE = 3.17          # fixed Dual-Gate torque (km/s/Mpc)

# Ordered list of the five empirical slices
SLICES = [
    {
        "name": "01_Planck_only",
        "description": "Planck 2018 high-ℓ TTTEEE + low-ℓ TT/EE + lensing",
        "required_params": ["H0", "Omega_m", "sigma8", "S8"]
    },
    {
        "name": "02_Planck_DESI",
        "description": "Planck + DESI BAO",
        "required_params": ["H0", "Omega_m", "sigma8", "S8"]
    },
    {
        "name": "03_Planck_DESI_Pantheon",
        "description": "Planck + DESI + Pantheon+",
        "required_params": ["H0", "Omega_m", "sigma8", "S8"]
    },
    {
        "name": "04_Planck_DESI_Pantheon_DESY6",
        "description": "Planck + DESI + Pantheon+ + DES Y6 3×2pt",
        "required_params": ["H0", "Omega_m", "sigma8", "S8", "A_IA", "logT_AGN"]
    },
    {
        "name": "05_Full_Five_Pillar",
        "description": "Full matrix: Planck + DESI + Pantheon+ + DES Y6 + KiDS-Legacy",
        "required_params": ["H0", "Omega_m", "sigma8", "S8", "A_IA", "logT_AGN"]
    },
]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def load_slice(root, slice_name):
    """Load GetDist samples for a given slice."""
    path = os.path.join(root, slice_name)
    if not os.path.exists(path + ".txt") and not os.path.exists(path + "_1.txt"):
        print(f"[WARNING] Chain not found for {slice_name}")
        return None
    samples = loadMCSamples(path, settings={"ignore_rows": 0.3})
    return samples


def summarize(samples, params):
    """Return mean ± std for the requested parameters."""
    summary = {}
    for p in params:
        if p in samples.paramNames.list():
            mean = samples.mean(p)
            std  = samples.std(p)
            summary[p] = (mean, std)
        else:
            summary[p] = (np.nan, np.nan)
    return summary


def print_slice_report(slice_info, summary):
    """Pretty-print one slice."""
    print("\n" + "="*70)
    print(f"SLICE: {slice_info['name']}")
    print(f"Desc : {slice_info['description']}")
    print("-"*70)

    for param, (mean, std) in summary.items():
        if np.isnan(mean):
            print(f"  {param:12s} :  not found in chain")
        else:
            print(f"  {param:12s} :  {mean:8.4f}  ±  {std:7.4f}")

    # Dual-Gate specific derived quantity
    if "H0" in summary and not np.isnan(summary["H0"][0]):
        H0_base = summary["H0"][0]
        H0_local = H0_base + TORQUE
        print(f"  {'H0_local':12s} :  {H0_local:8.4f}   (base + {TORQUE})")
    print("="*70)


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Five-slice Dual-Gate diagnostics")
    parser.add_argument("--root", default="chains/jcrin_dual_gate",
                        help="Root directory containing the five slice chains")
    args = parser.parse_args()

    print("\nJCRIN Dual-Gate — Empirical Five-Slice Diagnostics")
    print(f"Torque = {TORQUE} km/s/Mpc")
    print(f"Looking for chains under: {args.root}\n")

    all_summaries = {}

    for slice_info in SLICES:
        samples = load_slice(args.root, slice_info["name"])
        if samples is None:
            continue

        summary = summarize(samples, slice_info["required_params"])
        print_slice_report(slice_info, summary)
        all_summaries[slice_info["name"]] = summary

    # Optional: quick comparison table at the end
    print("\n\nCOMPACT COMPARISON TABLE (mean values)")
    print(f"{'Slice':<35} {'H0_base':>8} {'H0_local':>9} {'Omega_m':>8} {'S8':>8}")
    print("-"*75)
    for name, summary in all_summaries.items():
        H0 = summary.get("H0", (np.nan,))[0]
        Om = summary.get("Omega_m", (np.nan,))[0]
        S8 = summary.get("S8", (np.nan,))[0]
        H0l = H0 + TORQUE if not np.isnan(H0) else np.nan
        print(f"{name:<35} {H0:8.3f} {H0l:9.3f} {Om:8.4f} {S8:8.4f}")

    print("\nDone. Inspect the individual slice posteriors above.")
    print("Next recommended step: generate triangle plots for slices 04 and 05.")


if __name__ == "__main__":
    main()
