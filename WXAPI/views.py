import json
from mysite import myResponse
from rest_framework.views import APIView
from WXAPI.subject import Subject
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
from selenium.common import exceptions
from django.core import serializers
# Create your views here.
class GradeTable(APIView):
    def get(self, request):
        # 创建 WebDriver 对象，指明使用chrome浏览器驱动
        wd = webdriver.Chrome(service=Service(r'chromedriver_win32/chromedriver.exe'))
        # 调用WebDriver 对象的get方法 可以让浏览器打开指定网址
        wd.get('https://jwglxt-proxy3.buct.edu.cn/jwglxt/xtgl/login_slogin.html?time=1609818249232')
        List = []
        try:
            ID = request.query_params['id']
            Password = request.query_params['passwd']
            semester = request.query_params['semester']
            if semester == "全部":
                semester = 0
            else:
                semester = eval(semester)
            # 根据id选择元素，返回的就是该元素对应的WebElement对象
            wd.find_element(By.ID, 'yhm').send_keys(ID)
            wd.find_element(By.ID, 'mm').send_keys(Password)
            # 通过该 WebElement对象，就可以对页面元素进行操作了
            wd.find_element(By.ID, 'dl').click()
            wd.implicitly_wait(5)
            wd.find_elements(By.ID, 'drop1')[3].click()
            wd.find_element(By.CSS_SELECTOR, '#cdNav > ul > li.dropdown.open > ul > li:nth-child(6) > a').click()
            for handle in wd.window_handles:
                # 先切换到该窗口
                wd.switch_to.window(handle)
                # 得到该窗口的标题栏字符串，判断是不是我们要操作的那个窗口
                if '学生成绩查询' in wd.title:
                    # 如果是，那么这时候WebDriver对象就是对应的该窗口，正好，跳出循环，
                    break
            wd.find_element(By.ID, 'xqm_chosen').click()
            select = wd.find_element(By.CSS_SELECTOR, '#xqm_chosen > div > ul')
            select.find_elements(By.TAG_NAME, 'li')[semester].click()
            # 暂停一秒点击查询才有效
            sleep(0.5)
            wd.find_element(By.ID, 'search_go').click()
            # 暂停一秒等待获取成绩列表
            sleep(0.5)
            html = wd.find_element(By.ID, 'tabGrid').get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'lxml')
            for line in soup.find_all(class_="ui-widget-content jqgrow ui-row-ltr"):
                credit = line.find(attrs={"aria-describedby": "tabGrid_xf"}).string
                score = line.find(attrs={"aria-describedby": "tabGrid_cj"}).string
                gradePoint = line.find(attrs={"aria-describedby": "tabGrid_xfjd"}).string
                schoolYear = line.find(attrs={"aria-describedby": "tabGrid_xnmmc"}).string
                # semester = line.fing(attrs={"aria-describedby": "tabGrid_xqmmc"}).string 有BUG
                name = line.find(attrs={"aria-describedby": "tabGrid_kcmc"}).string
                grade = line.find(attrs={"aria-describedby": "tabGrid_xf"}).string
                class_ = line.find(attrs={"aria-describedby": "tabGrid_jxbmc"}).string
                teacher = line.find(attrs={"aria-describedby": "tabGrid_jsxm"}).string
                subject = Subject(str(credit), str(score), str(gradePoint), str(schoolYear), str(name), str(grade), str(class_), str(teacher))
                # print(subject.schoolYear, subject.semester, subject.name, subject.credit, subject.score, subject.grade,
                #       subject.class_, subject.teacher, subject.gradePoint)
                if subject.score != "合格" or subject.score != "不合格":
                    List.append(subject.jsonserializer())
            if len(List) == 0:
                return myResponse.OK(msg="暂无成绩")
            # sum_gradePoint = 0
            # sum_credit = 0
            # for subject in List:
            #     sum_gradePoint += eval(subject.gradePoint)
            #     sum_credit += eval(subject.credit)
            # GPA = sum_gradePoint / sum_credit
            # print(GPA)
        except IndexError:
            tips = wd.find_element(By.ID, 'tips').text
            if(tips == ""):
                return myResponse.Error("加载失败，请重试")
            return myResponse.Error(tips)
        except:
            return myResponse.Error("未知错误")
        finally:
            wd.quit()
        return myResponse.OK(data=json.dumps(List, ensure_ascii=False))