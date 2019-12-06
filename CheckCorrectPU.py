import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM
from json import dumps



def GetTargetStepFromDAS(TargetStep,DAS):
    mcm = McM(dev=False)
    input_request=mcm.get("requests", query="produce="+DAS)
    member_of_chain=input_request[0]['member_of_chain']
    mychain=''
    for chain in member_of_chain:
        if TargetStep in chain:
            mychain=chain
    chained_request = mcm.get('chained_requests',
                              mychain)

    req=''

    for member in chained_request['chain']:
        if TargetStep in member:
            req=member

    return req

def GetPileUpDatasetName(prepid):
    mcm=McM(dev=False)
    request=mcm.get('requests',prepid)
    return request['pileup_dataset_name']


if __name__ == '__main__':
    
    DAS=sys.argv[1]
    DRprepid=GetTargetStepFromDAS('DR',DAS)
    pileupdataset=GetPileUpDatasetName(DRprepid)
    print pileupdataset
    if 'correctPU' in pileupdataset:
        print "correctPU :)"
