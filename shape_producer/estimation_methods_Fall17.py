# -*- coding: utf-8 -*-

from cutstring import *
from estimation_methods import EstimationMethod, SStoOSEstimationMethod, ABCDEstimationMethod
from estimation_methods_2016 import DataEstimation as DataEstimation2016
from estimation_methods_2016 import WEstimationWithQCD as WEstimationWithQCD2016
from estimation_methods_2016 import QCDEstimationWithW as QCDEstimationWithW2016
from systematics import *
from era import log_query



def get_triggerweight_for_channel(channel):
    weight = Weight("1.0","triggerweight")
    if "mt" in channel:
        weight = Weight("((trg_singlemuon || trg_singlemuon_lowpt)*singleTriggerDataEfficiencyWeight_1*(1-trg_muontau_lowptmu*crossTriggerDataEfficiencyWeight_2)+trg_muontau_lowptmu*crossTriggerDataEfficiencyWeight_1*crossTriggerDataEfficiencyWeight_2)/((trg_singlemuon || trg_singlemuon_lowpt)*singleTriggerMCEfficiencyWeight_1*(1-trg_muontau_lowptmu*crossTriggerMCEfficiencyWeight_2)+trg_muontau_lowptmu*crossTriggerMCEfficiencyWeight_1*crossTriggerMCEfficiencyWeight_2)","triggerweight")
    elif "et" in channel:
        weight = Weight("((trg_singleelectron || trg_singleelectron_lowpt)*singleTriggerDataEfficiencyWeight_1*(1-trg_electrontau*crossTriggerDataEfficiencyWeight_2)+trg_electrontau*crossTriggerDataEfficiencyWeight_1*crossTriggerDataEfficiencyWeight_2)/((trg_singleelectron || trg_singleelectron_lowpt)*singleTriggerMCEfficiencyWeight_1*(1-trg_electrontau*crossTriggerMCEfficiencyWeight_2)+trg_electrontau*crossTriggerMCEfficiencyWeight_1*crossTriggerMCEfficiencyWeight_2)","triggerweight")
    elif "tt" in channel:
        weight = Weight("(crossTriggerDataEfficiencyWeight_1*crossTriggerDataEfficiencyWeight_2)/(crossTriggerMCEfficiencyWeight_1*crossTriggerMCEfficiencyWeight_2)","triggerweight")
    return weight

def get_singlelepton_triggerweight_for_channel(channel):
    weight = Weight("1.0","triggerweight")
    if "mt" in channel or "et" in channel:
        weight = Weight("singleTriggerDataEfficiencyWeight_1/singleTriggerMCEfficiencyWeight_1","triggerweight")
    elif "tt" in channel:
        weight = Weight("(crossTriggerDataEfficiencyWeight_1*crossTriggerDataEfficiencyWeight_2)/(crossTriggerMCEfficiencyWeight_1*crossTriggerMCEfficiencyWeight_2)","triggerweight")
    return weight

def get_tauByIsoIdWeight_for_channel(channel):
    # WPs: VLoose 0.85, Loose 0.89, Medium 0.89, Tight 0.87, VTight 0.85, VVTight 0.82. Currently used: SR mt,et Tight; SR tt Tight, anti-iso CR tt Loose
    weight = Weight("1.0","taubyIsoIdWeight")
    if "mt" in channel or "et" in channel:
        #weight = Weight("((gen_match_2 == 5)*(0.87*(rerunDiscriminationByIsolationMVAOldDMrun2v1Tight2017_2>0.5)+0.89*(rerunDiscriminationByIsolationMVAOldDMrun2v1Tight2017_2<0.5 && rerunDiscriminationByIsolationMVAOldDMrun2v1Loose2017_2>0.5)) + (gen_match_2 != 5))", "taubyIsoIdWeight")
        weight = Weight("((gen_match_2 == 5)*0.87 + (gen_match_2 != 5))", "taubyIsoIdWeight")
    elif "tt" in channel:
        weight = Weight("((gen_match_1 == 5)*(0.87*(rerunDiscriminationByIsolationMVAOldDMrun2v1Tight2017_1>0.5)+0.89*(rerunDiscriminationByIsolationMVAOldDMrun2v1Tight2017_1<0.5 && rerunDiscriminationByIsolationMVAOldDMrun2v1Loose2017_1>0.5)) + (gen_match_1 != 5))*((gen_match_2 == 5)*(0.87*(rerunDiscriminationByIsolationMVAOldDMrun2v1Tight2017_2>0.5)+0.89*(rerunDiscriminationByIsolationMVAOldDMrun2v1Tight2017_2<0.5 && rerunDiscriminationByIsolationMVAOldDMrun2v1Loose2017_2>0.5)) + (gen_match_2 != 5))", "taubyIsoIdWeight")
    return weight

