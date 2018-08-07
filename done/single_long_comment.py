#! /usr/bin/python
import re, os

#input :-
#	state_update = xsvnic_chan_state_update(chanp, 0);      /* reports state updates */
#output :-
#	/* reports state updates */
#	state_update = xsvnic_chan_state_update(chanp, 0);
#input :-
#	/* XXX - do not grab chan lock as in rear situations, an old pending completion can
#output :-
#       /* XXX - do not grab chan lock as in rear situations, an old pending	
#	 * completion can
#input :-
#			/* TX chan of path is up, flush all queued packets in TX path*/
#output :-
#                       /* TX chan of path is up, flush all queued packets in
#			 * TX path*/
# author :- Raj Kamal <raj.x.kamal@oracle.com>
#------------------------------------------------------Begin----------------------------------------------#

#find the actual count of characters in line1
def line_length ( line1):
	count = 0;
	for character in line1:
		if (character == '\t'):
			temp_count = count % 8;
			temp_count = 8 - temp_count;
			count = count + temp_count;
		elif (character == "//"):
			comment_index = count;
			count = count + 1;
		else:
			count = count + 1;
	#end of loop for counting characters.
	return count;
#end of fucntion 	


#find the open index of comment.
def open_index (line1, index):
	count = 0;
	i = 0;
	c = '';
	prev_count = 0;
	for character in line1:
		if (character == '\t'):
			temp_count = count % 8;
			temp_count = 8 - temp_count;
			count = count + temp_count;
		elif (character == "/"):
			c = character;
			count = count + 1;
			prev_count = count; 
		elif (character == "*"):
			count = count + 1;
			d = c + character;
			if(d == "/*"):
				if(prev_count + 1 == count):
					i = i+1;
					if( i == index):
						return count;
						break;
		else:
			count = count + 1;
	#end of for loop.
#end of function.


#find the close index of comment.
def close_index (line1, index):
	count = 0;
	i = 0;
	c = '';
	prev_count = 0;
	for character in line1:
		#print "character ", character;
		if (character == '\t'):
			temp_count = count % 8;
			temp_count = 8 - temp_count;
			count = count + temp_count;
		elif (character == "*"):
			c = character;
			count = count + 1;
			prev_count = count;
		elif (character == "/"):
			count = count + 1;
			d = c + character;
			if ( d == "*/"):
				if(prev_count + 1 == count):
					i = i + 1;
					if (i == index):
						return count;
						break;
		else:
			count = count + 1;
#end of fucntion.	
			
#extract the comment.
def getcomment(line1, orig_start_index, orig_end_index, bit):
	count = 0;
	flag = 0;
	comment_line='';
	#half comment /*-----
	if (bit == 0):
		for character in line1:
			if (character == '\t'):
				temp_count = count % 8;
				temp_count = 8 - temp_count;
				count = count + temp_count;
				#if ( flag == 1):
				#	comment_line = comment_line + character;
			else:
				count = count + 1;
				if ((count >= orig_start_index)):
					comment_line = comment_line + character;
	#full comment /*---*/
	else :
		for character in line1:
			if (character == '\t'):
				temp_count = count % 8;
				temp_count = 8 - temp_count;
				count = count + temp_count;
				#if ( flag == 1):
				#	comment_line = comment_line + character;
			else:
				count = count + 1;
				if ((count >= orig_start_index) and (count <= orig_end_index)):
					comment_line = comment_line + character;
	#print comment_line;
	return comment_line;
#end of function.
		
#extract the line removing the comment.
def getline(line1, sindex, eindex, len1, space):
	tab_count = space/8;
	space_count = space % 8;
	#count = sindex;
	count = 0;
	flag = 0;
	line = '';
	if (tab_count > 0):
		for i in range(tab_count):
			line = line + "\t";
	if (space_count > 0):
		for i in range(space_count):
			line = line + " ";
	#print "here";
	for character in line1:
		if ((character == '\t')):
			temp_count = count % 8;
			temp_count = 8 - temp_count;
			count = count + temp_count;
			if (( count >= sindex) and (count < eindex)):
			 	line = line + character;
			if (count > eindex):
				break;
		else:
			count = count + 1;
			if (( count >= sindex) and (count < eindex)):
				line = line + character;
			if (count > eindex):
				break;
		
	len1 = len1 - count;
	#print "len1 -> ", len1;
	#print "space :", space;
	return line, len1;
#end of function.

#find the word that cause the split of comment.	
def findword (comment_line, orig_start_index, orig_end_index, substring ):
	word_list = comment_line.split();
	count = orig_start_index ;
	word = '';
	#print word_list;
	for index in range(len(word_list)):
		count = count + len(word_list[index]) + 1 ; #one for space.
		if (count < 80):
			word = word_list[index];
			substring = substring + word + " ";
			#print word , "->", count; 
			#word = word + word_list[index] + " ";
		else:
			count = count - len(word_list[index]) - 1 ; #one for space.
			#print word , "->", count; 
			break;
	#print "--", count; 
	#print word;
	#print substring;
	#index = comment_line.find (word, 0, len(comment_line));
	#print "here" ,comment_line[:line];
	#return comment_line[:index];
	return count;

