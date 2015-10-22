#This script just makes pytables and Root trees. Need to use another script to actually plot the datas
#from __future__ import division
from icecube import icetray
from icecube import dataio,tableio,phys_services,hdfwriter,rootwriter,dataclasses
from icecube import dataio,tableio,phys_services,hdfwriter,rootwriter,dataclasses
from icecube.phys_services import converters 
from icecube.phys_services.converters import I3EventInfoConverterFromRecoPulses 
from I3Tray import I3Tray
from icecube.hdfwriter import I3HDFTableService
from icecube.tableio import I3TableWriter
from icecube.dataclasses import converters
from icecube.dataclasses.converters import I3DoubleConverter
from icecube.rootwriter import I3ROOTTableService
from icecube import neutrinoflux,NoiseEngine,millipede
from icecube.weighting import weighting
from glob import glob
import healpy,numpy,math
import scipy
from scipy import special
import os
import sys

tray = I3Tray()
#I3 file with stuff I want in a table
gcd = "/home/mamday/IceCube/data/IC86/SantaIgel/GeoCalibDetectorStatus_IC86.55697_corrected_V2.i3"
gcdlist = []
gcdlist.append(gcd)
#file_list = glob("/net/user/mamday/icesim/scripts/output/SANTA/*NuE*JP*")

cors_ds = 6939

n_files = 500 
#n_files = 1053
flux = neutrinoflux.ConventionalNeutrinoFlux("honda2006_numu")

####file_list = glob("/net/user/mamday/icesim/scripts/output/Mono/*")
file_list = glob("/media/mamday/Mismelania/UWFiles/JPNuMu/*Core*NuMu*L5*")
#file_list = glob("/net/user/mamday/icesim/scripts/output/Corsika/*Core*L5*")
#file_list = glob("/net/user/mamday/icesim/scripts/output/JPNuMu/JPVuv*genie*L5*")
#file_list = glob("/net/user/mamday/icetray/build/SebastianScripts/eventSelection/output/*.000[0-9][0-9][0-9]*L4*")

#file_list = glob("/net/user/mamday/icesim/scripts/output/JPNuMu/*L7*")
tray.AddModule('I3Reader','reader',FilenameList = gcdlist+file_list)
#Create the pytable
hdf = I3HDFTableService('JPVuvNuMu-ChargeCoreATWDInfo.hd5')
#Create the root trees 
#roottree = I3ROOTTableService('Test.root','master_tree')
gcdfile = dataio.I3File("/home/mamday/IceCube/data/IC86/SantaIgel/GeoCalibDetectorStatus_IC86.55697_corrected_V2.i3")

geo_frame = gcdfile.pop_frame()
while not geo_frame.Has('I3Geometry'): geo_frame = gcdfile.pop_frame()
geometry_ = geo_frame.Get('I3Geometry')

def addMCTreeItem(frame):
  mostEnergetic = frame["I3MCTree"].most_energetic_muon
  mostEnePrim = frame["I3MCTree"].most_energetic_primary
  mostEneCasc = frame["I3MCTree"].most_energetic_cascade
####  print "Energy ",mostEnePrim.energy
  frame['MostEnergMuon'] = mostEnergetic
  frame['MostEnergPrim'] = mostEnePrim
  frame['MostEnergCasc'] = mostEneCasc

tray.AddModule(addMCTreeItem,'addMCTree')

def simprodweight(frame):
  nfiles, generator = weighting.from_simprod(cors_ds)
  generator *= nfiles
  print generator
  frame["weight"] = generator

#tray.AddModule(simprodweight,"Weighting")

def insert_corsikaweight(frame):
    if "CorsikaWeightMap" in frame:
      cMap = frame["CorsikaWeightMap"]
      dipWeight = cMap["DiplopiaWeight"]
      polyWeight = cMap["Polygonato"]
      timeScale = cMap["TimeScale"]
      cWeight = cMap["Weight"]
      if not "weight" in frame :
        frame["weight"] = dataclasses.I3Double(cWeight*polyWeight*dipWeight/(n_files*timeScale)) 

#tray.AddModule(insert_corsikaweight,'insert_corsikaweight')
 
def insert_weight(frame):
    if "I3MCTree" and "I3MCWeightDict" in frame:
      tree = frame["I3MCTree"]
      weight_dict = frame["I3MCWeightDict"]
      nu_type = tree.most_energetic_primary.type
      nu_energy = tree.most_energetic_primary.energy
      nu_costheta = math.cos(tree.most_energetic_primary.dir.zenith)
      atmoflux = flux.getFlux(nu_type, nu_energy, nu_costheta)
      weight = weight_dict["OneWeight"]*atmoflux/(n_files*weight_dict["NEvents"])
      if not "weight" in frame :
        frame["weight"] = dataclasses.I3Double(weight)

tray.AddModule(insert_weight,'insert_weight')

