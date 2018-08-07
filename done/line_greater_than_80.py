#! /usr/bin/python
import re
#correct the line > 80 cstyle error.
#input :-
#	static int xsvnic_chan_init_xve_memb(xsvnic_channel_t *chanp, uint8_t chan_type, void *path);
#output :-
#	static int xsvnic_chan_init_xve_memb(xsvnic_channel_t *chanp, uint8_t chan_type,
#	    void *path);
#input :-
#	static void xsvnic_session_watch_cancel(xsvnic_t *xsvnicp, xsvnic_session_t *sessp);
#output :-
#	static void xsvnic_session_watch_cancel(xsvnic_t *xsvnicp, xsvnic_session_t
#	    *sessp);
#input :-
#                                __func__, xsvnicp->name, chanp->chan_conf.chan_type, state);
#output :-
#                                __func__, xsvnicp->name,
#                                    chanp->chan_conf.chan_type, state);
#input :-
#                xsvnic_taskq_delayed_dispatch(xsvnicp, xsvnic_chan_process_state_change,
#output :-
#                xsvnic_taskq_delayed_dispatch(xsvnicp,
#                    xsvnic_chan_process_state_change,
#input :-
#  	DPRINT(XSVNIC_SESS, "%s: chan disconnect: type %d, flags %x\n", VNIC_NAME(xsvnicp), chan_type, chanp->flags);
#output :-
#	DPRINT(XSVNIC_SESS, "%s: chan disconnect: type %d, flags %x\n",
#	    VNIC_NAME(xsvnicp), chan_type, chanp->flags);
#input :-
#                                cmn_err(CE_WARN, "%s: couldn't reclaim all buffers\n",
#output :-
#                                cmn_err(CE_WARN, "%s: couldn't reclaim all
#                                    buffers\n",
#input :-
#                if (!(chanp->flags & XSVNIC_CHAN_FLAGS_STATE_ERR_EV) && (!atomic_read(&chanp->sessp->disconn))) {
#output :-
#                if (!(chanp->flags & XSVNIC_CHAN_FLAGS_STATE_ERR_EV) &&
#                    (!atomic_read(&chanp->sessp->disconn))) {



#It slices the line till 80 and copy the remaining to next line adding 4 space to it in beginning
#with same alignment as before.
#input :-
#               * xtl should possibly simply return error in such cases rather than trying
#output :-
#               * xtl should possibly simply return error in such cases rather
#               * than trying
#input :-
#                       chanp->flags &= ~(XSVNIC_CHAN_FLAGS_STATE_ERR_EV|XSVNIC_CHAN_FLAGS_DISCONN_EV);
#output :-
#                       chanp->flags &=
#                           ~(XSVNIC_CHAN_FLAGS_STATE_ERR_EV|XSVNIC_CHAN_FLAGS_DISCONN_EV);

#author :- Raj Kamal <raj.x.kamal@oracle.com>
#-------------------------------------Begin------------------------------------------------------#
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

        #print count, space_count, tab_count;
        tab_count = count / 8;
        space_count = count % 8;

        return count, space_count, tab_count;
#end of function

#find the word causing the split, exceeding 80 characters
def findword(line1, count, index):
        word_list = line1.split(",");
        word ="";
        #print word_list;
        #print "count->", count;

        if (index == 0):
                count = count + 8 * len(re.findall("\t", word_list[0]));

        tab = count / 8;
        ##print "count->", count;
        #print "\n";
        word_list[0] = word_list[0].lstrip("\t");

        for i in range(len(word_list)):
                count = count + len(word_list[i]) + 1;
                if (count < 80):
                        word = word_list[i];
                else:
                        break;
        #end of for loop

        word = word+",";
        #print "word before split :-> ", word;

        return word, tab;
#end of function;


#split the line into two lines if the length is greater than 80
def split_lines (line1 , count, tab_count, space_count , index):
        first_line = "";
        second_line = "";

        if (index == 0):
                count = count + 8;

        word, tab = findword (line1, count, index);
        i1 = line1.find(word) + len(word);
        #print "word->", word, " index: ", i1;
        #print "line1:-> ", line1[ :i1+1 ];
        #print "line2:-> ", line1[ i1+1: ];

        first_line = line1[ :i1+1].rstrip() + "\n";
        temp_line = line1[i1+1:];
        temp_line = temp_line.lstrip();
        temp_line = temp_line.rstrip("\n");
        temp_line = temp_line.rstrip();
        temp_line = temp_line + "\n";
        #print temp_line;

        if (index == 1):
                for i in range(tab + 1):
                        second_line = second_line + "\t";
        else:
                for i in range(tab - 1 ):
                        second_line = second_line + "\t";
        #end of else loop

        #second_line = second_line + "    " + temp_line ;
        second_line = second_line + temp_line ;


        return first_line, second_line;
#end of function.

#find the word from where spliting is done.
def findword1(line1 ):
        #split by space
        word_list = line1.split(" ");
        word ="";
        ##print word_list;
        ##print "count->", count;
        ##print "\n";
        tab_count = re.findall ("\t", word_list[0]);
        count = len (tab_count) * 8;
        word_list[0] = word_list[0].lstrip("\t");

        for i in range(len(word_list)):
                #first word so no space count
                if (i == 0):
                        count = count + len(word_list[i]);
                else :
                        count = count + len(word_list[i]) + 1;

                if (count <= 80):
                        word = word_list[i];
                else:
                        break;
        #end of for loop
        ##print "word before split :-> ", word;
        return word