def get_eleHLTZvtxWeight_for_channel(channel):
    weight = Weight("1.0","eleHLTZvtxWeight")
    if "et" in channel:
        weight = Weight("(trg_singleelectron || trg_singleelectron_lowpt || trg_electrontau)*0.991 + (!(trg_singleelectron || trg_singleelectron_lowpt || trg_electrontau))*1.0", "eleHLTZvtxWeight")
    return weight

class DataEstimation(DataEstimation2016):
    pass

class WEstimationWithQCD(WEstimationWithQCD2016):
    pass


class QCDEstimationWithW(QCDEstimationWithW2016):
    pass


class QCDEstimation_SStoOS_MTETEM(SStoOSEstimationMethod):
    def __init__(self,
                 era,
                 directory,
                 channel,
                 bg_processes,
                 data_process,
                 extrapolation_factor=1.0):
        super(QCDEstimation_SStoOS_MTETEM, self).__init__(
            name="QCD",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            bg_processes=bg_processes,
            data_process=data_process,
            extrapolation_factor=extrapolation_factor)


class QCDEstimation_ABCD_TT_ISO2(ABCDEstimationMethod):
    def __init__(self, era, directory, channel, bg_processes, data_process):
        super(QCDEstimation_ABCD_TT_ISO2, self).__init__(
            name="QCD",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            bg_processes=bg_processes,
            data_process=data_process,
            AC_cut_names=[ # cuts applied in AC, which should be removed in the BD control regions
                "tau_2_iso"
            ],
            BD_cuts=[      # cuts to be applied instead of cuts removed above
                Cut("rerunDiscriminationByIsolationMVAOldDMrun2v1Tight2017_2<0.5", "tau_2_iso"),
                #Cut("byMediumIsolationMVArun2v1DBoldDMwLT_2<0.5", "tau_2_iso"),
                Cut("rerunDiscriminationByIsolationMVAOldDMrun2v1Loose2017_2>0.5",
                    "tau_2_iso_loose")
            ],
            AB_cut_names=[ # cuts applied in AB, which should be removed in the CD control regions
                "os"
            ],
            CD_cuts=[      # cuts to be applied instead of cuts removed above
                Cut("q_1*q_2>0", "ss")
            ]
        )


class QCDEstimation_ABCD_TT_ISO2_TRANSPOSED(ABCDEstimationMethod):
    def __init__(self, era, directory, channel, bg_processes, data_process):
        super(QCDEstimation_ABCD_TT_ISO2_TRANSPOSED, self).__init__(
            name="QCD",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            bg_processes=bg_processes,
            data_process=data_process,
            AB_cut_names=[ # cuts applied in AB, which should be removed in the CD control regions
                "tau_2_iso"
            ],
            CD_cuts=[      # cuts to be applied instead of cuts removed above
                Cut("byTightIsolationMVArun2v1DBoldDMwLT_2<0.5", "tau_2_iso"),
                #Cut("byMediumIsolationMVArun2v1DBoldDMwLT_2<0.5", "tau_2_iso"),
                Cut("byLooseIsolationMVArun2v1DBoldDMwLT_2>0.5",
                    "tau_2_iso_loose")
            ],
            AC_cut_names=[ # cuts applied in AC, which should be removed in the BD control regions
                "os"
            ],
            BD_cuts=[      # cuts to be applied instead of cuts removed above
                Cut("q_1*q_2>0", "ss")
            ]
        )