def EarliestStringHit(srtPulse,ehvect,ehzvect):
#Get the earliest hit time and z position on each string
    for omkey1, series1 in srtPulse:
        if(ehvect[omkey1.string]>series1[0].time):
          ehvect[omkey1.string] = series1[0].time 
          ehzvect[omkey1.string] = geometry_.omgeo[omkey1].position[2]

def OneStringZVect(omkey,series,srtPulse,oszvect,stringcount):
#Calculate unit vector length in z direction for all hit pairs, keep track of how many hit pairs went into each value
    for omkey1, series1 in srtPulse:
          if(omkey.string==omkey1.string):  
            stringcount[omkey.string]+=1
            zDist = geometry_.omgeo[omkey].position[2]-geometry_.omgeo[omkey1].position[2]
    #        print 'Positions: ',math.copysign(1.0,zDist),omkey.string,omkey1.string,geometry_.omgeo[omkey].position[2]-geometry_.omgeo[omkey1].position[2],series[0].time
            oszvect[omkey.string]+=math.copysign(1.0,zDist)

def HitPairAlg(omkey,series,srtPulse,mode,hpBins,vMin=0.0,vMax=1.0,vErr=0.0):
#Calculate weighted(in one of two modes) value of magnets for hit pairs
    vellist = []
    zlist = []
    zenlist = []
    azilist = []
    uvect = dataclasses.I3Position(0,0,0)
    hitpair = NoiseEngine.HitPair()
#Accumulate hit pair information
    for omkey1, series1 in srtPulse:
      if(not(omkey==omkey1)):
        if(series1[0].time>series[0].time):
          hitpair.settimes(series[0],series1[0])
          hitpair.setangles(geometry_.omgeo[omkey].position,geometry_.omgeo[omkey1].position)
          if(mode==0):
#Weight by the ratio of the velocity (m/ns) to the speed of light
            if((float(hitpair.getvelocity())/0.3)<1):
              weight = float(hitpair.getvelocity())/0.3
            else:
              weight = (0.6-float(hitpair.getvelocity()))/0.3
#Require that hit is not faster than light by more than a reasonable amount and that hit is faster than typical noise hit
            if(weight<(vMax+vErr) and weight>vMin):
              hitpair.settimes(series[0],series1[0])
              hitpair.setangles(geometry_.omgeo[omkey].position,geometry_.omgeo[omkey1].position)
              if(not(hitpair.getzenith()==0) and not(hitpair.getazimuth()==0)):
                vellist.append(weight*hitpair.getvelocity())
                azilist.append(weight*math.cos(hitpair.getazimuth()))
                zenlist.append(weight*math.cos(hitpair.getzenith()))
                zlist.append(weight*(geometry_.omgeo[omkey1].position.z-geometry_.omgeo[omkey].position.z))
                thePos = geometry_.omgeo[omkey1].position-geometry_.omgeo[omkey].position
                uvect += (weight)*thePos/thePos.magnitude
                hpBins[healpy.ang2pix(2,hitpair.getzenith(),hitpair.getazimuth())] +=1
          if(mode==1):
#Weight by the average charge of the hits 
            #weight = (series[0].charge+series1[0].charge)/2
#No weight
            weight=1
            hitpair.settimes(series[0],series1[0])
            hitpair.setangles(geometry_.omgeo[omkey].position,geometry_.omgeo[omkey1].position)
            if(not(hitpair.getzenith()==0) and not(hitpair.getazimuth()==0)):
              vellist.append(weight*hitpair.getvelocity())
              azilist.append(weight*math.cos(hitpair.getazimuth()))
              zenlist.append(weight*math.cos(hitpair.getzenith()))
              zlist.append(weight*(geometry_.omgeo[omkey1].position.z-geometry_.omgeo[omkey].position.z))
              thePos = geometry_.omgeo[omkey1].position-geometry_.omgeo[omkey].position
              uvect += (weight)*thePos/thePos.magnitude
              hpBins[healpy.ang2pix(2,hitpair.getzenith(),hitpair.getazimuth())] +=1

    return vellist,zenlist,azilist,zlist,uvect


def DCTriggerInfo(frame):
#Get DeepCore trigger time(for PINGU or IC86)
  triggers = frame["I3TriggerHierarchy"]
  trigID = 1011
#  trigID = 60001
  trigTime = dataclasses.I3Double()
  for trig in triggers:
    if(trig.key.config_id==1011):
#    if(trig.key.config_id==60001):
      trigTime = dataclasses.I3Double(trig.time)
  frame['DCTrigTime']=trigTime

tray.AddModule(DCTriggerInfo,'trigInfo')

def SebL7(frame):
    triggers = frame["I3TriggerHierarchy"]
    string3T = -9999 
    if(frame.Has('String3Pulses')):
      s3Mask = frame['String3Pulses']
      if (len(s3Mask.apply(frame))>0):
        s3Time = [(j[0].time,geometry_.omgeo[i].position) for i,j in s3Mask.apply(frame)]
        s3Time.sort()
        string3T = s3Time[0][0]
    trigID = 1011
