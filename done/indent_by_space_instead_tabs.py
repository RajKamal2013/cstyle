#! /usr/bin/python
import re,os
#AIM  -> repalce space with tab in beginning.
#DONE -> Not editing comment done
#DONE -> space in the bginning is repalced with appropriate number of tabs
#DONE -> for function case assuming the space is made during writing, execess number of space after separationa  are converted to space 
#input :-
#                       mac_capab_lso_t *cap_lso = cap_data;
#output :-
#			mac_capab_lso_t *cap_lso = cap_data;
#author :- Raj Kamal <raj.x.kamal@oracle.com>
#---------------------------------BEGIN-----------------------------------------------------#
#count the actual length of line
def line_length (line1):
        count = 0;
        for character in line1:
                if (character == '\t'):
                        temp_count = count % 8;
                        temp_count = 8 - temp_count;
                        count = count + temp_count;
                else:
                        count = count + 1;
        #end of loop for counting characters.
        ##print "count of line = ", count;
        return count;
#end of fucntion.


#removes indent by spaces intead of tabs errror
def indent_spaces_intead_tabs (line1):
	#search for comments
	comment = re.findall (r"(^/.+|^\s*/|^\s\*)", line1);
	line3 = line1;
		
	# line is not comment than only change 
	if (len(comment) == 0):
		index = 0;
		count = 0;
		#line3 = line1;
		
		char = line1[index];
		while (char == " "):
			count = count + 1;
			index = index + 1;
			char  = line1[index];
		#end of while loop
			
		#count number of space and tab
		num_tabs = count/8;
		num_space = count % 8;
		line2 = line1.lstrip(' ');
		line3 = ''; 	

		#if ((num_space >0) and (num_space <=4)):
		#	num_space = 4;
					
		#for converting space into tab
		while (num_tabs > 0):
			line3 = line3 + '\t';
			num_tabs = num_tabs - 1;
		#end of while loop

		#for maintaining the space after tab
		while (num_space > 0):
			line3 = line3 + ' ';
			num_space = num_space - 1;
		#end of	 while loop
		
		line3 = line3 + line2;
	#end of if loop
	return line3;
#end of fucntion.

#main function defination 
def main():
	fin = open("temp.txt", "r+");
	fout = open("temp1.txt", "w+");

	#iterate through th file name
        for line in fin:
                ##print line;
                #extract the original filename
                line = line.lstrip (" ");
                line = line.lstrip ("\t");
                line = line.rstrip (" ");
                line = line.rstrip ("\t");
                line = line.rstrip ("\n");
                ##print "filename--------------------------------------------------------------------------", line;
                filename_orig = line;
                #make the duplicate of the original of filename
                temp_name = re.findall (".*/(.*)", line);
                filename_temp = str (temp_name[0]);
                filename_temp = filename_temp.strip (" ");
                filename_temp = filename_temp.strip ("\t");
                filename_temp = filename_temp.strip ("\n");
                #to search for just filename eg xsvnic.c
                filename_str  = filename_temp;
                filename_temp = "step1"+"/"+filename_temp;
                fout.write (filename_temp);
                fout.write ("\n");
		###print filename_orig;
                ###print filename_temp;

                #open the  files
                fin1 = open (filename_orig, "r+");
                fout1 = open (filename_temp, "w+");

                #create a list for storing the lines with cstyle error
                line_list = list();

                #to get line number from error file
                filename1 = "step0.txt";
                fin0 = open (filename1, "r+");

		#open the error file to get the line containing cstyle error
                for line2 in fin0:
			###print line2;
                        flag = re.findall (filename_str, line2);
                        if (len(flag) > 0):
				##print line2;
                                flag1 = re.findall ("indent by spaces instead of tabs", line2);
                                #create a search string.
                                string = filename_str + ":"+ " " + "(.+):";
                                if (len(flag1) > 0 ) :
                                        line_number = re.findall (string, line2)  #file name is needed.
					if (len(line_number) > 0):
                                        	line_list.append (int(line_number[0]));
                                #end if if loop for extracting line_number
                        #end of if loop
                #end of for loop

		###print line_list;
                #indicate the line count in every file
                line_no = 0;
                #indicatet the length of line
                char_count = 0;

		#print "total Number of errrors ->", len (line_list);
		#iterate through the file
 		for line1 in fin1:
                        line_no = line_no + 1;
			#if line contains cstyle errors
                        if ( line_no in line_list):
				#get the length of line
                                char_count = line_length (line1);
				#correct the line
				first_line = indent_spaces_intead_tabs (line1);
				#first_line = line1;
				#write to the file
				fout1.write (first_line);
				#print "---------------------------indent by spaces instead of tabs-----------------------------------------"; 
				#print "line number ->", line_no, "length of line ->", char_count;
				#print line1;
				#print first_line;
		 	#end of if loop
			
			#if line do not contain error.
			else:
				fout1.write(line1);
			#end of else loop

			#os.remove (filename_orig);
			#os.rename (filename_temp, filename_orig);
		#end for loop
	#end of for loop	
#end of function 

#---------------------------------------------------------------main program starts here--------------------------------------------------#
main();
#---------------------------------------------------------------end of program------------------------------------------------------------#
