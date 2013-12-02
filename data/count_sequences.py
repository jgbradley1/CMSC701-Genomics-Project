# this is just a quick script to count the number of sequence in a FAST-A file
import sys

seq_count = 0

if (len(sys.argv) > 1):
	file_name = sys.argv[1]
	
	total_line_length = 0.0;

	input_file = file(file_name, 'r')

	line_length = 0;
	for line in input_file:
		if line[0] == '>':
			seq_count+=1
			total_line_length += line_length
			line_length = 0
		else:
			line_length += (len(line) - 1)	# don't count the newline
	
	input_file.close()


	print file_name
	print 'Sequence Count: ' + str(seq_count);
	print 'Average Sequence Length: ' + str(total_line_length/seq_count)

else:
	print 'ERROR: must give file name in command line'