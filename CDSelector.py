# coding = utf8
# =====================================================
#   Copyright (C) 2016-2021 All rights reserved.
#   
#   filename : CDSelector.py
#   author   : okcd00 / okcd00@qq.com
#   date     : 2020-09-22
#   desc     : UCAS Course_Selection Program
# =====================================================

import re
import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from configparser import RawConfigParser


index_course = {
    '910': u'数学', '911': u'物理', '957': u'天文', '912': u'化学', '928': u'材料',
    '913': u'生命', '914': u'地球', '921': u'资环', '951': u'计算', '952': u'电子',
    '958': u'工程', '917': u'经管', '945': u'公管', '927': u'人文', '964': u'马克',
    '915': u'外语', '954': u'中丹', '955': u'国际', '959': u'存济', '946': u'体育',
    '961': u'微电', '962': u'未来', '963': u'网络', '968': u'心理', '969': u'人工',
    '970': u'纳米', '971': u'艺术', '972': u'光电', '967': u'创新', '973': u'核学',
    '974': u'现代', '975': u'化学', '976': u'海洋', '977': u'航空', '979': u'杭州'
}

dept_ids_dict = dict([(v, k) for k, v in index_course.items()])


header_store = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
]


class UCASEvaluate:
    def __init__(self):
        self.__read_from_course_id('./courseid')

        cf = RawConfigParser()
        cf.read('config')
        
        self.username = cf.get('info', 'username')
        self.password = cf.get('info', 'password')
        self.runtime = cf.getint('info', 'runtime')
        self.debug = cf.getboolean('action', 'debug')
        self.enroll = cf.getboolean('action', 'enroll')
        self.evaluate = cf.getboolean('action', 'evaluate')
        self.select_bat = cf.getboolean('action', 'select_bat')
        self.watch_logo = cf.getboolean('action', 'watch_logo')

        self.loginPage = 'http://sep.ucas.ac.cn'
        self.loginUrl = self.loginPage + '/slogin'
        self.courseSystem = self.loginPage + '/portal/site/226/821'
        self.courseBase = 'http://jwxk.ucas.ac.cn'
        self.courseLogin = self.courseBase + '/login'
        self.courseIdentify = self.courseBase + '/login?Identity='
        self.courseSelected = self.courseBase + '/courseManage/selectedCourse'
        self.courseSelectionBase = self.courseBase + '/courseManage/main'
        self.courseCategory = self.courseBase + '/courseManage/selectCourse?s='

        self.courseSave = self.courseBase + '/courseManage/saveCourse?s='
        # deptIds=913&sids=9D5ACABA58C8DF02
        # deptIds=913&sids=2585B359205108D6&did_2585B359205108D6=2585B359205108D6

        self.studentCourseEvaluateUrl = 'http://jwjz.ucas.ac.cn/Student/DeskTopModules/'
        self.selectCourseUrl = 'http://jwjz.ucas.ac.cn/Student/DesktopModules/Course/SelectCourse.aspx'

        self.enrollCount = {}
        self.headers = {
            'Host': 'jwxk.ucas.ac.cn',
            'Connection': 'keep-alive',
            # 'Pragma': 'no-cache',
            # 'Cache-Control': 'no-cache',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': header_store[-5],
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        }
        # self.headers = None

        self.s = requests.Session()
        self.s.get(self.loginPage, headers=self.headers)

    def dump_check(self, response, page_name='check'):
        if self.debug:
            with open('./{}.html'.format(page_name), 'wb+') as f:
                text = response.text.replace('href="/static', 'href="static')
                text = text.replace('src="/static', 'src="static')
                f.write(text.encode('utf-8'))

    def dump_here(self, response):
        self.dump_check(response, 'here')

    @staticmethod
    def show_http_request(url, data):
        request_str = '{}'.format(url)
        if data is not None:
            request_str += '?'
            request_str += '&'.join(['{}={}'.format(k, v) for k, v in data.items()])
        return request_str

    def show_response(self, response, url="", data=None, description=""):
        if 200 <= int(response.status_code) < 300:
            status_str = "Link Success"
        else:
            status_str = "Link failed with code {}".format(int(response.status_code))
        print('[{}] {}'.format(description, status_str))
        if self.debug:
            print("\tReq as {}".format(self.show_http_request(url, data)))
            print("\tView as {}".format(response.url))
            print("\tCookie: {}".format(self.s.cookies.get_dict()))

    def update_headers_with_cookie(self):
        self.headers.update({'Cookie': ';'.join(['{}={}'.format(k, v) for k, v in self.s.cookies.items()])})

    def session_get(self, url, data=None, desc=""):
        response = self.s.get(
            url=url, data=data, headers=self.headers)
        self.show_response(
            response, url, data, description=desc)
        self.update_headers_with_cookie()
        return response

    def session_post(self, url, data=None, desc=""):
        response = self.s.post(
            url=url, data=data, headers=self.headers)
        self.show_response(
            response, url, data, description=desc)
        self.update_headers_with_cookie()
        return response

    def login(self):
        post_data = {
            'userName': self.username,
            'pwd': self.password,
            'sb': 'sb'
        }
        response = self.s.post(
            self.loginUrl, data=post_data, headers=self.headers)
        self.show_response(response, self.loginUrl, post_data, 'Login')
        if 'sepuser' in self.s.cookies.get_dict():
            return True
        return False

    @staticmethod
    def get_message(restext):
        css_soup = BeautifulSoup(restext, 'html.parser')
        text = css_soup.select('#main-content > div > div.m-cbox.m-lgray > div.mc-body > div')[0].text
        return "".join(line.strip() for line in text.split('\n'))

    def __read_from_course_id(self, filename):
        courses_file = open(filename, 'rb')
        self.coursesId = {}
        self.coursesDept = {}
        print('[Loading CourseID]')
        for line in courses_file.readlines():
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            line = line.strip().replace(' ', '').split(':')
            course_dept = dept_ids_dict.get(line[0][:2])
            print(line[1], line[0][:2], 'ID:', course_dept)
            course_id = line[1]
            is_degree = False
            if len(line) == 3 and line[2] == 'on':
                is_degree = True
            self.coursesId[course_id] = is_degree
            self.coursesDept[course_id] = course_dept
        print("")

    def enrollCourses(self):
        response = self.session_get(
            url=self.courseSystem, desc='SEP AppStore')
        soup = BeautifulSoup(response.text, 'html.parser')
        identity = re.findall(r'"http://jwxk.ucas.ac.cn/login\?Identity=(.*)&amp;roleId=[0-9]{2,4}"',
                              str(soup))[0]
        print("[Obtain Identity]", identity)
        try:
            post_data = {
                'roleId': 821,
            }
            response = self.session_get(  # Notification homepage
                url=self.courseIdentify + identity, data=post_data, desc='Notification List')

            response = self.session_get(  # SelectedCourse List
                url=self.courseSelected, desc='SelectedCourse List')
            self.dump_check(response, '已选课程')

            idx, last_msg = 0, ""
            while True:
                msg = ""
                if self.select_bat:
                    # select at the same time
                    result, msg = self.__enrollCourses(self.coursesId)
                    if result: 
                        self.coursesId.clear()
                else:
                    # select one by one
                    for each_course in self.coursesId:
                        # Ignore the courses already selected
                        if each_course in response.text:
                            print("Course " + each_course + " has been selected.")
                            continue
                        if (each_course in self.enrollCount and
                                self.enrollCount[each_course] == 0):
                            continue
                        
                        self.enrollCount[each_course] = 1
                        result, msg = self.__enrollCourse(
                            course_id=each_course, isDegree=self.coursesId[each_course])
                        
                        if result:
                            self.enrollCount[each_course] = 0

                for enroll in self.enrollCount:
                    if self.enrollCount[enroll] == 0:
                        self.coursesId.pop(enroll)
                self.enrollCount.clear()
                if not self.coursesId:
                    return 'INVALID COURSES_ID'
                idx += 1
                time.sleep(self.runtime)
                show_text = "\r> 第 {} 次尝试： <{}> {}\n".format(
                        idx, msg,
                        time.asctime(time.localtime(time.time())))
                last_msg = msg
                sys.stdout.write(show_text)
                sys.stdout.flush()
        except KeyboardInterrupt as e:
            print("\nKeyboardInterrupt Detected, bye!")
            return "STOP"
        except Exception as e:
            print("Catch Error: {}".format(e))
            return "Course_Selection_Port is not open, waiting..."

    def __enrollCourse(self, course_id, isDegree):
        response = self.session_get(  # SelectedCourse List
            url=self.courseSelectionBase, desc='Course Selection Board')
        self.dump_check(response, '预选课程')

        soup = BeautifulSoup(response.text, 'html.parser')
        dept_ids = self.coursesDept.get(course_id)
        identity = soup.form['action'].split('=')[1]

        # 查看 对应学院
        # /courseManage/selectCourse?s=fd287a9f-a12b-4219-820a-bbd65800901a&deptIds=911&deptIds=914&sb=0
        post_data = {
            'deptIds': dept_ids,
            'sb': 0
        }
        response = self.session_post(
            self.courseCategory + identity, data=post_data,
            desc='Step into {}'.format(index_course[dept_ids]))
        self.dump_check(response, index_course[dept_ids] + '学院')

        soup = BeautifulSoup(response.text, 'html.parser')
        course_table = soup.body.form.table
        if course_table:
            course_table = course_table.find_all('tr')[1:]
        else:
            return False, "Course Selection is unreachable or not started."
        course_dict = dict([(c.span.contents[0], c.span['id'].split('_')[1])
                            for c in course_table])
        # print(course_dict)

        if course_id in course_dict:
            post_data = {
                'deptIds': dept_ids,
                'sids': course_dict[course_id]
            }

            if isDegree:
                post_data['did_' + course_dict[course_id]] = course_dict[course_id]

            response = self.session_post(
                self.courseSave + identity, data=post_data)

            self.dump_check(response, '抢课结果_{}'.format(course_id))
            if 'class="error' not in response.text:
                return True, '[Success] ' + course_id
            else:
                return False, self.get_message(response.text).strip()
        else:
            return False, "No such course"

    def __enrollCourses(self, course_ids):
        """
        一般来说不推荐一下选好几个，一个一个选比较好，选得多了其中任意一个人满了都会失败
        但是英语需要同时选择听说/读写，才可以成功选课，所以也提供一下这个方法
        :param course_ids:
        :return:
        """
        response = self.session_get(  # SelectedCourse List
            url=self.courseSelectionBase, desc='Course Selection Board')
        self.dump_check(response, '预选课程')

        soup = BeautifulSoup(response.text, 'html.parser')
        identity = soup.form['action'].split('=')[1]

        dept_ids = []
        for course_id in course_ids:
            dept_ids.append(self.coursesDept.get(course_id))
        
        post_data = {
            'deptIds': dept_ids,
            'sb': 0
        }

        response = self.session_post(
            self.courseCategory + identity, data=post_data,
            desc='Step into {}'.format(index_course[dept_ids]))
        self.dump_check(response, index_course[dept_ids] + '学院')
        
        soup = BeautifulSoup(response.text, 'html.parser')
        course_table = soup.body.form.table
        if course_table:
            course_table = course_table.find_all('tr')[1:]
        else:
            return False, "Course Selection is unreachable or not started."
        course_dict = dict([(c.span.contents[0], c.span['id'].split('_')[1])
                            for c in course_table])
        # print(course_dict)

        post_data = {
            'deptIds': dept_ids,
            'sids': [course_dict[courseId] for courseId in course_ids]
        }

        response = self.session_post(
            self.courseSave + identity, data=post_data)
        self.dump_check(response, '抢课结果')

        if 'class="error' not in response.text:
            return True, '[Success] ' + course_ids
        else:
            return False, self.get_message(response.text).strip()

            
