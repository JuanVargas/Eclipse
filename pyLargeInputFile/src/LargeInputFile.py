
'''
This File will eventually be renamed wq.py. For now the name stays LargeInputFile.py

wq.py is an exercise in writing software that can operate with *very large* data sets. 
wq.py contains Python classes that read very big files, (e.g. the entire English version of Wikipedia) 
and writes into N smaller files.

The LargeInputFile class reads huge files and replicates them as sets of smaller files

The entire English content of Wikipedia, as of April 2011, is 30.2 GB. LargeInputFile replicated that 
content into 320 smaller files, each of 96.6 MBs. The smaller files are then used to do the queries in a map-reduce style, i.e., 
launching 32 processes (in Amazon AWS, AppEngine, or Azure) each of which handles 10 files. 
Maybe I will need to do 64 processes reading 5 files each  
'''

import os
import time


'''
The purpose of the LargeInputFile class is to read a very large text file and write its content
into a set of smaller files. For example the English version of Wikipedia is about 30.2 GB of 
text in the form of a XML file. I read the large file file and wrote the content into 320 smaller 
files (96.6 MBs each).

The code executed for 1341 seconds (22.35 minutes) in ArchLinux (the old AMD box)
'''

class LargeInputFile(object):

  def __init__(self):
    "constructor"

    self.inFileName = None
    self.inFileSize = None
    self.inFileReadSegments = None
    self.inFileSegmentSize = None 
    self.name = "LargeInputFile Class"
    self.outFileNameTemplate = None 
    self.outFileNames = []

  def __str__(self):
    return self.name
    
  def getParams( self, aFileName, nSegments ):
    self.inFileName = aFileName
    self.inFileReadSegments = nSegments
    self.inFileSize = os.path.getsize( aFileName )
    self.inFileSegmentSize = self.inFileSize / self.inFileReadSegments
    self.name = "LargeInputFile Class"
    self.outFileNameTemplate = self.inFileName + '_out'
    self.outFileNames = []

  '''
  The method readFile_WriteSegments does the following:
  1. It opens the LargeInputFile
  2. Reads the LargeInputFile into N segments
  3. Writes each segment into a smaller file of name inFileName_out_i where i is the segment number 
  4. At the end the method creates an index file called inFileName_out_index that contains, for each
  segment file, a pair of values = {aSegmentFileName, aSegmentFileSize}
  '''   
  def readFileWriteSegments(self ):

    result = False
    if self.inFileReadSegments <= 0 :
      return result
    if self.inFileSize <= 0 :
      return result
    self.inFile = open ( self.inFileName , 'r')
    i = 0
    nTotalBytesRead = 0;

    if self.inFileReadSegments <= 1 : # special case, simply read file and dump to output
      s = self.inFile.read( self.inFileSegmentSize )
      nLocBytesRead = len(s)
      outFileName = self.inFileName + "_out_" + str(i)
      outFile = open ( outFileName , 'w')
      outFile.write( s )
      outFile.close()
      aTuple = outFileName, nLocBytesRead  # aTuple that contains filename and size    
      self.outFileNames.append( aTuple ) # deposit tuple in list
      nTotalBytesRead += nLocBytesRead # check if auto-increment arithmetic operators work in Python
      result = True
      return result
    
    nLastSegment = self.inFileReadSegments - 1          
    while i < self.inFileReadSegments :
      
      if i == nLastSegment :
        s = self.inFile.read( self.inFileSize - nTotalBytesRead )
      else :  
        s = self.inFile.read( self.inFileSegmentSize )
      
      nLocBytesRead = len(s)
      outFileName = self.inFileName + "_out_" + str(i)
      outFile = open ( outFileName , 'w')
      outFile.write( s )
      outFile.close()
      aTuple = outFileName, nLocBytesRead  # aTuple that contains filename and size    
      self.outFileNames.append( aTuple ) # deposit tuple in list
      nTotalBytesRead += nLocBytesRead # check if auto-increment arithmetic operators work in Python
      i = i+1 # increment counter
    
    if nTotalBytesRead == self.inFileSize :
      result = True
      return result
    else:  
      return result
 

  '''
  The method WritePageArticles ( self, aString, outFileName )  receives in aString 
  the content that is to be written into outFileName. WritePageArticles opens outFileName for 
  append or write, and parses through aStrig, searching for substrings of the form 
  <page> ... text ... </page>. The substrings are written into the outFile.  
  '''
  def writePageArticles(self, aString, outFileName) :
    
    result = False
    k = len( aString )
    if k <= 0:
      return result
    
    fo = open( outFileName, 'a')

    i = 0
    while i != -1 :
      i = aString.find("<page>", i)
      if i != -1 :        
        fo.close()
        return 

      j = aString.find("</page>", i)
      j +=8 # </page> has 7 characters plus newLine
      p = aString[i:j]
      fo.write(p)
      i = j

    fo.close()
    result = True
    return result


