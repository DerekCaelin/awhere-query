import http.client
import pandas as pd
import json


inputfile = pd.read_csv('input.csv') #file with just latitude and longitutde coordinates. If you have other columns, need to add them to the output file below
timestart = "2017-09-01" #begining timeframe
timestop = "2017-09-06" #ending timeframe
conn = http.client.HTTPSConnection("api.awhere.com")

from credentials import headers as headers
newheaders = {}
output = []
accessToken = ""

def defineFilestructure():
    global output
    output = pd.DataFrame(columns = inputfile.columns.values)
    print(output)
    output['ppet'] =""
    output['precipitation'] =""
    output['pet'] =""
    print(output)
    
def getAuthorization():
    #set up api request
    conn = http.client.HTTPSConnection("api.awhere.com")
    payload = "grant_type=client_credentials"
    


    #request an auth token
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    datab = json.loads(data)
    
    #remember the auth token
    global accessToken
    accessToken = datab['access_token']
    print("got accessToken "+accessToken)
    
    #include auth token in my query
    global newheaders
    newheaders = {
        'authorization': "Bearer "+accessToken,
        }
     
def queryAPI():
    #for each lat, long in the input file
     for i in range(0,len(inputfile)):

        #ask for agronomic data
        conn.request("GET", "/v2/agronomics/locations/"+str(inputfile.loc[i,"Latitude"])+","+str(inputfile.loc[i,"Longitude"])+"/agronomicvalues/"+timestart+","+timestop+"?properties=accumulations", headers=newheaders)
        
        res = conn.getresponse()
        data = res.read()
        datab = json.loads(data)
        
        #read the api's json output, get variables
        try:
              
            precipitation = (datab['accumulations']['precipitation']['amount'])
            try:
                #sometimes there's no value for pet (evaporation)
                pet = datab['accumulations']['pet']['amount']
            except:
                pet ="Unknown"
                    
            if pet != "Unknown":
                try:
                    #and if there's no value for evap you can't calculate the ratio of precip to evap
                    ppet = precipitation/pet
                except:
                    ppet = "Unknown"
            else:
                pet = "Unknown"
                ppet = "Unknown"
                    
            Latitude = inputfile.loc[i,"Latitude"]
            Longitude = inputfile.loc[i,"Longitude"]
            
            #keep me posted on progress
            print("At row "+str(i)+" of "+str(len(inputfile))+", getting values")   
            
            #add any other column fields that are in your input file
            output.loc[i] = [inputfile.loc[i,"Latitude"],inputfile.loc[i,"Longitude"],ppet,precipitation,pet]
        except:
            print("error at row "+str(i)+", "+str(inputfile.loc[i,"Latitude"])+","+str(inputfile.loc[i,"Longitude"]))

def putOutThatOutput():
    #exports the results as output
    filename = 'output.csv'
    output.to_csv(filename, index=False, encoding='utf-8')
    print(output)
    
###START    
    
defineFilestructure()
if accessToken == "":
    getAuthorization()
queryAPI()
putOutThatOutput()

