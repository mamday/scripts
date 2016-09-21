import sys
def decrypt(chunk,word):
  all_chunks = {}
  chunk_list = list(chunk)
  word_list = list(word)
  word_len = len(word_list)
  cur_chunks = [chunk_list]
  while(len(cur_chunks)>0):
    current = cur_chunks.pop()
    chunk_len = len(current)
    for letter in xrange(0,(chunk_len-word_len)+1):
      if(current[letter:letter+word_len]==word_list):
        if(not(''.join(current[:letter]+current[(letter+word_len):]) in all_chunks)):
          cur_chunks.append(current[:letter]+current[(letter+word_len):])
          if(letter==0):
            all_chunks[''.join(current[:letter]+current[(letter+word_len):])] = len(current[:letter]+current[(letter+word_len):]) 
          else:
            all_chunks[''.join(current[:letter]+current[(letter+word_len):])] = len(current[:letter]+current[(letter+word_len):]) 
  sort_vals = [(i,j) for i,j in zip(all_chunks.keys(),all_chunks.values())]
  sort_vals.sort()
  sort_vals.sort(key=lambda k: k[1])
  return sort_vals[0][0]

def answer(chunk, word):

    # your code here

    all_chunks = {}

    chunk_list = list(chunk)

    word_list = list(word)

    word_len = len(word_list)

    cur_chunks = [chunk_list]

    while(len(cur_chunks)>0):

        current = cur_chunks.pop()

        chunk_len = len(current)

        for letter in xrange(0,(chunk_len-word_len)+1):

            if(current[letter:letter+word_len]==word_list):

                if(not(''.join(current[:letter]+current[(letter+word_len):]) in all_chunks)):

                    cur_chunks.append(current[:letter]+current[(letter+word_len):])

                    all_chunks[''.join(current[:letter]+current[(letter+word_len):])] = len(current[:letter]+current[(letter+word_len):])

    sort_vals = [(i,j) for i,j in zip(all_chunks.keys(),all_chunks.values())]

    sort_vals.sort()

    sort_vals.sort(key=lambda k: k[1])

    return sort_vals[0][0]


ch=sys.argv[1]
w=sys.argv[2]
#output = decrypt(ch,w)
output = answer(ch,w)
print output
 
