# CDSelector
UCAS Course Selector

# Usage
+ Modify File `config`
    + username = you@somewhere.com
    + password = yourpassword
+ Modify File `courseid`
    + 由于课程编号和学院编号脱钩，目前需要在 courseid 里手动增加学院名称，"学院"二字允许省略：
    + such as `计算机:081203M04003H` as 沈华伟、罗平老师等 开设的推荐系统课程
    + such as `计算机学院:081203M04003H:on` as 某个需要被选为学位课的课程
+ Run Script 
    + `$ python CDSelector.py`
    + Done
+ If not done
    + try `$ pip install -r requirement.txt`
    + 目前大多数新东西都已经处理完，目前可以拿到正确的Identity, sids, deptId等
    + 可以通过拼接生成的url在浏览器中起到登陆、筛选、选课等功能
    + 但目前网站反爬虫的 Forbidden 403 尚未解决，需要想想有没有别的法子使得命令行脚本有效

# Blog Article
（等这一版大改更新了之后我再写一篇去）
http://blog.csdn.net/okcd00/article/details/72827861


# Note
请使用无线网连入UCAS，或者网线直连网络接口（不经过路由器中转），     
这样属于内网直连，登SEP时不需要输验证码。
