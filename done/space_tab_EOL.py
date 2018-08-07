#! /usr/bin/python 
import re,os

#removes space or tab at the end of line cstytle error
#DONE -> removed space/tab at the end of line.---------------------------------> done.
#space and tab at empty line.--------------------------------------------------> done
#space at the end of line in comment.------------------------------------------> done.
#space the line continuation while defining functions.-------------------------> done.

#input :-
#	static void xsvnic_session_watch_cancel(xsvnic_t *xsvnicp, xsvnic_session_t *sessp);     
#output :-
#	static void xsvnic_session_watch_cancel(xsvnic_t *xsvnicp, xsvnic_session_t *sessp);
#input :-
#	static void xsvnic_session_watch_cancel(xsvnic_t *xsvnicp, xsvnic_session_t *sessp);	
#output :-
#	static void xsvnic_session_watch_cancel(xsvnic_t *xsvnicp, xsvnic_session_t *sessp);
#input :-
#	  (empty line with space or tab or both)
#output :-
# (removed the line)
# Author :- Raj Kamal<raj.x.kamal@oracle.com>
#-----------------------------------Begin-------------------------------------------# 
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

#removes space at the end of line
def space_at_the_end_of_line (line1):
	line2 = '';
	line2 = line1[ :(len(line1)-2)];
        line2=line2.rstrip(' ');
        line2 = line2+"\n";
	return line2;
#end of function.

#removes tab at the end of line
def tab_at_the_end_of_line (line1):
	line2 = '';
	line2 = line1[ :(len(line1)-2)];
	line2=line2.rstrip(' ');
        line2=line2.rstrip('\t');
        line2=line2+"\n";
	return line2;
#end of function.

#main function :-
def main():
	fin = open("temp3.txt", "r+");
	fout = open("temp5.txt", "w+");
 
	for line in fin:
                ##print line;
                #extract the original filename
                line = line.lstrip (" ");
                line = line.lstrip ("\t");
                line = line.rstrip (" ");
                line = line.rstrip ("\t");
                line = line.rstrip ("\n");
                #print "filename--------------------------------------------------------------------------", line;
                filename_orig = line;
                #make the duplicate of the original of filename
                temp_name = re.findall (".*/(.*)", line);
                filename_temp = str (temp_name[0]);
                filename_temp = filename_temp.strip (" ");
                filename_temp = filename_temp.strip ("\t");
                filename_temp = filename_temp.strip ("\n");
                #to search for just filename eg xsvnic.c
                filename_str  = filename_temp;
                filename_temp = "step5"+"/"+filename_temp;
                fout.write (filename_temp);
                fout.write ("\n");
                ##print filename_temp;

                #open the  files
                fin1 = open (filename_orig, "r+");
                fout1 = open (filename_temp, "w+");

                #create a list for storing the lines with cstyle error
                line_list = list();

                #to get line number from error file
                filename1 = "step3.txt"
                fin0 = open (filename1, "r+");

		#open the error file to get the line containing cstyle error
                for line2 in fin0:
                        flag = re.findall (filename_orig, line2);
                        if (len(flag) > 0):
                                flag1 = re.findall ("space or tab at end of line", line2)
                                #create a search string.
                                string = filename_str + ":" + " " + "(.+):";
                                if (len(flag1) > 0 ) :
                                        line_number = re.findall (string, line2)  #file name is needed.
					if (len (line_number) > 0):
                                        	line_list.append (int(line_number[0]));
                                #end if if loop for extracting line_number
                        #end of if loop
                #end of for loop


                #indicate the line count in every file
                line_no = 0;
                #indicatet the length of line
                char_count = 0;

		#print "Total number of error -> ", len(line_list);
		#print line_list;

		#iterate throught the file line by line
 		for line1 in fin1:
                        line_no = line_no + 1;
			#if line contains cstyle errors
                        if ( line_no in line_list):
                                char_count = line_length (line1); 
			
				first_line = line1;	
				line_t = line1;
				line_t = line_t.lstrip (" ");
				line_t = line_t.lstrip ("\t");
				line_t = line_t.rstrip ("\n");

				#end of line is space
                        	if(line1[len(line1)-2] == ' '):
					first_line = space_at_the_end_of_line (line1);
                                	#print "-----------------------------------case 1 space at the end ------------------------------------------";
                                	#print "line number ->", line_no, "length of line ->", char_count;
                                	#print line1;
                                	#print first_line;
				#end of if loop				

                        	#end of the line is tab
                        	elif(line1[len(line1)-2] == '\t' ):
					first_line = tab_at_the_end_of_line (line1);
                                	#print "--------------------------------------case 1 tab at the end ------------------------------------------";
                                	#print "line number ->", line_no, "length of line ->", char_count;
                                	#print line1;
                                	#print first_line;
				#end of if loop
				
				else:
					first_line = line1.rstrip(" ");
					first_line = first_line.rstrip ("\t");
					#print "--------------------------------------case 1 space, tab at the end ---------------------------------------";
					#print "line number ->", line_no, "length of line ->", char_count;
                                        #print line1;
                                        #print first_line;
				#end of if loop

				fout1.write (first_line);
			#end of if loop

			#if line din contain error
			else:
				fout1.write (line1);
			#end of else loop
		#end of for loop .
	#end of for loop
#end of defining function.

#--------------------------------------------------------------program starts here----------------------------------------------------------#
main();
#-------------------------------------------------------------end of program----------------------------------------------------------------#
