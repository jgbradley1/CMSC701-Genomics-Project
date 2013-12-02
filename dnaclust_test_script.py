import os
from subprocess import call
import timeit

num_data_points = 10;
num_total_references = 99	# confirmed by a counting script
num_total_queries = 1069684	# confirmed by a counting script


ref_file_name = 'data/reference.fna'
ref_file_name_prefix = 'data/reference_tmp_'

query_file_name = 'data/query.fna'
query_file_name_prefix = 'data/query_tmp_'


refs_per_group = num_total_references/num_data_points;
queries_per_group = num_total_queries/num_data_points;

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

		if (count-1) == refs_per_group*(i+1):
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

		if (count-1) == queries_per_group*(i+1):
			break
		f.write(line)

	input_file.close()
	f.close()
'''


################  Run Experiments  #####################

#comm = "call(['ls'," + "'-l'])"	# <-- this is a much simpler command to show how the call must be structured

# modifying the number of references
for i in range(num_data_points):
	comm = "call(['./dnaclust_linux_release3/dnaclust', '-i', 'data/query.fna', '-p', 'data/reference_tmp_" + i + ".fna', '-s', '0.01', '>', '../cluster'])"
	process_time = timeit.timeit(stmt=comm, setup="from subprocess import call", number=1)
	print 'Full Query File, # of Refs: ' + refs_per_group*(i+1) + '\tCPU Process Time: ' + str(process_time)

# modifying the number of queries
for i in range(num_data_points):
	comm = "call(['./dnaclust_linux_release3/dnaclust', '-i', 'data/query_tmp_" + i + ".fna', '-p', 'data/reference.fna', '-s', '0.01', '>', '../cluster'])"
	process_time = timeit.timeit(stmt=comm, setup="from subprocess import call", number=1)
	print 'Full Reference File, # of Queries: ' + queries_per_group*(i+1) + '\tCPU Process Time: ' + str(process_time)


# modifying the edit distance -- increasing in increments of 1%
for i in range(num_data_points):
	comm = "call(['./dnaclust_linux_release3/dnaclust', '-i', 'data/query.fna', '-p', 'data/reference.fna', '-s', '" + str(0.01*(i+1)) + "', '>', '../cluster'])"
	process_time = timeit.timeit(stmt=comm, setup="from subprocess import call", number=1)
	print 'Full Query File, Full Reference File, ED: ' + str(0.01*(i+1)) + '\tCPU Process Time: ' + str(process_time)



'''
# uncomment this portion of code when all temporary files can be stored on the local hard drive so 1000s of GB of data isn't generated

################  Remove Temporary Test Files  #####################
print 'Cleaning up temporary files...'
for i in range(num_data_points):
	ref_file_to_remove = 'data/reference_tmp_' + str(i) + '.fna'
	query_file_to_remove = 'data/query_tmp_' + str(i) + '.fna'

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
