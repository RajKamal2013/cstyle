#! /usr/bin/python
import re
#correct the continuation line not indented by 4 spaces
#input :-
#				VNIC_NAME(xsvnicp), chan_type);
#output :-
#				    VNIC_NAME(xsvnicp), chan_type);
#author :- Raj Kamal <raj.x.kamal@oracle.com>
#----------------------------------------------------------Begin-----------------------------------------------#

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
#end of fucntion

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

#removes the extra space
def remove_space (line1):
	#get the space and tab count.
	count, space_count, tab_count = getstartindex (line1);
	#print "space count: ", space_count, "tab_count :", tab_count;
	temp_line = line1;
	temp_line = temp_line.lstrip("\t");
	temp_line = temp_line.lstrip(" ");
	first_line = "";
	
	#adding tab in front
	for index in range(tab_count):
		first_line = first_line + "\t";
	#end of for loop 

	first_line = first_line + temp_line;

	return first_line;
#end of function

#add extra space
def add_space (line1) :
	#get the space and tab count.
        count, space_count, tab_count = getstartindex (line1);
        #print "space count: ", space_count, "tab_count :", tab_count;
        temp_line = line1;
        temp_line = temp_line.lstrip("\t");
        temp_line = temp_line.lstrip(" ");
        first_line = "";

        #adding tab in front
        for index in range(tab_count):
                first_line = first_line + "\t";
        #end of for loop

	#adding four spaces in the beginning for line continuation
	for index in range(4):
		first_line = first_line + " ";
	#end of for loop

        first_line = first_line + temp_line;

        return first_line;
#end of function


#main fucntion
def main():
        fin = open ("temp5.txt", "r+");
        fout = open ("temp6.txt", "w+");

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
                filename_temp = "step6"+"/"+filename_temp;
                fout.write (filename_temp);
                fout.write ("\n");
                ##print filename_temp;
               
		#open the  files
		fin1 = open (filename_orig, "r+");
                fout1 = open (filename_temp, "w+");

		#create a list for storing the lines with cstyle error
		line_list = list();

		#to get line number from error file
		filename1 = "step5.txt"
		fin0 = open (filename1, "r+");
		
		#open the error file to get the line containing cstyle error
		for line2 in fin0:
        		flag = re.findall (filename_orig, line2);
        		if (len(flag) > 0):
                		flag1 = re.findall ("4 spaces", line2)
				#create a search string.
				string = filename_str + ":" + " " + "(.+):";
				if (len(flag1) > 0 ) :
                      			line_number = re.findall (string, line2)  #file name is needed.
					if (len(line_number) > 0 ):
                        			line_list.append (int(line_number[0]));
                		#end if if loop for extracting line_number
        		#end of if loop
		#end of for loop
	

		#indicate the line count in every file
                line_no = 0;
		#indicatet the length of line
                char_count = 0;

		for line1 in fin1:
        		line_no = line_no + 1;
        		if ( line_no in line_list):
				char_count = line_length (line1);
				#line contians a loop.
				is_loop = re.findall ("if | for | else | elif ", line1);
			
				#line contains loop.
				if (len(is_loop) > 0 ): 	
					first_line = remove_space (line1);
               				#print "--------------------------4 spaces (removing)----------------------------";
					#print "line_no ->", line_no, "lenght of line ->", char_count;
              				#print line1;
					#print first_line;
					#copy the corrected line to file
					fout1.write (first_line);
				#end of if loop
				
				#line is normal statement
				else :
					first_line = add_space (line1);
               				#print "----------------------------4 spaces(adding)----------------------------";
					#print "line_no ->", line_no, "lenght of line ->", char_count;
              				#print line1;
					#print first_line;
					#copy the corrected line to file
					fout1.write (first_line);
				#end of else loop.step6/xsvnic.c: 1097: continuation line not indented by 4 spaces
        		#end of if loop
			
			#line has no 4 spaces error 
			else:
				fout1.write (line1);
			#end of else loop.
		#end of for loop for iterating the file line by line
	#end of for loop for iterating the file names
#end of function

#-------------------------------------------------------------------main program starts here----------------------------------------------------------#

#calling main function.
main();
#-----------------------------------------------------------------end of program---------------------------------------------------------------------#
