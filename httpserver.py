# -.- coding:utf-8 -.-
import socket,datetime
import os,time

import config
import log

PORT = 8080
HOST = 'Localhost'

#默认地址前缀
path_pre = "/root/kun/hs"

#servername版本号
server_name = "Severdemo/0.1"

#缓存时间
expires = datetime.timedelta(days=1)

#GMT时间格式
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

logger = log.log()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))

#网页内容

content_type = {
        '.bmp'    : 'image/x-ms-bmp',
        '.css'    : 'text/css',
        '.doc'    : 'application/msword',
        '.exe'    : 'application/octet-stream',
        '.gif'    : 'image/gif',
        '.htm'    : 'text/html',
        '.html'   : 'text/html',
        '.jpe'    : 'image/jpeg',
        '.jpeg'   : 'image/jpeg',
        '.jpg'    : 'image/jpeg',
        '.js'     : 'application/x-javascript',
        '.mht'    : 'message/rfc822',
        '.mhtml'  : 'message/rfc822',
        '.mp3'    : 'audio/mpeg',
        '.mpeg'   : 'video/mpeg',
        '.mpg'    : 'video/mpeg',
        '.pdf'    : 'application/pdf',
        '.png'    : 'image/png',
        '.ppt'    : 'application/vnd.ms-powerpoint',
        '.swf'    : 'application/x-shockwave-flash',
        '.tar'    : 'application/x-tar',
        '.zip'    : 'application/zip',
}

def gettype(url):
	filepath,ext = os.path.splitext(url)
	ext = ext.lower()
	if ext in content_type:
		return content_type[ext]
	else:
		return 'text/html'

def rp_request_url(request_url):
	new_request_url = request_url.split(os.path.sep)
	j = 0
	new = ''
	ll = len(new_request_url)
	for i in new_request_url:
		new_request_url[j] = new_request_url[j].replace(' ','%20')
		if j == ll-1 :
			new = new + new_request_url[j]
		else:
			new = new + os.path.sep + new_request_url[j]
		j = j + 1
	return new

def Path_Handle(path,request_url):
	http_path = path
	url = request_url
	a = os.listdir(path)
	content = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>''' + path + '''</title>
<style type="text/css">
tr{
	display:block;
}
tr:hover {
	border:1px solid #ccc;
}
th{
	cursor:pointer;
}
div {
border:1px solid #ccc;
box-shadow: 0 0 5px #000;
border-radius:10px;
}
</style>

</head>

<body style="background:#D2B48C;">
<h1>Index of ''' + path + '''</h1>
<div style="position:relative;margin:0 auto;background:#fff;width:1000px;">
<table cellspacing="5" cellpadding="1" align="center">
	<thead>
		<tr>
			<th width="500" align="left">文件名</th>
			<th width="100" align="left">大小</th>
			<th width="300" align="right">修改时间</th>
		</tr>
	</thead>
	<tbody>
	'''
	for i in a:
		statinfo = os.stat(f_path+ os.path.sep +i)
		if url == '/':
			content = content + '<tr><td width="500"><a href="'+ url  + i + '">' + i + '</a></td>'
		else:
			content = content + '<tr><td width="500"><a href="'+ url  + os.path.sep + i + '">' + i + '</a></td>'
		if os.path.isfile(f_path+ os.path.sep +i):
			size = os.path.getsize(f_path+ os.path.sep +i)
			content = content + '<td width="100" align="left">'+ str(size) +'</td>'
		else:
			content = content + '<td width="100" align="left"></td>'
		content = content + '<td width="300" align="right">'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(statinfo.st_ctime))+'</td></tr>'
	content = content + '</tbody></table></div></body></html>'
	return content
	
s.listen(5)
logger.info("servers success start up on port %d ... \r\n" %PORT)

while 1:
	clientsock,clientaddr = s.accept()


	#接受浏览器请求，此时不处理，但是计算now时有用
	request = clientsock.recv(1024)
	client_request_line = request.split("\r\n")
	logger.info('Got connection from [%s] - - "%s"\r\n' %(clientaddr[0],client_request_line[0]))
	#提取头部信息
	temp_split = client_request_line[0].split()
	print len(temp_split)
	if(len(temp_split)==3):
		request_method = temp_split[0]
		request_url = temp_split[1]
		request_version = temp_split[2].split("/")[1]
	
	print '''--Request Header:
	Request_method: %s
	Request_url: %s
	Request_version: %s
	''' %(request_method,request_url,request_version)
	
	
	print "request_url: " + request_url
#	request_url = rp_request_url(request_url)
	f_path = (path_pre + request_url)
	print "f_path: " + f_path
	charset_flag = ''
	
	
        try:
		if request_url == "/":
			content = Path_Handle(f_path,request_url)
			
		elif os.path.isfile(f_path):
			content = open(f_path,"rb").read()
		
		elif os.path.isdir(f_path):
			content = Path_Handle(f_path,request_url)
		else:
			content = "<h1>404: Not Found</h1>"
			logger.info("404: Not Found")
	except:
		content = "<h1>服务器执行过程出错</h1>"
		charset_flag = ';charset=utf8'
	
	#请求时间
	now = datetime.datetime.utcnow()
	response = \
'''HTTP/1.1
Server: %s
Date: %s
Expires: %s
Content-Type: %s%s
Content-Length: %s
Connection: keep-alive

%s''' % (
	server_name, 
	now.strftime(GMT_FORMAT), 
	(now + expires).strftime(GMT_FORMAT),
	gettype(f_path),
	charset_flag,
	len(content),
	content
	)
	#使用socket从服务器传送到浏览器
	clientsock.send(response) 
	clientsock.close()
