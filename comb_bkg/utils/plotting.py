import ROOT
from ROOT import TLegend, TCanvas, TH1F
from ROOT import gStyle

from utils.variable import variable
from utils.category import category
from utils.cmsstyle import CMS_lumi

gStyle.SetOptStat(0)
dir_plots = 'plots/combinatorial_bkg'
dir_results = 'results/combinatorial_bkg'

def createHisto(df, histoName, var, norm=1, over=True):
  '''
  Make a histogram form a dataframe
  '''
  histo  = TH1F(histoName, "", var.nbins, var.xmin, var.xmax)
  for varVal in df[var.name]:
    histo.Fill(varVal)
  if(over):
    histo.SetBinContent(1, histo.GetBinContent(0) + histo.GetBinContent(1))
    histo.SetBinError(1, math.sqrt(pow(histo.GetBinError(0), 2) + pow(histo.GetBinError(1), 2)))
    histo.SetBinContent(var.nbins, histo.GetBinContent(var.nbins) + histo.GetBinContent(var.nbins+1))
    histo.SetBinError(var.nbins, math.sqrt(pow(histo.GetBinError(var.nbins), 2) + pow(histo.GetBinError(var.nbins+1), 2)))
  hist_int = histo.Integral()
  return histo, hist_int

def plotComparisonByCats(categories, variables, prefix, normalize=True):
  for var in variables:
    legend = TLegend(0.12, 0.75, 0.49, 0.86)
    c1 = TCanvas("","",800, 800)

    histos = [createHisto(cat.get_df(), cat.get_name(), var, 1, False) for cat in categories]
    #maxValHisto = 0
    for histo, cat in zip(histos, categories):
      legend.AddEntry(histo[0], cat.get_legend(), "lp")
      if(normalize):
        histo[0].Scale(1./histo[1])
      else:
        histo[0].Scale(cat.get_weight())
      #if(maxValHisto < histo[0].GetMaximum()):
      maxValHisto = histo[0].GetMaximum()
      histo[0].SetLineColor(cat.get_color())
      #histo[0].SetMarkerStyle(cat.get_marker)
      #histo[0].SetMarkerColor(cat.get_color)
      histo[0].SetLineWidth(2)
      histo[0].GetYaxis().SetTitle("a.u.")
      histo[0].GetXaxis().SetTitle("%s [%s]" % (var.xlabel, var.unit))
      histo[0].SetMaximum(1.5 * maxValHisto)
      #histo[0].DrawNormalized("same hist")
      histo[0].Draw("same hist")
    legend.SetTextFont(43)
    legend.SetTextSize(15)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.Draw("SAME")
    #c1.SetLogy(1)
    CMS_lumi(c1, 0, 0)
    #c1.SaveAs("%s/%s_%s.pdf" % (dir_plots, prefix, var.name))
    c1.SaveAs("%s/%s_%s.png" % (dir_plots, prefix, var.name))
    del c1, legend, histos

def plotPull(cats, variables, prefix, normalize):
  for var in variables:
    c1 = TCanvas("","",800, 800)
    histos = [createHisto(cat.get_df(), cat.get_name(), var, 1, False) for cat in cats]

    if(normalize):
      histos[0][0].Scale(1./histos[0][1])
      histos[1][0].Scale(1./histos[1][1])
    else:
      histos[0][0].Scale(cat.get_weight())
      histos[1][0].Scale(cat.get_weight())
    #maxValHisto = histo[0].GetMaximum()
    histos[0][0].SetLineColor(cats[0].get_color())
    histos[0][0].SetMarkerStyle(cats[0].get_marker())
    histos[0][0].SetMarkerColor(cats[0].get_color())