#  trigID = 60001
    trigTime = dataclasses.I3Double()
    for trig in triggers:
      if(trig.key.config_id==1011):
#    if(trig.key.config_id==60001):
        trigTime = trig.time
    refHitPos = dataclasses.I3Position(0.,0.,0.)
    hitPos = dataclasses.I3Position(0.,0.,0.)
    refHitTime = -9999 
    hitTime = trigTime 
    hitDistance = dataclasses.I3VectorDouble()
    hitTimeDiff = dataclasses.I3VectorDouble()
    s3TimeDiff = dataclasses.I3VectorDouble()

    for om, launchSeries in frame["InIceRawData"]:
        for launch in launchSeries:
            hitTime = launch.time
            if hitTime==trigTime:
                refHitTime = hitTime
                refHitPos = geometry_.omgeo[om].position

    for om, launchSeries in frame["InIceRawData"]:
        for launch in launchSeries:
            hitTime = launch.time
            hitPos = geometry_.omgeo[om].position

            hitDistance.append((hitPos-refHitPos).magnitude)
            hitTimeDiff.append(refHitTime - hitTime)
            s3TimeDiff.append(string3T-hitTime)

    frame['SebL7Dist'] = hitDistance
    frame['SebL7Time'] = hitTimeDiff 
#    frame['S3L7Time'] = s3TimeDiff 

tray.AddModule(SebL7,'sebInfo')

def StringNHits(pulses,time_dist,charge_dist,n_strings,string_hits,string_xpos,string_ypos,string_zpos): 
  nhits_string = 0
  cur_string = -1
  count = 0
  nFourHits = 0 
  oldKey = icetray.OMKey()
  for omkey, series in pulses:
#Count hits per string
    if(cur_string!=omkey.string):
        if(nhits_string>=1):
            n_strings.append(cur_string)
            string_hits.append(nhits_string)
        if(nhits_string>=4):
          nFourHits+=1
        nhits_string=0

    if(len(series)>0):
        time_dist.append(series[0].time)
        charge_dist.append(series[0].charge)
    else:
        time_dist.append(-9999)
        charge_dist.append(-9999)

    string_xpos.append(geometry_.omgeo[omkey].position[0])
    string_ypos.append(geometry_.omgeo[omkey].position[1])
    string_zpos.append(geometry_.omgeo[omkey].position[2])
    cur_string = omkey.string
    oldKey = omkey
    nhits_string +=1
    count += 1
    if(count==len(pulses)):
      if(nhits_string>=1):
          if(nhits_string>=4):
              nFourHits+=1
          n_strings.append(cur_string)
          string_hits.append(nhits_string)
#  print charge_dist,time_dist   
#  if(nFourHits<2):
#    return False

def stringInfo(pulses):
#  tupList = [(i.string,geometry_.omgeo[i].position,j[0].time,j[0].charge) for i,j in pulses] 
#Big terrible algorithm to get information from three hit cleaned pulses that I will spend no time explaining
  timeList = 87*[0]
  xposList = 87*[0]
  yposList = 87*[0]
  zdistList = 87*[0]
  chargeList = 87*[0]
  nStringList = 87*[0]
  allzposList = 87*[()]
  for omkey,series in pulses:
#    print omkey.string
    nStringList[omkey.string]+=1
    timeList[omkey.string]+=series[0].time
    chargeList[omkey.string]+=series[0].charge
    xposList[omkey.string]=(geometry_.omgeo[omkey].position[0]) 
    yposList[omkey.string]=(geometry_.omgeo[omkey].position[1]) 
    allzposList[omkey.string]+=(geometry_.omgeo[omkey].position[2],)
#    print geometry_.omgeo[omkey].position[2]
  strings = [i for i,x in enumerate(nStringList) if x>0]
  timeAvg = [i/j for i,j in zip(timeList,nStringList) if j>0]
  chAvg = [l/m for l,m in zip(chargeList,nStringList) if m>0]
  xposAvg = [n for n in xposList if n!=0]
  yposAvg = [n for n in yposList if n!=0]
  zposAvg = [numpy.mean(q) for q in allzposList if q!=()]
  medZ = [numpy.median(i) for i in allzposList if i!=()]
  zDist = [max(i)-min(i) for i in allzposList if i!=()]

  myPosList = [] 
  stringDist = []
  timeDist = []
  for i in xrange(len(xposAvg)):
    myPosList.append(dataclasses.I3Position(xposAvg[i],yposAvg[i],zposAvg[i]))
    if(i>0):
      stringDist.append((myPosList[i]-myPosList[i-1]).magnitude) 
      timeDist.append(timeAvg[i]-timeAvg[i-1])
  if(len(xposAvg)==1):
    stringDist.append(-9999)
    timeDist.append(-9999)
  if(len(xposAvg)>2):
    stringDist.append((myPosList[2]-myPosList[0]).magnitude)
    timeDist.append(timeAvg[2]-timeAvg[0])

  for i in xrange(len(allzposList)):
    for j in xrange(len(allzposList[i])):
      if(len(allzposList[i])==1 and allzposList[i]!=()):
        zdistList[i]=-9999
      if(j>0 and allzposList[i]!=()):
        zdistList[i]+=allzposList[i][j]-allzposList[i][j-1]
