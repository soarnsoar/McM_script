import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM
from json import dumps
import os





#request_prepid_to_clone
#fragment
#dataset_name
#notes
#total_events
def clone_and_edit_jhchoi(request_prepid_to_clone,fragment, dataset_name, notes,total_events, generators):

    mcm = McM(dev=False)

    modifications = { 'fragment' : fragment, 'dataset_name' : dataset_name, 'notes' : notes, 'total_events' : total_events, "generators": generators 
                 
                     }


    #request_prepid_to_clone = "SUS-RunIIWinter15wmLHE-00040"
    
    request = mcm.get('requests', request_prepid_to_clone)
    
    for key in modifications:
        request[key] = modifications[key]

    clone_answer = mcm.clone_request(request)

    if clone_answer.get('results'):
        print "@@"
        new_prepid=clone_answer['prepid']
        print('Clone PrepID: %s' % (clone_answer['prepid']))
        new_request=mcm.get('requests', new_prepid)
        print new_request['dataset_name']
        mcm.approve('requests', new_prepid, None)
        print "---"
        f=open('success.txt','a')
        f.write(new_prepid+"\n")
        f.close()
    else:
        print('Something went wrong while cloning a request. %s' % (dumps(clone_answer)))
        f=open('fail.txt','a')
        f.write(dataset_name+"\n")
        f.close()




if __name__ == '__main__':
    
    #mass
    #ref
    
    #gridpack
    #request_prepid_to_clone
    #fragment
    #dataset_name
    #notes
    #total_events
    ##################
    #masslist=[126,130,135,140,145,150,155,160,165,170,180,190,210,230,250,270,750]
    masslist=[300,350,400,500,550,600,700,800,900,1500,2000,2500,3000]
    vJHUGen='710'
    gridpacklist={  \

                  300:'/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_gghWWlnuqq300/v2/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_9_3_0_gghWWlnuqq300.tgz',\
                  350:'/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_gghWWlnuqq350/v2/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_9_3_0_gghWWlnuqq350.tgz',\
                  400:'/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_gghWWlnuqq400/v2/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_9_3_0_gghWWlnuqq400.tgz',\
                  500:'/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_gghWWlnuqq500/v2/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_9_3_0_gghWWlnuqq500.tgz',\
                  550:'/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_gghWWlnuqq550/v2/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_9_3_0_gghWWlnuqq550.tgz',\
                  600:'/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_gghWWlnuqq600/v2/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_9_3_0_gghWWlnuqq600.tgz',\
                  700:'/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_gghWWlnuqq700/v2/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_9_3_0_gghWWlnuqq700.tgz',\
                  800:'/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_gghWWlnuqq800/v2/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_9_3_0_gghWWlnuqq800.tgz',\
                  900:'/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_gghWWlnuqq900/v2/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_9_3_0_gghWWlnuqq900.tgz',\
                  1500:'/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_gghWWlnuqq1500/v2/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_9_3_0_gghWWlnuqq1500.tgz',\
                  2000:'/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_gghWWlnuqq2000/v2/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_9_3_0_gghWWlnuqq2000.tgz',\
                  2500:'/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_gghWWlnuqq2500/v2/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_9_3_0_gghWWlnuqq2500.tgz',\
                  3000:'/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/powheg/V2/gg_H_quark-mass-effects_gghWWlnuqq3000/v2/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_9_3_0_gghWWlnuqq3000.tgz',\
  
 }
    generators= ["PowhegV2+JHUGenV"+vJHUGen]
    request_prepid_to_clone='HIG-RunIISummer15wmLHEGS-02326'  ##template request
    total_events=200000
    for mass in masslist:
        dataset_name='GluGluHToWWToLNuQQ_M'+str(mass)+'_13TeV_powheg_JHUGenV'+vJHUGen+'_pythia8'
        notes="gg->H->WW->LNuQQ mH="+str(mass)+" JHUGenV"+vJHUGen+"\nNNPDF3.1"
        ##Set Reference comment##
        if mass>300:
            ref='#https://github.com/cms-sw/genproductions/blob/62b999a9af8f28315dbeb337a9cb6f800d51afe3/bin/Powheg/production/2017/13TeV/Higgs/gg_H_WW_quark-mass-effects_NNPDF31_13TeV/makecards.py\n#https://github.com/cms-sw/genproductions/blob/23f4c0dfc28b92f8649f8e2a08e61f7018fbca97/bin/JHUGen/cards/decay/WWlnuqq_withtaus_reweightdecay_CPS.input\n'
        else:
            ref='#https://github.com/cms-sw/genproductions/blob/62b999a9af8f28315dbeb337a9cb6f800d51afe3/bin/Powheg/production/2017/13TeV/Higgs/gg_H_WW_quark-mass-effects_NNPDF31_13TeV/makecards.py\n#https://github.com/cms-sw/genproductions/blob/23f4c0dfc28b92f8649f8e2a08e61f7018fbca97/bin/JHUGen/cards/decay/WWlnuqq_withtaus.input\n'
        if gridpacklist[mass]:
            gridpack=gridpacklist[mass]
        else :
            gridpack='/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc630/13TeV/Powheg/V2/GluGluHToWWToLNuQQ_NNPDF31_13TeV_powheg_JHUGen727/MassVariation/v1/gg_H_quark-mass-effects_slc6_amd64_gcc630_CMSSW_10_1_6_gghWWlnuqq_jhu'+str(mass)+'.tgz'
        
        if os.path.isfile(gridpack):
            print "--gridpack checked--"
        else :
            print "--@@@@@@@@@@@@@@@@@@@@@@@@@@@!!no gridpack!!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            print "--Pass mass point "+str(mass)+"  :::::"+dataset_name
            continue
        fragment="import FWCore.ParameterSet.Config as cms\n\nexternalLHEProducer = cms.EDProducer(\"ExternalLHEProducer\",\n    args = cms.vstring('"+gridpack+"'),\n    nEvents = cms.untracked.uint32(5000),\n    numberOfParameters = cms.uint32(1),\n    outputFile = cms.string('cmsgrid_final.lhe'),\n    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')\n)\n\n"+ref+"\n#\nimport FWCore.ParameterSet.Config as cms\nfrom Configuration.Generator.Pythia8CommonSettings_cfi import *\nfrom Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *\nfrom Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *\n\ngenerator = cms.EDFilter(\"Pythia8HadronizerFilter\",\n                         maxEventsToPrint = cms.untracked.int32(1),\n                         pythiaPylistVerbosity = cms.untracked.int32(1),\n                         filterEfficiency = cms.untracked.double(1.0),\n                         pythiaHepMCVerbosity = cms.untracked.bool(False),\n                         comEnergy = cms.double(13000.),\n                         PythiaParameters = cms.PSet(\n        pythia8CommonSettingsBlock,\n        pythia8CUEP8M1SettingsBlock,\n        pythia8PowhegEmissionVetoSettingsBlock,\n        processParameters = cms.vstring(\n            'POWHEG:nFinal = 1',   ## Number of final state particles\n                                   ## (BEFORE THE DECAYS) in the LHE\n                                   ## other than emitted extra parton\n          ),\n        parameterSets = cms.vstring('pythia8CommonSettings',\n                                    'pythia8CUEP8M1Settings',\n                                    'pythia8PowhegEmissionVetoSettings',\n                                    'processParameters'\n                                    )\n        )\n                         )\n\nProductionFilterSequence = cms.Sequence(generator)\n"
        
        
    
        
        clone_and_edit_jhchoi(request_prepid_to_clone,fragment, dataset_name, notes,total_events, generators)
    
