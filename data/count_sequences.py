# this is just a quick script to count the number of sequence in a FAST-A file
import sys
import argparse;

#describe what the program will do
parser = argparse.ArgumentParser(description='Creates a new sequence file with a specified number of sequence')

# add the reference filename argument to the command line
parser.add_argument('-f',
					required=True,
                    help='input filename')

# parse out all the arguments
args = parser.parse_args();

file_name = args.f


total_line_length = 0.0;
input_file = file(file_name, 'r')
seq_count = 0
line_length = 0;

for line in input_file:
	if line[0] == '>':
		seq_count+=1
		total_line_length += line_length
		line_length = 0
	else:
		line_length += (len(line) - 1)	# don't count the newline

input_file.close()


print 'File: ' + file_name
print 'Sequence Count: ' + str(seq_count);
print 'Average Sequence Length: ' + str(total_line_length/seq_count)