import ROOT
import os

fIn = ROOT.TFile("Higgs_data.root")
tree_bkg = fIn.Get("bkg_tree")
tree_sig = fIn.Get("sig_tree")
fOut = ROOT.TFile("myBDToutput.root","RECREATE")

ROOT.TMVA.Tools.Instance()

factory = ROOT.TMVA.Factory("TMVAClassification", fOut,":".join(["!V","Transformations=I;D;P;G,D","AnalysisType=Classification"]))

dataloader = ROOT.TMVA.DataLoader()


# Both Float and Double variable types must be indicated as F
dataloader.AddVariable("lepton_pT","F")
# dataloader.AddVariable("lepton_eta","F") # 15
# dataloader.AddVariable("lepton_phi","F") # 15
dataloader.AddVariable("missing_energy_magnitude","F") # 15
# dataloader.AddVariable("missing_energy_phi","F") # 15
dataloader.AddVariable("jet1_pt","F")
# dataloader.AddVariable("jet1_eta","F") # 15
# dataloader.AddVariable("jet1_phi","F") # 15
# dataloader.AddVariable("jet1_btag","F") # 10
dataloader.AddVariable("jet2_pt","F")
# dataloader.AddVariable("jet2_eta","F") # 15
# dataloader.AddVariable("jet2_phi","F") # 15
# dataloader.AddVariable("jet2_btag","F") # 15
# dataloader.AddVariable("jet3_pt","F") # 10
# dataloader.AddVariable("jet3_eta","F") # 10
# dataloader.AddVariable("jet3_phi","F") # 15
# dataloader.AddVariable("jet3_btag","F") # 15
# dataloader.AddVariable("jet4_pt","F") # 10
# dataloader.AddVariable("jet4_eta","F") # 15
# dataloader.AddVariable("jet4_phi","F") # 15
# dataloader.AddVariable("jet4_btag","F") # 15
# dataloader.AddVariable("m_jj","F") # corr 2 # 9
dataloader.AddVariable("m_jjj","F")
# dataloader.AddVariable("m_lv","F") # 10
dataloader.AddVariable("m_jlv","F")
dataloader.AddVariable("m_bb","F")
dataloader.AddVariable("m_wbb","F") # corr 1
dataloader.AddVariable("m_wwbb","F") 

sig_weight = 1.
bkg_weight = 1.

dataloader.AddSignalTree(tree_sig, sig_weight)
dataloader.AddBackgroundTree(tree_bkg, bkg_weight)

# dataloader.SetWeightExpression("weight")

mycutSig = ROOT.TCut("")
mycutBkg = ROOT.TCut("")

dataloader.PrepareTrainingAndTestTree(mycutSig, mycutBkg, ":".join(["!V","nTrain_Signal=7000:nTrain_Background=7000:nTest_Signal=0:nTest_Background=0"]))

method_btd  = factory.BookMethod(dataloader, ROOT.TMVA.Types.kBDT, "BDT", ":".join(["H","!V","NTrees=500", "MinNodeSize=2.5%","MaxDepth=3","BoostType=AdaBoost","AdaBoostBeta=0.4","nCuts=30","NegWeightTreatment=IgnoreNegWeightsInTraining"]))

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

fOut.Close()

weightfile_dir = "TMVAClassification_BDT.weights.xml"