#find the length of comment_line.
def find_length (comment_line, space, tab):
	count = 0;	
	for i in range (tab):
		count = count + 8;
	for i in range (space):
		count = count + 1;
	for character in comment_line:
		count = count + 1;
	return count;


#split comment line into 3 lines.
def split23comment (comment_line, space, tab):
	first_line = "";
	second_line = "";
	third_line = "";
	count = 0;
	temp_line = "";
	for i in range (tab):
		temp_line = temp_line + "\t";
		count = count + 8;
	for i in range (space):
		temp_line = temp_line + " ";
		count = count + 1;
	comment_line = comment_line.lstrip("\t");
	comment_line = comment_line.lstrip();
	comment = comment_line.split();
	#print "list", comment;
	index = 0;
	for i in range(len(comment)):
		count = count + len(comment[i]) + 1; #1 for space
		if (count <= 80):
			word = comment[i];
			first_line = first_line +  comment[i] + " ";
		else :
			second_line = second_line + comment[i] + " ";
	second_line = second_line.rstrip();
	first_line = first_line.rstrip() + "\n";
	if (second_line == "*/"):
		second_line = temp_line + " " + second_line + "\n";
		third_line = "";
	else:
		second_line = second_line.rstrip("*/");
		second_line = second_line.rstrip();
		second_line = temp_line + " " + "*" + " " + second_line + "\n";
		third_line = temp_line + " " + "*/";
		third_line = third_line + "\n";
	first_line = temp_line + first_line;
	return first_line, second_line, third_line;
#end of function;

#split comment into 2 lines of comment
def split22comment (comment_line, space, tab):
	first_line = "";
	second_line = "";
	temp_line="";
	count = 0;
	for i in range (tab):
		temp_line = temp_line + "\t";
		count = count + 8;
	for i in range (space):
		temp_line = temp_line + " ";
		count = count + 1;
	comment_line = comment_line.lstrip("\t");
	comment_line = comment_line.lstrip();
	comment = comment_line.split();
	#print "list", comment;
	index = 0;
	for i in range(len(comment)):
		count = count + len(comment[i]) + 1; #1 for space
		if (count <= 80):
			word = comment[i];
			first_line = first_line + comment[i] + " ";
		else :
			second_line = second_line + comment[i] + " ";
	second_line = second_line.rstrip();
	first_line = temp_line + first_line.rstrip() + "\n";
	if (second_line == "*/"):
		second_line = temp_line + " " + second_line + "\n";
	else:
		second_line = temp_line + " " + "*" + " " + second_line + "\n";
	return first_line, second_line;
#end of function;
	
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

#set the comment removing line.
def setcomment (comment, space, tab):
	line = "";
	if ( tab > 0):
		for i in range (tab):
			line = line + "\t";
	if (space > 0):
		for i in range (space):
			line = line + " ";
	comment = comment.lstrip (" ");
	comment = comment.lstrip ("\t");
	comment = comment.rstrip (" ");
	comment = comment.rstrip ("\t");
	comment = comment.rstrip ("\n");
	line = line + comment + "\n";
	return line;
#end of function

#set the line, removing comment
def setline (line1):
	line="";
	index = line1.find("/*");
	line = line + line1[:index];
	line = line.rstrip ("\t");
	line = line.rstrip (" ");
	line = line.rstrip ("\n");
	line = line + "\n";
	return line;
#end of function
			

