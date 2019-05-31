import requests
import json
import time
import os
from bs4 import BeautifulSoup
from io import BytesIO

if __name__ == "__main__":
    headers = {
        'Referer':'http://202.115.47.141/login',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Host':'202.115.47.141'
        }
    evaheaders={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://202.115.47.141',
            'Referer': 'http://202.115.47.141/student/teachingEvaluation/teachingEvaluation/evaluationPage',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        #get
    login_url = 'http://202.115.47.141/login' 
    post_url = 'http://202.115.47.141/j_spring_security_check'
    logincaptcha = 'http://202.115.47.141/img/captcha.jpg'
    evaluatedCourseInfo = 'http://202.115.47.141/student/teachingEvaluation/teachingEvaluation/search'
    evaluationPage = 'http://202.115.47.141/student/teachingEvaluation/teachingEvaluation/evaluationPage'
    evaluationpost = 'http://202.115.47.141/student/teachingEvaluation/teachingEvaluation/evaluation'
    session = requests.Session()


    print('SsorryQaQ的自动评教小工具')
    username = input("请输入学号：")
    passwd =  input("请输入密码：")

    imgbuf = session.get(logincaptcha).content
    file_handle=open('验证码.png',mode='wb')
    
    file_handle.write(imgbuf)
    file_handle.close()
    vercode = input("输入验证码(验证码再本程序根目录下`验证码.png`):")



    post_data = {
        'j_username':username,
        'j_password':passwd,
        'j_captcha':str(vercode)
    }
    
    response = session.post(post_url,data=post_data,headers=headers)
    # response = session.get(get_user_url,headers = headers)
    data = response.content
    data = BeautifulSoup(data,'lxml')
    user = data.find('span',attrs = {"class":"user-info"})
    print(user)

    response = session.post(evaluatedCourseInfo,headers=headers)
    response = response.json()
    coursesInfo = response.get('data')

    for course in coursesInfo:
        evaluatedPeople = course['evaluatedPeople']
        evaluatedContent = course['evaluationContent']

        coureSequenceNumber_id = course['id']['coureSequenceNumber']
        evaluatedPeople_id = course['id']['evaluatedPeople']
        evaluationContentNumber_id = course['id']['evaluationContentNumber']
        questionnaireCoding_id = course['id']['questionnaireCoding']
        questionnaireName = course['questionnaire']['questionnaireName']
        isEvaluated = course['isEvaluated']
        if (isEvaluated == "是"):
            print(evaluatedPeople + '的' + evaluatedContent + '课程已经评教..自动跳过..ヾ|≧_≦|〃')
            continue
        evaluationPage_postdata = {
            'evaluatedPeople': evaluatedPeople,
            'evaluatedPeopleNumber': evaluatedPeople_id,
            'questionnaireCode': questionnaireCoding_id,
            'questionnaireName': questionnaireName,
            'evaluationContentNumber': evaluationContentNumber_id,
            'evaluationContentContent': ''
        }
        evaluatedPage = session.post(evaluationPage,data=evaluationPage_postdata,headers=headers)
        evaluatedPage = evaluatedPage.content
        evaluatedPage = BeautifulSoup(evaluatedPage,'lxml')
        tokenValue = evaluatedPage.find('input',attrs = {"name":"tokenValue"})['value']

        ketang_postdata = {
            'tokenValue':tokenValue,
            'questionnaireCode':questionnaireCoding_id,
            'evaluationContentNumber':evaluationContentNumber_id,
            'evaluatedPeopleNumber':evaluatedPeople_id,
            'count':'0',
            '0000000107':'10_1',
            '0000000108':'10_1',
            '0000000123':'10_1',
            '0000000127':'10_1',
            '0000000128':'10_1',
            '0000000129':'10_1',
            '0000000131':'10_1',
            'zgpj':'test'
        }
        
        tiyu_postdata = {
            'tokenValue':tokenValue,
            'questionnaireCode':questionnaireCoding_id,
            'evaluationContentNumber':evaluationContentNumber_id,
            'evaluatedPeopleNumber':evaluatedPeople_id,
            '0000000096':'10_1',
            '0000000097':'10_1',
            '0000000098':'10_1',
            '0000000099':'10_1',
            '0000000100':'10_1',
            '0000000101':'10_1',
            '0000000102':'10_1',
            'zgpj':'test'
        }

        shiyan_postdata = {
            'tokenValue':tokenValue,
            'questionnaireCode':questionnaireCoding_id,
            'evaluationContentNumber':evaluationContentNumber_id,
            'evaluatedPeopleNumber':evaluatedPeople_id,
            '0000000082':'10_1',
            '0000000083':'10_1',
            '0000000084':'10_1',
            '0000000085':'10_1',
            '0000000086':'10_1',
            '0000000087':'10_1',
            '0000000088':'10_1',
            'zgpj':'test'
        }

        zhujiao_postdata = {
            'tokenValue':tokenValue,
            'questionnaireCode':questionnaireCoding_id,
            'evaluationContentNumber':evaluationContentNumber_id,
            'evaluatedPeopleNumber':evaluatedPeople_id,
            '0000000028':'10_1',
            '0000000029':'10_1',
            '0000000030':'10_1',
            '0000000031':'10_1',
            '0000000032':'10_1',
            '0000000033':'10_1',
            'zgpj':'test'
        }
        if (questionnaireName == "学生评教（课堂教学）"):
            session.post(evaluationpost,headers = evaheaders,data=ketang_postdata)
        if (questionnaireName == "学生评教（实验教学）"):
            session.post(evaluationpost,headers = evaheaders,data=shiyan_postdata)
        if (questionnaireName == "学生评教（体育教学）"):
            session.post(evaluationpost,headers = evaheaders,data=tiyu_postdata)
        if (questionnaireName == "研究生助教评价"):
            session.post(evaluationpost,headers = evaheaders,data=zhujiao_postdata)
            
        print(evaluatedPeople + '的' + evaluatedContent + '课程评教完成..自动等待2分钟ヾ|≧_≦|〃')
        i = 122
        while (i > 0):
            print('当前剩余:'+ str(i) + 's...')
            i-=1
            time.sleep(1)