if __name__ == "__main__":
    print("starting...")
    # os.system('MODE con: COLS=128 LINES=32 & TITLE Welcome to CDSelector')
    # if watch_logo:
    #     from logo import show_logo
    #     show_logo() # delete this for faster start 23333
    #     os.system('cls')

    time.sleep(1)
    os.system("color 0A")
    os.system('MODE con: COLS=72 LINES=10 & TITLE CD_Course_Selecting is working')

    while True:
        try:
            ucasEvaluate = UCASEvaluate()
            break
        except Exception as e:
            if e == "Connection aborted.":
                ucasEvaluate = UCASEvaluate()

    if ucasEvaluate.debug:
        print("Debug Mode: %s" % str(ucasEvaluate.debug) )
        print("In debug mode, you can check snapshot with html files.")
        print("By the way, Ctrl+C to stop.")
    
    if not ucasEvaluate.login():
        print('Login error. Please check your username and password.')
        exit()

    print('Login success: ' + ucasEvaluate.username)
    if ucasEvaluate.debug:
        print("[Obtain SepUser]", ucasEvaluate.s.cookies.get_dict()['sepuser'])
    print("-----" * 5)
    print('Enrolling starts')
    if not ucasEvaluate.enroll:
        # at least run once
        status = ucasEvaluate.enrollCourses()
        status += time.asctime(time.localtime(time.time()))
        sys.stdout.write("%s\r" % status)

    while ucasEvaluate.enroll:
        status = ucasEvaluate.enrollCourses()
        if status.startswith('STOP'):
            break
        else: 
            status += time.asctime(time.localtime(time.time()))
            sys.stdout.write("%s\r" % status)
    print('Enrolling finished')
