trigger_dimuon0 = "mu1_isFromMuT & mu2_isFromMuT & k_isFromMuT"
trigger_psiprime = "mu1_isFromTrkPsiPT & mu2_isFromTrkPsiPT & k_isFromTrkPsiPT"
trigger_jpsitrk = "mu1_isFromTrkT & mu2_isFromTrkT & k_isFromTrkT"
trigger_nonresonant =  "mu1_isFromTrkNResT & mu2_isFromTrkNResT & k_isFromTrkNResT"
trigger_dict = {
  "trigger_dimuon0": trigger_dimuon0,
  "trigger_psiprime" : trigger_psiprime,
  "trigger_jpsitrk": trigger_jpsitrk,
  "trigger_nonresonant" : trigger_nonresonant,
  "trigger_dimuon0_alone" : "%s and not ( %s or %s or %s)" % (trigger_dimuon0 , 
                                                            trigger_psiprime, 
                                                            trigger_jpsitrk, 
                                                            trigger_nonresonant),
  "trigger_psiprime_alone" : "%s and not ( %s or %s or %s)" % (trigger_psiprime, 
                                                            trigger_dimuon0 , 
                                                             trigger_jpsitrk, 
                                                             trigger_nonresonant),
  "trigger_jpsitrk_alone" :"%s and not ( %s or %s or %s)" % (trigger_jpsitrk, 
                                                             trigger_dimuon0 , 
                                                             trigger_psiprime, 
                                                             trigger_nonresonant),
  "trigger_nonresonant_alone" : "%s and not ( %s or %s or %s)" % (trigger_nonresonant, 
                                                             trigger_dimuon0 , 
                                                             trigger_psiprime, 
                                                             trigger_jpsitrk)
}