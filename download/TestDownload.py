#-*- codeing = utf-8 -*-
# @Time: 2020-05-12 20:09
# @Author: Claws
# @File: TestDownload.py
# @Software: PyCharm
# @Description: 下载所有题目信息

import json
import multiprocessing
import os
from download.utils.unzip import unzip_question
from download.utils.download import download_one

listOfQuestion = []

def downloadTest(case):
        id=case["case_id"]
        url=case["case_zip"]

        if id not in listOfQuestion:
            # 创建题目目录
            caseDir="TestDownload/"+id+'/'
            try:
                    os.mkdir(caseDir)
            except Exception:
                print(listOfQuestion)
                print('\033[7;31mwarn || 创建 '+id+' 题目文件夹失败，可能文件夹已经存在\033[0m')

            # 下载并解压题目
            questionPath=caseDir+'/tmp.zip'
            download_one(questionPath,url)
            unzip_question(questionPath)
            os.remove(questionPath)

            # 将烦人的文件结构整理清楚
            insideDir = caseDir + '.mooctest/'
            answerPathIn = insideDir + 'answer.py'
            testCasesPathIn = insideDir + 'testCases.json'

            answerPathOut = caseDir + 'answer.py'
            testCasesPathOut = caseDir + 'testCases.json'

            os.rename(answerPathIn, answerPathOut)
            os.rename(testCasesPathIn,testCasesPathOut)
            os.rmdir(insideDir)
            print("info || download complete ===> question "+id)
            listOfQuestion.append(id)


if __name__=="__main__":

    # 创建根目录
    try:
        os.mkdir('TestDownload')
    except Exception:
        print('\033[7;31mwarn || 创建下载文件夹失败，可能文件夹已经存在\033[0m')

    # 导入json文件
    jFile = open('data/test_data.json', encoding='utf-8')
    content = jFile.read()
    data = json.loads(content)

    #多进程下载
    pool = multiprocessing.Pool(1)
    for user in data:
        cases = data[user]
        case = cases["cases"]
        pool.map(downloadTest, case)
    pool.close()
    pool.join()
    print('****************************over****************************')
