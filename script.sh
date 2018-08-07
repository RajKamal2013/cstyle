#! /bin/bash
# This is driver script . Commment in case you dont want to exercute that step.
# Author :- Raj Kamal <raj.x.kamal@oracle.com>
#---------------------------------Begin----------------------------------------#

#this script will copy all the file .c or .h  in step0 directory
./createbackup.sh
#runs cstyle on the directoty and produce the log
./cstyle.sh
#this copies needed file to step 0 directory
cp step0.txt done/
echo "Number of cstyle errors (intially) (Step 0):->":
wc -l step0.txt


cur_dir=$(pwd)

cd done/

./script_dub.sh
./cstyle.sh
./indent_by_space_instead_tabs.py 
./cstyle.sh
./space_tab_at_the_end_of_line.py 
./cstyle.sh
./single_long_comment.py
./cstyle.sh
./line_greater_than_80.py 
./cstyle.sh
./space_tab_EOL.py
./cstyle.sh
./fourspaces.py
./cstyle.sh 
./spacesinsteadtabs.py   
./cstyle.sh
./spacesbetweentabs.py
./cstyle.sh
./tabsbetweenspaces.py
./cstyle.sh
./improper_first_line_comment.py  
./cstyle.sh
./improper_block_comment.py  
./cstyle.sh
./unparenthesized_return_expression.py
./cstyle.sh
./comma_semicolon_followed_by_non-blank.py
./cstyle.sh
./continuation_4_spaces.py 
./cstyle.sh
./non-continuation_4_space.py 
./cstyle.sh

echo "Cstyle errors after space tab removal (Step 1):->"
wc -l step1.txt

echo "Cstyle errors after removing space, tab at End of line (Step 2):->"
wc -l step2.txt

echo "Cstyle errors after editing 80 + lines containing comments (Step 3):->"
wc -l step3.txt

echo "Cstyle errors after editing 80 +  (Step 4):->"
wc -l step4.txt

echo "Cstyle errors after removing space and tab at end of line  (Step 5):->"
wc -l step5.txt

echo "Cstyle errors after removing 4 spaces error (Step 6):->"
wc -l step6.txt

echo "Cstyle errors after removing spaces instead of tabs error (Step 7):->"
wc -l step7.txt

echo "Cstyle errors after removing spaces between tabs error (Step 8):->"
wc -l step8.txt


echo "Cstyle errors after removing tabs between spaces error (Step 9):->"
wc -l step9.txt

echo "Cstyle errors after removing improper first line of block comments (Step 10):->"
wc -l step10.txt

echo "Cstyle errors after removing improper block comments (Step 11):->"
wc -l step11.txt

echo "Cstyle errors after removing unparenthesized return expression  (Step 12):->"
wc -l step12.txt

echo "Cstyle errors after removing comma or semicolon followed by non blank  (Step 13):->"
wc -l step13.txt

echo "Cstyle error after (step 14) :->"
wc -l step14.txt

echo "Cstyle error after (Step 15) :->"
wc -l step15.txt

cd $cur_dir
#--------------------------------------------------end-------------------------------------#
