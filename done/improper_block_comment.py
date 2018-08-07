#! /usr/bin/python
import re
###########-----------------------some cases could not be handled need to do manually ##################-------------
#correct the improper block comment
#input :-
#	/*
#	 pvt_datap = &chanp->xve_cm_pvt_data;
#	*/
#output :-
#	/*
#	 * pvt_datap = &chanp->xve_cm_pvt_data;
#	 */
#input :-
#	 /*
#	  * No spl link up msg is rcvd.
#	  * link down is taken care in control message handler
#	  * For pvi its alwaysup.
#	  */
#output :-
#	/*
#	 * No spl link up msg is rcvd.
#	 * link down is taken care in control message handler
#	 * For pvi its alwaysup.
#	 */
#input :-
#	/*
#	 * TBD what happens if the LINK is not up
#	   Do we need to do all this stuff */
#output :-
#	/*
#	 * TBD what happens if the LINK is not up
#	 * Do we need to do all this stuff 
#	 */
#input :-
#       /*
#	 *
#	 */
#output :-
#	/*
#	 * TBD what happens if the LINK is not up
#	 * Do we need to do all this stuff 
#	 */
#input :-
#	**
#output :-
#	* *
#input :-
#	**/
#output :-
#	* */
# author :- Raj Kamal <raj.x.kamal@oracle.com>
#------------------------------------------------------------Begin---------------------------------------------------------------#
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

#correct the alignment of first line of comment.
def correct_alignment (line1) :
        #get the space, tab count
        space, tab = getspacetab (line1);
        first_line = "";
        line_t = line1.lstrip ("\t");
        line_t = line_t.lstrip (" ");
	line_t = line_t.lstrip ("\t");
	
	if( space >= 7):
		tab = tab + 1;
	
        #add tabs in front.
        for index in range (tab):
                first_line = first_line + "\t";
        #end of of for loop.

        first_line = first_line + line_t;

        return first_line, space, tab;
#end of function

#correct the improper block comments
def improper_first_block_comment (line1):
	#get the space tab count
	space, tab = getspacetab (line1);
	return_line = "";	

	if (space >= 7):
		tab = tab + 1;

	for index in range(tab):
		return_line = return_line + "\t";

	line_t = line1.lstrip ("\t");
	line_t = line_t.lstrip (" ");
	line_t = line_t.lstrip ("\t");
	line_t = line_t.rstrip ("\n");
	###print line_t;

	
	list_t = re.findall("^\*(.*)", line_t);
	###print list_t;

	#if * is present
	if (len(list_t)>0):
		#if line is */
		if (list_t[0] is '/'):
			return_line = return_line + " " + "*/" + "\n";
		else:
			return_line = return_line + " " + "*" + " " + list_t[0].lstrip(" ") + "\n";
	#end of if loop

	#if * is not present
	else :
		return_line = return_line + " " + "*" + " " + line_t.lstrip (" ") + "\n";
	#end of else loop

	return return_line;
#end of function.

#main fucntion
def main():
        fin = open ("temp10.txt", "r+");
        fout = open ("temp11.txt", "w+");

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
                filename_temp = "step11"+"/"+filename_temp;
                fout.write (filename_temp);
                fout.write ("\n");
                ####print filename_temp;

                #open the  files
                fin1 = open (filename_orig, "r+");
                fout1 = open (filename_temp, "w+");

                #create a list for storing the lines with cstyle error
                line_list = list();

                #to get line number from error file
                filename1 = "step10.txt"
                fin0 = open (filename1, "r+");

                #open the error file to get the line containing cstyle error
                for line2 in fin0:
                        flag = re.findall (filename_orig, line2);
                        if (len(flag) > 0):
                                flag1 = re.findall ("improper block comment", line2);
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
				
			#if the alignment of first line of comment is not correct
			list_t = re.findall ("/\*", line1);
                        if (len (list_t) > 0):
				temp_line = line_no + 1;
				if (temp_line in line_list):
					first_line, space, tab = correct_alignment (line1);
					#print "--------------------corrected first block of comments------------------"
					#print "--------------------improper block comment----------------------------";
					#print "line_no-->", line_no, "length of line -->", char_count;
					#print line1;
					#print first_line;
					line1 = first_line;
				#end of if loop
				
			#end of if loop

			#if the line has improper block of comment error
			if ( line_no in line_list):
				first_line = improper_first_block_comment (line1);
				#print "--------------------improper block comment----------------------------";
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


