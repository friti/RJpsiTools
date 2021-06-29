import math
from utils.variable import variable
from utils.category import category
from utils.selections import preselection, pass_id
from utils.plotting import *

#from utils.pyUtils import MakeRooDataSet as makeds
from utils.cmsstyle import CMS_lumi
import ROOT
from ROOT import gSystem, gROOT, gStyle
from ROOT import TFile, TCanvas, TLegend, TH1F, TF1, TProfile, TVector3
from root_pandas import read_root
from uproot_methods import TLorentzVectorArray, TVector3Array
from uproot_methods import TLorentzVector
import yaml
import numpy as np
import pandas as pd
import os

gStyle.SetOptStat(0)
dir_plots = 'plots/combinatorial_bkg'
dir_results = 'results/combinatorial_bkg'


def get_df_mass_scaled(cat_source, cat_target, correction=0):
  BC_MASS_PDG = 6.2756
  source_df = cat_source.get_df().copy()

  if correction==1:
    width_normal = 0.028
    dimuon_mass_scaled = np.random.normal(cat_target.get_mass_mean(), width_normal, source_df.jpsi_mass.size)
  elif correction==2:
    width_uniform = (cat_target.get_mass_range()[1] - cat_target.get_mass_range()[0])/math.sqrt(12)
    dimuon_mass_scaled = np.random.uniform(cat_target.get_mass_mean()- width_uniform, cat_target.get_mass_mean() + width_uniform, source_df.jpsi_mass.size)
  else:
    dimuon_mass_scaled = cat_target.get_mass_mean()

  dimuon_p4 = TLorentzVectorArray.from_ptetaphim(source_df.jpsi_pt,
                                                   source_df.jpsi_eta,
                                                   source_df.jpsi_phi,
                                                   dimuon_mass_scaled)

  mu1_p4 = TLorentzVectorArray.from_ptetaphim(source_df.mu1pt,
                                              source_df.mu1eta,
                                              source_df.mu1phi,
                                              source_df.mu1mass)

  mu2_p4 = TLorentzVectorArray.from_ptetaphim(source_df.mu2pt,
                                              source_df.mu2eta,
                                              source_df.mu2phi,
                                              source_df.mu2mass)

  k_p4 = TLorentzVectorArray.from_ptetaphim(source_df.kpt,
                                              source_df.keta,
                                              source_df.kphi,
                                              source_df.kmass)
  '''
  b_p3 = TVector3.from_cartesian(source_df.beamspot_x - source_df.bvtx_vtx_x,
                                  source_df.beamspot_y - source_df.bvtx_vtx_y,
                                  source_df.pv_z - source_df.bvtx_vt_z)
  b_eta =  []
  b_phi = []
  for index, entry in source_df.iterrows():
    b_p3 = TVector3(entry.bvtx_vtx_x - entry.beamspot_x, entry.bvtx_vtx_y - entry.beamspot_y, entry.bvtx_vtx_z - entry.pv_z)
    b_phi.append(b_p3.Phi())
    b_eta.append(b_p3.Eta())

  b_ori_p4 = k_p4 + dimuon_p4
  b_p4 = TLorentzVectorArray.from_ptetaphim(b_ori_p4.pt,
                                            b_eta,
                                            b_phi,
                                            BC_MASS_PDG)

  '''
  b_p4 = k_p4 + dimuon_p4
  b_p4_scaled = TLorentzVectorArray.from_ptetaphim(BC_MASS_PDG*np.divide(b_p4.pt, b_p4.mass),
                                                        b_p4.eta,
                                                        b_p4.phi,
                                                        BC_MASS_PDG)
  df_scaled = pd.DataFrame()
  df_scaled = pd.DataFrame()
  df_scaled['Q_sq'] = (b_p4_scaled - dimuon_p4).mag2
  df_scaled['m_miss_sq'] = (b_p4_scaled - k_p4 - dimuon_p4).mag2
  df_scaled['pt_miss'] = b_p4_scaled.pt - k_p4.pt - dimuon_p4.pt
  df_scaled['pt_miss_vec'] = (b_p4_scaled - k_p4 - dimuon_p4).pt
  df_scaled['pt_var'] = dimuon_p4.pt - k_p4.pt

  mu3_p4 = k_p4.copy()
  mu3_p4_boosted = mu3_p4.boost(-b_p4.boostp3)
  df_scaled['E_mu_star'] = mu3_p4_boosted.fE
  # print(k_p4[0])



  #TODO: Add the rest of the variables.

  return df_scaled

