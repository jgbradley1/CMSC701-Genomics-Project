import pdb # python debugger
import argparse
import radix_sort as sort
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
					default='ref.fna',
                    help='reference filename');

# add the query filename argument to the command line
parser.add_argument('-q',
					required=False,	# will change this later when program is complete
					default='query.fna',
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
#################################  Start of the actual program code  ##################################
'''


'''
This is the max edit distance we want to find:
Return sequences with edit distance LESS THAN OR EQUAL TO the threshhold
'''
THRESH = args.k


'''
# This code will be used to import and sort the ref and query files once debugging is done - for now, skip
# this step and use the test cases below
ref_tree = sort.sort_file(ref_file_name);
query_tree = sort.sort_file(query_file_name);
'''


'''
Assuming the reference and query are already in sorted order:
'''
#ref_tree = ["aaaaaa", "aabbbb", "aabbcc", "aabbcd", "abbbbb", "bcccdd", "bcdddd"]
#query_tree = ["aaa", "aaaaaa", "aaab", "abbc", "accc", "baaaa", "bccaa", "bcd"]

ref_tree = ['abc']
query_tree = ['abbcd']

#ref_tree = ['abc', 'abde', 'bcde']
#query_tree = ['aabcd', 'abbcd', 'abcde', 'bbcde', 'bcdef']



'''
Initialize the table:
Right now, use a numpy array, and assume we have the length of the longest sequence in ref/query
'''
max_length = 5
table = np.zeros((max_length+1, max_length+1))
for i in range(len(table)):
    table[i][0] = i
    table[0][i] = i


'''
Preprocessing:
Make implicit tree by storing for sequence i the position j in sequence i+1 where a mismatch occurs
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
matches = {x:[] for x in ref_tree}


print 'Reference Next Index'
for i in range(num_refs-1):
	print 'Ref: ' + ref_tree[i] + '\tNext Idx: ' + str(ref_tree_next[i])
print 'Ref: ' + ref_tree[num_refs-1] + '\tNext Idx: none'

print 'Query Next Index'
for i in range(num_queries-1):
	print 'Query: ' + query_tree[i] + '\tNext Idx: ' + str(query_tree_next[i])
print 'Query: ' + query_tree[num_queries-1] + '\tNext Idx: none'
print '\n'

'''
Build the table (from the beginning):
'''
def build_table():
    ref_idx = 0
    query_idx = 0

    for i, ref in enumerate(ref_tree):
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

<<<<<<< HEAD
            #print "Start row = ", start_row+1
            #print "End row = ", end_row+1
=======

            print 'ref= ' + ref + '\ti= ' + str(i)
            print 'query= ' + query + '\tj= ' + str(j)
            print 'start_row= ', start_row
            print 'end_row= ', end_row
            print 'Ref Idx= ' + str(ref_idx)
            print 'Query Idx= ' + str(query_idx)
            print 'Row Focus=[' + str(start_row) + '-' + str(end_row-1) + ']'
>>>>>>> 0851d4077f40a3802f2612a804a08154c1d65761

            for row in range(start_row, end_row):

                if row < ref_idx:
                    start_col = max(query_idx, row - THRESH)
                else:
                    start_col = max(0, row - THRESH)
                end_col = min(len(query), row + THRESH + 1)

<<<<<<< HEAD
                #print "\tstartcol = ", start_col+1
                #print "\tendcol = ", end_col+1
=======
                print '    Col Focus=[' + str(start_col) + '-' + str(end_col-1) + ']'
>>>>>>> 0851d4077f40a3802f2612a804a08154c1d65761


<<<<<<< HEAD
                    #print '\t\t', row+1, col+1
=======
                for col in range(start_col, end_col):
>>>>>>> 0851d4077f40a3802f2612a804a08154c1d65761

                    print '\t\trow=' + str(row) + ' col=' + str(col)

                    pen = 0 if ref[row] == query[col] else 1

                    '''
                    If the cell directly ABOVE (row, col) is outside the main diagonal
                    '''
                    if col > row - 1 + THRESH:
                        up = THRESH + 1
                    else:
                        up = table[row][col+1] + 1

                    '''
                    If the cell directly to the LEFT of (row, col) is outside of the main diagonal
                    '''
                    if col-1 < row - THRESH:
                        left = THRESH + 1
                    else:
                        left = table[row+1][col] + 1

                    upleft = table[row][col] + pen

<<<<<<< HEAD
                    #print '\t\t\t', left, upleft, up
=======
                    print '\t\t\tL=' + str(left) + ' UL=' + str(upleft) + ' U=' + str(up)
>>>>>>> 0851d4077f40a3802f2612a804a08154c1d65761

                    ed = min(up, left, upleft)
                    print '\t\t\ttable[' + str(row+1) + '][' + str(col+1) + ']=' + str(ed)
                    table[row+1][col+1] = ed

            print 'test message: ' + str(end_row) + ' ' + str(end_col)
            '''
            Find the best edit distance:
            '''
            qlen = len(query)
            rlen = len(ref)
            best = qlen

<<<<<<< HEAD
            for row in range(max(qlen-1-THRESH, 0), min(qlen+THRESH, rlen)):
=======
            print '\nLooking for best ED in col=' + str(qlen) + ' and rows [' + str(max(qlen-1-THRESH, 0)) + '-' + str(min(qlen+THRESH, len(ref))) + ']'
            for row in range(max(qlen-THRESH, 0), min(qlen+THRESH, len(ref))):
>>>>>>> 0851d4077f40a3802f2612a804a08154c1d65761

                print '  looking at table[' + str(row+1) + '][' + str(qlen) + ']'

                ed = table[row+1][qlen]
                print '\tsaw ', ed
                '''
                We might only need to check here if we can find an alignment with ed < THRESH (not the minimum ed)
                '''
                if ed < best:
                    best = ed

            '''
            Also need to look in last row:
            '''

            for col in range(max(rlen-THRESH, 0), min(rlen+THRESH, qlen)):
            	ed = table[rlen][col]
            	print '\tsaw', ed
            	if ed < best:
            		best = ed



            if best <= THRESH:
                matches[ref].append(query)

            print '\nref: ' + ref + ' \tquery: ' + query + '\tbest ED: ' + str(best)
            print table
            print ''


            '''
            Set indices to where they should be next:
            '''
            if j == num_queries-1:
                break
            query_idx = query_tree_next[j]
            '''
            For a given reference, we can say we've seen the reference up to the end for all queries:
            '''
            #ref_idx = len(ref)

        '''
        I DON'T THINK THAT THIS IS WORKING --- CHECK MORE CAREFULLY!
        '''
        if i == num_refs-1:
            break
        ref_idx = ref_tree_next[i]
        query_idx = 0



'''
Build the table:
'''
build_table()

print 'All References:\t' + str(ref_tree)
print 'All Queries: \t' + str(query_tree)
print '\n'


for ref in matches:
    queries = matches[ref]
    print ref + "-->" + str([q for q in queries])