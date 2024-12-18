ssh rdubey36@login-ice.pace.gatech.edu -L 8888:localhost:8888
ml anaconda3

salloc --nodes=1 --gres=gpu:A100 -t5:00:00 --ntasks-per-node=24
# requests a single A100 gpu and 24 cpu cores
# H100 is better.
nvidia-smi


# https://wandb.ai/avivekanand/arithmetic_training/runs/eyq2m09t?nw=nwuseravivekanand

jupyter notebook --ip 0.0.0.0

