#! /usr/bin/python
import re,os
#remove the continuation should be indented by 4 spaces
#input :-
#		 (ccp->chan_type == XSTL_CHAN_TYPE_XCM)) {
#output :-
#		    (ccp->chan_type == XSTL_CHAN_TYPE_XCM)) {
# Author :- Raj Kamal <raj.x.kamal@oracle.com>
#-----------------------------------------Begin-------------------------------------------------------#
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

#get the spaces and tab count in the begining of line
#count the space, tab , until line started
def getstartindex (line1):
        space_count = 0;
        tab_count = 0;
        #count the characters
        count = 0;
        for character in line1:
                if (character == "\t"):
                        ##print "tab";
                        temp_count = count % 8;
                        temp_count = 8 - temp_count;
                        count = count + temp_count;
                elif (character == " "):
                        ##print "space";
                        count = count + 1;
                else:
                        ##print "chracter : ", character;
                        break;
        #end of for loop
        ##print count, space_count, tab_count;
        tab_count = count / 8;
        space_count = count % 8;
        return count, space_count, tab_count;
#end of function

#removes continuation should be indented by 4 spaces
def continuation_indented_4_spaces (line1, space_count, tab_count):
	#get the space and tab count.
        #count, space_count, tab_count = getstartindex (line1);
        ##print "space count: ", space_count, "tab_count :", tab_count;
        temp_line = line1;
        temp_line = temp_line.lstrip("\t");
        temp_line = temp_line.lstrip(" ");
        first_line = "";

        #adding tab in front
        for index in range(tab_count):
                first_line = first_line + "\t";
        #end of for loop
	
	space_count = 4;

        #adding four spaces in the beginning for line continuation
        for index in range(space_count):
                first_line = first_line + " ";
        #end of for loop

        first_line = first_line + temp_line;

        return first_line;
#end of function

		
	return line3;
#end of fucntion.

#main function defination 
def main():
	fin = open("temp13.txt", "r+");
	fout = open("temp14.txt", "w+");

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
                filename_temp = "step14"+"/"+filename_temp;
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
                filename1 = "step13.txt";
                fin0 = open (filename1, "r+");

		#open the error file to get the line containing cstyle error
                for line2 in fin0:
			###print line2;
                        flag = re.findall (filename_str, line2);
                        if (len(flag) > 0):
				##print line2;
                                flag1 = re.findall ("continuation should be indented 4 spaces", line2);
                                #create a search string.
                                string = filename_str + ":"+ " " + "(.+):";
                                if (len(flag1) > 0 ) :
                                        line_number = re.findall (string, line2)  #file name is needed.
                                        line_list.append (int(line_number[0]));
                                #end if if loop for extracting line_number
                        #end of if loop
                #end of for loop

		###print line_list;
                #indicate the line count in every file
                line_no = 0;
                #indicatet the length of line
                char_count = 0;
		space = 0;
		tab = 0;
		count = 0;

		#print "total Number of errrors ->", len (line_list);
		#iterate through the file
 		for line1 in fin1:
                        line_no = line_no + 1;
			#if line contains cstyle errors
                        if ( line_no in line_list):
				#get the length of line
                                char_count = line_length (line1);
				#correct the line
				first_line = continuation_indented_4_spaces (line1, space, tab)
				#write to the file
				fout1.write (first_line);
				#print "---------------------------continuation should be indented 4 spaces-----------------------------------------"; 
				#print "line number ->", line_no, "length of line ->", char_count;
				#print line1;
				#print first_line;
		 	#end of if loop
			
			#if line do not contain error.
			else:
				if ((line_no + 1) in line_list): 
					#print "----------------------------previous line---------------------------------------------------------------";
					count, space, tab = getstartindex (line1);
					#print line1;
				#end of if loop.
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
