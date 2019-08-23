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







if __name__ == '__main__2':
    whichStep='Nano'
    req_root='HIG-RunIIFall17NanoAODv5-00824'
    req=GetDRofMiniAOD(req_root)
    #req=PrintStepPrepID(whichStep,req_root)
    print req


if __name__ == '__main__':

    KEY='1RlYGSg0BLosRoQumsrPhPvZII2rNic7fTeuPsxFpmE0'
    #def GetRootRequstList(KEY,sheet,cell_range):
    sheet='Interference'
    cell_range='H1:H1000'
    rootlist=GetRootRequstList(KEY,sheet,cell_range)

    dic_DR={}
    for req_mini in rootlist:
        thisDR=GetDRofMiniAOD(req_mini)
        #DRlist.append(thisDR)
        dic_DR[req_mini]=thisDR
    whichStep='NanoAODv5'

    
    f=open(whichStep+'.txt','w')
    nanolist=[]
    for req_root in rootlist:
        #print "req_root-->",req_root
        #def PrintStepPrepID(step,request_prepid_to_check):


        req=PrintStepPrepID(whichStep,dic_DR[req_root])
        if req=='#None':
            req=PrintStepPrepID(whichStep,req_root)
        #print req
        f.write(str(req_root)+'\t'+str(req)+'\n')
        nanolist.append(req)


    f.write('----NanoOnly----'+'\n')

    for req_nano in nanolist:
        f.write(str(req_nano)+'\n')
    
    f.close()
    