#The most horrible of them all
  zDists = [i/j for i,j in zip([p for p in zdistList if p!=0],[float(len(k)-1) for k in allzposList if k!=() and len(k)>1])]

  return timeAvg,chAvg,medZ,zDist,xposAvg,yposAvg,zposAvg,zDists,stringDist,timeDist

#  print nStringList,[i for i,x in enumerate(nStringList) if x>0],[i[1] for i in [p/q for p,q in zip(posList,nStringList) if q>0]],[j for j in i for i in allposList if i!=()]

def pulseAlgs(frame):
#An old bad algorithm for calculating the number of hits on each string, plus hit pair magnets...
  velMeanVec = dataclasses.I3VectorDouble()
  velMedVec = dataclasses.I3VectorDouble()
  zenMeanVec = dataclasses.I3VectorDouble()
  zenMedVec = dataclasses.I3VectorDouble()
  aziMeanVec = dataclasses.I3VectorDouble()
  aziMedVec = dataclasses.I3VectorDouble()

  nStrings3 = dataclasses.I3VectorDouble()
  timeDist3 = dataclasses.I3VectorDouble()
  chargeDist3 = dataclasses.I3VectorDouble()
  stringXPos3 = dataclasses.I3VectorDouble()
  stringYPos3 = dataclasses.I3VectorDouble()
  stringZPos3 = dataclasses.I3VectorDouble()
  stringHits3 = dataclasses.I3VectorDouble()

  nStrings = dataclasses.I3VectorDouble()
  timeDist = dataclasses.I3VectorDouble()
  chargeDist = dataclasses.I3VectorDouble()
  stringXPos = dataclasses.I3VectorDouble()
  stringYPos = dataclasses.I3VectorDouble()
  stringZPos = dataclasses.I3VectorDouble()
  stringHits = dataclasses.I3VectorDouble()
  if(frame.Has('OfflinePulses')):
    offPulse = frame['OfflinePulses']
    posDiff = dataclasses.I3VectorDouble() 
    tDiff = dataclasses.I3VectorDouble() 
    mtDiff = dataclasses.I3VectorDouble() 
    atDiff = dataclasses.I3VectorDouble() 

#    if(len(offPulse)>0):
    offTime = [(i,k.time,k.charge,k.flags,j[0].time,j[-1].time) for i,j in offPulse for k in j if len(j)>1]
    totCharge = numpy.sum([p.charge for i,j in offPulse for p in j])
    chargeFrac = [(p.time,i,[p.charge for p in j],numpy.sum([p.charge for p in j])/totCharge) for i,j in offPulse]
    chargeFrac.sort()
    print chargeFrac,'\n'
    offTime.sort()
    count = 0
    for k in xrange(len(offTime)):
      mtDiff.append(offTime[k][5]-offTime[k][4])

      if(not((offTime[k][3] & dataclasses.I3RecoPulse.PulseFlags.ATWD))):
        atDiff.append(offTime[k][1]-offTime[k][4])


      if(k>0 and k<(len(offTime)-1) and offTime[k][2]<0.5 and (offTime[k][3] & dataclasses.I3RecoPulse.PulseFlags.ATWD)):
        lowTDiff = numpy.fabs(offTime[k-1][1]-offTime[k][1])
        hTDiff = numpy.fabs(offTime[k+1][1]-offTime[k][1])
        tDiff.append(min(lowTDiff,hTDiff))
      elif(k==0 and offTime[k][2]<0.5 and (offTime[k][3] & dataclasses.I3RecoPulse.PulseFlags.ATWD)):
        tDiff.append(offTime[k+1][1]-offTime[k][1])
      elif(k==len(offTime)-1 and offTime[k][2]<0.5 and (offTime[k][3] & dataclasses.I3RecoPulse.PulseFlags.ATWD)):
        tDiff.append(offTime[k][1]-offTime[k-1][1])
      
  if(frame.Has('OfflinePulses_sRT')):
    srtMask = frame['OfflinePulses_sRT']
   # print 'Yeah...'
#  if(frame.Has('SRT_TW_Cleaned_OfflinePulses')):
#    srtMask = frame['SRT_TW_Cleaned_OfflinePulses']
  else:
    #print 'No pulse cleaning'
    return False
  string3X = -9999
  string3Y = -9999
  string3Z = -9999
  string3T = -9999
  if(frame.Has('String3Pulses')):
    s3Mask = frame['String3Pulses']
    if (len(s3Mask.apply(frame))>0):
      s3Time = [(j[0].time,i.string,geometry_.omgeo[i].position) for i,j in s3Mask.apply(frame)]
      s3Time.sort()
      string3X = s3Time[0][2][0]
      string3Y = s3Time[0][2][1]
      string3Z = s3Time[0][2][2]
      string3T = s3Time[0][0]
      string3T2 = s3Time[1][0]
      firstString = s3Time[0][1]
      string23T = -9999
      string23T2 = -19998
      for i in xrange(len(s3Time)):
        #print i, s3Time[i][1],firstString
        if(s3Time[i][1]!=firstString):
          string23T = s3Time[i][0]
          string23T2 = s3Time[i+1][0]
          break 
