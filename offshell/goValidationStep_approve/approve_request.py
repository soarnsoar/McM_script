# NEED this to be sourced before
# export PYTHONPATH=/afs/cern.ch/cms/PPD/PdmV/tools/wmcontrol:${PYTHONPATH}
# export PATH=/afs/cern.ch/cms/PPD/PdmV/tools/wmcontrol:${PATH}
# source /afs/cern.ch/cms/PPD/PdmV/tools/wmclient/current/etc/wmclient.sh

import os
import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM


def Run(prepid):

    mcm = McM(dev=False)
    #mcm.approve("requests", "EXO-RunIISummer15wmLHEGS-02343", 1) 

    #0:new
    #1:validation
    #2:define
    #3:approved
    #4:submit
    approve = mcm.approve('requests', prepid,1)
    print approve['results']


if __name__ == '__main__':
    prepid=sys.argv[1]
    Run(prepid)


