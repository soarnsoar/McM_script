import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
sys.path.append('../')
from rest import McM
from json import dumps
from GetTargetStep import GetTargetStepFromDAS


#DAS=sys.argv[1]

def Run(DAS):
    #prepid=GetTargetStepFromDAS('LHE','/VBFHToWWTo2L2Nu_M190_13TeV_powheg_JHUgenv628_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM')
    prepid=GetTargetStepFromDAS('LHE',DAS)
    #print prepid
    
    mcm = McM(dev=False)
    this_request=mcm.get('requests',prepid)

    fragment=this_request['fragment']

    #print fragment
    #print "-------"
    #print DAS
    for line in fragment.split('\n'):
        if line.replace(' ','').startswith('#'):
            if "bin/Powheg" in line:
                print line



DAS=sys.argv[1]
Run(DAS)


