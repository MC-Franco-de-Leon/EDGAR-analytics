
# code by Mariano Franco de Leon for Insight Data challenge EDGAR-analytics

import csv
import os

#this function computes the elapsed time between two queries (up to days of difference)
def counttime(datetime1,datetime2):
	d1=int(datetime1[8:10])
	d2=int(datetime2[8:10])
	h1=int(datetime1[11:13])
	h2=int(datetime2[11:13])
	m1=int(datetime1[14:16])
	m2=int(datetime2[14:16])
	s1=int(datetime1[17:19])
	s2=int(datetime2[17:19])
	count=(s2-s1)+(m2-m1)*60+(h2-h1)*3600+(d2-d1)*24*3600
	return count
#this function is the easy way to count seconds of sessions with the same date
def rtime(datetime): 
	h1=int(datetime[11:13])
	m1=int(datetime[14:16])
	s1=int(datetime[17:19])
	count=s1+m1*60+h1*3600
	return count
# this function counts the number of seconds between queries with different date
def countgap(otime,ntime):
	y1=int(otime[0:4])	
	mo1=int(otime[5:7])
	d1=int(otime[8:10])
	h1=int(otime[11:13])
	mm1=int(otime[14:16])
	s1=int(otime[17:19])

	y2=int(ntime[0:4])	
	mo2=int(ntime[5:7])
	d2=int(ntime[8:10])
	h2=int(ntime[11:13])
	mm2=int(ntime[14:16])
	s2=int(ntime[17:19])

	leap1=0
	leap2=0
	if (y1 % 4)==0:
		leap1=1
	if (y2 % 4)==0:
		leap2=1

	if leap1==1:
		vecmonths1=[31,29,31,30,31,30,31,31,30,31,30,31]
	else:
		vecmonths1=[31,28,31,30,31,30,31,31,30,31,30,31]

	if leap2==1:
		vecmonths2=[31,29,31,30,31,30,31,31,30,31,30,31]
	else:
		vecmonths2=[31,28,31,30,31,30,31,31,30,31,30,31]
	gapyears=y2-y1
	if gapyears>1:
		return 86401
	else:
		daymonths2=0
		if mo2>1:
			for i in range (0,mo2-1):
				daymonths2=daymonths2+vecmonths2[i]
		daymonths1=0
		if mo1>1:
			for i in range (0,mo1-1):
				daymonths1=daymonths1+vecmonths1[i]

		totaldaysec2=(gapyears*365+daymonths2)*24*3600
		totaldaysec1=(daymonths1)*24*3600
		count2=totaldaysec2+d2*24*3600+h2*3600+mm2*60+s2
		count1=totaldaysec1+d1*24*3600+h1*3600+mm1*60+s1
		count=count2-count1
		if count>86400:
			count=86401
		return count
		
#Here is the main code
#****************************************    		
os.chdir('./input')
per = open('inactivity_period.txt')
lines = per.readlines()
inactivity_period = int(lines[0])


with open('./log.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	os.chdir('..')
	current=os.getcwd()
	os.chdir('./output')	
	prevtime=0
	newtime=0

	opensessions=[[]]
	closesessions=[[]]
	nrows=0
	for row in reader:
		if nrows==0:#initialize date and time
			prevtimedate=row['date']+' '+row['time']
			nrows+=1

		rowip=row['ip']
		rowdate=row['date']
		rowtime=row['time']	
		rowcik=row['cik']
		rowaccession=row['accession']
		rowextention=row['extention']
		newtime=int(rtime(rowdate+' '+rowtime))
		newtimedate=row['date']+' '+row['time']
		looksession=0
		i=0
		j=0
		while (j < len(opensessions)) & (looksession==0):#update elapsed time of each open session
			if not opensessions[j]:#check if the list of open sessions is empty
				opensessions[0]=[rowip,rowdate+' '+rowtime,rowdate+' '+rowtime,0,1]
				looksession=1
			else:
				item=opensessions[j]
				gap=newtime-prevtime
				if gap <= 0 :
					gap=countgap(prevtimedate,newtimedate)
				opensessions[j]=[item[0],item[1],item[2],item[3]+gap,item[4]]
				j+=1
		while (i < len(opensessions)) & (looksession==0):#look if session already exists to update
			item=opensessions[i]#=[ip,dt first,dt last,duration,count]
			if item[0]==rowip:#the user already exist
				looksession=1#update session
				timesession=counttime(item[1],rowdate+' '+rowtime)
				opensessions[i]=[rowip,item[1],rowdate+' '+rowtime,item[3],item[4]+1]
			elif i==len(opensessions)-1:#open new session
				opensessions.append([rowip,rowdate+' '+rowtime,rowdate+' '+rowtime,0,1])
				looksession=1
			else:#keep looking
				i+=1
		n=len(opensessions)
		i=0
		for j in range (0,n):# here we check what sessions is ready to close
			item=opensessions[i]
			timesession=countgap(item[1],item[2])
			if (item[3]-timesession > inactivity_period):#check if it is time to close the session
				if not closesessions[0]:#check if the list of close sessions is empty
					closesessions[0]=[item[0],item[1],item[2],timesession+1,item[4]]
					oline=item[0]+','+item[1]+','+item[2]+','+str(timesession+1)+','+str(item[4])+'\n'
					with open('sessionization.txt', 'w') as Out_file:
        					Out_file.write(oline)	
				else:#close existing session
					closesessions.append([item[0],item[1],item[2],timesession+1,item[4]])
					oline=item[0]+','+item[1]+','+item[2]+','+str(timesession+1)+','+str(item[4])+'\n'
					with open('sessionization.txt', 'a') as Out_file:
        					Out_file.write(oline)
				opensessions.remove(item)
			else:
				i+=1
		prevtime=newtime
		prevtimedate=newtimedate
	#close any other open session
	n=len(opensessions)
	for j in range (0,n):
		item=opensessions[j]
		timesession=counttime(item[1],item[2])
		if not closesessions[0]:#check if the list of close sessions is empty
			closesessions[0]=[item[0],item[1],item[2],timesession+1,item[4]]
		else:#close existing session
			closesessions.append([item[0],item[1],item[2],timesession+1,item[4]])
		oline=item[0]+','+item[1]+','+item[2]+','+str(timesession+1)+','+str(item[4])+'\n'
		with open('sessionization.txt', 'a') as Out_file:
        		Out_file.write(oline)

	print('closed sessions:')#print the results in screen
	for i in range (0,len(closesessions)):
		print(closesessions[i])	