'''
The purpose of the QueryFile class is to open medium-size text file (50 to 100 MBs) with content
structured as in Wikipedia articles, and return the number of articles that contain the given query. 
It looks like articles in Wikipedia have the structure below, which sort of makes sense:
<page>
   <title> ...some title ... </title>
   <id> ... a number...</id>
   <timestamp> a time stamp </timestamp>
   <contributor> .. several fields ... </contributor> 
   <minor />
   <comment> ... possibly more than one ...  </comment>
   <text> ....the bulk of the article is here, including text, references, etc.... </text>
 </page>
 
therefore, QueryFile should search for the query tokens in the text part of each article.
''' 

class QueryFile(object):

  def __init__(self):
    "constructor"
    self.inFileName = None
    self.nQueryToken = None
    self.nQueryToken.Count = None
    self.nArticlesInFile = None

  def __str__(self):
    return self.name
    
    
'''
The purpose of the QueryArticle class is to return the number of times a given query token 
is found in the text part of an article. Note that a wikipedia article follows this structure:
<page>
   <title> ...some title ... </title>
   <id> ... a number...</id>
   <timestamp> a time stamp </timestamp>
   <contributor> .. several fields ... </contributor> 
   <minor />
   <comment> ... possibly more then one ...  </comment>
   <text> ....the bulk of the article is here, including text, references, etc.... </text>
</page>
 
therefore, QueryArticle  should count how many times the query token is found in the text part of the article.
It looks I should use the re module or simply use the string.count(s, sub[, start[, end]]) method,
which return the number of (non-overlapping) occurrences of substring sub in string s[start:end]. 
Defaults for start and end and interpretation of negative values are the same as for slices.

''' 

class QueryArticle (object):

  def __init__(self):
    "constructor"
    self.nQueryToken = None
    self.nQueryToken.Count = None
        
  def __str__(self):
    return self.name


      

def test():
  # fn = "/home/juan/Downloads/enwiki.xml"
  fn = "/home/juan/Downloads/enwiki.xml_out_0"
  o = LargeInputFile()
  o.getParams( fn, 100 )
  o.readFileWriteSegments( )



def fifo() :
  fo = open("/home/juan/oFile_1", 'w')
  fi = open("/home/juan/iFile_1", 'r')
  s = fi.read()
  k = len(s)

  i = 0
  while i != -1 :
    i = s.find("<page>", i)
    if i != -1 :    
      j = s.find("</page>", i)
      if j != -1 :
        j +=8 # </page> has 7 characters plus newLine
        p = s[i:j]
        fo.write(p)
        i = j
      else:
        i = -1  

  fo.close()
  fi.close()


def fifa() :
  fo = open("/home/juan/oFile_1", 'w')
  fi = open("/home/juan/iFile_1", 'r')
  s = fi.read()
  k = len(s)      # I use k during debug

  i = 0
  while True :
    i = s.find("<page>", i)
    if i == -1 :    
      break
    j = s.find("</page>", i)
    if j == -1 :
      break
    j += 8        # </page> has 7 characters plus newLine
    p = s[i:j]    # p contains a string delimited by <page> ... </page>
    fo.write(p)
    i = j

  fo.close()
  fi.close()


t1 = time.time()
res = fifa()
t2 = time.time()
print '%s took %0.3f ms' % (fifo.func_name, (t2-t1)*1000.0)
print 'chiao'



#t1 = time.time()
#res = test()
#t2 = time.time()
#print '%s took %0.3f ms' % (test.func_name, (t2-t1)*1000.0)
#print 'chiao'
    