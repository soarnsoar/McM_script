##python create_request_spreadsheet.py --sheet <sheet> --key <key>

 


import sys
import os
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM
from json import dumps
import random
import csv
#sys.path.append('genproductions/bin/utils/')
#from request_fragment_check import * 


def getNrow(KEY,sheet):
    
    cell_range="A1:A"
    download_url='"https://docs.google.com/spreadsheets/d/'+KEY+'/gviz/tq?tqx=out:csv&sheet='+sheet+'&range='+cell_range+'"'
    myhash = random.getrandbits(128)
    filename='_temp'+str(myhash)+'_.txt'

    os.system('wget -q -O '+filename+" "+download_url)

    f=open(filename)
    info_list = []
    csv_reader = csv.reader(f)

    nrow=sum(1 for line in csv_reader)
    print nrow
    os.system('rm '+filename)
    f.close()
    return nrow
   

def check_reqeust_info(this_dic):
    
    gridpackPATH=this_dic['gridpackPATH']
    dataset_name=this_dic['dataset_name']
    generators=this_dic['generators']
    PSfragment=this_dic['PSfragment']
    member_of_campaign=this_dic['member_of_campaign']

    MassInName=dataset_name.split('_M')[1].split('_')[0]
    vJHUGenInName=dataset_name.lower().split('jhugen')[1].split('_')[0].split('v')[-1]
    Tuning='-----'
    FTuning='----'
    if '15' in member_of_campaign:
        Tuning='CUETP8M1'
        FTuning='CUEP8M1'

    else:
        Tuning='CP5'
        FTuning='CP5'
    TuningInName=(Tuning in dataset_name)
    ScaleUpInName=('PSscaleUp' in dataset_name)
    ScaleDownInName=('PSscaleDown' in dataset_name)
    TuningUpInName=(Tuning+'Up' in dataset_name)
    TuningDownInName=(Tuning+'Down' in dataset_name)
    MinloInName=('minlo' in dataset_name.lower())

    GGH=('GluGlu' in dataset_name and not 'minlo' in dataset_name.lower())
    GGH_MINLO=('GluGlu' in dataset_name and 'minlo' in dataset_name.lower())
    VBF=('VBF' in dataset_name)
    Wminus=('Wminus' in dataset_name)
    Wplus=( 'Wplus' in dataset_name)
    ZH=('HZJ' in dataset_name)

    ##dataset_name and gridpack
    if GGH:
        if not 'gg_H_quark' in gridpackPATH:
            print "!!not matched gridpack process GGH"

    elif GGH_MINLO:
        if not 'HJJ' in gridpackPATH:
            print "!! not matched gridpack process GGH_MINLO"

    elif VBF:
        if not 'vbf' in gridpackPATH.lower():
            print "!! not matched gridpack process VBFH"
    elif Wminus:
        if not 'Wminus' in gridpackPATH:
            print "!! not matched gridpack process Wminus" 
    elif Wplus:
        if not 'Wplus' in gridpackPATH:
            print "!! not matched gridpack process Wplus"
    elif ZH:
        if not 'HZJ' in gridpackPATH:
            print "!! not matched gridpack process Wplus ZH"

    print member_of_campaign,dataset_name
    if not TuningInName:
        print 'No tuning in datasetname'
        ##tuning vs datasetname                                                                                                                                                           
    if not FTuning in PSfragment and not Tuning in PSfragment:
        print "!!No tuning info in Fragment "
    

    ##minlo
    if MinloInName:
        if not 'HJJ' in gridpackPATH:
            print "!!wrong minlo gridpack path"
    else:
        if 'HJJ' in gridpackPATH:
            print "!! not minlo but minlo gridpack"
    ## scale up/down vs datasetname
    if ScaleUpInName:
        if not 'TimeShower:renormMultFac=4.0' in PSfragment.replace(' ','') or not 'SpaceShower:renormMultFac=4.0' in PSfragment.replace(' ',''):
            print "!!Wrong ScaleUp Fragment"

    if ScaleDownInName:
        if not 'TimeShower:renormMultFac=0.25' in PSfragment.replace(' ','') or not 'SpaceShower:renormMultFac=0.25' in PSfragment.replace(' ',''):
            print "!!Wrong ScaleDown Fragment"

    ## tune up/down vs dataset name                                                                                                                                                   
    if TuningUpInName:
        if not 'pythia8'+FTuning+'Up' in PSfragment and not 'pythia8'+Tuning+'Up' in PSfragment:
            print "!!Wrong tuning setup"

    if TuningDownInName:
        if not 'pythia8'+FTuning+'Down' in PSfragment and not 'pythia8'+Tuning+'Down' in PSfragment:
            print "!!Wrong tuning setup"

    ## gridpack jhugen version vs dataset name                                                                                                                                        

    if not vJHUGenInName in gridpackPATH:
        print "!!wrong jhugen version"

    ##gridpack mass vs datasetname                                                                                                                                                    

    if not MassInName in gridpackPATH:
        print "!!wrong higgs mass"
    


def MakeLHEpart(gridpackPATH):
    LHEpart='import FWCore.ParameterSet.Config as cms\nexternalLHEProducer = cms.EDProducer("ExternalLHEProducer",\n    args = cms.vstring("'+\
    gridpackPATH.replace("\n","")\
    +'"'+"),\n    nEvents = cms.untracked.uint32(5000),\n    numberOfParameters = cms.uint32(1),\n    outputFile = cms.string('cmsgrid_final.lhe'),\n    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')\n    )\n"
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


