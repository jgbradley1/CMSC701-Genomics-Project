MAX_LENGTH = 125

'''
Performs MSD radix sort on a list of strings
Inserts strings in sorted order in WordList which starts out as empty
'''
def radix_sort(originalList, numWords, offset, maxWordLength, WordList):
	if offset == maxWordLength:
		return

	buckets = [ [] for i in range(MAX_LENGTH) ]
	for i in range(numWords):
		if( offset < len(originalList[i][1]) ):
			c = originalList[i][1][offset]

			# place string in appropriate bucket
			if (c != None):
				buckets[ord(c)].append(originalList[i])
		else:
			WordList.append(originalList[i])

	# call radix_sort() recursively
	# to sort the words in each bucket according to offset.
	for i in range(MAX_LENGTH):
		sizeCheck = len(buckets[i]);
		if sizeCheck > 1:	# sort list of words in buckets[i]
			radix_sort(buckets[i], sizeCheck, offset+1, maxWordLength, WordList)
		elif sizeCheck == 1:
			WordList.append(buckets[i][0])




def sort_file(filename):
	dataset = []
	sortedList = []

	f = open(filename, 'r')
	max_length = 0 # Keep track of max length sequence for later

	# Read in data:
	id = "-"
	while True:
		if len(id) is 0:
			break
		if id[0] == ">":
			seq = ""
			nxt = f.readline().strip()
			while nxt[0] != ">":
				seq += nxt
				nxt = f.readline().strip()
				if len(nxt) == 0:
					break
			slen = len(seq)
			if slen > max_length:
				max_length = slen
			dataset.append((id[1:].strip(), seq))
			id = nxt
		else:
			id = f.readline()

	f.close()

	# perform radix sort
	radix_sort(dataset, len(dataset), 0, max_length, sortedList)

	values, ids = [x[1] for x in sortedList], [x[0] for x in sortedList]

	return values, ids, max_length
