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

***************************
PM私货时间
**************************
1.这个PM特别丢人，tag存储的时候居然是直接存list而不是开了个新的表；
2.这个PM特别懒，基本上没有什么地方用了类似alert的弹窗，而是跳到新的信息提示页面再回到主页，因为懒得推广ajax；
3.这个PM特别屑，推荐算法里面的向量/画像居然是即时运算；
4.这个PM审美过于钢铁直男（首页蜜汁大红字）；
5.这个PM……算了，想接坑的且碰上问题了，QQ/TIM联系541537340，注明20软工（不保证全都能解决，不准问Django基础知识，请自己去看Django英文文档）。




