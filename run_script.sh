#!/bin/bash -l
## Nazwa zlecenia
#SBATCH -J Combine_channels
## Nazwa grantu do rozliczenia zu  ycia zasob  w CPU
#SBATCH -A plgomenn-cpu
## Specyfikacja partycji
#SBATCH -p plgrid
## Plik ze standardowym wyj ^{ciem
#SBATCH --output="data_output.out"
## Plik ze standardowym wyj ^{ciem b ^b ^yd  w
#SBATCH --error="data_error.err"
## Maksymalny czas trwania zlecenia (format HH:MM:SS)
#SBATCH --time=72:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
## przejscie do katalogu z ktorego wywolany zostal sbatch

rm -rf /net/afscra/people/plgjkosciukiewi/datasets/bray_4_channel

cd $HOME/DataEngineering
source .venv/bin/activate
python ./combine_channels.py