def GetTitleFromSpreadsheet(KEY,sheet,i_column="A",f_column="Z"):

    #print "==GetTitleFromSpreadsheet=="
    ##Title row
    cell_range=i_column+"1:"+f_column+"1"
    download_url='"https://docs.google.com/spreadsheets/d/'+KEY+'/gviz/tq?tqx=out:csv&sheet='+sheet+'&range='+cell_range+'"'
    myhash = random.getrandbits(128)
    #print myhash
    filename='_temp'+str(myhash)+'_title.txt'

    
    os.system('wget -q -O '+filename+" "+download_url)

    f=open(filename)
    title_list = []
    

    csv_reader=csv.reader(f)
    for line in csv_reader: 
        #print line
        for element in line:
            #if element!="" and !element.startswith('#'):
            if element!="":
                title_list.append(element)
    os.system('rm '+filename)
    f.close()
    return title_list


def GetInfoFromSpreadsheet(index,KEY,sheet,i_column="A",f_column="Z"):
    #print "==GetInfoFromSpreadsheet=="
    myhash = random.getrandbits(128)
    filename='_temp'+str(myhash)+'_.txt'
    cell_range=i_column+str(index)+':'+f_column+str(index)
    download_url='"https://docs.google.com/spreadsheets/d/'+KEY+'/gviz/tq?tqx=out:csv&sheet='+sheet+'&range='+cell_range+'"'
    myhash = random.getrandbits(128)
    filename='_temp'+str(myhash)+'_.txt'
    
    os.system('wget -q -O '+filename+" "+download_url)

    f=open(filename)
    info_list = []
    csv_reader = csv.reader(f)
    for line in csv_reader: 
        for element in line:
            info_list.append(element)
    os.system('rm '+filename)
    f.close()
    return info_list




def Run(idx_row,KEY,sheet):

    output_msg=''
    #KEY='1bAdzoB9bg6nbyxCOBsTAWSSJy6FHNfmkrIDqY-Nmdi0'
    #sheet='2018'




    info_list=GetInfoFromSpreadsheet(idx_row,KEY,sheet,i_column="A",f_column="Z")
    if len(info_list)==0: 
        print "pass"
        return
    title_list=GetTitleFromSpreadsheet(KEY,sheet,i_column="A",f_column="Z")
    this_dic={}

    for i in range(0,len(title_list)):
        title=title_list[i]
        #print title
        value=info_list[i]
        #print value
        if not value.replace(' ','')=='': this_dic[title]=value
        
    
    ##Combine card refs
    if 'card_ref2' in this_dic:
        this_dic['card_ref']=this_dic['card_ref']+'\n'+this_dic['card_ref2']
    

    if not 'size_event' in this_dic:
        this_dic['size_event']=[600]
    elif this_dic['size_event'].replace(' ','')=='':
        this_dic['size_event']=[600]
    if not 'time_event' in this_dic:
        this_dic['time_event']=[60]
    elif this_dic['time_event'].replace(' ','')=='':
        this_dic['time_event']=[60.]
    FullFragment=MakeFullFragment(this_dic["gridpackPATH"], this_dic["PSfragment"],this_dic["card_ref"])
    generator_parameters=Make_generator_parameters(float(this_dic["cross_section"]),\
                                                   float(this_dic["filter_efficiency"]),\
                                                   float(this_dic["filter_efficiency_error"]),\
                                                   float(this_dic["match_efficiency"]),\
                                                   float(this_dic["match_efficiency_error"]),\
                                                   float(this_dic["negative_weights_fraction"]))


    print this_dic['dataset_name']


    
    new_request = {'pwg': 'HIG', 'member_of_campaign': this_dic['member_of_campaign'],'dataset_name':this_dic['dataset_name'],'generators':this_dic['generators'].split(','),"fragment":FullFragment,'generator_parameters':generator_parameters,'total_events':int(this_dic['total_events']),'mcdb_id':0,'size_event':this_dic['size_event'],'time_event':this_dic['time_event']}

    check_reqeust_info(this_dic)

    if 'PrepID' in this_dic:
        #print "ALREADY"
        mcm = McM(dev=False)
        this_request=mcm.get("requests",this_dic["PrepID"])

        for key in new_request:
            
            this_request[key]=new_request[key]
        update=mcm.update('requests', this_request)
        
        return this_dic["PrepID"]+str(update['results'])
    # push it to McM
    #mcm = McM(dev=False,cookie="dev-cookie.txt")
    #mcm = McM(dev=False,cookie='prod-cookie.txt')
    mcm = McM(dev=False)
    put_answer = mcm.put('requests', new_request)
    
    if put_answer.get('results'):
        prepid=put_answer['prepid']
        
        print('New PrepID: %s' % (prepid))
        #f.write(prepid+'\n')
        output_msg=str(prepid)
    else:
        print('Something went wrong while creating a request. %s' % (dumps(put_answer)))
        #f.write("fail,idx_row-->"+this_dic['dataset_name']+'\n')
        output_msg="fail"+str(idx_row)+"-->"+this_dic['dataset_name']
    #print output_msg
    return output_msg





if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("--key", help="google spreadsheet's key")
    parser.add_argument("--sheet", help="name of sheet")
    parser.add_argument("--log", help="logfile path")
    args = parser.parse_args()


    if args.key:
        key=args.key
    else:
        print 'need --key'
        exit()
    if args.sheet:
        sheet=args.sheet
    else:
        print 'need --sheet'
        exit()
    if args.log:
        log=args.log
    else:
        log='log_prepid.txt'

    nrow=getNrow(key,sheet)
    f=open(log,'w')
    for i in range(2,nrow+1):
        #for i in range(2,3):
        out=Run(i,key,sheet)
        if out!="" and out!=None:  
            f.write(out+"\n")
            
    f.close()
