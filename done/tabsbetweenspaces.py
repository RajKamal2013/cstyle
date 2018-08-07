#! /usr/bin/python
import re

#correct the tabs between spaces error.
#input :-
# * 	  typically happens when a fresh L2 entry is learnt.
#output :-
# * 	typically happens when a fresh L2 entry is learnt.
#input :-
# * 	  typically happens on a Tx Path.
#output :-
# * 	typically happens on a Tx Path.
# author :- Raj Kamal <raj.x.kamal@oracle.com>
#---------------------------------------------------------------Begin--------------------------------------------------#
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

#removes the tabs between spaces error
def tabs_between_spaces (line1):
        #get the the issues and store in list
        pattern = re.findall (" +\t+ +", line1);
        count_issue = len(pattern);

        return_line = line1;

        #whenever we encounter the space tab issue
        for index in range (count_issue):
                #split the line based on pattern
                line_split = return_line.split(pattern[index]);

		temp_list = re.findall (" +\t", pattern[index]);
		space = re.findall (" ", temp_list[0]);
                tab = re.findall ("\t", pattern[index]);
                
		pattern[index] = "";
		#put the tab infront of spaces
		for i in range (len(space)):
                	pattern[index]= pattern[index] + " ";

                #add the tab afterwards
                for i in range (len (tab)):
			pattern[index] = pattern[index] + "\t";
                #end of for loop.

                #now join the splitted line based on pattern
                return_line = pattern[index].join (line_split);
        #end of for loop.

        return return_line;
#end of function.




#main fucntion
def main():
        fin = open ("temp8.txt", "r+");
        fout = open ("temp9.txt", "w+");

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
                filename_temp = "step9"+"/"+filename_temp;
                fout.write (filename_temp);
                fout.write ("\n");
                ####print filename_temp;

                #open the  files
                fin1 = open (filename_orig, "r+");
                fout1 = open (filename_temp, "w+");

                #create a list for storing the lines with cstyle error
                line_list = list();

                #to get line number from error file
                filename1 = "step8.txt"
                fin0 = open (filename1, "r+");

                #open the error file to get the line containing cstyle error
                for line2 in fin0:
                        flag = re.findall (filename_orig, line2);
                        if (len(flag) > 0):
                                flag1 = re.findall ("tabs between spaces", line2);
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
				first_line = tabs_between_spaces (line1);
				char_count = line_length (line1);
				#print "----------------------tabs between spaces(general)----------------------------";
				#print "line_no-->", line_no, " length of line -->", char_count;
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


