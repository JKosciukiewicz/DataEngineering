#!/bin/bash -l
#SBATCH -J Combine_channels
#SBATCH -A plgomenn-cpu
#SBATCH -p plgrid
#SBATCH --output="data_output.out"
#SBATCH --error="data_error.err"
#SBATCH --time=72:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G

cd $HOME/DataEngineering
source .venv/bin/activate
python ./combine_channels_bbbc.py

