import sys
import os
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM
from json import dumps
import random
import csv
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


def GetTitleFromSpreadsheet(KEY,sheet,i_column="A",f_column="Z"):

    print "==GetTitleFromSpreadsheet=="
    ##Title row
    cell_range=i_column+"1:"+f_column+"1"
    download_url='"https://docs.google.com/spreadsheets/d/'+KEY+'/gviz/tq?tqx=out:csv&sheet='+sheet+'&range='+cell_range+'"'
    myhash = random.getrandbits(128)
    print myhash
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
    print "==GetInfoFromSpreadsheet=="
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





KEY='1bAdzoB9bg6nbyxCOBsTAWSSJy6FHNfmkrIDqY-Nmdi0'
sheet='Sheet1'



title_list=GetTitleFromSpreadsheet(KEY,sheet,i_column="A",f_column="Z")
info_list=GetInfoFromSpreadsheet(2,KEY,sheet,i_column="A",f_column="Z")

this_dic={}

for i in range(0,len(title_list)):
    title=title_list[i]
    print title
    value=info_list[i]
    print value
    this_dic[title]=value





FullFragment=MakeFullFragment(this_dic["gridpackPATH"], this_dic["PSfragment"],this_dic["card_ref"])
generator_parameters=Make_generator_parameters(this_dic["cross_section"],\
                                               this_dic["filter_efficiency"],\
                                               this_dic["filter_efficiency_error"],\
                                               this_dic["match_efficiency"],\
                                               this_dic["match_efficiency_error"],\
                                               this_dic["negative_weights_fraction"])

new_request = {'pwg': 'HIG', 'member_of_campaign': this_dic['member_of_campaign'],'dataset_name':this_dic['dataset_name'],'generators':this_dic['generators'],"fragment":FullFragment,'generator_parameters':generator_parameters}

# push it to McM
put_answer = mcm.put('requests', new_request)

if put_answer.get('results'):
    print('New PrepID: %s' % (put_answer['prepid']))
else:
    print('Something went wrong while creating a request. %s' % (dumps(put_answer)))

