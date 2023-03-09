import requests
import xml.etree.ElementTree as ET

class ABBWebService:
    """Class implenmenting ABB Robot Web Services in python.
    """

    def __init__(self, base_url="http://localhost/rw/rapid/symbol/data/RAPID", username='Default User', password='robotics', module='Module1'):
        self.ip = base_url
        self.robot = "T_ROB1"
        self.module = module
        self.username = username
        self.password = password
        self.auth=requests.auth.HTTPDigestAuth(self.username, self.password)

        
    def update_RAPID_var(self, name, value):
        url = self.ip+"/"+self.robot+"/"+self.module+"/"+name+"?action=set"
        data = {"value": value}
        rp=requests.post(url, auth=self.auth, data=data)
        #url = ip+"/"+robot+"/"+module+"/"+name
        #response = requests.get(url,auth=requests.auth.HTTPDigestAuth(username, password))
        #root = ET.fromstring(response.text)
        # Find the element with the class "rap-data"
        #rap_data = root.find(".//*[@class='rap-data']")

        # Find the <span> element with the class "value" inside "rap-data"
        #response_data = rap_data.find(".//*[@class='value']")

        # Print the result  
        #while(not math.isclose(float(response_data.text), value)):
            #print("waiting for sugnal to update")
        print(rp.text)
        print("Variable "+name+" is updated to "+str(value)+"!")
    
    #need to develop so that we can modify a part of the data
    def set_robtarget(self, var, trans, rot):
        """Sets the robtarget variable in RAPID.
        """
        self.update_RAPID_var(var, "[[" + ','.join(
            [str(s) for s in trans]) + "]"+ ",[" +','.join(
            [str(s) for s in rot]) + "],[-1,0,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]]")
    
    def set_wobj(self, var, trans, rot):
        self.update_RAPID_var(var,"[FALSE,TRUE,\"\","+ "[[" + ','.join(
            [str(s) for s in trans]) + "]"+ ",[" +','.join(
            [str(s) for s in rot]) +"]],[[0,0,0],[1,0,0,0]]]")
    
serviceA = ABBWebService()
serviceA.update_RAPID_var("offX",122)
serviceA.set_robtarget("nocam",[100.0,0.1,0.1],[0.0,0.1,0.2,0.1])
serviceA.set_wobj("wobj_cam",[200.0,20.323,232.323],[0.1,0.33,0.2,0.2])