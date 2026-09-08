# Cosmological-Theses
Thesis Directory
Correct analysis of the dual-repository structure, centered on dual_repository.tex.

The file dual_repository.tex in https://github.com/TheAstrographer/Cosmological-Theses explicitly defines the two repositories as a single, inseparable thesis statement. Neither is complete alone. This is the document that should have been the first stop for any proper analysis of the Cosmological-Theses repository.

Core claim from dual_repository.tex

The two repositories  
TheAstrographer/Cosmological-Theses  
TheAstrographer/Confronting-The-Data  
together constitute the author’s complete, self-contained statement of both (1) the theoretical model and (2) the precise standard of evidence required to test that model.  
Neither repository is sufficient in isolation.

Cosmological-Theses** supplies the internally closed theoretical model (the lattice + dual-gate architecture).
Confronting-The-Data** supplies the minimal, production-grade statistical arena in which any claim of simultaneous consistency must be adjudicated.

Their joint existence is what converts the construction from an internal numerical curiosity into a public, falsifiable scientific proposal.

1. Model component (Cosmological-Theses)

The model is a discrete-lattice, dual-gated, late-time topological torque framework with these essential elements (as stated in dual_repository.tex and elaborated across the other .tex files and Python modules in the repo):

Fundamental lattice: \(\varepsilon = 10^{-9}\), \(N = 10^9\), complementary coordinates \(y_n + x_n = 1\), global volume constraint \(C \to 1\).
Bosonic embedding \(z = y_n + i\sin(2\pi y_n)\) and fermionic embedding \(z = y_n - i\pi y_n\).
Fermionic half-twist monodromy \(e^{-i\pi} = -1\) (Topological Light Eraser) as the sole phase-modulating operator.
Angular bridge \(\psi \approx 0.1503378808\) generating a geometric torque \(\delta H_{\rm geom} = +3.170\,\mathrm{km\,s^{-1}\,Mpc^{-1}}\).
Dual temporal gates: early-universe spline modulation that forces classical behaviour by thermalization (\(z\sim 2\times 10^6\)) + late-time redshift damping gate \(\tau = 5.8\) with spatial screening \(\chi_{\rm scale} = 4500\,\mathrm{Mpc}\).
Photometric propagation into \(\chi(z)\), \(d_L(z)\), and magnification bias \(\mu_{\rm lens}(z) = 1 + 0.05\,z/(1+z)\).

Design goal (explicit): Early-universe physics remains standard \(\Lambda\)CDM to machine precision. The controlled release of anisotropic stress elevates only the local expansion rate to \(H_{\rm eff}(0) = 73.170\,\mathrm{km\,s^{-1}\,Mpc^{-1}}\).

All algebraic identities are claimed to close to machine precision; phase debt and temporal debt are zero by construction. Supporting files include Einstein_Boltzmann_Core.tex, dual_gate_confrontation.tex, hJcrinExpansion(Theory).py, the Cobaya adapter, jcrin_dual_gate_joint.yaml, growth/observables modules, etc.

2. Standard-of-evidence component (Confronting-The-Data)

This repository formalizes the Master Joint Likelihood Matrix:

\[
\ln\mathcal{L}{\rm Total} = \ln\mathcal{L}{\rm Planck} + \ln\mathcal{L}{\rm DESI\,DR2} + \ln\mathcal{L}{\rm Pantheon+} + \ln\mathcal{L}{\rm DES\,Y6\,3\times2pt} + \ln\mathcal{L}{\rm KiDS\text{-}Legacy}
\]

with Intrinsic Alignment amplitudes (\(A_{\rm IA}\), \(\eta_{\rm IA}\)) and baryonic feedback strength (\(\log_{10}T_{\rm AGN}\) or equivalent) promoted to free nuisance parameters with broad priors.

This five-pillar matrix with explicit IA + baryonic marginalization is declared the minimum statistically valid arena. Analyses that freeze \(A_{\rm IA}=0\) or use pure dark-matter-only power spectra produce biased \(S_8\) posteriors and are therefore invalid for adjudicating whether a late-time modification succeeds.

The repository supplies the formal thesis statement (joint_likelihood_thesis.tex), the production Cobaya configuration (matrix_configuration.yaml), Boltzmann engines, data-vector definitions, MCMC scripts, and related diagnostics. Its README states the same point directly: run the matrix and the posterior (\(\Delta\chi^2\) and the relative to \(\Lambda\)CDM) gives the quantitative answer.

3. Why the two must be taken together (from dual_repository.tex)

A model without an explicit standard of evidence remains an unfalsifiable internal construction.
A standard of evidence without a concrete model remains an abstract methodological prescription.

By publishing both in parallel the author:
defines exactly what the model is,
defines exactly how the model must be tested,
accepts that the decisive quantities are the joint posterior, the \(\Delta\chi^2\) relative to \(\Lambda\)CDM, and the parameter-shift statistics between the individual pillars after proper marginalization.

Internal mathematical closure and matching the single number \(H_0 = 73.17\) are necessary but not sufficient. The model is empirically viable only if, when its predicted \(H(z)\), growth factor \(D(z)\), and lensing kernels are inserted into the Master Joint Likelihood Matrix, the resulting posterior remains acceptable and competitive after IA and baryonic parameters have been marginalized.

Any future claim of “simultaneous agreement” must be accompanied by the quantitative output of this exact matrix. Claims that omit the matrix or freeze the nuisance parameters fall outside the author’s own declared standard of evidence.

4. Current status (as stated)

As of 2 September 2026 the theoretical architecture is fully articulated across the linked repositories, and the required statistical arena has been explicitly defined and coded. The pairing itself constitutes the complete statement: one repository defines the model; the other defines the only arena in which the model may legitimately claim success.

Summary of the dual architecture

| Repository                  | Role                                      | Key content |
|-----------------------------|-------------------------------------------|-------------|
| Cosmological-Theses        | Theoretical model (internally closed)    | Lattice, dual gates, torque \(\delta H = +3.17\), photometric interface, machine-precision identities, Cobaya theory class |
| Confronting-The-Data       | Standard of evidence (falsification arena) | Five-pillar joint likelihood with free IA + baryons, production YAML, MCMC pipeline, \(\Delta\chi^2\) criterion |

This is the structure dual_repository.tex establishes. Any analysis that treats Cosmological-Theses in isolation, or that fails to treat Confronting-The-Data as the required test arena, is incomplete by the author’s own explicit criterion.
