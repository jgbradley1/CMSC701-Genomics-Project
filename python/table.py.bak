'''
This is the max edit distance we want to find:
Return sequences with edit distance LESS THAN OR EQUAL TO the threshhold
'''
THRESH = 1


'''
Assuming the reference and query are already in sorted order:
'''
#ref_tree = ["aaaaaa", "aabbbb", "aabbcc", "aabbcd", "abbbbb", "bcccdd", "bcdddd"]
#query_tree = ["aaa", "aaaaaa", "aaab", "abbc", "accc", "baaaa", "bccaa", "bcd"]

ref_tree = ['abc', 'abde', 'bcde']
query_tree = ['aabcd', 'abbcd', 'abcde', 'bbcde', 'bcdef']


'''
Initialize the table:
Right now, use a numpy array, and assume we have the length of the longest sequence in ref/query
'''

import numpy as np

max_length = 6
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

            print "Start row = ", start_row+1
            print "End row = ", end_row+1

            for row in range(start_row, end_row):

                if row < ref_idx:
                    start_col = max(query_idx, row - THRESH)
                else:
                    start_col = max(0, row - THRESH)
                end_col = min(len(query), row + THRESH + 1)

                print "\tstartcol = ", start_col+1
                print "\tendcol = ", end_col+1

                for col in range(start_col, end_col):

                    print '\t\t', row+1, col+1


                    pen = 0 if ref[row] == query[col] else 1

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

                    upleft = table[row][col] + pen

                    print '\t\t\t', left, upleft, up

                    ed = min(up, left, upleft)


                    table[row+1][col+1] = ed


            '''
            Find the best edit distance:
            '''
            qlen = len(query)
            best = qlen

            for row in range(max(qlen-1-THRESH, 0), min(qlen+THRESH, len(ref))):

                print "Looking for the answer in ", row+1, qlen

                ed = table[row+1][qlen]
                '''
                We might only need to check here if we can find an alignment with ed < THRESH (not the minimum ed)
                '''
                if ed < best:
                    best = ed

            if best <= THRESH:
                matches[ref].append(query)

            print ref, query
            print table
            print "BEST = " + str(best)
            print


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

print "All queries:"
print query_tree

for ref in matches:
    queries = matches[ref]
    print ref + "-->" + str([q for q in queries])







'''
Tree traversal pseudo-code:

search(reference.root, query.root)

search(node ref_node, q_node): // args probably correspond to character positions
                                // maybe check against next one in list?

    if (red_node and q_node at bottom): // if they're both past the end of the string
        // fill out table
        // check for valid ED

    for c in n.children:


'''