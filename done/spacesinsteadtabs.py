#! /usr/bin/python
import re

#correct the spaces instead tabs error.
#input :-
#	#include <sys/dlpi.h>           /* Contains checksum related info*/
#output :-
#	#include <sys/dlpi.h>		/* Contains checksum related info*/
#input :-
#	#define XSVNIC_MAX_RRING        1
#output :-
#	#define XSVNIC_MAX_RRING	1
#input :-
#       struct xsvnic_s         *xsvnicp;
#output :-
#	struct xsvnic_s		*xsvnicp;

# Author :- Raj Kamal<raj.x.kamal@oracle.com>
#---------------------------------------------------------------Begin--------------------------------------------#
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

        ###print "count of line = ", count;
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
                        ###print "tab";
                        temp_count = count % 8;
                        temp_count = 8 - temp_count;
                        count = count + temp_count;
                elif (character == " "):
                        ###print "space";
                        count = count + 1;
                else:
                        ###print "chracter : ", character;
                        break;
        #end of for loop
        ###print count, space_count, tab_count;
        tab_count = count / 8;
        space_count = count % 8;
        return count, space_count, tab_count;
#end of function

#get count in case word contains tab
def getcount (word, count):
	for character in word:
		if (character == "\t"):
                        ###print "tab";
                        temp_count = count % 8;
                        temp_count = 8 - temp_count;
                        count = count + temp_count;
                else:
                        ###print "chracter : ", character;
			count = count + 1;
        #end of for loop
	return count;
#end of function

#replace #define with #define\t
def space_instead_tab1 (line1):
	define_list = re.split("#define", line1);

	#remove space and tab after #define
	for index in range(len(define_list)):
		define_list[index] = define_list[index].lstrip (" ");
		define_list[index] = define_list[index].lstrip ("\t");
	#end of for loop
	
	#get the string to join
	string = "#define" + "\t";
	
	#merge the list
	first_word = string.join (define_list);

	return first_word;
#end of function	



#removes the space and add the equivalent space.
def space_instead_tab (line1):
	#get the space, tab count and actual index of starting character.
	count, space_count, tab_count = getstartindex (line1);
	wordlist = line1.split (" ");
	
	#removes space and tab at the beginning of line 
	#to account the first word in line
	k = 0;
	for index in range (len(wordlist)):
		#get the first word in line and remove spaces and tab at the beginning.
		if (len (wordlist[index]) > 0):
			wordlist[index] = wordlist[index].lstrip ("\t");
			wordlist[index] = wordlist[index].lstrip (" ");
			k = index;
			break;
		#end of if loop
	##print "wordlist[k]:-> ", wordlist[k];

	#to get the idea about the previous word is space or not.
	flag = 0;
	first_line="";
	final_line="";

	#replace space with tab if space count is more than 4
	if (space_count > 4):
		space_count = 0;
		tab_count = tab_count + 1;
	#end of if loop


	#add the space and tab as original
	for index in range (tab_count):
		final_line = final_line + "\t";
	for index in range (space_count):
		final_line = final_line + " ";

	#to maintain the space record
	space = 0;
	#to maintain required tab
	tab_equivalent = 0;
	#to maintian required space
	space_equivalent = 0;
	#to balance the space count for tab less than 8
	required_space_4_tab = 0;

	##print "starting index ->", k;
	#iterate the list
	for index in range(k, len(wordlist)):
		##print "index-- ", index, wordlist[index];
		#first word in line
		if (index == k):
			#search for tab
			tab = re.findall ("\t", wordlist[index]);
			
			#if tab then get the count
			if ( len (tab) > 0):
				count = getcount(wordlist[index] , count);
			#end of if loop
			
			#if no tab then general rule
			else:
				count = count + len(wordlist[index]);
			#end of else loop

			first_line = first_line + wordlist [index];
		#end of if loop

		#other than first word in line
		else :
			#search for tab
			tab = re.findall ("\t", wordlist[index]);
			
			#if tab is present in word
			if (len(tab) > 0):
				count = getcount (wordlist[index], count) + 1; #1 plus for space as we split based on space
			#end of if loop
	
			#if no tab then general rule
			else:
				count = count + len(wordlist[index]) + 1; #1 plus for space as we split based on space
			
			#if the word is space
			if (wordlist[index] == ''):
				#set flag if first space is found
				if (flag == 0):
					flag = 1;
					#initialize the space count
					space = 1;
					#get the required space count in case space requirement is less than 8
					required_space_4_tab = 8-(( count - 1 ) % 8);
				#end of if loop
				
				#flag is set, now space we encounter is not first space, continuos spaces
				else:
					space = space + 1;
				#end of else loop

			#end of if loop
			
			#if word is not space
			else :
				space = space + 1;   #as we split based on space
				
				#previous word is space
				if (flag == 1):
					
					diff = space;	
					###print "space -> ", space;				
					###print "required space for tab ->", required_space_4_tab;
					
					#get the actual space and tab required between two words
					if ((diff - required_space_4_tab) >= 0):
						tab_equivalent = tab_equivalent + 1;
						diff = diff - required_space_4_tab;
						tab_equivalent = tab_equivalent + (diff / 8);
						space_equivalent = diff % 8;
					#end of if loop

					#no tab is needed, insufficient space count
					else :
						space_equivalent = diff;
					#end of else loop
					
					#if space_equivalent is greater than 4
					if (space_equivalent > 4):
						space_equivalent = 0;
						tab_equivalent = tab_equivalent + 1;

					#add equivalent tab
					###print "tab_equivalent ", tab_equivalent;
					###print "space_equivalent ", space_equivalent;
					for i in range (tab_equivalent):
						first_line = first_line + "\t";
					
					#add equivalent space
					for i in range (space_equivalent):
						first_line = first_line + " ";
					
					#adding word to line
					first_line = first_line + wordlist[index];
					flag = 0;
					space = 0;
					tab_equivalent = 0;
					space_equivalent = 0;
				#end of if loop.
				
				#if flag is unset
				else:
					first_line = first_line + " " + wordlist[index];
				#end of else loop

			#end of else loop	

		#end of else loop

	#end of for loop.

	final_line = final_line + first_line;
	return final_line;
