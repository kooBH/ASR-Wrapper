#-*- coding:utf-8 -*-

import os,sys
import urllib3
import json
import base64

import time

openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
accessKey = "YOUR_ACCESS_KEY"
languageCode = "korean"
 
fileKey = open("key/ETRI.key","r") 
accessKey = fileKey.readline()
accessKey = accessKey.rstrip('\n')
fileKey.close()

#print('ACCESSKEY::'+str(accessKey))

def ASR(audioFilePath):
  audioFilePath= audioFilePath
  file = open(audioFilePath, "rb")
  audioContents = base64.b64encode(file.read()).decode("utf8")
  file.close()
   
  requestJson = {
      "access_key": accessKey,
      "argument": {
          "language_code": languageCode,
          "audio": audioContents
      }
  }
   
  http = urllib3.PoolManager()

  try : 
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
 
    data = response.data.decode('utf-8')
    json_data = json.loads(data)
    #print(json_data)
    if(json_data['result']==0) :
      ret = json_data['return_object']['recognized']
    else :
      ret = json_data['reason']
    return ret
  except Exception as ex: 
    print('ETRI::First Exception occurred')
    try : 
      response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
      )
 
      data = response.data.decode('utf-8')
      json_data = json.loads(data)
      #print(json_data)
      if(json_data['result']==0) :
        ret = json_data['return_object']['recognized']
      else :
        ret = json_data['reason']
      return ret
    except Exception as ex: 
      print(ex)
      return str(ex)
                        