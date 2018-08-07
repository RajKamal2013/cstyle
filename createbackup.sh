# /bin/bash
# Author :- Raj Kamal <raj.x.kamal@oracle.com>
#--------------------------------------------------Begin---------------------------------------#
dirname=step0
rm -r $dirname
mkdir $dirname
rm step0.txt
cp *.h step0/
cp *.c step0/
#:%s/step0/step0
#-----------------------------------------------End--------------------------------------------#
