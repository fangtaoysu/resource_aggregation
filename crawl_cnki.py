import requests
from lxml import etree
import time
import time


def get_response(title1, title2, title3, key1, key2, key3, set_ope1, set_ope2, page=1):
	'''定制请求'''
	url = 'https://kns.cnki.net/kns8/Brief/GetGridTableHtml'
	headers = {
		'Accept':'text/html, */*; q=0.01',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
		'Connection':'keep-alive',
		'Content-Length':'1268',
		'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		'Cookie':'Ecp_ClientId=1230329142001253792; Ecp_ClientIp=111.19.32.146; knsLeftGroupSelectItem=2%3B1%3B; _pk_ref=%5B%22%22%2C%22%22%2C1680489740%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; Ecp_loginuserjf=18394604239; _pk_id=43964911-13e7-45e4-899d-de9f6df26b74.1680070828.3.1680489755.1680489740.; Hm_lvt_dcec09ba2227fd02c55623c1bb82776a=1680489936; ASP.NET_SessionId=gz2scrqlja1e3qccytyulfg3; cangjieStatus_NZKPT2=true; cangjieConfig_NZKPT2=%7B%22status%22%3Atrue%2C%22startTime%22%3A%222022-10-20%22%2C%22endTime%22%3A%222023-10-20%22%2C%22orginHosts%22%3A%22kns.cnki.net%22%2C%22type%22%3A%22mix%22%2C%22poolSize%22%3A%2210%22%2C%22intervalTime%22%3A10000%2C%22persist%22%3Afalse%7D; Ecp_IpLoginFail=230519111.18.36.171; SID_recommendapi=126001; CurrSortField=%e7%9b%b8%e5%85%b3%e5%ba%a6%2frelevant%2c(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27time%27)+desc; CurrSortFieldType=desc; SID_kns_new=kns128003; cnkiUserKey=ea80ca5a-9225-9980-acdf-33c1cd028053; SID_kns8=123149; dblang=ch',
		'Host':'kns.cnki.net',
		'Origin':'https://kns.cnki.net',
		'Referer':'https://kns.cnki.net/kns8/AdvSearch?',
		'sec-ch-ua':'"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
		'sec-ch-ua-mobile':'?0',
		'sec-ch-ua-platform':'"Windows"',
		'Sec-Fetch-Dest':'empty',
		'Sec-Fetch-Mode':'cors',
		'Sec-Fetch-Site':'same-origin',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
		'X-Requested-With':'XMLHttpRequest',
	}
	title_list = ['主题', '篇关摘', '关键字', '篇名', '全文', '作者', '第一作者', '通讯作者', '作者单位', '基金', '摘要', '小标题', '参考文献', '分类号', '文献来源', 'DOI']

	name_list = ['SU', 'TKA', 'KY', 'TI', 'FT', 'AU', 'FI', 'RP', 'AF', 'FU', 'AB', 'CO', 'RF', 'CLC', 'LY', 'DOI']
	name1, name2, name3 = "", "", ""
	if title1:
		name1 = name_list[title_list.index(title1)]
	if title2:
		name2 = name_list[title_list.index(title2)]
	if title3:
		name3 = name_list[title_list.index(title3)]
	title = ''
	if 'SU' in (name1, name2, name3):
		title = title_list[0]
	query_json = {
		"Platform":"",
		"DBCode":"CFLS",
		"KuaKuCode":"CJFQ,CCND,CIPD,CDMD,BDZK,CISD,SNAD,CCJD,GXDB_SECTION,CJFN,CCVD",
		"QNode":{
			"QGroup":[
				{"Key":"Subject",
				# 主题
				"Title":title,
				"Logic":4,
				"Items":[],
				"ChildItems":[
					{"Key":"input[data-tipid=gradetxt-1]",
					# 主题
					"Title":title1,
					"Logic":0,
					"Items":[
						{"Key":"",
						"Title":key1,
						"Logic":1,
						# SU
						"Name":name1,
						"Operate":"%=",
						"Value":key1,
						"ExtendType":1,
						"ExtendValue":"中英文对照",
						"Value2":""}
						],
					"ChildItems":[]},
					{"Key":"input[data-tipid=gradetxt-2]",
					"Title":title2,
					# 1:AND, 2:OR, 3:NOT
					"Logic":set_ope1,
					"Items":[
						{"Key":"",
						"Title":key2,
						"Logic":1,
						"Name":name2,
						"Operate":"%=",
						"Value":key2,
						"ExtendType":1,
						"ExtendValue":"中英文对照",
						"Value2":""}
						],
					"ChildItems":[]},
					{"Key":"input[data-tipid=gradetxt-3]",
					"Title":title3,
					"Logic":set_ope2,
					"Items":[
						{"Key":"",
						"Title":key3,
						"Logic":1,
						"Name":name3,
						"Operate":"%=",
						"Value":key3,
						"ExtendType":1,
						"ExtendValue":"中英文对照",
						"Value2":""}
						],
					"ChildItems":[]},
					]},
				{"Key":"ControlGroup",
				"Title":"",
				"Logic":1,
				"Items":[],
				"ChildItems":[]}]},
		"CodeLang":"",
	}
	is_search = (page == 1)
	data = {
		'IsSearch':str(is_search),
		# 此处要把json转字符串
		'QueryJson':str(query_json),
		'PageName':'AdvSearch',
		'DBCode':'CFLS',
		'KuaKuCodes':'CJFQ,CCND,CIPD,CDMD,BDZK,CISD,SNAD,CCJD,GXDB_SECTION,CJFN,CCVD',
		'CurPage':str(page),
		'RecordsCntPerPage':'50',
		'CurDisplayMode':'listmode',
		'CurrSortField':'',
		'CurrSortFieldType':'desc',
		'IsSentenceSearch':'false',
		'Subject':'',
	}
	response = requests.post(url=url, data=data, headers=headers)
	return response

