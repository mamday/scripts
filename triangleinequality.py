def solution(A):
    # write your code in Python 2.7
    A.sort()
    prev = 0
    preprev=0
    tBool=False
    for ind,i in enumerate(A):
        #print ind,i
        if(ind==0):
            preprev=i
            continue
        elif(ind==1):
            prev=i
            continue
        else:
            psum = prev+preprev
            if(psum>i):
                tBool=True
            preprev=prev
            prev=i
    #print int(tBool)
    return int(tBool)

def MSort(lis):
    if(len(lis)<2):
        return lis
    r_lis = MSort(lis[len(lis)/2:])
    l_lis = MSort(lis[:len(lis)/2])
    #print r_lis,l_lis
    new_lis=[]
    r=0
    l=0
    while(len(new_lis)<len(lis)):
      #print r,l,len(r_lis),len(l_lis),r_lis,l_lis
      if(len(r_lis)<(r+1)):
          #print 'One'
          new_lis+=l_lis[l:]
      elif(len(l_lis)<(l+1)):
          #print 'Two'
          new_lis+=r_lis[r:]
      elif(r_lis[r]<l_lis[l]):
          #print 'Three'
          new_lis.append(r_lis[r])
          r+=1
      else:
          #print 'Four'
          new_lis.append(l_lis[l])
          l+=1
    #print new_lis
    return new_lis
        #print 'right',l_lis+r_lis


def MSsolution(A):
    # write your code in Python 2.7
    #print A
    A = MSort(A)
    #print A
    prev = 0
    preprev=0
    tBool=False
    for ind,i in enumerate(A):
        #print ind,i
        if(ind==0):
            preprev=i
            continue
        elif(ind==1):
            prev=i
            continue
        else:
            psum = prev+preprev
            if(psum>i):
                tBool=True
            preprev=prev
            prev=i
    #print int(tBool)
    return int(tBool)
