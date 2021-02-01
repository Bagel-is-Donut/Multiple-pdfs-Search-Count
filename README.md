# Multiple pdfs Search & Count
The code searches for a list of keywords in a directory of pdfs. \
For each keyword, it returns the file name along with the occurrences. \
Developed for literature review purpose.

# Input file "keywords.txt"
In order to save runtime, I made the following conventions for the keywords you enter:\
	1. For common words, input "all lowercases", separate each word by a new line "\n":\
		key -> [key, Key]\
	the code searches two variants of the word\
	2. For naming words, input "the first letter CAPITAL, the other letters in lowercase", separate each word by a new line "\n":\
		Alice -> [Alice]\
	the code detects that word.lower() != word, so it will only search the entered word\
	3. For special words, input all possible variants by hand, IN ONE LINE, separate each word by a tab "\t"\
		FinTech Fintech fintech -> [FinTech, Fintech, fintech]\
	the code will search all variants you listed and count them towards the first word\
\
See "keywords - sample.txt"

# Input local path for the directory of pdfs you want to search
To run the code on your PC, you need to change the path in the directory to your local path.\
The code will only run through the pdfs in the immediate directory; it skips any other files.

# Output file "keywords search & count.txt"
presents in each row the word, file, and frequency\
\
See "keywords search & count - sample.txt"

# Run file
"pdf search keyword fast.py"

# Notice
Due to the limitations of the pyPDF2 package, the code works very well one some pdfs, but not others. It works on the majority of journal publications. Since I randomly tested on 22 very recent corporate finance publications, and it worked on 19 of them. The ones it failed to work are usually pdfs with many photographs and markings.\
In testing the sample of 22 research papers, averaging 40 pages long each, with 9 keywords, the total runtime is 27 second, so around 1.2 seconds per paper.

# Reference
Searching text in a PDF using Python? (2013, June 13). Stack Overflow. https://stackoverflow.com/questions/17098675/searching-text-in-a-pdf-using-python


