para_dict = {
    'Projectile':  "Au",         # projectile nucleus name
    'Target'    :  "Au",         # target nucleus name
    'resetProjWS':  1,
    'resetTargWS':  1,
    'ProjWS_R':  5.09,
    'ProjWS_a':  0.46,
    'ProjWS_beta2':  0.16,
    'ProjWS_beta3':  0.0,
    'ProjWS_beta4':  0.,
    'ProjWS_gamma':  0.0,
    'ProjWS_da':  0.01,
    'ProjWS_dR':  0.015,
    'd_min': 0.9,
    'useQuarks': 1,
    'Q2': 1.,
    'roots'     :   200,         # collision energy (GeV)
    'seed'      :   -1,          # random seed (-1: system)
    'baryon_junctions': 1,       # 0: baryon number assumed to be at string end
                                 # 1: baryon number transported assuming baryon
                                 # junctions (at smaller x)
                                 # see arXiv:nucl-th/9602027
    'electric_junctions':  1,
    'integer_electric_charge': 1,
    'electricChargeInStringProb': 0.1,
    'lambdaB': 1.0,              # parameter the controls the strength of
    'lambdaQ': 1.0,              # parameter the controls the strength of
                                 # the baryon junction stopping
    'lambdaBs': 1.0,             # fraction of single-to-double string junction stopping
    'lambdaQs': 1.0,             # fraction of single-to-double string junction stopping
    'baryonInStringProb': 0.1,

    'BG': 16.,
    'shadowing_factor':  0.60,   # a shadowning factor for producing strings from multiple scatterings
    'rapidity_loss_method': 4,
    'remnant_energy_loss_fraction': 0.5,         # nucleon remnants energy loss fraction (fraction of string's y_loss) [0, 1]
    'ylossParam4At2': 1.70,
    'ylossParam4At4': 2.00,
    'ylossParam4At6': 2.20,
    'ylossParam4var': 0.5,
    'evolve_QCD_string_mode': 4,        # string evolution mode
                                        # 1: deceleration with fixed rapidity loss (m/sigma = 1 fm, dtau = 0.5 fm)
                                        # 2: deceleration with LEXUS sampled rapidit loss (both dtau and sigma fluctuate)
                                        # 3: deceleration with LEXUS sampled rapidit loss (m/sigma = 1 fm, dtau fluctuates)
                                        # 4: deceleration with LEXUS sampled rapidit loss (dtau = 0.5 fm, m/sigma fluctuates)
    'cenMin':0.0,
    'cenMax':10.0,

}
