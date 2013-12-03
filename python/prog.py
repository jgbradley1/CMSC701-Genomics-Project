'''






To-do list:

1.) Document code
2.) Write up how it works, add figures, and write up how to run it (include assumptions, clearly!)
3.) Run experiments in running time and display the figures in the writeup
4.) Run some test cases
5.) Tune-ups
6.) Turn it in before midnight











'''


import argparse;
import radix_sort as sort;
import numpy as np

#describe what the program will do
parser = argparse.ArgumentParser(description='Finds all query reads that match a reference read set.');

# add the edit distance argument to the command line
parser.add_argument('-k',
					type=int,
					default=2,
					required=True,
                    help='edit distance');

# add the reference filename argument to the command line
parser.add_argument('-r',
					required=False,	# will change this later when program is complete
					default='../data/reference.fna',
                    help='reference filename');

# add the query filename argument to the command line
parser.add_argument('-q',
					required=False,	# will change this later when program is complete
					default='../data/query.fna',
                    help='query filename');

# add the output filename argument to the command line
parser.add_argument('-o',
					required=False, # will change this later when program is complete
					default='output',
                    help='output filename');

# add the output filename argument to the command line
parser.add_argument('-maxr',
					type=int,
					required=False, # will change this later when program is complete
					default='-1',
                    help='Max number of references to read');

# add the output filename argument to the command line
parser.add_argument('-maxq',
					type=int,
					required=False, # will change this later when program is complete
					default='-1',
                    help='Max number of queries to read');


# parse out all the arguments
args = parser.parse_args();

ref_file_name = args.r;
query_file_name = args.q;
output_file_name = args.o;
maxr = args.maxr
maxq = args.maxq

# For now, print out program information for debugging purposes
print 'Reference File: ' + ref_file_name
print 'Query File: \t' + query_file_name
print 'Output File: \t' + output_file_name
print 'Edit Distance: \t' + str(args.k)
print '\n'



