#! /bin/bash
# Author : Raj Kamal >raj.x.kamal@oracle.com>
#-----------------------------------------------------Begin------------------------------------------#
touch tempdir.txt
path="../.."

ls ../step0 > temp.txt

array=(`cat temp.txt`)

rm temp.txt

filename2='';

for filename in ${array[*]}
do
	#print $filename
	filename2="$path/$filename"
	#echo $filename2;
	echo $filename2 >> tempdir.txt
done

cat /dev/null > temp.txt
cat tempdir.txt > temp.txt

rm tempdir.txt

rm -r step1
rm -r step2
rm -r step3
rm -r step4
rm -r step5
rm -r step6
rm -r step7
rm -r step8
rm -r step9
rm -r step10
rm -r step11
rm -r step12
rm -r step13
rm -r step14
rm -r step15

rm step1.txt
rm step2.txt
rm step3.txt
rm step4.txt
rm step5.txt
rm step6.txt
rm step7.txt
rm step8.txt
rm step9.txt
rm step10.txt
rm step11.txt
rm step12.txt
rm step13.txt
rm step14.txt
rm step15.txt

rm temp1.txt
rm temp2.txt
rm temp3.txt
rm temp4.txt
rm temp5.txt
rm temp6.txt
rm temp7.txt
rm temp8.txt
rm temp9.txt
rm temp10.txt
rm temp11.txt
rm temp12.txt
rm temp13.txt
rm temp14.txt
rm temp15.txt


mkdir step1
mkdir step2
mkdir step3
mkdir step4
mkdir step5
mkdir step6
mkdir step7
mkdir step8
mkdir step9
mkdir step10
mkdir step11
mkdir step12
mkdir step13
mkdir step14
mkdir step15

touch step1.txt
touch step2.txt
touch step3.txt
touch step4.txt
touch step5.txt
touch step6.txt
touch step7.txt
touch step8.txt
touch step9.txt
touch step10.txt
touch step11.txt
touch step12.txt
touch step13.txt
touch step14.txt
touch step15.txt


touch temp1.txt
touch temp2.txt
touch temp3.txt
touch temp4.txt
touch temp5.txt
touch temp6.txt
touch temp7.txt
touch temp8.txt
touch temp9.txt
touch temp10.txt
touch temp11.txt
touch temp12.txt
touch temp13.txt
touch temp14.txt
touch temp15.txt


#cat touchname2 > tempdir.txt
#ls | grep 'xs*' | grep '.[ch]$' > temp.txt
#--------------------------------------------END------------------------------------------------------#


