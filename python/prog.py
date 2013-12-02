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


# parse out all the arguments
args = parser.parse_args();

ref_file_name = args.r;
query_file_name = args.q;
output_file_name = args.o;

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
ref_tree, ref_ids, max_ref = sort.sort_file(ref_file_name)
query_tree, query_ids, max_query = sort.sort_file(query_file_name)

'''
Initialize the table:
CAUTION: INDICES IN THE TABLE ARE ALL +1
'''
table = np.zeros((max_ref+1, max_query+1))
for i in range(len(table)):
    table[i][0] = i
for i in range(len(table[0])):
	table[0][i] = i


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

    for i, ref in enumerate(ref_tree):

		# <------------------------------------------------------ REMOVE THIS REMOVE THIS REMOVE THIS!!! !! ! !! !!!
    	if i > 3:
    		break

    	ref_id = ref_ids[i]

        for j, query in enumerate(query_tree):

            '''
            CAREFUL ABOUT THE CHANGE OF INDICES BETWEEN THE TABLE AND REF/QUERY!
            '''

            '''
            We start at the row that's at most THRESH away from the diagonal at column query_idx,
            which is where we have to start building the table
            '''
            start_row = max(0, query_idx - THRESH)

            '''
            We end at at most the row where the diagonal meets the end of the query + THRESH
            or at MOST the length of the reference
            '''
            end_row = min(len(ref), len(query) + THRESH)

            for row in range(start_row, end_row):

                if row < ref_idx:
                    start_col = max(query_idx, row - THRESH)
                else:
                    start_col = max(0, row - THRESH)
                end_col = min(len(query), row + THRESH + 1)

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

					ed = min(up, left, upleft)
					table[row+1][col+1] = ed


            '''
            Find the best edit distance:
            '''
            qlen = len(query)
            rlen = len(ref)
            best = qlen

            matched = False

            for row in range(max(qlen-1-THRESH, 0), min(qlen+THRESH, rlen)):
                ed = table[row+1][qlen]
                if ed < THRESH:
					matches[ref_id].append(query_ids[j])
					matched = True
					break

            if not matched:
	            for col in range(max(rlen-1-THRESH, 0), min(rlen+THRESH, qlen)):
	            	ed = table[rlen][col+1]
	            	if ed < THRESH:
	            		matches[ref_id].append(query_ids[j])
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

			'''
			Set indices for reference to where they should be next:
			'''
			if i == num_refs-1:
				break
			ref_idx = ref_tree_next[i]
			query_idx = 0


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