def get_all_response(title1, title2, title3, response, key1, key2, key3, set_ope1, set_ope2):
	'''获取剩余页的response'''
	# 根据第一页的response获取页码
	tree = etree.HTML(response.text)
	page = tree.xpath('//div[@id="countPageDiv"]//span[2]/text()')
	res_list = [response]
	if not page:
		return res_list
	page = page[0].split('/')[1]
	# 请求其余页码的响应
	for i in range(2, int(page) + 1):
		res = get_response(title1, title2, title3, key1, key2, key3, set_ope1, set_ope2, i)
		res_list.append(res)
	return res_list
		

def get_link(response):
	'''根据响应获取文章响应'''
	key_tree = etree.HTML(response.text)
	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'Cookie':'Ecp_ClientId=1230329142001253792; Ecp_ClientIp=111.19.32.146; knsLeftGroupSelectItem=2%3B1%3B; _pk_ref=%5B%22%22%2C%22%22%2C1680489740%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; Ecp_loginuserjf=18394604239; _pk_id=43964911-13e7-45e4-899d-de9f6df26b74.1680070828.3.1680489755.1680489740.; ASP.NET_SessionId=gz2scrqlja1e3qccytyulfg3; cangjieStatus_NZKPT2=true; cangjieConfig_NZKPT2=%7B%22status%22%3Atrue%2C%22startTime%22%3A%222022-10-20%22%2C%22endTime%22%3A%222023-10-20%22%2C%22orginHosts%22%3A%22kns.cnki.net%22%2C%22type%22%3A%22mix%22%2C%22poolSize%22%3A%2210%22%2C%22intervalTime%22%3A10000%2C%22persist%22%3Afalse%7D; Ecp_IpLoginFail=230519111.18.36.171; SID_recommendapi=126001; CurrSortField=%e7%9b%b8%e5%85%b3%e5%ba%a6%2frelevant%2c(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27time%27)+desc; CurrSortFieldType=desc; cnkiUserKey=ea80ca5a-9225-9980-acdf-33c1cd028053; dblang=ch; SID_kns8=123154; SID_kxreader_new=15131001; Hm_lvt_dcec09ba2227fd02c55623c1bb82776a=1684482782; Hm_lpvt_dcec09ba2227fd02c55623c1bb82776a=1684485298; SID_kns_new=kns25128004',
		'Host':'kns.cnki.net',
		'Referer':'https://kns.cnki.net/kns8/AdvSearch?',
		'sec-ch-ua':'"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
		'sec-ch-ua-mobile':'?0',
		'sec-ch-ua-platform':'"Windows"',
		'Sec-Fetch-Dest':'document',
		'Sec-Fetch-Mode':'navigate',
		'Sec-Fetch-Site':'same-origin',
		'Sec-Fetch-User':'?1',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
	}
	response_list = []
	link_list = key_tree.xpath('//a[@class="fz14"]/@href')
	for link in link_list:
		link = f'https://kns.cnki.net/{link}'
		response = requests.get(url=link)
		response_list.append(response)
	return response_list

