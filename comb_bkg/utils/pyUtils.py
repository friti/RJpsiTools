from ROOT import TFile, TTree, RooRealVar, RooArgSet, RooDataSet

def MakeRooDataSet(inputFileName, inputTreeName):
  '''
  Create a dataset from the BcTo2MuParticle
  it can accomodate different variables depending on the 
  decay reconstructed
  '''
  inputTreeName = 'BTo3Mu'
  inputFile = TFile.Open(inputFileName, "READ")
  tree = inputFile.Get(inputTreeName)

  jpsi_mass = RooRealVar("jpsi_mass", "jpsi_mass", 2., 4.)
  Q_sq = RooRealVar("Q_sq", "Q_sq", -10., 20.)

  dataArgSet = RooArgSet(jpsi_mass, Q_sq)

  #variables = (Q_sq)
  #for var in variables:
  #  dataArgSet.add(var)

  dataSet = RooDataSet("BcDataSet", "Bc RooDataSet", tree, dataArgSet)
  return dataSet