#      s3String = sorted(s3Time, key=lambda x: x[1])
   #   print s3Time,string3T,string3T2,string23T,string23T2
  else:
    return False
  #Test hit pairs
  srtPulse = srtMask.apply(frame)
  s3Pulse = s3Mask.apply(frame)
  if len(s3Pulse)==0:
    return False
#Get information about pulses from pulse series
  StringNHits(s3Pulse,timeDist3,chargeDist3,nStrings3,stringHits3,stringXPos3,stringYPos3,stringZPos3)
  StringNHits(srtPulse,timeDist,chargeDist,nStrings,stringHits,stringXPos,stringYPos,stringZPos)

  time_avg = []
  ch_avg = []
  med_z = []
  z_dist = []
  x_pos_avg = []
  y_pos_avg = []
  z_pos_avg = []
  z_dists = []
  string_dist = []
  time_dist = []
  time_avg,ch_avg,med_z,z_dist,x_pos_avg,y_pos_avg,z_pos_avg,z_dists,string_dist,time_dist = stringInfo(s3Pulse)

  hitpair = NoiseEngine.HitPair()
  lecount = 0
  hpbins = 48*[0] 
  hpbinsCut = 48*[0] 
  allvelList = [] 
  allzenList = [] 
  allzList = [] 
  alluVect = dataclasses.I3Position(0,0,0) 
  allaziList = [] 
#  allvelListCut = [] 
#  allzenListCut = [] 
#  allzListCut = [] 
#  alluVectCut = dataclasses.I3Position(0,0,0) 
#  allaziListCut = [] 
  oszVect = 87*[0]
  nhzVect = 87*[0]
  nhstringCount = 87*[0]
  stringCount = 87*[0]
  ehzVect = 87*[0]
  ehVect = 87*[99999999]
  EarliestStringHit(srtPulse,ehVect,ehzVect)
  #print ehzVect, ehVect
  for omkey, series in s3Pulse:
    #Z magnet value with respect to the earliest hit on the string
    zDist = geometry_.omgeo[omkey].position[2]-ehzVect[omkey.string]
    nhzVect[omkey.string]+=math.copysign(1.0,zDist)
    nhstringCount[omkey.string]+=1
    #Condense hit pair algorithm
    velList,zenList,aziList,zList,uVect = HitPairAlg(omkey,series,srtPulse,1,hpbins)
#####    velListCut,zenListCut,aziListCut,zListCut,uVectCut = HitPairAlg(omkey,series,srtPulse,0,hpbinsCut,0.25,.3,0.05)
    #Z magnet value for all hit pairs on a single string 
    OneStringZVect(omkey,series,srtPulse,oszVect,stringCount)

#Vectors for magnets
    allvelList.extend(velList)
    allzList.extend(zList)
    allzenList.extend(zenList)
    allaziList.extend(aziList)
    alluVect += uVect
#    allvelListCut.extend(velListCut)
#    allzListCut.extend(zListCut)
#    allzenListCut.extend(zenListCut)
#    allaziListCut.extend(aziListCut)
#    alluVectCut += uVectCut
    if(len(velList)>0):
      velMeanVec.append(numpy.mean(velList))
      zenMeanVec.append(numpy.mean(zenList))
      aziMeanVec.append(numpy.mean(aziList))
      velMedVec.append(numpy.median(velList))
      zenMedVec.append(numpy.median(zenList))
      aziMedVec.append(numpy.median(aziList))
    else:
      velMeanVec.append(-9999)
      zenMeanVec.append(-9999)
      aziMeanVec.append(-9999)
      velMedVec.append(-9999)
      zenMedVec.append(-9999)
      aziMedVec.append(-9999)

#    print "Means: ",velMean,zenMean,"Medians: ",velMed,zenMed 

  ratVal = dataclasses.I3Double(oszVect[stringCount.index(max(stringCount))]/max(stringCount))
  eratVal = dataclasses.I3Double(nhzVect[nhstringCount.index(max(nhstringCount))]/max(nhstringCount))
