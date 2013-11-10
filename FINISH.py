import timeit
import itertools
import datetime
import os
start = timeit.default_timer()
def timeFormat(time):
    str=time.split(":")
    return (int(str[2])+int(str[1])*60+int(str[0])*3600)


def Proccess(interval,filename):
    zone = ""

    date=""
    zonecheck=""
    starttime=""
    endtime=""
    nowtimeinterval=0
    price=0
    opv = 0
    clv = 0
    hiv = 0
    lov = 0
    vol = 0
    nowvol=0
    first=True
    invalid=True
    firstend=True
    with open(filename,"r") as splitfile:
        for columns in [line.split("\t") for line in itertools.islice(splitfile,4,None)]:
            datime=columns[0].split(" ")
            nowvol=int(columns[3])
            timesecond=timeFormat(datime[1])
            price=int(columns[2])
            if(date != datime[0]):
                if not os.path.exists(datime[0].replace("/","-")):
                    os.makedirs(datime[0].replace("/","-"))
                myfile = open(datime[0].replace("/","-")+"/"+str(interval)+"morning.txt",'w')
                startime=timeFormat("9:15:00")
                nowtimeinterval=startime
                endtime=timeFormat("12:00:00")
                zone = "morning"
                zonecheck="AM"
                opv = 0
                clv = 0
                hiv = 0
                lov = 0
                Vol = 0
                date=datime[0]
                first=True
            if((columns[1]=="TRADE")&(columns[4].isspace())&(timesecond>=startime)&(timesecond<endtime)&(datime[2]==zonecheck)&(price>0)):
                invalid=True
                #myfile.write(' '.join(columns))
                while(invalid):
                    if(timesecond<(nowtimeinterval+interval)):
                        invalid = False
                        if(first):
                            opv=price
                            hiv=price
                            lov=price
                            clv=price
                            vol=nowvol
                            first = False
                        else:
                            if(price>hiv):
                                hiv=price
                            if(price<lov):
                                lov=price
                            vol+=nowvol
                            clv=price
                            pass
                    else:
                        first=True
                        myfile.write(str(datetime.timedelta(seconds=nowtimeinterval))+"\t"+str(vol)+"\t"+str(opv)+"\t"+str(hiv)+"\t"+str(lov)+"\t"+str(clv)+"\n")
                        nowtimeinterval+=interval
                    pass

            else:
                if(timesecond>endtime):
                    if((zone=="afternoon")&(firstend)&(timesecond<43200)):
                        myfile.write(str(datetime.timedelta(seconds=nowtimeinterval))+"\t"+str(vol)+"\t"+str(opv)+"\t"+str(hiv)+"\t"+str(lov)+"\t"+str(clv)+"\n")
                        myfile.close()
                        firstend=False
                        pass
                    if(zone=="morning"):
                        myfile.write(str(datetime.timedelta(seconds=nowtimeinterval))+"\t"+str(vol)+"\t"+str(opv)+"\t"+str(hiv)+"\t"+str(lov)+"\t"+str(clv)+"\n")
                        startime=timeFormat("1:00:00")
                        nowtimeinterval=startime
                        endtime=timeFormat("4:15:00")
                        zone = "afternoon"
                        zonecheck="PM"
                        opv = 0
                        clv = 0
                        hiv = 0
                        lov = 0
                        Vol = 0
                        date=datime[0]
                        first=True
                        myfile.close()
                        myfile = open(datime[0].replace("/","-")+"/"+str(interval)+"afternoon.txt",'w')
                        pass
            #myfile.write(' '.join(columns))
    
fn = input("Input a file name: ")

for x in range(30, 97):
    Proccess(x,fn);
stop = timeit.default_timer()
print(stop - start) 
input("please enter to exit")