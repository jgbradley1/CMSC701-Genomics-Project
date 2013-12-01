MAX_LENGTH = 125;

'''
Performs MSD radix sort on a list of strings
Inserts strings in sorted order in WordList which starts out as empty
'''
def radix_sort(originalList, numWords, offset, maxWordLength, WordList):
	if offset == maxWordLength:
		return;

	buckets = [ [] for i in range(MAX_LENGTH) ];
	for i in range(numWords):
		if( offset < len(originalList[i]) ):
			c = originalList[i][offset];

			# place string in appropriate bucket
			if (c != None):
				buckets[ord(c)].append(originalList[i]);
		else:
			WordList.append(originalList[i]);

	# call radix_sort() recursively
	# to sort the words in each bucket according to offset.
	for i in range(MAX_LENGTH):
		sizeCheck = len(buckets[i]);
		if sizeCheck > 1:	# sort list of words in buckets[i]
			radix_sort(buckets[i], sizeCheck, offset+1, maxWordLength, WordList);
		elif sizeCheck == 1:
			WordList.append(buckets[i][0]);




def sort_file(filename):
	dataset = [];
	sortedList = [];

	f = open(filename, 'r');

	# read in data
	maxWord = "";
	for line in f:
		dataset.append(line.strip());
		if ( len(line.strip()) > len(maxWord) ):
			maxWord = line.strip();
	f.close();
	
	# perform radix sort
	radix_sort(dataset, len(dataset), 0, len(maxWord), sortedList);

	return sortedList;