'''
This is the max edit distance we want to find:
Return sequences with edit distance LESS THAN OR EQUAL TO the threshhold
'''
THRESH = args.k



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
Import and sort reference and query data:
'''
print "Importing and sorting..."
ref_tree, ref_ids, max_ref = sort.sort_file(ref_file_name, maxr)
query_tree, query_ids, max_query = sort.sort_file(query_file_name, maxq)


print "Initializing table..."
'''
Initialize the table:
CAUTION: INDICES IN THE TABLE ARE ALL +1
'''
table = np.zeros((max_ref+1, max_query+1))
for i in range(len(table)):
    table[i][0] = i
for i in range(len(table[0])):
	table[0][i] = i


print "Preprocessing..."
'''
Preprocessing:
Make implicit tree by storing for each sequence i the position j in sequence i+1 where a mismatch occurs
'''
ref_tree_next = {}
for i in range(len(ref_tree)-1):
    seq1 = ref_tree[i]
    seq2 = ref_tree[i+1]
    j = 0
    l1 = len(seq1)
    l2 = len(seq2)
    while (j < l1 and j < l2 and seq1[j]==seq2[j]):
        j += 1
    ref_tree_next[i] = j

query_tree_next = {}
for i in range(len(query_tree)-1):
    seq1 = query_tree[i]
    seq2 = query_tree[i+1]
    j = 0
    l1 = len(seq1)
    l2 = len(seq2)
    while (j < l1 and j < l2 and seq1[j]==seq2[j]):
        j += 1
    query_tree_next[i] = j


print "Building table..."
print "Number of references = ", len(ref_tree)

num_refs = len(ref_tree)
num_queries = len(query_tree)

'''
Temporary variable to keep track of the matches being found:
'''
matches = {x:[] for x in ref_ids}

'''
Build the table (from the beginning):
'''
def build_table():

	ref_idx = 0
	query_idx = 0

	i=0
	while i < num_refs:

		ref = ref_tree[i]

		ref_id = ref_ids[i]

		j = 0
		while j < num_queries:

			#print "Reference:", ref, ref_id


			query = query_tree[j]

			#print "Query", query, query_ids[j]

			'''
			CAREFUL ABOUT THE CHANGE OF INDICES BETWEEN THE TABLE AND REF/QUERY!
			'''

			'''
			We start at the row that's at most THRESH away from the diagonal at column query_idx,
			which is where we have to start building the table
			'''
			lim1 = query_idx - THRESH
			start_row = lim1 if lim1 > 0 else 0

			'''
			We end at at most the row where the diagonal meets the end of the query + THRESH
			or at MOST the length of the reference
			'''
			lim1 = len(ref)
			lim2 = len(query) + THRESH
			end_row = lim1 if lim1 < lim2 else lim2

			'''
			For later - should I skip this query?
			'''
			skip_query = False

			for row in range(start_row, end_row):

				if row < ref_idx:
					'''
					Add comments here
					'''
					lim1 = query_idx
					lim2 = row - THRESH
					start_col = lim1 if lim1 > lim2 else lim2
				else:
					lim1 = row - THRESH
					start_col = lim1 if lim1 > 0 else 0


				'''
				The min end column is...
				'''
				lim1 = len(query)
				lim2 = row + THRESH + 1
				end_col = lim1 if lim1 < lim2 else lim2

				'''
				This is the min edit dist in this row. If it is > Thresh we can stop.
				'''
				row_ed_min = THRESH

				for col in range(start_col, end_col):

					'''
					If the cell directly above (row, col) has col < ?
					'''
					if col > row - 1 + THRESH:
						up = THRESH + 1
					else:
						up = table[row][col+1] + 1

					'''
					If the cell directly to the left of (row, col) has col < ?
					'''
					if col-1 < row - THRESH:
						left = THRESH + 1
					else:
						left = table[row+1][col] + 1


					'''
					Take the score in the cell above and to the left plus 1 if there's a mismatch:
					'''
					pen = 0 if ref[row] == query[col] else 1
					upleft = table[row][col] + pen

					'''
					Compute the minimum predecessor
					'''
					ed = up
					if left < ed:
						ed = left
					if upleft < ed:
						ed = upleft
					table[row+1][col+1] = ed

					if ed < row_ed_min:
						row_ed_min = ed

				'''
				If the minimum edit dist in the current row is > THRESH, there is no way of
				aligning the current ref/query with an acceptable edit distance:
				'''
				if row_ed_min > THRESH:
					skip_query = True # Do we skip the 'find best ED' code below?
					print '\t', "Ran into impassible row"
					if j == num_queries-1:
						j += 1
						break
					skip_all_queries = False
					while (query_tree_next[j] >= end_col):
						j += 1

						if j == num_queries-1:
							skip_all_queries = True
							break

					if skip_all_queries:
						j += 1
						break

					query_idx = query_tree_next[j]
					j += 1


			if not skip_query:

				'''
				Find the best edit distance:
				'''
				qlen = len(query)
				rlen = len(ref)
				best = qlen

				matched = False

				for row in range(max(qlen-1-THRESH, 0), min(qlen+THRESH, rlen)):
				    ed = table[row+1][qlen]
				    if ed <= THRESH:
						matches[ref_id].append(query_ids[j])
						matched = True
						break

				if not matched:
				    for col in range(max(rlen-1-THRESH, 0), min(rlen+THRESH, qlen)):
				    	ed = table[rlen][col+1]
				    	if ed <= THRESH:
				    		matches[ref_id].append(query_ids[j])
				    		matched = True
				    		break

				'''
				Set indices to where they should be next:
				'''
				if j == num_queries-1:
					break
				query_idx = query_tree_next[j]
				'''
				For a given reference, we can say we've seen the reference up to the end for all queries:
				'''
				ref_idx = len(ref)

				j += 1



		'''
		Set indices for reference to where they should be next:
		'''
		if i == num_refs-1:
			break
		ref_idx = ref_tree_next[i]
		query_idx = 0

		i += 1


# TEST RUN: python prog.py -k=1 -r=../testdata/reference.fna -q=../testdata/query.fna


'''
Build the table:
'''
build_table()

outfile = open(output_file_name, 'w')
for r_id in matches:
	line = r_id
	q_ids = matches[r_id]
	for q_id in q_ids:
		line += " " + q_id
	outfile.write(line + '\n')