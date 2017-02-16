import sys

def get_anagrams(word):

    word_list=[]

    if(len(word)<=1):

          word_list.append(word)

          return word_list

    for i,let in enumerate(word):

          f_word = word[:i]
          l_word = word[i+1:] 
          cur_list = get_anagrams(f_word+l_word)

          for i in cur_list:
              word_list.append(let+i)

    return word_list

w_list = get_anagrams(sys.argv[1])

print len(w_list)
