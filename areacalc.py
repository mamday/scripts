import sys,os

my_in = sys.argv[1]
xyz_list = []
for line in open(my_in).readlines():
  xyz_list.append([int(p) for p in line.split('x')])
#tot_area = 0
tot_rib = 0
for vals in xyz_list:
  #comb_list=[vals[0]*vals[1],vals[1]*vals[2],vals[0]*vals[2]]
  comb_list=[vals[0]+vals[1],vals[1]+vals[2],vals[0]+vals[2]]
  min_val=min(comb_list)
  #tot_area+=min_area+2*vals[0]*vals[1]+2*vals[1]*vals[2]+2*vals[0]*vals[2]
  per_len=2*min_val
  bow_len=vals[0]*vals[1]*vals[2]  
  tot_rib+=per_len+bow_len
#print tot_area
print tot_rib
