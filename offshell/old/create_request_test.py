import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM
from json import dumps

mcm = McM(dev=False)


def MakeLHEpart(gridpackPATH):
    LHEpart='import FWCore.ParameterSet.Config as cms\nexternalLHEProducer = cms.EDProducer("ExternalLHEProducer",\n    args = cms.vstring('+\
    gridpackPATH\
    +"),\n    nEvents = cms.untracked.uint32(5000),\n    numberOfParameters = cms.uint32(1),\n    outputFile = cms.string('cmsgrid_final.lhe'),\n    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')\n    )\n"
    return LHEpart

def MakeFullFragment(gridpackPATH, PSfragment,card_ref):
    LHEpart=MakeLHEpart(gridpackPATH)
    PSpart=PSfragment
    ref_list=card_ref.split('\n')
    ref_part=''
    for ref in ref_list:
        ref_part+="#"+ref+'\n'

    FullFragment=LHEpart+'\n'+ref_part+'\n'+PSpart
    return FullFragment
    #print FullFragment
    
def Make_generator_parameters(cross_section,filter_efficiency,filter_efficiency_error,match_efficiency,match_efficiency_error,negative_weights_fraction):
    generator_parameters=[{'cross_section':cross_section,'filter_efficiency':filter_efficiency,'filter_efficiency_error':filter_efficiency_error,'match_efficiency':match_efficiency,'match_efficiency_error':match_efficiency_error,'negative_weights_fraction':negative_weights_fraction}]
    return generator_parameters


##For 1st line of spreadsheet
card_ref=''
member_of_campaign='RunIISummer15wmLHEGS'
dataset_name='GluGluHToWWTo2L2Nu_M125_13TeV_powheg_JHUGenV735_pythia8'
generators=["powheg","JhugenV735"]
PSfragment='''import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from Configuration.Generator.Pythia8PowhegEmissionVetoSettings_cfi import *

generator = cms.EDFilter(""Pythia8HadronizerFilter"",
                         maxEventsToPrint = cms.untracked.int32(1),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(1.0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(13000.),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        pythia8PowhegEmissionVetoSettingsBlock,
        processParameters = cms.vstring(
            'POWHEG:nFinal = 1',   ## Number of final state particles
                                   ## (BEFORE THE DECAYS) in the LHE
                                   ## other than emitted extra parton
          ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'pythia8PowhegEmissionVetoSettings',
                                    'processParameters'
                                    )
        )
                         )

ProductionFilterSequence = cms.Sequence(generator)'''

gridpackPATH='/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/jhugen/V735/gg_H_quark-mass-effects_slc6_amd64_gcc481_CMSSW_7_1_16_patch1_jhugen735_HToWW2l2nu_M160/v1/gg_H_quark-mass-effects_slc6_amd64_gcc481_CMSSW_7_1_16_patch1_jhugen735_HToWW2l2nu_M160.tar.gz'
cross_section=1
filter_efficiency=1
filter_efficiency_error=0
match_efficiency=1
match_efficiency_error=0
negative_weights_fraction=0

# Example to create a request from input dictionary
# Get a default dictionary with the minimal info required


FullFragment=MakeFullFragment(gridpackPATH, PSfragment,card_ref)
generator_parameters=Make_generator_parameters(cross_section,filter_efficiency,filter_efficiency_error,match_efficiency,match_efficiency_error,negative_weights_fraction)

new_request = {'pwg': 'HIG', 'member_of_campaign': member_of_campaign,'dataset_name':dataset_name,'generators':generators,"fragment":FullFragment,'generator_parameters':generator_parameters}

# push it to McM
put_answer = mcm.put('requests', new_request)

if put_answer.get('results'):
    print('New PrepID: %s' % (put_answer['prepid']))
else:
    print('Something went wrong while creating a request. %s' % (dumps(put_answer)))
