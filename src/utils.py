import sys

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