class QCDEstimation_ABCD_TT_ISO1(ABCDEstimationMethod):
    def __init__(self, era, directory, channel, bg_processes, data_process):
        super(QCDEstimation_ABCD_TT_ISO1, self).__init__(
            name="QCD",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            bg_processes=bg_processes,
            data_process=data_process,
            AC_cut_names=[ # cuts applied in AC, which should be removed in the BD control regions
                "tau_1_iso"
            ],
            BD_cuts=[      # cuts to be applied instead of cuts removed above
                Cut("byTightIsolationMVArun2v1DBoldDMwLT_1<0.5", "tau_1_iso"),
                #Cut("byMediumIsolationMVArun2v1DBoldDMwLT_1<0.5", "tau_1_iso"),
                Cut("byLooseIsolationMVArun2v1DBoldDMwLT_1>0.5",
                    "tau_1_iso_loose")
            ],
            AB_cut_names=[ # cuts applied in AB, which should be removed in the CD control regions
                "os"
            ],
            CD_cuts=[      # cuts to be applied instead of cuts removed above
                Cut("q_1*q_2>0", "ss")
            ]
        )


class VVEstimation(EstimationMethod):
    def __init__(self, era, directory, channel):
        super(VVEstimation, self).__init__(
            name="VV",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            mc_campaign="RunIIFall17MiniAOD")

    def get_weights(self):
        return Weights(

            # MC related weights
            Weight("generatorWeight", "generatorWeight"),
            Weight("numberGeneratedEventsWeight",
                   "numberGeneratedEventsWeight"),
            Weight("crossSectionPerEventWeight", "crossSectionPerEventWeight"),

            # Weights for corrections
            #get_triggerweight_for_channel(self.channel.name),
            get_singlelepton_triggerweight_for_channel(self.channel.name),
            Weight("puweight", "puweight"),
            Weight("eleTauFakeRateWeight*muTauFakeRateWeight", "leptonTauFakeRateWeight"),
            get_tauByIsoIdWeight_for_channel(self.channel.name),
            get_eleHLTZvtxWeight_for_channel(self.channel.name),

            # Data related scale-factors
            self.era.lumi_weight)

    def get_files(self):
        query = {
            "process": "(WW|ZZ|WZ)",  # Query for Di-Boson samples
            "data": False,
            "generator": "^pythia8",
            "campaign": self._mc_campaign
        }
        files = self.era.datasets_helper.get_nicks_with_query(query)

        query = {
            "process": "ST",  # Query for Single-Top samples
            "data": False,
            "generator": "powheg\-pythia8",
            "campaign": self._mc_campaign
        }
        files += self.era.datasets_helper.get_nicks_with_query(query)

        log_query(self.name, query, files)
        return self.artus_file_names(files)


class EWKEstimation(EstimationMethod):
    def __init__(self, era, directory, channel, friend_directory=None):
        super(EWKEstimation, self).__init__(
            name="EWK",
            folder="nominal",
            era=era,
            directory=directory,
            friend_directory=friend_directory,
            channel=channel,
            mc_campaign="RunIIFall17MiniAOD")

    def get_weights(self):
        return Weights(

            # MC related weights
            Weight("generatorWeight", "generatorWeight"),
            Weight("numberGeneratedEventsWeight",
                   "numberGeneratedEventsWeight"),
            Weight("crossSectionPerEventWeight", "crossSectionPerEventWeight"),

            # Weights for corrections
            Weight("puweight", "puweight"),
            #get_triggerweight_for_channel(self.channel.name),
            get_singlelepton_triggerweight_for_channel(self.channel.name),
            Weight("eleTauFakeRateWeight*muTauFakeRateWeight", "leptonTauFakeRateWeight"),
            get_tauByIsoIdWeight_for_channel(self.channel.name),
            get_eleHLTZvtxWeight_for_channel(self.channel.name),

            # Data related scale-factors
            self.era.lumi_weight)

    def get_files(self):
        query = {
            "process": "^EWK",
            "data": False,
            "campaign": self._mc_campaign,
            "generator": "madgraph\-pythia8",
        }
        files = self.era.datasets_helper.get_nicks_with_query(query)

        log_query(self.name, query, files)
        return self.artus_file_names(files)


