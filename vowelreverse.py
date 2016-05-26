import time
#Reversing vowels in O(n) time! Long live pop! Strings are the damn devil!
class Solution(object):

    def reverseVowels(self, s):

        """

        :type s: str

        :rtype: str

        """

        vowels = {'a','e','i','o','u','A','E','I','O','U'}

        s_list = list(s)

        news = ''

        s_len = len(s)

        v_str =[]

        c_str=[]

        v_inds=set()

        c_inds=set()

        start = time.time()

        for i in xrange(s_len):

            letter=s_list.pop()

            if(letter in vowels):

                v_str.append(letter)

                v_inds |= {(s_len-1)-i}

            else:

                c_str.append(letter)

                c_inds |= {(s_len-1)-i}

            #print i,s_list,letter,news

        f_time = time.time()

        v_str=v_str[::-1]

        c_str=c_str

        s_time = time.time()

        news=[]

        for i in xrange(s_len):

            #print v_str,c_str,v_inds,c_inds,i,((s_len-1)-i),news

            if(i in v_inds):

                news.append(v_str.pop())

            elif(i in c_inds):

                news.append(c_str.pop())

        end = time.time()

        #print start,f_time,s_time,end

        return ''.join(news)
