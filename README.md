# Simple and Tight Verifiable Delay Functions
The code in this repository implements the "Simple VDF" of Pietrzak (https://eprint.iacr.org/2018/627.pdf) as well as the "Tight VDF" (by Döttling et al.) application on it (https://eprint.iacr.org/2019/659.pdf) on user specifiable timing parameters. 

## Usage
To run a simple example comparing both VDFs run 
'python3 src/protocol/systemtests.py t'
with T = 2^t as timing parameter
To execute only the simple VDF run
'python3 src/protocol/systemtests.py t -s'
respectively for the tight VDF
'python3 src/protocol/systemtests.py t -t'

## Comparison table
To get a table with preset range of t comparing both VDFs run 
'python3 src/protocol/systemtests.py 0 -c'
The range can be adjusted in the main function of src/protocol/systemtests.py 

## Notes
'python3 src/protocol/systemtests.py -h'
will print a simple usage guide

- The VDFs with t=30 will already take several minutes to be computed. Hence we suggest to not run the implementation with much higher values of t just for demonstration purposes. 