class DYJetsToLLEstimation(EstimationMethod):
    def __init__(self, era, directory, channel):
        super(DYJetsToLLEstimation, self).__init__(
            name="DYJetsToLL",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            mc_campaign="RunIIFall17MiniAOD")

    def get_weights(self):
        return Weights(

            # MC related weights
            Weight("generatorWeight", "generatorWeight"),
            #Weight("numberGeneratedEventsWeight","numberGeneratedEventsWeight"), # to be used only for one inclusive sample
            #Weight("crossSectionPerEventWeight","crossSectionPerEventWeight"), # to be used only for one inclusive sample
            Weight(
                "(((genbosonmass >= 50.0 && (npartons == 0 || npartons >= 4))*5.94801691e-05) + ((genbosonmass >= 50.0 && npartons == 1)*1.35840903e-05) + ((genbosonmass >= 50.0 && npartons == 2)*1.39144195e-05) + ((genbosonmass >= 50.0 && npartons == 3)*1.49539992e-05) + ((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight))",
                "z_stitching_weight"),

            # Weights for corrections
            Weight("puweight", "puweight"),
            #get_triggerweight_for_channel(self.channel._name),
            get_singlelepton_triggerweight_for_channel(self.channel.name),
            Weight("eleTauFakeRateWeight*muTauFakeRateWeight", "leptonTauFakeRateWeight"),
            get_tauByIsoIdWeight_for_channel(self.channel.name),
            get_eleHLTZvtxWeight_for_channel(self.channel.name),
            #Weight("zPtReweightWeight", "zPtReweightWeight"),

            # Data related scale-factors
            self.era.lumi_weight)

    def get_files(self):
        query = {
            "process": "(DYJetsToLL_M10to50|DY(1|2|3|)JetsToLL_M50)",
            #"process": "(DYJetsToLL_M10to50|DYJetsToLL_M50)",
            "data": False,
            "campaign": self._mc_campaign,
            "generator": "madgraph\-pythia8",
            #"extension": "^$",
            #"version": "v1" # to be used if only one inclusive sample is desired
        }
        files = self.era.datasets_helper.get_nicks_with_query(query)
        log_query(self.name, query, files)
        return self.artus_file_names(files)


class ZTTEstimation(DYJetsToLLEstimation):
    def __init__(self, era, directory, channel):
        super(DYJetsToLLEstimation, self).__init__(
            name="ZTT",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            mc_campaign="RunIIFall17MiniAOD")

    def get_cuts(self):

        ztt_genmatch_cut = Cut("1 == 1", "ztt_genmatch")
        if self.channel.name in ["mt", "et"]:
            ztt_genmatch_cut = Cut("gen_match_2==5", "ztt_genmatch")
        elif self.channel.name == "tt":
            ztt_genmatch_cut = Cut("(gen_match_1==5) && (gen_match_2==5)",
                                   "ztt_genmatch")
        elif self.channel.name == "em":
            ztt_genmatch_cut = Cut("(gen_match_1>2) && (gen_match_2>3)",
                                   "ztt_genmatch")
        return Cuts(ztt_genmatch_cut)


class ZLLEstimation(DYJetsToLLEstimation):
    def __init__(self, era, directory, channel):
        super(DYJetsToLLEstimation, self).__init__(
            name="ZLL",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            mc_campaign="RunIIFall17MiniAOD")

    def get_cuts(self):
        zll_genmatch_cut = Cut("1 == 1", "zll_genmatch")
        if self.channel.name in ["mt", "et"]:
            zll_genmatch_cut = Cut("gen_match_2!=5", "zll_genmatch")
        elif self.channel.name == "tt":
            zll_genmatch_cut = Cut("(gen_match_1!=5) || (gen_match_2!=5)",
                                   "zll_genmatch")
        elif self.channel.name == "em":
            zll_genmatch_cut = Cut("(gen_match_1<3) || (gen_match_2<4)",
                                   "zll_genmatch")
        return Cuts(zll_genmatch_cut)


