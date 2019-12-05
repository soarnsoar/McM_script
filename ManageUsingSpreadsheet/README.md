parser.add_argument("--key", help="google spreadsheet's key")
    pars    er.add_argument("--sheet", help="name of sheet")
    parser.add_argument("--log", help="logfile path")
    args = parser.parse_args()



python create_request_spreadsheet.py --key <google spreadsheet key> --sheet <name of sheet> --log <logfile>




*How to Use

1) key of spreadsheet
if url = https://docs.google.com/spreadsheets/d/1dSs6uR281Y7f3JrCc449otF9yht9RDZhiJUbGGWmGpk/edit?usp=sharing
->key = 1dSs6uR281Y7f3JrCc449otF9yht9RDZhiJUbGGWmGpk

2) Your spreadsheet must have title row with 

member_of_campaign  
dataset_name
cross_section
filter_efficiency	
filter_efficiency_error	
match_efficiency 
match_efficiency_error 
negative_weights_fraction 
generators 
PSfragment 
Notes 
gridpackPATH 
card_ref 
total_events 
PrepID

->Check example spreadsheet 

https://docs.google.com/spreadsheets/d/1dSs6uR281Y7f3JrCc449otF9yht9RDZhiJUbGGWmGpk/edit?usp=sharing


3) Fill the info and run 

python create_request_spreadsheet.py --key <google spreadsheet key> --sheet <name of sheet> --log <logfile>