def readIntervalsFromFile():
  '''
  Reads the yaml file with the information from the fit.
  '''
  try:
    with open('%s/sideBandsIntervals.yaml' % (dir_results)) as f:
      intervals=yaml.full_load(f)
      return intervals
  except FileNotFoundError:
    print('sideBandsInterval.yaml not found')
  return None

def get_cat_pol1_fit_params(df, var_x, var_y):
  c = TCanvas("","",800, 800)
  prof = TProfile("prof", "", var_x.nbins, var_x.xmin, var_x.xmax, var_y.xmin, var_y.xmax)
  for var_x_val, var_y_val in zip(df[var_x.name],df[var_y.name]) :
    prof.Fill(var_x_val, var_y_val,1)

  myPol = TF1("myPol", "[0]+[1]*x", var_x.xmin, var_x.xmax)
  fit_res = prof.Fit("myPol","W").Get()
  prof.Draw()
  CMS_lumi(c, 4, 0)
  #c.SaveAs("%s/dimuon_mass_%3.1f_%3.1f_vs_q_sq_profile.pdf" % (dir_plots, var_x.xmin, var_x.xmax))
  c.SaveAs("%s/dimuon_mass_%3.1f_%3.1f_vs_q_sq_profile.png" % (dir_plots, var_x.xmin, var_x.xmax))
  return myPol.GetParameter(0), myPol.GetParameter(1)


def get_sb_fit_params(categories, vars_x, vars_y):
  '''
  Takes the two categories of the side bands,
  does fit in the two region and extrapolates
  a line that joins the upper limit of the lsb
  and the lower limit of the rsb with line and
  issues the the parameter of the three lines
  '''
  fit_params = []
  for cat, var_x, var_y in zip(categories, vars_x, vars_y):
    fit_params.append(get_cat_pol1_fit_params(cat.get_df(), var_x, var_y))

  x1 = vars_x[0].xmax
  x2 = vars_x[1].xmin
  x_r = x1/x2

  b1 = fit_params[0][0]
  m1 = fit_params[0][1]


  b3 = fit_params[1][0]
  m3 = fit_params[1][1]


  b2 = (b1 + b3)/2.#(m1*x1 + b1 - x_r * (m3*x2 + b3))/(1 - x_r)
  m2 = (m1 + m3)/2.#(m1*x1 + b1 -b2)/x1

  return m1 ,b1 , m2, b2, m3, b3

def gaus_pol_fit(histo, var,plt_name="", path="", ps=[None,None,None,None,None,None], pol="pol1"):
  '''
  Perform a fit with a gaussian for the resonance and
  a exponential or a polynomial as background
  '''
  c = TCanvas("","",800, 800)
  func= TF1("model", "gaus(0) +"+ pol + "(3)", var.xmin, var.xmax)
  for i,p in enumerate(ps):
    if(p!=None):
      func.SetParameter(i,p)
  for i in range(1, histo.GetNbinsX()+1):
    histo.SetBinError(i, math.sqrt(histo.GetBinContent(i)))
  fit_result = histo.Fit(func, "S")
  histo.Draw()
  CMS_lumi(c, 4, 0)
  #c.SetLogy()
  #c.SaveAs("%s/dimuon_mass_fit.pdf" % (dir_plots))
  c.SaveAs("%s/dimuon_mass_fit.png" % (dir_plots))
  #c.Draw()
  return fit_result