#end of function.
				

#main fucntion
def main():
        fin = open ("temp6.txt", "r+");
        fout = open ("temp7.txt", "w+");

        for line in fin:
                ###print line;
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
                filename_temp = "step7"+"/"+filename_temp;
                fout.write (filename_temp);
                fout.write ("\n");
                ###print filename_temp;
               
		#open the  files
		fin1 = open (filename_orig, "r+");
                fout1 = open (filename_temp, "w+");

		#create a list for storing the lines with cstyle error
		line_list = list();

		#to get line number from error file
		filename1 = "step6.txt"
		fin0 = open (filename1, "r+");
		
		#open the error file to get the line containing cstyle error
		for line2 in fin0:
        		flag = re.findall (filename_orig, line2);
        		if (len(flag) > 0):
                		flag1 = re.findall ("spaces instead of tabs", line2);
				flag2 = re.findall ("space instead of tab", line2);
				#create a search string.
				string = filename_str + ":" + " " + "(.+):";

				if (len(flag1) > 0 ) :
                      			line_number = re.findall (string, line2)  #file name is needed.
					if (len (line_number) > 0):
                        			line_list.append (int(line_number[0]));
				#end of if loop

				if (len(flag2) > 0 ) :
                      			line_number1 = re.findall (string, line2)  #file name is needed.
					if (len (line_number1) > 0):
                        			line_list.append (int(line_number1[0]));
                		#end if if loop for extracting line_number

        		#end of if loop

		#end of for loop
	
		#print "Total number of errors :- ", len(line_list);
		#print "--------------------------------------------------------------------------------------------";
		#indicate the line count in every file
                line_no = 0;
		#indicatet the length of line
                char_count = 0;

		for line1 in fin1:
			char_count = line_length (line1);
        		line_no = line_no + 1;
        		if ( line_no in line_list):
				first_line = space_instead_tab (line1);
               			#print "-------------------------spaces instead of tabs(general)----------------------------";
				#print "line_no ->", line_no, "lenght of line  ->", char_count ;
              			#print line1;
				#print first_line;	

				#if it contains the define word
				is_define = re.findall ("#define", first_line);
				if (len(is_define) > 0):
					first_line = space_instead_tab1 (first_line);
               				#print "---------------------spaces instead of tabs(#define)----------------------------";
					#print "line_no ->", line_no, "lenght of line  ->", char_count ;
              				#print line1;
					#print first_line;	
				#end of if loop

				#copy the corrected line to file
				fout1.write (first_line);
			#end of if loop
			
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
