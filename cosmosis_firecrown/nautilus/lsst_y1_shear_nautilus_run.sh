#!/bin/bash -l
#SBATCH --qos=debug
#SBATCH --constraint=haswell
#SBATCH -J desc-tutorial
#SBATCH -n 64
#SBATCH --cpus-per-task=1
#SBATCH --constraint=cpu
#SBATCH -t 00:30:00
#SBATCH -o lssty1shear.log
#SBATCH -e lssty1shear.error

# Put here the path to the desc tutorial repo location
cd $SCRATCH/desc/desc_tutorial_cosmoinference_2024
cd cosmosis_firecrown/

# Load environment
source /global/cfs/cdirs/lsst/groups/MCP/setup_forecasts_prod.sh
source /opt/cray/pe/cpe/23.12/restore_lmod_system_defaults.sh

# Run the chain
time srun cosmosis --mpi nautilus/lsst_y1_shear_nautilus.ini