def get_int_gaus_pol(fit_result, minVal, maxVal, nBins):
  '''
  Get the integral of a gaussian plus a polynomial
  '''
  gaus = TF1("gaus","gaus(0)")
  pol = TF1("pol", "pol1(0)")
  gaus.SetParameter(0, fit_result.Parameter(0))
  gaus.SetParameter(1, fit_result.Parameter(1))
  gaus.SetParameter(2, fit_result.Parameter(2))
  pol.SetParameter(0, fit_result.Parameter(3))
  pol.SetParameter(1,fit_result.Parameter(4))
  normVal = (maxVal - minVal)/nBins
  gaus_int = gaus.Integral(minVal, maxVal)/normVal
  pol_int = pol.Integral(minVal, maxVal)/normVal
  return gaus_int, pol_int

def getSBIntervals(cat):
  '''
  Get the interval of the side bands (SB)
  making a fit of the invariant mass of the
  dimuon invariant mass.
  The SB will be defined based on the mean and
  the sigma of the fit of the resonance
  '''
  #var = variable("jpsi_mass", "m(2#mu)", "m(2#mu)", "[GeV]", 40, 2.97, 3.23)
  var = variable("jpsi_mass", "m(2#mu)", "m(2#mu)", "[GeV]", 40, 2.95, 3.25)
  histoName = "jpsi_mass"
  massHisto, massHisto_int = createHisto(cat.get_df(), histoName, var, 1, False)
  fit_result = gaus_pol_fit(massHisto, var, "Dimuon invariant mass","", [None,3.1,.2,None,None,None], "pol1")
  var_m = fit_result.Parameter(1) #jpsi mass mean
  var_s = fit_result.Parameter(2) #jpsi mass sigma

  ls = 3.0 # lower number of sigmas from the mean
  us = 8.0 # upper number of sigmas from the mean

  intervals = {'lsb':{'minVal': var_m - us*var_s , 'maxVal':var_m - ls*var_s}, 'rsb':{'minVal': var_m + ls*var_s, 'maxVal':var_m+ us*var_s}}
  fit_integrals = get_int_gaus_pol(fit_result, intervals['lsb']['maxVal'], intervals['rsb']['minVal'], massHisto.GetNbinsX())
  with open('%s/sideBandsIntervals.yaml' % (dir_results), 'w') as f:
    yaml.dump(intervals, f)
  return intervals, fit_integrals

def saveHistos(cat, variables):
  f = TFile(dir_results+'/'+cat.get_name()+'.root', 'recreate')
  f.cd()
  for var in variables:
    massHisto, massHisto_int = createHisto(cat.get_df(), var.name, var, 1, False)
    massHisto.Write()
  f.Write()
  f.Close()
  return

  

def make_scaling(cats_source, cat_target, variables, prefix='', seed =0):
  dfs = []
  cats_extrapolated = []
  for i, cat in enumerate(cats_source):
    dfs.append(get_df_mass_scaled(cat, cat_target, 0))
    cats_extrapolated.append(category("region_extrapolated_from_region_%d"%(i), dfs[i], None, None,
                                 "region extrapolated from %d"%(i),
                                 ROOT.kOrange + 2, ROOT.kFullCircle, 1.0)
                            )

  all_extrapolated_df = pd.concat(dfs)
  all_extrapolated = category(cat_target.get_name()+"_extrapolated", all_extrapolated_df, None, None,"Extrapolated",
                                 ROOT.kGray + 1 , ROOT.kFullCircle, 1.0)

  cats_result = [all_extrapolated,cat_target]
  plotPull(cats_result, variables, prefix + "_pull", True)

  saveHistos(all_extrapolated, variables)

  plotComparisonByCats(cats_result, variables, prefix, True)
  plotComparisonByCats(cats_result+cats_source, variables, prefix + '_all', True)
  return all_extrapolated

