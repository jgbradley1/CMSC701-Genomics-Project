import os
import timeit
#import argparse;
from subprocess import call


# num_total_references = 99		# total number of references in the main reference.fna file
# num_total_queries = 1069684	# total number of queries in the main query.fna file

'''
#describe what the program will do
parser = argparse.ArgumentParser(description='Makes test files to be run through DNAClust')

# add the maximum number of references to be used argument to the command line
parser.add_argument('-d',
					type=int,
					required=True,
                    help='number of output files to generate')

# add the maximum number of references to be used argument to the command line
parser.add_argument('-rs',
					type=int,
					required=True,
                    help='size of reference data chunks to produce')

# add the maximum number of references to be used argument to the command line
parser.add_argument('-qs',
					type=int,
					required=True,
                    help='size of query data chunks to produce')

# add the reference filename argument to the command line
parser.add_argument('-r',
					required=True,
                    help='reference filename')

# add the reference filename argument to the command line
parser.add_argument('-q',
					required=True,
                    help='query filename')

# parse out all the arguments
args = parser.parse_args();
'''
#python dnaclust_test_script.py -r data/reference_subset_20.fna -q data/query_subset_50000.fna -rs 5 -qs 5000 -d 5

#ref_file_name = args.r
ref_file_name = 'data/reference_subset_20.fna'

#ref_file_name_prefix = ref_file_name[:-4] + '_tmp_'
ref_file_name_prefix = 'data/reference_subset_20_tmp_'

#query_file_name = args.q
query_file_name = 'data/query_subset_50000.fna'

#query_file_name_prefix = query_file_name[:-4] + '_tmp_'
query_file_name_prefix = 'data/query_subset_50000.fna_tmp_'

#ref_chunk_size = args.rs;
ref_chunk_size = 5

#query_chunk_size = args.qs;
query_chunk_size = 5000;

#num_data_points = args.d
num_data_points = 5

#print '# of references: ' + str(max_refs)
#print '# of queries: ' + str(max_queries)
print '# of output files generated: ' + str(num_data_points)

'''
# uncomment this portion of code when the all the temporary files can be stored on the local hard drive
################  Create Temporary Test Files  #####################
# changing the number of references
for i in range(num_data_points):
	print 'Creating Ref File: ' + str(i)
	input_file = file(ref_file_name, 'r')
	f = file(ref_file_name_prefix + str(i) + '.fna', 'w')


	count = 0;
	# add refs to the file
	for line in input_file:
		if line[0] == '>':
			count+=1

		if (count-1) >= ref_chunk_size*(i+1):
			break
		f.write(line)

	input_file.close()
	f.close()

for i in range(num_data_points):
	print 'Creating Query File: ' + str(i)
	input_file = file(query_file_name, 'r')
	f = file(query_file_name_prefix + str(i) + '.fna', 'w')
	
	count = 0;
	# add queries to the file
	for line in input_file:
		if line[0] == '>':
			count+=1

		if (count-1) >= query_chunk_size*(i+1):
			break
		f.write(line)

	input_file.close()
	f.close()

'''


################  Run Experiments  #####################

# modifying the number of references
for i in range(num_data_points):
	comm = "call(['./dnaclust_linux_release3/dnaclust', '-i', '" + query_file_name + "', '-p', '" + ref_file_name_prefix + str(i) + ".fna', '>', '../cluster'])"
	process_time = timeit.timeit(stmt=comm, setup="from subprocess import call", number=1)
	print 'Full Query File, # of Refs: ' + str(ref_chunk_size*(i+1)) + '\tCPU Process Time: ' + str(process_time)
	#print '1Command: ' + comm

print
# modifying the number of queries
for i in range(num_data_points):
	comm = "call(['./dnaclust_linux_release3/dnaclust', '-i', '" + query_file_name_prefix + str(i) + ".fna', '-p', '" + ref_file_name + "', '>', '../cluster'])"
	process_time = timeit.timeit(stmt=comm, setup="from subprocess import call", number=1)
	print 'Full Reference File, # of Queries: ' + str(query_chunk_size*(i+1)) + '\tCPU Process Time: ' + str(process_time)
	#print '2Command: ' + comm

print
# modifying the edit distance -- increasing in increments of 1%
for i in range(num_data_points):
	comm = "call(['./dnaclust_linux_release3/dnaclust', '-i', '" + query_file_name + "', '-p', '" + ref_file_name + "', '-s', '" + str(1 - 0.01*(i+1))+ "' '>', '../cluster'])"
	process_time = timeit.timeit(stmt=comm, setup="from subprocess import call", number=1)
	print 'Full Query File, Full Reference File, ED: ' + str(0.01*(i+1)) + '\tCPU Process Time: ' + str(process_time)
	#print '3Command: ' + comm


'''
# uncomment this portion of code when all temporary files can be stored on the local hard drive so 1000s of GB of data isn't generated

################  Remove Temporary Test Files  #####################
print 'Cleaning up temporary files...'
for i in range(num_data_points):
	ref_file_to_remove = ref_file_name_prefix + str(i) + '.fna'
	query_file_to_remove = query_file_name_prefix + str(i) + '.fna'

	try:
		os.remove(ref_file_to_remove)
	except OSError:
		pass

	try:
		os.remove(query_file_to_remove)
	except OSError:
		pass

print 'Test Evaluation Complete'
'''