from flask import Flask, render_template,request
import csv
iqzone = Flask(__name__)

@iqzone.route('/')
def index():
	return render_template('index.html')

def compare(inputtext,datalist,rangeset,yestotal,nototal):
	yescont = 0
	nocont =0
	if float(inputtext)>=rangeset[0] and float(inputtext)<=rangeset[1]:
		yescont = datalist[0][1]/yestotal
		nocont =  datalist[0][2]/nototal
	if float(inputtext)>=rangeset[2] and float(inputtext)<=rangeset[3]:
		yescont = datalist[1][1]/yestotal
		nocont =  datalist[1][2]/nototal
	if float(inputtext)>=rangeset[4] and float(inputtext)<=rangeset[5]:
		yescont = datalist[2][1]/yestotal
		nocont =  datalist[2][2]/nototal	
	return yescont,nocont

def datacount(columnlist,rangeset,resultlist,databracket):
	for row in range(len(columnlist)):  
		if columnlist[row]>=rangeset[0] and columnlist[row]<=rangeset[1] and resultlist[row]==1:databracket[0][1]+=1
		elif columnlist[row]>=rangeset[0] and columnlist[row]<=rangeset[1] and resultlist[row]==0:databracket[0][2]+=1
		if columnlist[row]>=rangeset[2] and columnlist[row]<=rangeset[3] and resultlist[row]==1:databracket[1][1]+=1
		elif columnlist[row]>=rangeset[2] and columnlist[row]<=rangeset[3] and resultlist[row]==0:databracket[1][2]+=1
		if columnlist[row]>=rangeset[4] and columnlist[row]<=rangeset[5] and resultlist[row]==1:databracket[2][1]+=1
		elif columnlist[row]>=rangeset[4] and columnlist[row]<=rangeset[5] and resultlist[row]==0:databracket[2][2]+=1	 	
	return databracket

