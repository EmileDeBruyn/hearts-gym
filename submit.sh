#!/bin/bash 

#SBATCH --job-name=hearts_att_train 
#SBATCH --nodes=1 
#SBATCH --tasks-per-node=1 
#SBATCH --time=24:00:00 
#SBATCH --partition=gpus 
#SBATCH --output=./logs/base_attention.out 
#SBATCH --error=./logs/base_attention.err 
#SBATCH --gres=gpu:1

python train.py
