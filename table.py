'''
This is the max edit distance we want to find:
Return sequences with edit distance LESS THAN OR EQUAL TO the threshhold
'''
THRESH = 3


'''
Assuming the reference and query are already in sorted order:
'''
ref_tree = ["aaaaaa", "aabbbb", "aabbcc", "aabbcd", "abbbbb", "bcccdd", "bcdddd"]
query_tree = ["aaa", "aaaaaa", "aaab", "abbc", "accc", "baaaa", "bccaa", "bcd"]

#ref_tree = ["abc", "ade"]
#query_tree = ["aa", "bb"]



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

            print ref_idx, query_idx
            '''
            We need to fill out the table starting at ref_idx+1, query_idx+1
            CAREFUL ABOUT THE CHANGE OF INDICES BETWEEN THE TABLE AND REF/QUERY!
            '''
            for row in range(ref_idx, len(ref)):
                for col in range(query_idx, len(query)):


                    pen = 0 if ref[row] == query[col] else 1
                    ed = min(table[row][col+1] + 1, table[row+1][col] + 1, table[row][col] + pen)

                    '''
                    NEED TO FIGURE OUT SOME WAY TO STOP LOOKING WHEN YOU GET ABOVE THE MAX E.D.
                    '''
                    # Figure this out later
                    #if ed > THRESH:
                    #    break

                    table[row+1][col+1] = ed

            '''
            Find the best edit distance:
            '''
            qlen = len(query)
            best = qlen
            for row in range(ref_idx, len(ref)):
                ed = table[row+1][qlen]
                '''
                We might only need to check here if we can find an alignment with ed < THRESH (not the minimum ed)
                '''
                if ed < best:
                    best = ed

            if best < THRESH:
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
        I DON'T THINK THAT THIS IS WORKING --- CHECK MORE CAREFULLY!
        '''
        if i == num_refs-1:
            break
        ref_idx = ref_tree_next[i]
        ref_idx = 0 # <----------------------- Setting it to 0 for now!



'''
Build the table:
'''
build_table()

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