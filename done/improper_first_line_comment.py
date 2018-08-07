#! /usr/bin/python
import re

#correct the improper first line of block comment
#input :-
#			/* TX chan of path is up, flush all queued packets in
#output :-
#			/*
#			 * TX chan of path is up, flush all queued packets in
# Author :- Raj Kamal <raj.x.kamal@oracle.com>
#----------------------------------------------------------Begin---------------------------------------------------#
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

        ####print "count of line = ", count;
        return count;
#end of fucntion

#find the tab and space count.
def getspacetab (line1):
        count = 0;
        flag = 0;
        for character in line1:
                if ((character == '\t')):
                        temp_count = count % 8;
                        temp_count = 8 - temp_count;
                        count = count + temp_count;
                elif (character == " "):
                        count = count + 1;
                else:
                        break;
        #end of for loop
        tab_count = count / 8;
        space_count = count % 8;
        return space_count, tab_count;
#end of function

#correct the improper first line of block comments
def improper_first_line_comment (line1):
	#get the required space tab
	space, tab = getspacetab (line1);

	#add required space and tab
	line = "";
	if ( tab > 0):
                for i in range (tab):
                        line = line + "\t";
        if (space > 0):
                for i in range (space):
                        line = line + " ";	

	###print "line1  ->", line1;
	#create the first line of comment
	return_line1 = line + "/*" + "\n";
	
	#create the second line of comment
 	list1 = re.findall (r"\*.*", line1);
	###print "list-->", list1
	return_line2 = line + " " +list1[0] + "\n";

	return return_line1, return_line2;
#end of function.

#main fucntion
def main():
        fin = open ("temp9.txt", "r+");
        fout = open ("temp10.txt", "w+");

        for line in fin:
                ####print line;
                #extract the original filename
                line = line.lstrip (" ");
                line = line.lstrip ("\t");
                line = line.rstrip (" ");
                line = line.rstrip ("\t");
                line = line.rstrip ("\n");
                #print "filename-----------------------------------",line,"----------------------------------------";
                filename_orig = line;
                #make the duplicate of the original of filename
                temp_name = re.findall (".*/(.*)", line);
                filename_temp = str (temp_name[0]);
                filename_temp = filename_temp.strip (" ");
                filename_temp = filename_temp.strip ("\t");
                filename_temp = filename_temp.strip ("\n");
                #to search for just filename eg xsvnic.c
                filename_str  = filename_temp;
                filename_temp = "step10"+"/"+filename_temp;
                fout.write (filename_temp);
                fout.write ("\n");
                ####print filename_temp;

                #open the  files
                fin1 = open (filename_orig, "r+");
                fout1 = open (filename_temp, "w+");

                #create a list for storing the lines with cstyle error
                line_list = list();

                #to get line number from error file
                filename1 = "step9.txt"
                fin0 = open (filename1, "r+");

                #open the error file to get the line containing cstyle error
                for line2 in fin0:
                        flag = re.findall (filename_orig, line2);
                        if (len(flag) > 0):
                                flag1 = re.findall ("improper first line of block comment", line2);
                                #create a search string.
                                string = filename_str + ":" + " " + "(.+):";

                                if (len(flag1) > 0 ) :
                                        line_number = re.findall (string, line2)  #file name is needed.
					if (len (line_number) > 0):
                                        	line_list.append (int(line_number[0]));
                                #end of if loop

                         #end if if loop for extracting line_number

                #end of for loop

                #print "Total number of errors :- ", len(line_list);
                #print "--------------------------------------------------------------------------------------------";
                #indicate the line count in every file
                line_no = 0;
                #indicatet the length of line
                char_count = 0;

		for line1 in fin1:
                        line_no = line_no + 1;
			char_count = line_length (line1);
			if ( line_no in line_list):
				first_line, second_line = improper_first_line_comment (line1);
				#print "--------------------improper first line of block comment----------------------------";
				#print "line_no-->", line_no, "length of line -->", char_count;
                                #print line1;
                                #print first_line;
				#print second_line;

                                #copy the corrected line to file
                                fout1.write (first_line);
				fout1.write (second_line);
                        #end of if loop

                        else:
				##print "line_no;
                                fout1.write (line1);
                        #end of else loop.

                #end of for loop for iterating the file line by line

        #end of for loop for iterating the file names

#end of function


#-------------------------------------------------------------------main program starts here----------------------------------------------------------#
#calling main function.
main();
#-----------------------------------------------------------------end of program---------------------------------------------------------------------#


