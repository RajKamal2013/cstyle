#! /usr/bin/python
import re
#correct the unparenthesized return expression cstyle errors
#input :-
# 	return B_FALSE;
#output :-
# 	return (B_FALSE);
# Author :- Raj Kamal<raj.x.kamal@oracle.com>
#-----------------------------------------------------------begin-----------------------------------------------
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

#remove the unparenthesized return expression
def unparenthesized_return_expression (line1):
	#find the word after which ( is to be added
	word = re.findall ("return ", line1);
	#create word with ( attached after return
	pattern = word[0] + "(";
	#add the ( in the line
	first_line = re.sub (word[0], pattern, line1);
	#find the word before which ) is to be added
	word = re.findall (";", first_line);
	#create the new pattern with the ) before ;
	pattern = ")" + word[0];
	#add the pattern in the line
	first_line = re.sub (word[0], pattern, first_line);
	#return the line 
	return first_line;
#end of function

#main fucntion
def main():
        fin = open ("temp11.txt", "r+");
        fout = open ("temp12.txt", "w+");

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
                filename_temp = "step12"+"/"+filename_temp;
                fout.write (filename_temp);
                fout.write ("\n");
                ####print filename_temp;

                #open the  files
                fin1 = open (filename_orig, "r+");
                fout1 = open (filename_temp, "w+");

                #create a list for storing the lines with cstyle error
                line_list = list();

                #to get line number from error file
                filename1 = "step11.txt"
                fin0 = open (filename1, "r+");

                #open the error file to get the line containing cstyle error
                for line2 in fin0:
                        flag = re.findall (filename_orig, line2);
                        if (len(flag) > 0):
                                flag1 = re.findall ("unparenthesized return expression", line2);
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
		#store the previous lines
		previous_line = "";
		#incase previous line is required to edit
		flag = 0;
		#record space and tab
		space = 0;
		tab = 0;
		list_t = list();

		for line1 in fin1:
                        line_no = line_no + 1;
			char_count = line_length (line1);
				

			#if the line has unparenthesized return expression error
			if ( line_no in line_list):
				first_line = unparenthesized_return_expression (line1);
				#print "--------------------unparenthesized return expression---------------------";
				#print "line_no-->", line_no, "length of line -->", char_count;
                                #print line1;
                                #print first_line;

                                #copy the corrected line to file
                                fout1.write (first_line);
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