@iqzone.route('/predict',methods=['POST','GET'])
def predict():
	form = request.form
	InputGender= form.get('gender')
	InputAge = form.get('age')
	InputTime = form.get('time')
	InputWarts = form.get('numwarts')
	InputType = form.get('typewarts')
	InputArea = form.get('areawarts')
	LineCounter = 0
	GenderSet=[]
	AgeSet = []
	TimeSet = []
	WartsSet = []
	TypeSet=[]
	AreaSet = []
	ResultsSet = []

	with open('warts.csv','r') as csv_file:
		for row in csv_file:
			csvList = row.split(',')
			if LineCounter==0:
				LineCounter+=1
			else:
				GenderSet.append(csvList[0])
				AgeSet.append(float(csvList[1]))
				TimeSet.append(float(csvList[2]))
				WartsSet.append(float(csvList[3]))
				TypeSet.append(csvList[4])
				AreaSet.append(float(csvList[5]))
				ResultsSet.append(int(csvList[6]))
				LineCounter+=1

		AgeInterval = (max(AgeSet)-min(AgeSet))/3
		TimeInterval = (max(TimeSet)-min(TimeSet))/3
		WartsInterval = (max(WartsSet)-min(WartsSet))/3
		AreaInterval = (max(AreaSet)-min(AreaSet))/3

		AgeRange = [min(AgeSet),min(AgeSet)+AgeInterval,min(AgeSet)+AgeInterval,min(AgeSet)+AgeInterval+AgeInterval,min(AgeSet)+AgeInterval+AgeInterval,max(AgeSet)]
		TimeRange = [min(TimeSet),min(TimeSet)+TimeInterval,min(TimeSet)+TimeInterval,min(TimeSet)+TimeInterval+TimeInterval,min(TimeSet)+TimeInterval+TimeInterval,max(TimeSet)]
		WartsRange = [min(WartsSet),min(WartsSet)+WartsInterval,min(WartsSet)+WartsInterval,min(WartsSet)+WartsInterval+WartsInterval,min(WartsSet)+WartsInterval+WartsInterval,max(WartsSet)]
		AreaRange = [min(AreaSet),min(AreaSet)+AreaInterval,min(AreaSet)+AreaInterval,min(AreaSet)+AreaInterval+AreaInterval,min(AreaSet)+AreaInterval+AreaInterval,max(AreaSet)]
		GenCount = [["Male:  ",0,0],["Female:  ",0,0]]
		TypeCount=[["Type 1:",0,0],["Type 2:",0,0],["Type 3:",0,0]]
		AgeBracket=[[str(str(AgeRange[0])+" - "+str(AgeRange[1])),0,0],[str(str(AgeRange[2])+" - "+str(AgeRange[3])),0,0],[str(str(AgeRange[4])+" - "+str(AgeRange[5])),0,0]]
		TimeBracket=[[str(str(TimeRange[0])+" - "+str(TimeRange[1])),0,0],[str(str(TimeRange[2])+" - "+str(TimeRange[3])),0,0],[str(str(TimeRange[4])+" - "+str(TimeRange[5])),0,0]]
		WartBracket=[[str(str(WartsRange[0])+" - "+str(WartsRange[1])),0,0],[str(str(WartsRange[2])+" - "+str(WartsRange[3])),0,0],[str(str(WartsRange[4])+" - "+str(WartsRange[5])),0,0]]
		AreaBracket=[[str(str(AreaRange[0])+" - "+str(AreaRange[1])),0,0],[str(str(AreaRange[2])+" - "+str(AreaRange[3])),0,0],[str(str(AreaRange[4])+" - "+str(AreaRange[5])),0,0]]


		for numrow in range(len(GenderSet)):  
			if GenderSet[numrow]=="1" and ResultsSet[numrow]==1: GenCount[0][1]+=1
			elif GenderSet[numrow]=="1" and ResultsSet[numrow]==0: GenCount[0][2]+=1
			if GenderSet[numrow]=="2" and ResultsSet[numrow]==1: GenCount[1][1]+=1
			elif GenderSet[numrow]=="2" and ResultsSet[numrow]==0: GenCount[1][2]+=1 
			if TypeSet[numrow]=="1" and ResultsSet[numrow]==1: TypeCount[0][1]+=1
			elif TypeSet[numrow]=="1" and ResultsSet[numrow]==0:TypeCount[0][2]+=1 
			if TypeSet[numrow]=='2' and ResultsSet[numrow]==1: TypeCount[1][1]+=1
			elif TypeSet[numrow]=='2' and ResultsSet[numrow]==0: TypeCount[1][2]+=1 
			if TypeSet[numrow]=='3' and ResultsSet[numrow]==1: TypeCount[2][1]+=1
			elif TypeSet[numrow]=='3' and ResultsSet[numrow]==0:TypeCount[2][2]+=1
		          

		datacount(AgeSet,AgeRange,ResultsSet,AgeBracket)
		datacount(TimeSet,TimeRange,ResultsSet,TimeBracket)
		datacount(WartsSet,WartsRange,ResultsSet,WartBracket)
		datacount(AreaSet,AreaRange,ResultsSet,AreaBracket)

	            
		TotalYes = AgeBracket[0][1]+AgeBracket[1][1]+AgeBracket[2][1]
		TotalNo = AgeBracket[0][2]+AgeBracket[1][2]+AgeBracket[2][2]
		GenTotal = TotalYes+TotalNo

		for outer in range(len(AgeBracket)):
			for inner in range(1,len(AgeBracket[0])):
				if AgeBracket[outer][inner] ==0:
					AgeBracket[outer][inner]+=1
				if TimeBracket[outer][inner] ==0:
					TimeBracket[outer][inner]+=1
				if WartBracket[outer][inner] ==0:
					WartBracket[outer][inner]+=1
				if AreaBracket[outer][inner] ==0:
					AreaBracket[outer][inner]+=1


		if InputGender=="1":
			genderyes = GenCount[0][1]/TotalYes
			genderno = GenCount[0][2]/TotalNo

		if InputGender=="2":
			genderyes = GenCount[1][1]/TotalYes
			genderno = GenCount[1][2]/TotalNo

		if InputType=="1":
			typeyes = TypeCount[0][1]/TotalYes
			typeno = TypeCount[0][2]/TotalNo

		if InputType=="2":
			typeyes = TypeCount[1][1]/TotalYes
			typeno = TypeCount[1][2]/TotalNo

		if InputType=="3":
			typeyes = TypeCount[2][1]/TotalYes
			typeno = TypeCount[2][2]/TotalNo


		ageyes,ageno = compare(InputAge,AgeBracket,AgeRange,TotalYes,TotalNo)
		timeyes,timeno = compare(InputTime,TimeBracket,TimeRange,TotalYes,TotalNo)
		wartsyes,wartsno = compare(InputWarts,WartBracket,WartsRange,TotalYes,TotalNo)
		areayes,areano = compare(InputArea,AreaBracket,AreaRange,TotalYes,TotalNo)


		Yes = (genderyes/TotalYes)*(typeyes/TotalYes)*(ageyes/TotalYes)* (timeyes/TotalYes) * (wartsyes/TotalYes) *(areayes/TotalYes) * ((TotalYes)/GenTotal)
		No = (genderno/TotalNo)*(typeno/TotalNo)*(ageno/TotalNo)* (timeno/TotalNo) * (wartsno/TotalNo) *(areano/TotalNo) * (TotalNo/GenTotal)
		PerYes = Yes/(No+Yes)
		PerNo = No/(No+Yes)
		Treat = ''
		if PerNo<PerYes:
			Treat = "Treated"
		else:
			Treat = "Not treated"
   

	return render_template('results.html', PerNo=PerNo,PerYes=PerYes,InputGender=InputGender, InputAge=InputAge,InputTime=InputTime,InputType=InputType,InputWarts=InputWarts,InputArea=InputArea,Treat=Treat,GenCount=GenCount,TypeCount=TypeCount,AgeBracket=AgeBracket,TimeBracket=TimeBracket,WartBracket=WartBracket,AreaBracket=AreaBracket,GenTotal=GenTotal)

if __name__ == "__main__":
	iqzone.debug = True
	iqzone.run()

