from plottingTools import *
import ROOT

#in_file = ROOT.TFile.Open("data/tauTriggerFactorization2018-full.root")
in_file = ROOT.TFile.Open("data/tauTriggerFactorization2018-2D-v6.root")
WPs = ['vlooseTauMVA', 'looseTauMVA', 'mediumTauMVA', 'tightTauMVA', 'vtightTauMVA']
tauDMs = ['dm0', 'dm1', 'dm10']

#Parse arguments
import argparse

argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--isTH2',              action='store',         default=None)

args = argParser.parse_args()
histNames = ['inclusive']
for tau1DM in tauDMs:
    for tau2DM in tauDMs:
        histNames.append('tau1_'+tau1DM+'_tau2_'+tau2DM)


for h in histNames:
    for WP in WPs:
        triggeredHist_2D = in_file.Get('ditauTriggered_2D_'+WP+'_'+h)
        weightedHist_2D = in_file.Get("weightedDitau_2D_"+WP+"_"+h)
        denomHist_2D = in_file.Get("denomHists_2D_"+WP+"_"+h)
        triggeredHist_1D = in_file.Get('ditauTriggered_mass_'+WP+'_'+h)
        weightedHist_1D = in_file.Get("weightedDitau_mass_"+WP+"_"+h)
        denomHist_1D = in_file.Get("denomHists_mass_"+WP+"_"+h)

        triggeredHist_2D.Divide(denomHist_2D)
        weightedHist_2D.Divide(denomHist_2D)
        triggeredHist_1D.Divide(denomHist_1D)
        weightedHist_1D.Divide(denomHist_1D)

        destination = "/user/lwezenbe/CMSSW_10_2_13/src/TauTriggerTools/TauTagAndProbe/test/Factorization/Results/Factorization/HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v/"+WP+'_'+h
        
        draw2DHist(triggeredHist_2D, "p_{T}^{#tau_{1}} [GeV]", "p_{T}^{#tau_{2}} [GeV]", destination+"_2Dtriggered", option="EtextColz", x_log=False, y_log=False)
        draw2DHist(weightedHist_2D, "p_{T}^{#tau_{1}} [GeV]", "p_{T}^{#tau_{2}} [GeV]", destination+"_2Dweighted", option="EtextColz", x_log=False, y_log=False)
        ratio_hist_2D = weightedHist_2D.Clone("ratio plot 2D")
        ratio_hist_2D.Divide(triggeredHist_2D)
        draw2DHist(ratio_hist_2D, "p_{T}^{#tau_{1}} [GeV]", "p_{T}^{#tau_{2}} [GeV]", destination+"_2Dratio", option="EtextColz", x_log=False, y_log=False)
            
        plotClosure(triggeredHist_1D, weightedHist_1D, "M(#tau_{h}#tau_{h})", "Efficiency", "DYJets", destination, yLog = False)
