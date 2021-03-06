selection = ' & '.join([
    'mu1pt>4',
    'mu2pt>4',
    'kpt>2.5',
    'abs(mu1eta)<2.5',
    'abs(mu2eta)<2.5',
    'abs(keta)<2.5',
    'bvtx_svprob>1e-4',
    'jpsivtx_svprob>1e-2',
    'Bmass<6.3',
    'mu1_mediumID>0.5',
    'mu2_mediumID>0.5',
    'Bpt_reco>15',
    'dr12>0.01',
    'dr13>0.01',
    'dr23>0.01',
    'abs(mu1_dz-mu2_dz)<0.2',
    'abs(mu1_dz-k_dz)<0.2',
    'abs(mu2_dz-k_dz)<0.2',
    'abs(k_dxy)<0.05',
    'abs(mu1_dxy)<0.05',
    'abs(mu2_dxy)<0.05',
    'bvtx_cos2D>0.995',
    'abs(jpsi_mass-3.0969)<0.1',
    'mmm_p4_par>10',
    'mu1_isFromMuT',
    'mu2_isFromMuT',
    'mu1_isFromJpsi_MuT',
    'mu2_isFromJpsi_MuT',
    'k_isFromMuT',
])
pass_id = 'k_mediumID>0.5'
fail_id = '(!(k_mediumID>0.5))'