#end of function;


#split lines into two lines if line is comment.
def splitcomment22lines (line1 ):
        first_line = "";
        second_line = "";
        count = 0;

        word = findword1 (line1);

        wordlist = line1.split(" ");

        tab_count = re.findall ("\t", wordlist[0]);
        count = count + len (tab_count) * 8;

        wordlist[0] = wordlist[0].lstrip("\t");

        #set alignment
        for index in range(len(tab_count)):
                first_line = first_line + "\t";
                second_line = second_line + "\t";

        #add extra "*", so that second list is also comment
        second_line = second_line + " * ";

        for index in range(len(wordlist)):
                #first word so no space count
                if (index == 0):
                        count = count + len (wordlist[index]);
                else:
                        count = count + len (wordlist[index]) + 1; #space count

                if (count <= 80 ):
                        first_line = first_line + wordlist[index] + " ";
                else:
                        second_line = second_line + wordlist[index] + " ";
        #end of for loop;

        first_line = first_line.rstrip(" ");
        first_line = first_line.rstrip("\t");
        first_line = first_line.rstrip("\n");

	second_line = second_line.rstrip(" ");
        second_line = second_line.rstrip("\t");
        second_line = second_line.rstrip("\n");

        return first_line, second_line;
#end of function.

#split lines into two lines if line is scope, expression, statement.
def splitline22lines (line1):
        first_line = "";
        second_line = "";
        count = 0;

        word = findword1 (line1);

        wordlist = line1.split(" ");

        tab_count = re.findall ("\t", wordlist[0]);
        count = count + len (tab_count) * 8;

        wordlist[0] = wordlist[0].lstrip ("\t");

        #set alignment
        for index in range(len(tab_count)):
                first_line = first_line + "\t";
                second_line = second_line + "\t";

        #add extra 4 spaces for second line
        second_line = second_line + "    ";

	for index in range(len(wordlist)):
                #first word so no space count
                if (index == 0):
                        count = count + len (wordlist[index]);
                else:
                        count = count + len (wordlist[index]) + 1; #space count
                if (count <= 80 ):
                        first_line = first_line + wordlist[index] + " ";
                else:
                        second_line = second_line + wordlist[index] + " ";
        #end of for loop;

        first_line = first_line.rstrip(" ");
        first_line = first_line.rstrip("\t");
        first_line = first_line.rstrip("\n");

        second_line = second_line.rstrip(" ");
        second_line = second_line.rstrip("\t");
        second_line = second_line.rstrip("\n");

        return first_line, second_line;
#end of function.


#remove the comma or semicolon followed by non-blank
def line_greater_than_80 (line1):
	first_line = line1;
	#return the line 
	return first_line;
#end of function

#main fucntion
def main():
        fin = open ("temp3.txt", "r+");
        fout = open ("temp4.txt", "w+");

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
                filename_temp = "step4"+"/"+filename_temp;
                fout.write (filename_temp);
                fout.write ("\n");
                ####print filename_temp;

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
                                flag1 = re.findall ("line > 80", line2);
                                #create a search string.
                                string = filename_str + ":" + " " + "(.+):";

                                if (len(flag1) > 0 ) :
                                        line_number = re.findall (string, line2)  #file name is needed.
					if(len (line_number) > 0):
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
				

			#if the line has line > 80 cstyle error
			if ( line_no in line_list):
				 #find if line is comment.
                                is_comment = 0;
                                temp_line = line1.lstrip("\t");
                                temp_line = temp_line.lstrip(" ");
                                if(temp_line[0] == "*" ):
                                        is_comment = 1;

                                #one line of comment is splitted into two lines of comment
                                if(is_comment == 1):
                                        first_line, second_line = splitcomment22lines ( line1 );
                                        #print "-----------------------line > 80 (comment)--------------------";
                                        #print "line_number -->", line_no, "lenght of line ->", char_count;
                                        #print line1;
                                        #print first_line + "\n";
                                        #print second_line + "\n" ;
                                        fout1.write (first_line);
                                        fout1.write ("\n");
                                        fout1.write (second_line);
                                        fout1.write ("\n");
				#end of if loop

                                #line is splitted into two lines
                                else:
                                        first_line, second_line = splitline22lines (line1);
                                        #print "-----------------------line > 80 (comnmen)--------------------";
                                        #print "line_number -->", line_no, "length of line ->", char_count;
                                        #print line1;
                                        #print first_line + "\n";
                                        #print second_line + "\n";
                                        fout1.write (first_line);
                                        fout1.write ("\n");
                                        fout1.write (second_line);
                                        fout1.write ("\n");
				#end of else loop.

				#first_line, second_line = line_greater_than_80 (line1);
				##print "--------------------line > 80-----------------------";
				##print "line_no-->", line_no, "length of line -->", char_count;
                                ##print line1;
                                ##print first_line;
				##print second_line;

                                #copy the corrected line to file
                                #fout1.write (first_line);
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