#  if(ratVal<0.1):
#  if (max(nhstringCount)>4 and nhzVect[nhstringCount.index(max(nhstringCount))]/max(nhstringCount)<-0.3):
#    print oszVect[stringCount.index(max(stringCount))]/max(stringCount),nhzVect[nhstringCount.index(max(nhstringCount))]/max(nhstringCount)
#Median and mean of "magnets"
  if(len(allzenList)>0):
    zenMeanVal = dataclasses.I3Double((numpy.mean(allzenList)))
    zenMedVal = dataclasses.I3Double((numpy.median(allzenList)))
    zMedVal = dataclasses.I3Double((numpy.median(allzList)))
    aziMeanVal = dataclasses.I3Double((numpy.mean(allaziList)))
    aziMedVal = dataclasses.I3Double((numpy.median(allaziList)))
  else:
    zenMeanVal = dataclasses.I3Double(-9999)
    zenMedVal = dataclasses.I3Double(-9999)
    zMedVal = dataclasses.I3Double(-9999)
    aziMeanVal = dataclasses.I3Double(-9999)
    aziMedVal = dataclasses.I3Double(-9999)
#  if(len(allzenListCut)>0):
#    zenMeanValCut = dataclasses.I3Double((numpy.mean(allzenListCut)))
#    zenMedValCut = dataclasses.I3Double((numpy.median(allzenListCut)))
#    zMedValCut = dataclasses.I3Double((numpy.median(allzListCut)))
#    aziMeanValCut = dataclasses.I3Double((numpy.mean(allaziListCut)))
#    aziMedValCut = dataclasses.I3Double((numpy.median(allaziListCut)))
#  else:
#    zenMeanValCut = dataclasses.I3Double(-9999)
#    zenMedValCut = dataclasses.I3Double(-9999)
#    zMedValCut = dataclasses.I3Double(-9999)
#    aziMeanValCut = dataclasses.I3Double(-9999)
#    aziMedValCut = dataclasses.I3Double(-9999)

#Unit vector magnitude 
  if(len(allzenList)>0):
    uVecLen = dataclasses.I3Double(alluVect.magnitude)
#Van Mises-Fisher Distribution Variables
#    vmfdRBar = alluVect.magnitude/len(allzenList)
#    vmfdK0 = dataclasses.I3Double((vmfdRBar*(3-(vmfdRBar*vmfdRBar)))/(1-(vmfdRBar*vmfdRBar)))
#    vmfdK0Val = (vmfdRBar*(3-(vmfdRBar*vmfdRBar)))/(1-(vmfdRBar*vmfdRBar))
#    vmfdK1 = dataclasses.I3Double(vmfdK0Val - ((scipy.special.iv(3,vmfdK0Val)-vmfdRBar)/(1-(scipy.special.iv(3,vmfdK0Val)*scipy.special.iv(3,vmfdK0Val))-((2/vmfdK0Val)*scipy.special.iv(3,vmfdK0Val)))))
#    vmfdK1Val = vmfdK0Val - ((scipy.special.iv(3,vmfdK0Val)-vmfdRBar)/(1-(scipy.special.iv(3,vmfdK0Val)*scipy.special.iv(3,vmfdK0Val))-((2/vmfdK0Val)*scipy.special.iv(3,vmfdK0Val))))
#    vmfdK2 = dataclasses.I3Double(vmfdK1Val - ((vmfdK1Val-vmfdRBar)/(1-(scipy.special.iv(3,vmfdK1Val)*scipy.special.iv(3,vmfdK1Val)) - ((2/vmfdK1Val)*scipy.special.iv(3,vmfdK1Val)))))
  else:
    uVecLen = dataclasses.I3Double(0)
#    vmfdK0 = dataclasses.I3Double(0)
#    vmfdK1 = dataclasses.I3Double(0)
#    vmfdK2 = dataclasses.I3Double(0)

#Unit vector magnitude 
#  if(len(allzenListCut)>0):
#    uVecLenCut = dataclasses.I3Double(alluVectCut.magnitude)
#Van Mises-Fisher Distribution Variables
#    vmfdRBarCut = alluVectCut.magnitude/len(allzenListCut)
#    vmfdK0Cut = dataclasses.I3Double((vmfdRBarCut*(3-(vmfdRBarCut*vmfdRBarCut)))/(1-(vmfdRBarCut*vmfdRBarCut)))
#    vmfdK0ValCut = (vmfdRBarCut*(3-(vmfdRBarCut*vmfdRBarCut)))/(1-(vmfdRBarCut*vmfdRBarCut))
#    vmfdK1Cut = dataclasses.I3Double(vmfdK0ValCut - ((scipy.special.iv(3,vmfdK0ValCut)-vmfdRBarCut)/(1-(scipy.special.iv(3,vmfdK0ValCut)*scipy.special.iv(3,vmfdK0ValCut))-((2/vmfdK0ValCut)*scipy.special.iv(3,vmfdK0ValCut)))))
#    vmfdK1ValCut = vmfdK0ValCut - ((scipy.special.iv(3,vmfdK0ValCut)-vmfdRBarCut)/(1-(scipy.special.iv(3,vmfdK0ValCut)*scipy.special.iv(3,vmfdK0ValCut))-((2/vmfdK0ValCut)*scipy.special.iv(3,vmfdK0ValCut))))
 #   vmfdK2Cut = dataclasses.I3Double(vmfdK1ValCut - ((vmfdK1ValCut-vmfdRBarCut)/(1-(scipy.special.iv(3,vmfdK1ValCut)*scipy.special.iv(3,vmfdK1ValCut)) - ((2/vmfdK1ValCut)*scipy.special.iv(3,vmfdK1ValCut)))))