class ZttEmbeddingEstimation(EstimationMethod):
    def __init__(self, era, directory, channel):
        super(ZttEmbeddingEstimation, self).__init__(
            name="Ztt",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            mc_campaign=None)

    def get_weights(self):
        return Weights(

            # MC related weights
            Weight("generatorWeight*(generatorWeight <= 1)",
                   "generatorWeight"),

            # Weights for corrections

            # Data related scale-factors
        )

    def get_files(self):
        query = {"process": "Embedding2017(B|C)", "embedded": True}
        #query = {"process" : "Embedding2017(B|C|D|E|F)", "embedded" : True}
        if self.channel.name == "mt":
            query["campaign"] = "MuTauFinalState"
        elif self.channel.name == "et":
            query["campaign"] = "ElTauFinalState"
        elif self.channel.name == "tt":
            query["campaign"] = "TauTauFinalState"
        elif self.channel.name == "em":
            query["campaign"] = "ElMuFinalState"
        files = self.era.datasets_helper.get_nicks_with_query(query)
        log_query(self.name, query, files)
        return self.artus_file_names(files)

    def get_cuts(self):
        ztt_genmatch_cut = Cut("1 == 1", "ztt_genmatch")
        if self.channel.name in ["mt", "et"]:
            ztt_genmatch_cut = Cut("gen_match_2==5", "ztt_genmatch")
        elif self.channel.name == "tt":
            ztt_genmatch_cut = Cut("(gen_match_1==5) && (gen_match_2==5)",
                                   "ztt_genmatch")
        elif self.channel.name == "em":
            ztt_genmatch_cut = Cut("(gen_match_1>2) && (gen_match_2>3)",
                                   "ztt_genmatch")
        return Cuts(ztt_genmatch_cut)


class ZttEmbeddingEstimation_ScaledToMC(EstimationMethod):
    def __init__(self, era, directory, channel, embedding_process,
                 ttbar_tautau_mc_process, z_tautau_mc_process):
        super(ZttEmbeddingEstimation_ScaledToMC, self).__init__(
            name="Ztt",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            mc_campaign=None)
        self._embedding_process = copy.deepcopy(embedding_process)
        self._ttbar_tautau_mc_process = copy.deepcopy(ttbar_tautau_mc_process)
        self._z_tautau_mc_process = copy.deepcopy(z_tautau_mc_process)

    def create_root_objects(self, systematic):
        yield_category = copy.deepcopy(systematic.category)
        yield_category._variable = None

        shape_category = copy.deepcopy(systematic.category)
        shape_category._name += "_unscaled"

        root_objects = []
        systematic._embedding_systematics = []
        shape_systematic = Systematic(
            category=shape_category,
            process=self._embedding_process,
            analysis=systematic.analysis,
            era=self.era,
            variation=systematic.variation,
            mass=125)
        systematic._embedding_systematics.append(shape_systematic)
        shape_systematic.create_root_objects()
        root_objects += shape_systematic.root_objects

        for process in [
                self._embedding_process, self._ttbar_tautau_mc_process,
                self._z_tautau_mc_process
        ]:
            s = Systematic(
                category=yield_category,
                process=process,
                analysis=systematic.analysis,
                era=self.era,
                variation=systematic.variation,
                mass=125)
            systematic._embedding_systematics.append(s)
            s.create_root_objects()
            root_objects += s.root_objects
        return root_objects

    def do_estimation(self, systematic):
        if not hasattr(systematic, "_embedding_systematics"):
            logger.fatal(
                "Systematic %s does not have attribute _embedding_systematics needed for embedding scaled to MC estimation.",
                systematic.name)
            raise Exception

        for s in systematic._embedding_systematics:
            s.do_estimation()

        shapes = [s.shape for s in systematic._embedding_systematics]

        # embedding shape
        embedding_shape = shapes[0]

        # scale factor = MC(TTT + ZTT) yield / embedding yield
        sf = (shapes[2].result + shapes[3].result) / shapes[1].result
        print "Scale factor", sf

        # scaling shape
        embedding_shape.result.Scale(sf)

        embedding_shape.name = systematic.name
        return embedding_shape


