ssh avivekanand3@login-ice.pace.gatech.edu
ml anaconda3

salloc --nodes=1 --gres=gpu:A100 -t5:00:00 --ntasks-per-node=24
# requests a single A100 gpu and 24 cpu cores
nvidia-smi


jupyter notebook --ip 0.0.0.0