def scaling_comparison(cats_source, cat_target, variables, prefix='', seed=0):
  dfs_constant = []
  dfs_normal = []
  dfs_uniform = []
  for i, cat in enumerate(cats_source):
    dfs_constant.append(get_df_mass_scaled(cat, cat_target,0))
    dfs_normal.append(get_df_mass_scaled(cat, cat_target,1))
    dfs_uniform.append(get_df_mass_scaled(cat, cat_target,2))

  all_constant_df = pd.concat(dfs_constant)
  all_normal_df = pd.concat(dfs_normal)
  all_uniform_df = pd.concat(dfs_uniform)


  cat_extrapolated_constant = category("extrapolated_constant_dimuon_mass", all_constant_df,
                                        None, None, "extrapolated dimuon_mass constant",
                                        ROOT.kBlack, ROOT.kFullCircle, 1.0)
  cat_extrapolated_normal = category("extrapolated_normal_dimuon_mass", all_normal_df,
                                        None, None, "extrapolated dimuon_mass normal",
                                        ROOT.kRed, ROOT.kFullCircle, 1.0)
  cat_extrapolated_uniform = category("extrapolated_uniform_dimuon_mass", all_uniform_df,
                                        None, None, "extrapolated dimuon_mass uniform",
                                        ROOT.kSpring + 2, ROOT.kFullCircle, 1.0)

  all_cats = [cat_target, cat_extrapolated_constant, cat_extrapolated_normal, cat_extrapolated_uniform]

  plotComparisonByCats(all_cats, variables, prefix, True)

  cats_pull_constant = [cat_extrapolated_constant,cat_target]
  plotPull(cats_pull_constant, variables, prefix + "_constant", True)

  cats_pull_normal = [cat_extrapolated_normal,cat_target]
  plotPull(cats_pull_normal, variables, prefix + "_normal", True)

  cats_pull_uniform = [cat_extrapolated_uniform,cat_target]
  plotPull(cats_pull_uniform, variables, prefix + "_uniform", True)