#  else:
#    uVecLenCut = dataclasses.I3Double(0)
 #   vmfdK0Cut = dataclasses.I3Double(0)
 #   vmfdK1Cut = dataclasses.I3Double(0)
 #   vmfdK2Cut = dataclasses.I3Double(0)

#Healpix bin variables
  if(float(sum(hpbins))>0):
    hpBinRat = dataclasses.I3Double(float(max(hpbins))/float(sum(hpbins)))
    oldMax = float(max(hpbins))
    oldSum = float(sum(hpbins))
    ratInd = hpbins.index(max(hpbins))
    hpZeroBin = dataclasses.I3Double(float(hpbins.count(0))/len(hpbins))
    hpLowBin = dataclasses.I3Double(float(sum(1 for x in hpbins if x >= (oldMax/2)))/len(hpbins))
    hpbins[ratInd] = 0
    hpBinRatSum = dataclasses.I3Double(float(max(hpbins)+oldMax)/oldSum)
  else:
    hpBinRat = dataclasses.I3Double(0) 
    hpBinRatSum = dataclasses.I3Double(0) 
    hpZeroBin = dataclasses.I3Double(1) 
    hpLowBin = dataclasses.I3Double(1) 

#Healpix bin variables
#  if(float(sum(hpbinsCut))>0):
#    hpBinRatCut = dataclasses.I3Double(float(max(hpbinsCut))/float(sum(hpbinsCut)))
#    oldMax = float(max(hpbinsCut))
#    oldSum = float(sum(hpbinsCut))
#    ratInd = hpbinsCut.index(max(hpbinsCut))
#    hpZeroBinCut = dataclasses.I3Double(float(hpbinsCut.count(0))/len(hpbinsCut))
#    hpLowBinCut = dataclasses.I3Double(float(sum(1 for x in hpbinsCut if x >= (oldMax/2)))/len(hpbinsCut))
#    hpbinsCut[ratInd] = 0
#    hpBinRatSumCut = dataclasses.I3Double(float(max(hpbinsCut)+oldMax)/oldSum)
#  else:
#    hpBinRatCut = dataclasses.I3Double(0)
#    hpBinRatSumCut = dataclasses.I3Double(0)
#    hpZeroBinCut = dataclasses.I3Double(1)
#    hpLowBinCut = dataclasses.I3Double(1)


  frame['NumString2NHit']=dataclasses.I3Double(len(nStrings))
  frame['NumString2NHit3']=dataclasses.I3Double(len(nStrings3))
  frame['String3X']=dataclasses.I3Double(string3X)
  frame['String3Y']=dataclasses.I3Double(string3Y)
  frame['String3Z']=dataclasses.I3Double(string3Z)
  frame['String3T']=dataclasses.I3Double(string3T)
#  frame['String3LowQPosDiff']=posDiff
  frame['String3LowQTDiff']=tDiff
  frame['String3ATWDTDiff']=atDiff
  frame['String3MaxTDiff']=mtDiff
  frame['FirstStringDiff']= dataclasses.I3Double(string3T2-string3T)
  frame['FirstPairDiff']= dataclasses.I3Double(string23T-string3T)
  frame['SecondPairDiff']= dataclasses.I3Double(string23T2-string3T2)
  frame['SecondStringDiff']= dataclasses.I3Double(string23T2-string23T)
  frame['LenS3']=dataclasses.I3Double(len(s3Pulse))
  frame['ZRatVal']=ratVal
  frame['NHZRatVal']=eratVal
  frame['TimeAvg']=dataclasses.I3VectorDouble(time_avg)
  frame['CHAvg']=dataclasses.I3VectorDouble(ch_avg)
  frame['MedZ']=dataclasses.I3VectorDouble(med_z)
  frame['MaxZDist']=dataclasses.I3VectorDouble(z_dist)
  frame['XPosAvg']=dataclasses.I3VectorDouble(x_pos_avg)
  frame['YPosAvg']=dataclasses.I3VectorDouble(y_pos_avg)
  frame['ZPosAvg']=dataclasses.I3VectorDouble(z_pos_avg)
  frame['ZDists']=dataclasses.I3VectorDouble(z_dists)
  frame['StringDist']=dataclasses.I3VectorDouble(string_dist)
  frame['StringTimeDist']=dataclasses.I3VectorDouble(time_dist)
  frame['HitPairCount'] = dataclasses.I3VectorDouble(stringCount)
  frame['NHHitCount'] = dataclasses.I3VectorDouble(nhstringCount)
  frame['OneStringZVect'] = dataclasses.I3VectorDouble(oszVect)
  frame['NHOneStringZVect'] = dataclasses.I3VectorDouble(nhzVect)
  frame['HPBinRat']=hpBinRat
  frame['HPZeroBin']=hpZeroBin
  frame['HPLowBin']=hpLowBin
  frame['HPBinRatSum']=hpBinRatSum
