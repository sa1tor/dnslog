# dnslog
使用tornado写的一个dnslog平台，python2运行
## 准备
一个可以修改NS记录的域名和一台vps

例如阿里云购买域名和云服务器ECS
域名: saltor.icu
云服务器ip: 100.100.100.100

在云解析DNS处添加一条A记录和一条NS记录

![](https://github.com/sa1tor/dnslog/blob/master/1.webp)

云服务器ECS添加安全规则，放行53端口

![](https://github.com/sa1tor/dnslog/blob/master/2.webp)

## 安装
```
pip install -r requirement.txt
```
## 运行
```
python server.py --port=6002
```
指定端口6002运行，默认端口为8000

当然也可以使用Nginx+Tornado+Supervisor来部署

博客相关文章：[http://www.saltor.cn/archives/62](http://www.saltor.cn/archives/62)
