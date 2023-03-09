import requests
import xml.etree.ElementTree as ET
import math


def update_RAPID_var(name, value):
    ip = "http://localhost/rw/rapid/symbol/data/RAPID"
    robot = "T_ROB1"
    module = "Module1"
    url = ip+"/"+robot+"/"+module+"/"+name+"?action=set"
    username = "Default User"
    password = "robotics"
    data = {"value": value}

    rp=requests.post(url, auth=requests.auth.HTTPDigestAuth(username, password), data=data)
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
    
def set_robtarget_translation(var, trans):
    """Sets the translational data of a robtarget variable in RAPID.
    """
    #_trans, rot = self.get_robtarget_variables(var)
    update_RAPID_var(var, "[[" + ','.join(
        [str(s) for s in trans]) + "],[0,1,0,0],[-1,0,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]]")

def set_wobj(var, trans):

    update_RAPID_var(var,"[FALSE,TRUE,\"\",[[0.0,65.1388,-4.75403],[0.999928,-0.00335534,-0.00260265,0.011206]],[[0,0,0],[1,0,0,0]]]")
    
update_RAPID_var("offX",90)
set_robtarget_translation("nocam",[0.0,0.1,0.1])
set_wobj("wobj_cam",[])