#Main program starts here.	
#open file name	
def main():
	fin = open ("temp2.txt", "r+");
	fout = open ("temp3.txt", "w+");
	for line in fin:
		#extract the original filename
		line = line.lstrip (" ");
		line = line.lstrip ("\t");
		line = line.rstrip (" ");
		line = line.rstrip ("\t");
		line = line.rstrip ("\n");
		#print line
		filename_orig = line;
		#make the duplicate of the original of filename
		temp_name = re.findall (".*/(.*)", line);
		filename_temp = str (temp_name[0]);
		filename_temp = filename_temp.strip (" ");
		filename_temp = filename_temp.strip ("\t");
		filename_temp = filename_temp.strip ("\n");
		filename_temp = "step3"+"/"+filename_temp;
		fout.write (filename_temp);
		fout.write ("\n");
		#print filename_temp;
		fin1 = open (filename_orig, "r+");
		fout1 = open (filename_temp, "w+");

		#indicate the line count in every file
		line_no = 0;
		
		#iterate through the file line by line
		for line1 in fin1:
			line_no = line_no + 1;

			#check if line is comment.
			is_comment = line1.find("/*");

			#keeps record of number of characters.
			char_count = 0;

			#if flag 0 then copy the line directly
			flag = 0;
	
			#if line contains the comment.  /*----*/, /*----, ----- /*---*/
			#find the index of opening and closing comment symbol
			if(is_comment >= 0 ):
				#print "---------------------------------------------------------------------";
				#print "-", line_no;
				#print line1;
				#get the start and end index of comment in the line
				start_index = line1.find("/*");
				end_index = (line1[start_index: ]).find("*/");
				end_index = start_index + end_index + 2;
				
				#extract only the comment line
				comment = line1[start_index:end_index];	
				#print comment
					
				#find length of comment 
				comment_length = len(comment);
	
				#find actual length of line
				char_count = line_length (line1);
	
				#length greater than 80, we need to do split of lines
				if(char_count > 80):
					#set flag
					flag = 1;
					list1 = re.findall(r"/\*", line1);
					#print list1;	
					#print line_no,"-",  char_count, "-", comment_length;
					#print line1;
					#print line1[start_index:end_index];

					#exact start index of comment.
					orig_start_index = open_index (line1, 1)-1;

					#exact end end of comment.
					orig_end_index = close_index (line1, 1);
					#print "start ", orig_start_index;
					#print "end ", orig_end_index;
					substring = '';

					#extract comment
					#comment like this /*-----
					if (orig_end_index > 0):
						comment_line = getcomment(line1, orig_start_index, orig_end_index, 1);
					#if comment like this /*----*/
					else :
						comment_line = getcomment(line1, orig_start_index, orig_end_index, 0);

					#get the index of word causing split
					index = findword (comment_line, orig_start_index, orig_end_index, substring );
					#print "--", comment_line;
						
					#gives the number or spaces at the beginning of line
					space, tab = getspacetab(line1);
						
					#extract the comment out of line
					comment_line = setcomment(comment_line, space , tab);
						
					#line without comment
					line_t = setline (line1);
						
					#put in the file.
					#print comment_line;
					#print line;
					#remove all escape character from right of comment line
					comment_line = comment_line.rstrip();
					comment_line = comment_line.rstrip("\t");
					comment_line = comment_line.rstrip("\n");
	
					#removes all escape characters from right of line after removing comment
					line_t = line_t.rstrip();
					line_t = line_t.rstrip("\t");
					line_t = line_t.rstrip("\n");
					
					#copy the comments into file if comment exist.
					#length of comment line greater then zero
					if (len (comment_line) > 0):
						len1 = find_length (comment_line, space, tab);
						
						#if lenght of comments is greater than 80 we need to split
						if (len1 > 80):
							#print "------------------------------------------------------------";
							#print char_count, "==", len1, "->", line_no;
							#print line1;
							is_open = re.findall ("/\*", comment_line);
							is_close = re.findall ("\*/", comment_line);
							#print is_open, "->", is_close;

							#if comment is of type /*---*/
							if (len(is_close) > 0):
								is_start = line1.find ("/*");
								first_line, second_line, third_line = split23comment (comment_line, space, tab );
								if (third_line == ""):
									#print "1.", first_line;
									#print "2.", second_line;
									fout1.write (first_line);
									fout1.write (second_line);
								else:
									#print "1.", first_line;
									#print "2.", second_line;
									#print "3.", third_line;
									fout1.write (first_line);
									fout1.write (second_line);
									fout1.write (third_line);
							#end of if loop
							
							#if comment is of type /*----
							else :
								first_line, second_line = split22comment (comment_line, space, tab);
								if (second_line == ""):
									#print "1.", first_line;
									#print "2.", second_line;
									fout1.write (first_line);
									#fout1.write (second_line);
								else:
									#print "1.", first_line;
									#print "2.", second_line;
									fout1.write (first_line);
									fout1.write (second_line);
							#end of else loop.
						#if comment din need to be splited then just copy
						else:
							#print "---------------------not splitted comment---------------------------------";
							#print char_count, "==", len1, "->", line_no;
							#print line1;
							#print comment_line, "\n";
							fout1.write(comment_line);
							fout1.write("\n");
						#end of else loop 					
					#end of copying the comment to file

					#Now copy the line after extracting the comment to file.
					if (len (line_t) > 0):
							#print line_t, "\n";
							fout1.write(line_t);
							fout1.write("\n");
					#end of if loop 
				#end of if loop
			#end of if loop

			#line and line along with comments is less than 80 then copy as they are. 
			if (flag == 0):
				#print "+", line_no;
				fout1.write (line1);
			#end of if loop

		#end of for loop for iterrating through the files.
		fin1.close();
		fout1.close();		

	#end of for loop
	fin.close();
	fout.close();
#end of function .		


#---------------------------------------------------------------------program starts here-----------------------------------------#
main();
#end of program	
