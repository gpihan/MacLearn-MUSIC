import sys
import os
import random
import string

# All particles available
particle_list = ['9999', '211', '321', '2212', '-211', '-321', '-2212', 
                 '3122', '-3122', '3312', '-3312', '3334', '-3334',
                 '333', '111', '311', '-311', '2112', '-2112']

# Associated particles names
particle_name_list = ['charged_hadron', 'pion_p', 'kaon_p', 'proton',
                      'pion_m', 'kaon_m', 'anti_proton',
                      'Lambda', 'anti_Lambda', 'Xi_m', 'anti_Xi_p',
                      'Omega', 'anti_Omega', 'phi', 'pion_0', 'kaon_0', 'anti_kaon_0', 'neutron', 'anti_neutron']

Particles = {name:pdg_id for name,pdg_id in zip(particle_name_list, particle_list)}

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return folder_path
    else:
        random_char = random.choice(string.ascii_letters)
        folder_path_ = folder_path+"_"+str(random_char)
        return create_folder(folder_path_)

def checkLibraries() -> None:
    try:
        import sklearn
        print("scikit-learn is installed.")
    except ImportError:
        print("scikit-learn is not installed.")
    try:
        import h5py
        print("h5py is installed.")
    except ImportError:
        print("h5py is not installed.")
    try:
        import torch
        print("PyTorch is installed.")
    except ImportError:
        print("PyTorch is not installed.")
    try:
        import xgboost
        print("XGBoost is installed.")
    except ImportError:
        print("XGBoost is not installed.")
