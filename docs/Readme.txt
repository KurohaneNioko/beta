when Only uWsgi:
run-server:
    uwsgi --ini uwsgi.ini
stop-server:
    uwsgi --stop uwsgi.pid

解决RAM不够的办法：
https://blog.csdn.net/lym152898/article/details/77133260


云主机重启(reboot)后
supervisord -c /etc/supervisord.conf
再
supervisorctl -c /etc/supervisord.conf reload

重启supervisord(即重启uWsgi和Daphne)
supervisorctl -c /etc/supervisord.conf reload
log在SE2019/log

Mysql经常炸 用
service mysqld restart



[Mysql]
user=root
pwd=2019#SE-Phoenix#

user=PhoenixDBA
pwd=2019#SE-Phoenix#


[Django-Admin]
user=PhoenixKing
pwd=369258147


[PhoenixNest]
user=founder001
pwd=founder001

usre=founder002
pwd=founder002

user=investor003
pwd=investor003

*****************************
安装流程：
安装SE2019目录下的requirements.txt里面的库，或者就按照settings里面install_app的装
安装并配置nginx，我们用的配置文件已经放在SE2019里面了
配置文件放在/etc/nginx/nginx.conf

nginx将访问服务器8080端口的请求按照一定的规则分派给uwsgi和daphne
其中以/ws/为起始的请求分派给daphne，其余全部分派给uwsgi
daphne处理websocket请求，uwsgi处理http请求

Pip按照uWsgi配置uWsgi：可能出现的问题：动态链接库问题（google解决）
配置文件在/root/SE2019/script/uwsgi.ini
安装mysql
创建用户，赋予权限
redis:安装yum install redis 启动 service redis start
配置Daphne？
使用manage.py初始化Django环境
Migration
导入数据库
重建搜索引擎的索引

安装配置supervisorctl……
Supervisor:
配置文件位于/etc/supervisord.conf

启动 supervisord -c /etc/supervisord.conf   （配置文件启动）
重启 supervisorctl -c /etc/supervisord.conf reload
查看状态 supervisorctl -c /etc/supervisord.conf status
停止某个进程 supervisorctl -c /etc/supervisord.conf stop <name>
停止所有的进程 supervisorctl -c /etc/supervisord.conf stop all

uwsgi与daphne为supervisor启动，启动方式分别为配置文件启动与默认sock文件启动

获取服务器的ip地址，views里面发邮件的那个函数里面的ip地址改一下
使用具有最新正式版内核的Chrome浏览器（下称Chrome浏览器）访问
http://[ip地址]:8080/index（其中[ip地址]为上一步中获取到的服务器ip地址，下同）
使用Chrome浏览器访问http://[ip地址]:8080/admin，用户名输入PhoenixKing，密码输入369258147，确认能登录后台管理页面


***************************
PM私货时间
**************************
1.这个PM特别丢人，tag存储的时候居然是直接存list而不是开了个新的表；
2.这个PM特别懒，基本上没有什么地方用了类似alert的弹窗，而是跳到新的信息提示页面再回到主页，因为懒得推广ajax；
3.这个PM特别屑，推荐算法里面的向量/画像居然是即时运算；
4.这个PM审美过于钢铁直男（首页蜜汁大红字）；




