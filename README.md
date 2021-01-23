# CDSelector
UCAS Course Selector


# Usage
+ Modify File `config`
    + username = you@somewhere.com
    + password = yourpassword
    + capture = true/false (如果是需要输入验证码的环境，请把这个改成true)
+ Modify File `courseid`
    + 由于新选课系统中课程编号和学院编号脱钩，目前需要在 courseid 里手动增加学院名称，"学院"二字允许省略：
    + such as `计算机:081203M04003H` as 沈华伟、罗平老师等 开设的推荐系统课程
    + such as `计算机学院:081203M04003H:on` as 某个需要被选为学位课的课程
+ Run Script 
    + `$ python CDSelector.py`
    + wait and check html files in your folder.
    + if you find "results.html", Done.
+ If not done
    + try `$ pip install -r requirement.txt`


# About Capture
+ 使用无线网连入UCAS，或者网线直连网络接口时（不经过路由器中转），属于内网直连，登SEP时不需要输验证码
+ 通过外网连入UCAS时，需要在程序提示输入验证码时手动输入（考虑要不要加个轻量级OCR）


# Blog Article
http://blog.csdn.net/okcd00/article/details/72827861

