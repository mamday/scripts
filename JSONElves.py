import simplejson as json
from simplejson import JSONDecodeError
import sys,os

filename = sys.argv[1]
in_js1 = json.load(open(os.path.expandvars(filename)))

int_list = []

def ExpJSon(in_js):
  if(isinstance(in_js,list)):
    for i in in_js:
      if(isinstance(i,int)):
        print i
        int_list.append(i)
      else:
        ExpJSon(i)
  if(isinstance(in_js,dict)):
    if('red' in in_js.values()):
      return
    for i,j in in_js.iteritems():
      if(isinstance(i,int)):
        print i
        int_list.append(i)
      else:
        ExpJSon(i)
      if(isinstance(j,int)):
        print j
        int_list.append(j)
      else:
        ExpJSon(j)

ExpJSon(in_js1)

print 'Sum',sum(int_list)
