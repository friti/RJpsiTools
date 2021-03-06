sample_names = [
    'jpsi_tau' ,
    'jpsi_mu'  ,
#     'jpsi_pi'  ,
    'chic0_mu' ,
    'chic1_mu' ,
    'chic2_mu' ,
    'jpsi_hc'  ,
    'hc_mu'    ,
    'psi2s_mu' ,
    'psi2s_tau',
#     'jpsi_3pi' ,
    'jpsi_x_mu',
    #'fakes'   ,
    'data'     ,
]


weights = dict()

bc_weight = 1.53
fr = 0.19
hbmu_norm = 8.5 *1.5
#hbmu_norm = 8.5 *1.6


weights['jpsi_tau' ] = bc_weight
weights['jpsi_mu'  ] = bc_weight
weights['psi2s_mu' ] = bc_weight
weights['chic0_mu' ] = bc_weight
weights['chic1_mu' ] = bc_weight
weights['chic2_mu' ] = bc_weight
weights['hc_mu'    ] = bc_weight
weights['psi2s_tau'] = bc_weight
weights['jpsi_hc'  ] = bc_weight
weights['fakes'    ] = fr/(1-fr) #2.7 # 2.5 # 2.7
weights['data'     ] = 1.
weights['jpsi_x_mu'] = 1. * hbmu_norm # 10. # 8.5
weights['jpsi_pi'  ] = 1.
weights['jpsi_3pi' ] = 1.

titles = dict()
titles['jpsi_tau' ] = 'B_{c}#rightarrowJ/#Psi#tau'
titles['jpsi_mu'  ] = 'B_{c}#rightarrowJ/#Psi#mu'
titles['onia'     ] = 'J/#Psi + #mu'
titles['jpsi_pi'  ] = 'B_{c}#rightarrowJ/#Psi#pi'
titles['psi2s_mu' ] = 'B_{c}#rightarrow#Psi(2S)#mu'
titles['chic0_mu' ] = 'B_{c}#rightarrow#chi_{c0}#mu'
titles['chic1_mu' ] = 'B_{c}#rightarrow#chi_{c1}#mu'
titles['chic2_mu' ] = 'B_{c}#rightarrow#chi_{c2}#mu'
titles['hc_mu'    ] = 'B_{c}#rightarrowh_{c}#mu'
titles['psi2s_tau'] = 'B_{c}#rightarrow#Psi(2S)#tau'
titles['jpsi_3pi' ] = 'B_{c}#rightarrowJ/#Psi3#pi'
titles['jpsi_hc'  ] = 'B_{c}#rightarrowJ/#PsiH_{c}'
titles['data'     ] = 'observed'
titles['fakes'   ] = 'J/#Psi + X'
titles['jpsi_x_mu'] = 'J/#Psi + #mu'

#colors
import ROOT
from bokeh.palettes import viridis, all_palettes
col = list(map(ROOT.TColor.GetColor, all_palettes['Spectral'][11]))
colours = dict()
colours['jpsi_tau' ] = col[0]
colours['jpsi_mu'  ] = col[1]
colours['chic0_mu' ] = col[2]
colours['chic1_mu' ] = col[3]
colours['chic2_mu' ] = col[4]
colours['jpsi_hc'  ] = col[5]
colours['hc_mu'    ] = col[6]
colours['psi2s_mu' ] = col[7]
colours['psi2s_tau'] = col[8]
colours['jpsi_x_mu'] = col[9]
colours['fakes'   ] = col[10]
colours['data'     ] = ROOT.kBlack