def get_data(response):
	'''根据响应获取数据'''
	data = {}
	content_tree = etree.HTML(response.text)
	data['title'] = content_tree.xpath('//h1/text()')
	if len(data['title']) != 0:
		data['title'] = data['title'][0]
	data['authors'] = content_tree.xpath('//h3[@class="author"]//a/text()')
	# 组织
	data['orgs'] = content_tree.xpath('//div[@class="brief"]//h3[2]//a/text()')
	data['abstract'] = content_tree.xpath('//span[@id="ChDivSummary"]/text()')
	data['keywords'] = content_tree.xpath('//div[@class="row"]/p[@class="keywords"]//a/text()')
	for i in range(len(data['keywords'])):
		data['keywords'][i] = data['keywords'][i].rstrip()
	data['funds'] = content_tree.xpath('//div[@class="row"]/p[@class="funds"]/text()')
	# 专辑
	data['album'] = content_tree.xpath('//div[@class="row"]//li[1]/p/text()')
	# 专题
	data['special'] = content_tree.xpath('//div[@class="row"]//li[2]/p/text()')
	# 分类号
	data['class_number'] = content_tree.xpath('//div[@class="row"]//li[3]/p/text()')
	return data


def get_url(title):
	'''根据文献名获取可在线阅读的网站'''
	url = 'http://www.chinadoi.cn/portal/newsAction!searchDoi.action'
	headers={
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'Content-Length':'157',
		'Content-Type':'application/x-www-form-urlencoded',
		'Cookie':'JSESSIONID=BBE15DE29DD59EF1AAF586F89BD2CBC7',
		'Host':'www.chinadoi.cn',
		'Origin':'http://www.chinadoi.cn',
		'Referer':'http://www.chinadoi.cn/portal/index.htm',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
	}
	data = {
		'articleTitle': title,
	}
	response = requests.post(url=url, data=data, headers=headers)
	tree = etree.HTML(response.text)
	link = tree.xpath('//div[@class="search_list"]//span/a/@href')
	if not link:
		link = ''
	else:
		link = link[0]
	return link


def main(title1, title2, title3, key1, key2="", key3="", set_ope1=1, set_ope2=1):
	data_list = []
	res = get_response(title1, title2, title3, key1, key2, key3, set_ope1, set_ope2)
	res_list = get_all_response(title1, title2, title3, res, key1, key2, key3, set_ope1, set_ope2)
	for res in res_list:
		response_list = get_link(res)
		for response in response_list:
			data = get_data(response)
			data_list.append(data)
			time.sleep(0.1)
	return data_list


if __name__ == "__main__":
	key1, key2, key3 = "", "", ""
	key1 = input("input key1: ")
	if input("need second key(y/n)?: ") == "y":
		key2 = input("input key2: ")
		if input("need third key(y/n)?: ") == "y":
			key3 = input("input key3: ")
	while key1 != 'q':
		data_list = main(key1, key2, key3)
		for data in data_list:
			print(data)
		print(len(data_list))
		print('over')
		key1 = input("input key1: ")
		if input("need second key(y/n)?: ") == "y":
			key2 = input("input key2: ")
			if input("need third key(y/n)?: ") == "y":
				key3 = input("input key3: ")
