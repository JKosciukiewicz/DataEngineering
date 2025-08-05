#!/bin/bash -l
#SBATCH --job-name=conf_bbbc_train
#SBATCH --time=24:00:00
#SBATCH --account=plgomenn-gpu-a100
#SBATCH --partition=plgrid-gpu-a100
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --gres=gpu

cd $HOME/DataEngineering
source .venv/bin/activate
python ./combine_channels_bbbc.py

