# ---------------------------------------------------------------
# Directory setup
# ---------------------------------------------------------------
mkdir -p chains/jcrin_dual_gate
cd chains/jcrin_dual_gate

# ---------------------------------------------------------------
# SLICE 01 – Planck only
# ---------------------------------------------------------------
cobaya-run ../../jcrin_dual_gate_joint.yaml \
  --force \
  --output 01_Planck_only \
  --packages-path $COBAYA_PACKAGES_PATH \
  --force-reinstall false \
  -- "likelihood: {desi_2024_dr1_bao.main: null, pantheon_plus.binned: null, des_y6.3x2pt: null, kids_legacy.cosmic_shear: null}"

# ---------------------------------------------------------------
# SLICE 02 – Planck + DESI
# ---------------------------------------------------------------
cobaya-run ../../jcrin_dual_gate_joint.yaml \
  --force \
  --output 02_Planck_DESI \
  -- "likelihood: {pantheon_plus.binned: null, des_y6.3x2pt: null, kids_legacy.cosmic_shear: null}"

# ---------------------------------------------------------------
# SLICE 03 – Planck + DESI + Pantheon+
# ---------------------------------------------------------------
cobaya-run ../../jcrin_dual_gate_joint.yaml \
  --force \
  --output 03_Planck_DESI_Pantheon \
  -- "likelihood: {des_y6.3x2pt: null, kids_legacy.cosmic_shear: null}"

# ---------------------------------------------------------------
# SLICE 04 – Planck + DESI + Pantheon+ + DES Y6
# ---------------------------------------------------------------
cobaya-run ../../jcrin_dual_gate_joint.yaml \
  --force \
  --output 04_Planck_DESI_Pantheon_DESY6 \
  -- "likelihood: {kids_legacy.cosmic_shear: null}"

# ---------------------------------------------------------------
# SLICE 05 – Full five-pillar
# ---------------------------------------------------------------
cobaya-run ../../jcrin_dual_gate_joint.yaml \
  --force \
  --output 05_Full_Five_Pillar
