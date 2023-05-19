import requests
import xml.etree.ElementTree as ET
import time


class ABBWebService:
    """Class implenmenting ABB Robot Web Services in python.
    """

    def __init__(self, base_url="http://192.168.125.1:80/rw/rapid/symbol/data/RAPID", username='Default User', password='robotics', module='ModuleHVdemo'):
        self.ip = base_url
        self.robot = "T_ROB1"
        self.module = module
        self.username = username
        self.password = password
        self.auth=requests.auth.HTTPDigestAuth(self.username, self.password)
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '-http-session-=74::http.session::3c444662a8e5344528ff1f7395168f92; ABBCX=6'
            }
        self.session=requests.Session()

    def requestRMMP(self):


        url = "http://192.168.125.1:80/users/rmmp"
        data = {"privilege": "modify"}

        rp=self.session.post(url, auth=self.auth, data=data,headers=self.headers)
        print(rp.text)
        print(rp.cookies)
        #url = "http://192.168.125.1:80/users/rmmp/poll"
        #rp=requests.get(url, auth=self.auth, data=data,headers=self.headers)
        print(rp.status_code)
        # 设置cookie
        cookie = '-http-session-={0}; ABBCX={1}'.format(rp.cookies['-http-session-'], rp.cookies['ABBCX'])
        # 设置Coookie
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie
            }
        if(rp.status_code==202):
            print("Get RMMP")
            
            rp.close()
            
            return rp.text
        else:
            rp.close()
            return rp.text

    def get_RAPID_var(self, name):
        url = self.ip+"/"+self.robot+"/"+self.module+"/"+name
        rp=self.session.get(url, auth=self.auth,headers=self.headers)
        print(rp.status_code)
        root = ET.fromstring(rp.text)
        # Find the element with the class "rap-data"
        rap_data = root.find(".//*[@class='rap-data']")
        response_data = rap_data.find(".//*[@class='value']")
        if(rp.status_code==200):
            print("Variable "+name+" is "+response_data.text+"!")
            rp.close()
            return response_data.text
        else:
            rp.close()
            return None
        
    def update_RAPID_var(self, name, value):
        url = self.ip+"/"+self.robot+"/"+self.module+"/"+name+"?action=set"
        data = {"value": value}
        rp=requests.post(url, auth=self.auth, data=data,headers=self.headers)
        print("status code: "+str(rp.status_code))
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
        if(rp.status_code==204):
            print("Variable "+name+" is updated to "+str(value)+"!")
            rp.close()
            return True
        else:
            rp.close()
            return False
    
    #need to develop so that we can modify a part of the data
    def set_robtarget(self, var, trans, rot):
        """Sets the robtarget variable in RAPID.
        """
        rp=self.update_RAPID_var(var, "[[" + ','.join(
            [str(s) for s in trans]) + "]"+ ",[" +','.join(
            [str(s) for s in rot]) + "],[-1,0,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]]")
        if(rp):
            print("Variable "+var+" is updated to!")
            return True
        else:
            return False
    
    def set_wobj(self, var, trans, rot):


        rp=self.update_RAPID_var(var,"[FALSE,TRUE,\"\","+ "[[" + ','.join(
            [str(s) for s in trans]) + "]"+ ",[" +','.join(
            [str(s) for s in rot]) +"]],[[0,0,0],[1,0,0,0]]]")
        if(rp):
            print("Variable "+var+" is updated!")
            return True
        else:
            return False
        
    def communication_handshake(self, name, value, flag_name):
        while(True):
            time.sleep(0.5)
            if(self.update_RAPID_var(flag_name,"1")):
                print("Flag up")
                break
        while(self.get_RAPID_var(flag_name)=="1"):
            print("Wait for flag down")
            pass
        while(True):
            time.sleep(0.5)
            if(self.update_RAPID_var(name,value)):
                print("Updateing value")
                break
        while(True):
            time.sleep(0.5)
            if(self.update_RAPID_var(flag_name,"1")):
                print("Raise flag")
                break
                
                
    def communication_handshake_wobj(self, var, trans, rot, flag_name):
        while(True):
            time.sleep(0.5)
            if(self.update_RAPID_var(flag_name,"1")):
                print("Flag up")
                break
        while(self.get_RAPID_var(flag_name)=="1"):
            time.sleep(0.5)
            print("Wait for flag down")
            pass
        while(True):
            time.sleep(0.5)
            if(self.set_wobj(var,trans,rot)):
                print("Updateing value")
                break
        while(True):
            time.sleep(0.5)
            if(self.update_RAPID_var(flag_name,"1")):
                print("Raise flag")
                break
            
    def communication_handshake_robtarget(self, var, trans, rot, flag_name):
        while(True):
            time.sleep(0.5)
            if(self.update_RAPID_var(flag_name,"1")):
                print("Flag up")
                break
        while(self.get_RAPID_var(flag_name)=="1"):
            print("Wait for flag down")
            pass
        while(True):
            if(self.set_robtarget(var,trans,rot)):
                print("Updateing value")
                break
        while(True):
            if(self.update_RAPID_var(flag_name,"1")):
                print("Raise flag")
                break

    
#serviceA = ABBWebService()
#serviceA.update_RAPID_var("offX",122)
#serviceA.set_robtarget("nocam",[100.0,0.1,0.1],[0.0,0.1,0.2,0.1])
