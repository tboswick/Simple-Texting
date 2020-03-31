import requests
import xmltodict
import xml.etree.ElementTree as ET

class ResponseError(Exception):
    pass

class Client():

    def __init__(self, url="https://app2.simpletexting.com/v1/", token=None, session=None):
        self.url = url
        self.token = token
        self.session = session or requests.Session()

    def __request(self, dest=None, group=None,  request=None):
        headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
        }

        request['token'] = self.token

        url = self.url + dest
        res = self.__make_req(url, headers, request)
        parsed = ET.XML(res.text)

        response = list(xmltodict.parse(ET.tostring(parsed)).items())
        response = dict(response[0][1])

        errcode = response['code']
        errtext = response['message']
        if int(errcode) < 0:
            raise ResponseError('Received err #{0} : {1}'.format(errcode, errtext))

        return parsed

    def __make_req(self, url=None, headers=None, data=None):
        res = self.session.post(url,data,headers)
        return res

    def get_contacts(self, group):
        req = {}
        req['group'] = group
        dest='group/contact/list/'
        res = self.__request(dest, request=req)
        return xmltodict.parse(ET.tostring(res))

    def send_message(self, numbers, message):
        req = {}
        results = []
        dest = 'send/'
        for i in numbers:
            req['phone'] = i
            req['message'] = message
            res = self.__request(dest, request=req)
            results.append(xmltodict.parse(ET.tostring(res)))
            #response = dict(response[0][1])
        #return results

    def check_message_count(self):
        req = {}
        dest = 'messaging/check'
        res = self.__request(dest, request=req)
        response = list(xmltodict.parse(ET.tostring(res)).items())
        response = dict(response[0][1])
        return response['messagesCount']

    def check_keyword_availability(self, keyword):
        req = {}
        dest = 'keyword/check'
        req['keyword'] = keyword
        res = self.__request(dest, request=req)
        response = list(xmltodict.parse(ET.tostring(res)).items())
        response = dict(response[0][1])
        return response['message']