#  frame['HPBinRatCut']=hpBinRatCut
#  frame['HPZeroBinCut']=hpZeroBinCut
#  frame['HPLowBinCut']=hpLowBinCut
#  frame['HPBinRatSumCut']=hpBinRatSumCut
  frame['NStrings']=nStrings
  frame['NHitsString']=stringHits
  frame['StringXPos']=stringXPos
  frame['StringYPos']=stringYPos
  frame['StringZPos']=stringZPos
  frame['TimeDist']=timeDist
  frame['ChargeDist']=chargeDist
  frame['NStrings3']=nStrings3
  frame['NHitsString3']=stringHits3
  frame['StringXPos3']=stringXPos3
  frame['StringYPos3']=stringYPos3
  frame['StringZPos3']=stringZPos3
  frame['TimeDist3']=timeDist3
  frame['ChargeDist3']=chargeDist3
  frame['AllVels']=dataclasses.I3VectorDouble(allvelList)
  frame['VelocityMed']=velMedVec
  frame['VelocityMean']=velMeanVec
  frame['ZenithMed']=zenMedVec
  frame['ZMedVal']=zMedVal
#  frame['ZMedValCut']=zMedValCut
  frame['UnitVecLength']=uVecLen
#  frame['UnitVecLengthCut']=uVecLenCut
  frame['ZenithMean']=zenMeanVec
  frame['ZenithMedVal']=zenMedVal
  frame['ZenithMeanVal']=zenMeanVal
  frame['AzimuthMedVal']=aziMedVal
  frame['AzimuthMeanVal']=aziMeanVal
#  frame['ZenithMedValCut']=zenMedValCut
#  frame['ZenithMeanValCut']=zenMeanValCut
#  frame['AzimuthMedValCut']=aziMedValCut
#  frame['AzimuthMeanValCut']=aziMeanValCut
  frame['AzimuthMed']=aziMedVec
  frame['AzimuthMean']=aziMeanVec
#  frame['VMFDK0']=vmfdK0
#  frame['VMFDK1']=vmfdK1
#  frame['VMFDK2']=vmfdK2
#  frame['VMFDK0Cut']=vmfdK0Cut
#  frame['VMFDK1Cut']=vmfdK1Cut
#  frame['VMFDK2Cut']=vmfdK2Cut


tray.AddModule(pulseAlgs,'pAlgs')

#tray.AddModule(StringNHits,'sNHits')
#Make Root and Pytable Writers with keys->Frames I want in the trees, SubEventStreams has to be set for Q frames for some reason... 
tray.AddModule(I3TableWriter,'writer', tableservice = [hdf], SubEventStreams = ["in_ice"], types=[icetray.I3Bool, dataclasses.I3Double, dataclasses.I3EventHeader, dataclasses.I3MCTree, dataclasses.I3TriggerHierarchy, dataclasses.I3Particle], keys=['I3MCWeightDict','LenS3','AllVels','TimeAvg','CHAvg','MedZ','MaxZDist','XPosAvg','YPosAvg','ZPosAvg','ZDists','StringDist','StringTimeDist','String3X','String3Y','String3Z','String3T','String3LowQPosDiff','String3LowQTDiff','String3ATWDTDiff','String3MaxTDiff','ZRatVal','SebL7Dist','S3L7Time','SebL7Time','NHZRatVal','HitPairCount','NHHitCount','OneStringZVect','NHOneStringZVect','HPBinRat','HPBinRatCut','HPBinRatSum','HPBinRatSumCut','HPLowBin','HPLowBinCut','HPZeroBin','HPZeroBinCut','NStrings','NStrings3','StringXPos','StringXPos3','StringYPos','StringYPos3','StringZPos','StringZPos3','NHitsString','NHitsString3','TimeDist','TimeDist3','ChargeDist','ChargeDist3','VelocityMed','VelocityMean','AzimuthMean','AzimuthMeanVal','AzimuthMeanValCut','AzimuthMed','AzimuthMedVal','AzimuthMedValCut','ZenithMed','ZenithMedVal','ZenithMedValCut','VMFDK0','VMFDK0Cut','VMFDK1','VMFDK1Cut','VMFDK2','VMFDK2Cut','ZMedVal','ZMedValCut','UnitVecLength','UnitVecLengthCut','ZenithMean','ZenithMeanVal','ZenithMeanValCut','DCTrigTime','weight','MostEnergMuon','MostEnergPrim','MostEnergCasc','I3EventHeader','I3MCTree','I3TriggerHierarchy','CorsikaWeightMap','FirstStringDiff','FirstPairDiff','SecondStringDiff','SecondPairDiff'])
#Make everything nice 
tray.AddModule('TrashCan','yeswecan')
#Run It 
tray.Execute(100)
#Done! 
tray.Finish()
