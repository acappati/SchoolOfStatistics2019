import ROOT
import os
import argparse



fIn      = ROOT.TFile("notebooks/data/Higgs_data.root")
tree_sig = fIn.Get("sig_tree")
tree_bkg = fIn.Get("bkg_tree")
fOut     = ROOT.TFile("notebooks/data/output.root","RECREATE")


ROOT.TMVA.Tools.Instance()

factory = ROOT.TMVA.Factory("TMVAClassification", fOut,":".join(["!V","Transformations=I;D;P;G,D","AnalysisType=Classification"]))

dataloader = ROOT.TMVA.DataLoader()


dataloader.AddVariable("lepton_pT", "F") # Both Float and Double variable types must be indicated as F
dataloader.AddVariable("lepton_eta","F")
dataloader.AddVariable("lepton_phi","F")
dataloader.AddVariable("jet1_pt",   "F")
dataloader.AddVariable("jet1_eta",  "F")
dataloader.AddVariable("jet1_btag", "F")
dataloader.AddVariable("jet2_pt",   "F")
dataloader.AddVariable("jet2_eta",  "F")
dataloader.AddVariable("jet2_btag", "F")
dataloader.AddVariable("m_jj",      "F")


sig_weight = 1.
bkg_weight = 1.

dataloader.AddSignalTree(tree_sig, sig_weight)
dataloader.AddBackgroundTree(tree_bkg, bkg_weight)

#dataloader.SetWeightExpression("weight")

# eventuali tagli (tipo mjj>8)
mycutSig = ROOT.TCut("")
mycutBkg = ROOT.TCut("")

#queste righe applicano il BDT
dataloader.PrepareTrainingAndTestTree(mycutSig, mycutBkg, ":".join(["!V","nTrain_Signal=0:nTrain_Background=0:nTest_Signal=0:nTest_Background=0"])) 
method_btd  = factory.BookMethod(dataloader, ROOT.TMVA.Types.kBDT, "BDT", ":".join(["H","!V","NTrees=800", "MinNodeSize=2.5%","MaxDepth=3","BoostType=AdaBoost","AdaBoostBeta=0.25","nCuts=20","NegWeightTreatment=IgnoreNegWeightsInTraining"]))


factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

fOut.Close()

weightfile_dir = "default/weights/TMVAClassification_BDT.weights.xml"