class WEstimation(EstimationMethod):
    def __init__(self, era, directory, channel):
        super(WEstimation, self).__init__(
            name="W",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            mc_campaign="RunIISummer17MiniAOD")

    def get_weights(self):
        return Weights(

            # MC related weights
            Weight("generatorWeight", "generatorWeight"),
            #Weight("numberGeneratedEventsWeight","numberGeneratedEventsWeight"), # to be used only for one inclusive sample
            #Weight("crossSectionPerEventWeight","crossSectionPerEventWeight"), # to be used only for one inclusive sample
            Weight(
                "(((npartons == 0 || npartons >= 5)*2.36006270e-3) + ((npartons == 1)*2.34817764e-4) + ((npartons == 2)*1.31144867e-4) + ((npartons == 3)*1.39177532e-4) + ((npartons == 4)*6.46064804e-5))",
                "wj_stitching_weight"),

            # Weights for corrections
            Weight("puweight", "puweight"),
            #get_triggerweight_for_channel(self.channel._name),
            get_singlelepton_triggerweight_for_channel(self.channel.name),
            Weight("eleTauFakeRateWeight*muTauFakeRateWeight", "leptonTauFakeRateWeight"),
            get_tauByIsoIdWeight_for_channel(self.channel.name),
            get_eleHLTZvtxWeight_for_channel(self.channel.name),

            # Data related scale-factors
            self.era.lumi_weight)

    def get_files(self):
        query = {
            "process": "W.?JetsToLNu",
            #"process": "WJetsToLNu",
            "data": False,
            "campaign": self._mc_campaign,
            "generator": "madgraph-pythia8"
        }
        files = self.era.datasets_helper.get_nicks_with_query(query)
        log_query(self.name, query, files)
        return self.artus_file_names(files)


class TTEstimation(EstimationMethod):
    def __init__(self, era, directory, channel):
        super(TTEstimation, self).__init__(
            name="TT",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            mc_campaign="RunIIFall17MiniAOD")

    def get_weights(self):
        return Weights(

            # MC related weights
            Weight("generatorWeight", "generatorWeight"),
            Weight("numberGeneratedEventsWeight",
                   "numberGeneratedEventsWeight"),
            Weight("crossSectionPerEventWeight", "crossSectionPerEventWeight"),
            #Weight("0.5", "tt_stitching_weight"),

            # Weights for corrections
            Weight("puweight", "puweight"),
            #get_triggerweight_for_channel(self.channel._name),
            get_singlelepton_triggerweight_for_channel(self.channel.name),
            Weight("eleTauFakeRateWeight*muTauFakeRateWeight", "leptonTauFakeRateWeight"),
            get_tauByIsoIdWeight_for_channel(self.channel.name),
            get_eleHLTZvtxWeight_for_channel(self.channel.name),
            #Weight("topPtReweightWeight", "topPtReweightWeight"),

            # Data related scale-factors
            self.era.lumi_weight)

    def get_files(self):
        query = {
            "process": "TTTo.*",
            "data": False,
            "campaign": self._mc_campaign,
            #"version": "v1" # to be used if only one inclusive sample is desired
        }
        files = self.era.datasets_helper.get_nicks_with_query(query)
        log_query(self.name, query, files)
        return self.artus_file_names(files)


class TTTEstimation(TTEstimation):
    def __init__(self, era, directory, channel):
        super(TTEstimation, self).__init__(
            name="TTT",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            mc_campaign="RunIIFall17MiniAOD")

    def get_cuts(self):
        return Cuts(
            Cut("(gen_match_1 > 2 && gen_match_1 < 6) && (gen_match_1 > 2 && gen_match_2 < 6)",
                "gen_match_genuine_taus"))


class TTJEstimation(TTEstimation):
    def __init__(self, era, directory, channel):
        super(TTEstimation, self).__init__(
            name="TTJ",
            folder="nominal",
            era=era,
            directory=directory,
            channel=channel,
            mc_campaign="RunIIFall17MiniAOD")

    def get_cuts(self):
        return Cuts(
            Cut("!(gen_match_1 > 2 && gen_match_1 < 6) && (gen_match_1 > 2 && gen_match_2 < 6)",
                "gen_match_genuine_taus"))