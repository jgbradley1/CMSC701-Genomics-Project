# this is just a quick script to count the number of sequence in a FAST-A file
import sys

count = 0

if (len(sys.argv) > 1):
	file_name = sys.argv[1]
	
	input_file = file(file_name, 'r')
	for line in input_file:
		if line[0] == '>':
			count+=1
	
	input_file.close()

	print 'Total number of sequences in ' + file_name + ': ' + str(count);

else:
	print 'ERROR: must give file name in command line'