def main():
  force_fit = True
  if (os.path.exists(dir_plots) and os.path.isdir(dir_plots)): 
    print("%s directory alredy exist" % dir_plots)
  else:
    print("Making %s directory"% dir_plots)
    os.system("mkdir -p %s"%(dir_plots))

  if (os.path.exists(dir_results) and os.path.isdir(dir_results)): 
    print("%s directory alredy exist" % dir_results)
  else:
    print("Making %s directory"% dir_results)
    os.system("mkdir -p %s"%(dir_results))
  inputFile = '/Users/garamire/Work/RJPsi/pyrk/scripts/dataframes_local/data_ptmax_merged.root'
  inputFile_lm = '/Users/garamire/Work/RJPsi/pyrk/scripts/dataframes_local/datalowmass_ptmax_merged.root'
  inputFile_mc_bkg = '/Users/garamire/Work/RJPsi/pyrk/scripts/dataframes_local/2021Mar25/HbToJPsiMuMu_ptmax_merged.root'
  inputTree = 'BTo3Mu'
  common_cuts=" & ".join([ preselection, pass_id])
  data_df = read_root(inputFile, inputTree)
  data_df = data_df.query(common_cuts).copy()
  data_lm_df = read_root(inputFile_lm, inputTree)
  data_lm_df = data_lm_df.query(common_cuts).copy()
  mc_bkg = read_root(inputFile_mc_bkg, inputTree)
  
  cat_psi2s_lsb_1 = category("psi2s_lsb_1", data_df, "trigger_psiprime_alone", [3.4,3.5], "Source region I", ROOT.kSpring + 1, ROOT.kOpenCircle, 1.0)
  cat_psi2s_lsb_2 = category("psi2s_lsb_2",data_df, "trigger_psiprime_alone", [3.5,3.6], "Target region", ROOT.kPink + 1, ROOT.kOpenCircle, 1.0)
  cat_psi2s_lsb_3 = category("psi2s_lsb_3", data_df, "trigger_psiprime_alone", [3.6,3.7], "Source region II", ROOT.kAzure + 1, ROOT.kOpenCircle, 1.0)
  cat_jpsi_lsb = category("jpsi_lsb", data_lm_df, "trigger_nonresonant_alone", [2.5,2.85], "Source region I", ROOT.kCyan + 1, ROOT.kOpenCircle, 1.0)
  cat_jpsi_res = category("jpsi_res", data_df, "trigger_jpsitrk_alone", [2.95,3.25], "Target region", ROOT.kOrange + 2, ROOT.kOpenCircle, 1.0)
  cat_jpsi_rsb = category("jpsi_rsb", data_df, "trigger_psiprime_alone", [3.3,3.45], "Source region II", ROOT.kPink + 1, ROOT.kOpenCircle, 1.0)
  cat_jpsi_lsb_1 = category("jpsi_lsb_1", data_lm_df, "trigger_nonresonant_alone", [2.5,2.6], "Source region I", ROOT.kGreen + 1, ROOT.kOpenCircle, 1.0)
  cat_jpsi_lsb_2 = category("jpsi_lsb_2", data_lm_df, "trigger_nonresonant_alone", [2.68,2.72], "Target region", ROOT.kBlue + 1 , ROOT.kOpenCircle, 1.0)
  cat_jpsi_lsb_3 = category("jpsi_lsb_3", data_lm_df, "trigger_nonresonant_alone", [2.8,2.9], "Source region II", ROOT.kRed + 1, ROOT.kOpenCircle, 1.0)
  cat_mc_1 = category("mc_1", data_df, "trigger_dimuon0_alone", [2.95,3.08], "Source region I",  ROOT.kSpring + 1, ROOT.kOpenCircle, 1.0)
  cat_mc_2 = category("mc_2",data_df, "trigger_dimuon0_alone", [3.08,3.11], "Target region", ROOT.kPink + 1, ROOT.kOpenCircle, 1.0)
  cat_mc_3 = category("mc_3", data_df, "trigger_dimuon0_alone", [3.11,3.23], "Source region II", ROOT.kAzure + 1, ROOT.kOpenCircle, 1.0)
  
  var_list = [
    variable("Q_sq", "Q^{2}", "Q^{2}", "GeV^{2}", 24, 0., 14.),
    variable("m_miss_sq", "m_{miss}^{2}", "m_{miss}^{2}", "GeV^{2}", 30, 0., 10.),
    variable("pt_var", "pt_var", "pt_var", "GeV", 25, 0., 50.),
    variable("E_mu_star", "E^{*}", "E^{*}", "GeV", 30, 0., 3.),
    ]
  
  var_jpsi_lsb_mass = [variable("jpsi_mass", "m(#mu^{+}#mu^{-})", "m(#mu^{+}#mu^{-})", "[GeV]", 40, 2.45, 2.95)]
  var_jpsi_mass = [variable("jpsi_mass", "m(#mu^{+}#mu^{-})", "m(#mu^{+}#mu^{-})", "[GeV]", 40, 2.45, 3.3)]
  var_psi2s_lsb_mass = [variable("jpsi_mass", "m(#mu^{+}#mu^{-})", "m(#mu^{+}#mu^{-})", "[GeV]", 40, 3.35, 3.75)]
  var_mc_mass = [variable("jpsi_mass", "m(#mu^{+}#mu^{-})", "m(#mu^{+}#mu^{-})", "[GeV]", 40, 2.9, 3.3)]
  
  #Psi2s
  cat_allmass = [cat_psi2s_lsb_1, cat_psi2s_lsb_2, cat_psi2s_lsb_3]
  plotComparisonByCats(cat_allmass, var_list, "psi2s_nonModified_all", True)
  plotComparisonByCats(cat_allmass, var_psi2s_lsb_mass, "psi2s_nonModified_all", True)
  cats_psi2s_lsb = [cat_psi2s_lsb_1, cat_psi2s_lsb_3]
  make_scaling(cats_psi2s_lsb, cat_psi2s_lsb_2, var_list, "psi2s_scaling_lsb",0.0)
  
  #jpsi lsb
  cat_allmass_jpsi_lsb = [cat_jpsi_lsb_1, cat_jpsi_lsb_2, cat_jpsi_lsb_3]
  #plotComparisonByCats(cat_allmass_jpsi, var_list, "jpsi_nonModified_all", True)
  plotComparisonByCats(cat_allmass_jpsi_lsb, var_jpsi_lsb_mass, "jpsi_lsb_nonModified", False)
  cats_jpsi_lsb = [cat_jpsi_lsb_1, cat_jpsi_lsb_3]
  test_extrapolated = make_scaling(cats_jpsi_lsb, cat_jpsi_lsb_2, var_list, "jpsi_lsb_scaling", 0.0)
  scaling_comparison(cats_jpsi_lsb, cat_jpsi_lsb_2, var_list, 'jpsi_lsb_scalings_comparison', 0)
  
  #jpsi lsb
  cat_allmass_jpsi = [cat_jpsi_lsb, cat_jpsi_res]
  #plotComparisonByCats(cat_allmass_jpsi, var_list, "jpsi_nonModified_all", True)
  plotComparisonByCats(cat_allmass_jpsi, var_jpsi_lsb_mass, "jpsi_nonModified", False)
  #cats_jpsi_lsb = [cat_jpsi_lsb]
  test_extrapolated = make_scaling([cat_jpsi_lsb], cat_jpsi_res, var_list, "jpsi_scaling", 0.0)
  scaling_comparison([cat_jpsi_lsb], cat_jpsi_res, var_list, 'jpsi_scalings_comparison', 0)
  
  getSBIntervals(cat_jpsi_res)
  
  #MC
  #cats_mc = [cat_mc_1, cat_mc_3]
  #make_scaling(cats_mc, cat_mc_2, var_list, "mc_HbToJPsi_scaling" 0.0)
  
  '''
  import time
  Q_sq_var = variable("Q_sq", "Q^{2}", "Q^{2}", "GeV^{2}", 24, 0., 14.)
  histo_list = []
  for i in range(Q_sq_var.nbins):
    histo_list.append(TH1F("bin_%d"%(i),"",100, 0.8,1.2))
  
  histo_target, histo_target_int = createHisto(cat_jpsi_lsb_2.get_df(), "", Q_sq_var, 1, False)
  histo_target.Scale(1.0/histo_target_int)
  init_time = time.time()
  for s in seed:
    #print(s)
    test_extrapolated = make_scaling(cats_jpsi_lsb, cat_jpsi_lsb_2, var_list,s)
    histo, histo_int = createHisto(test_extrapolated.get_df(), "", Q_sq_var, 1, False)
    histo.Scale(1./histo_int)
    histo.Divide(histo_target)
    print(histo.GetBinContent(12))
    for i in range(Q_sq_var.nbins):
      #print(histo.GetBinContent(i+1))
      histo_list[i].Fill(histo.GetBinContent(i+1))
  canv = TCanvas("","",800, 800)
  CMS_lumi(canv, 0, 0)
  for i in range(Q_sq_var.nbins):
    
    histo_list[i].Draw()
    canv.SaveAs("%s/test_bin_%d_content.png" % (dir_plots,i))
  
  end_time = time.time()
  
  print("time for scaling: %5.3f" % (end_time - init_time))
  '''

if __name__ == '__main__':
  gROOT.SetBatch()
  gStyle.SetOptStat(0)
  main()
