import sys
import os
import time
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM

mcm = McM(dev=True)


def GetRootRequstList(KEY,sheet,cell_range):
    ##KEY=>
    #print 'https://docs.google.com/spreadsheets/d/1BG4BaHfPBDlYOVi-BW63sQwdS5WQ2ggZv2HWkIk29oU/edit#gid=986135503'
    #KEY = 1BG4BaHfPBDlYOVi-BW63sQwdS5WQ2ggZv2HWkIk29oU

    #cell_ragne =>    "B3:B1000"

    download_url='"https://docs.google.com/spreadsheets/d/'+KEY+'/gviz/tq?tqx=out:csv&sheet='+sheet+'&range='+cell_range+'"'

    filename='_temp'+str(time.time())+'.txt'
    #print 'wget -q -O '+filename+" "+download_url
    os.system('wget -q -O '+filename+" "+download_url)
    f=open(filename,'r')
    
    mylist=[]
    lines=f.readlines()
    for line in lines:
        if len(line.split('-'))==3:
            line=line.replace('"','').replace('\n','')
            #if line.startswith('#'):continue
            mylist.append(line)

            
    f.close()
    os.system('rm '+filename)
    return mylist



def GetDRofMiniAOD(req_miniaod):
    #mcm = McM(dev=True)
    global mcm

    req_DR=PrintStepPrepID('DR',req_miniaod)
    return req_DR


def GetLHEofMiniAOD(req_miniaod):
    #mcm = McM(dev=True)
    global mcm

    req_DR=PrintStepPrepID('LHE',req_miniaod)
    return req_DR




def PrintStepPrepID(step,request_prepid_to_check):
    if request_prepid_to_check.startswith('#'):return '#None'
    global mcm
    
    #mcm = McM(dev=True)
    #request_prepid_to_check = 'HIG-RunIISummer16MiniAODv3-00406'
    #field_to_update = 'time_event'

    # get a the dictionnary of a request
    request = mcm.get('requests', request_prepid_to_check)

    if 'prepid' not in request:
        # In case the request doesn't exist, there is nothing to update
        print('Request "%s" doesn\'t exist' % (request_prepid_to_check))
        return '#None'
    else:

        
        thisStepChain='--'
        for r_chained in request['member_of_chain']:
            #print r_chained
            if step in r_chained:
                #print r_chained
                thisStepChain=r_chained

        #print request_prepid_to_check,'   ',thisStepChain
    

        if not thisStepChain == '--':
            chained_request = mcm.get('chained_requests',
                                      thisStepChain)
            #print chained_request
            #for a in chained_request:
            #    print a,'-->',chained_request[a]
            
            #print chained_request['member_of_campaign']
            #print chained_request['chain']
            
            req=''
            
            for member in chained_request['chain']:
                #print member
                if step in member: 
                    #print member
                    req=member
            return req
 
        else:
            return '#None'



def GetGridpackOfLHE(thisLHE):
    global mcm
    request = mcm.get('requests', thisLHE)
    
    fragment=request['fragment']
    
    gridpack='/cvmfs'+fragment.split('/cvmfs')[1].split("'")[0]
    
    return gridpack


def RunCPSchecker(rootlist,filename):
    

    f=open(filename,'w')
    for req_mini in rootlist:
        thisLHE=GetLHEofMiniAOD(req_mini)
        thisgridpack=GetGridpackOfLHE(thisLHE)
        print thisgridpack
        CPS=False
        os.system('mkdir _temp_')
        os.chdir('_temp_')
        os.system('tar -xf '+thisgridpack)
        jhugen=open('JHUGen.input','r')
        lines=jhugen.readlines()
        for line in lines:
            if 'ReweightDecay' in line and 'WidthSchemeIn=3' in line.replace(' ',''):CPS=True
        f.write(thisgridpack+' \t '+str(CPS)+'\n')
        jhugen.close()
        os.chdir('../')
        os.system('rm -rf _temp_')
    f.close()


if __name__ == '__main__2':
    whichStep='Nano'
    req_root='HIG-RunIIFall17NanoAODv5-00824'
    req=GetDRofMiniAOD(req_root)
    #req=PrintStepPrepID(whichStep,req_root)
    print req


if __name__ == '__main__':


    #rootlist=GetRootRequstList(KEY,sheet,cell_range)
    Autumn18rootlist=[
'HIG-RunIIAutumn18MiniAOD-01085',
'HIG-RunIIAutumn18MiniAOD-01366',
'HIG-RunIIAutumn18MiniAOD-01367',
'HIG-RunIIAutumn18MiniAOD-01086',
'HIG-RunIIAutumn18MiniAOD-01368',
'HIG-RunIIAutumn18MiniAOD-01087',
'HIG-RunIIAutumn18MiniAOD-01088',
'HIG-RunIIAutumn18MiniAOD-01092',
'HIG-RunIIAutumn18MiniAOD-01091',
'HIG-RunIIAutumn18MiniAOD-01089',
'HIG-RunIIAutumn18MiniAOD-01090',
'HIG-RunIIAutumn18MiniAOD-01093',
'HIG-RunIIAutumn18MiniAOD-01094',
'HIG-RunIIAutumn18MiniAOD-01095',
'HIG-RunIIAutumn18MiniAOD-01096',
'HIG-RunIIAutumn18MiniAOD-01097',
'HIG-RunIIAutumn18MiniAOD-01098',
'HIG-RunIIAutumn18MiniAOD-01099',
'HIG-RunIIAutumn18MiniAOD-01100',
'HIG-RunIIAutumn18MiniAOD-01101',
'HIG-RunIIAutumn18MiniAOD-01102',
'HIG-RunIIAutumn18MiniAOD-01103',
'HIG-RunIIAutumn18MiniAOD-01294',
'HIG-RunIIAutumn18MiniAOD-01295',
]


    RunCPSchecker(Autumn18rootlist,'Autumn18_gridpack_check_CPS.txt')    
    

    Fall17rootlist=[
'HIG-RunIIFall17MiniAODv2-02146',
'HIG-RunIIFall17MiniAODv2-04172',
'HIG-RunIIFall17MiniAODv2-04202',
'HIG-RunIIFall17MiniAODv2-02147',
'HIG-RunIIFall17MiniAODv2-04188',
'HIG-RunIIFall17MiniAODv2-02148',
'HIG-RunIIFall17MiniAODv2-02149',
'HIG-RunIIFall17MiniAODv2-02150',
'HIG-RunIIFall17MiniAODv2-02151',
'HIG-RunIIFall17MiniAODv2-02152',
'HIG-RunIIFall17MiniAODv2-02153',
'HIG-RunIIFall17MiniAODv2-02154',
'HIG-RunIIFall17MiniAODv2-02155',
'HIG-RunIIFall17MiniAODv2-02156',
'HIG-RunIIFall17MiniAODv2-02157',
'HIG-RunIIFall17MiniAODv2-02158',
'HIG-RunIIFall17MiniAODv2-02159',
'HIG-RunIIFall17MiniAODv2-02160',
'HIG-RunIIFall17MiniAODv2-02161',
'HIG-RunIIFall17MiniAODv2-02162',
'HIG-RunIIFall17MiniAODv2-02163',
'HIG-RunIIFall17MiniAODv2-02164',
'HIG-RunIIFall17MiniAODv2-04151',
'HIG-RunIIFall17MiniAODv2-04152',
]
    RunCPSchecker(Fall17rootlist,'Fall17_gridpack_check_CPS.txt')
