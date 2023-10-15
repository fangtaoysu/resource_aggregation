import requests
from urllib.request import quote
from lxml import etree
import json
import time

global headers
headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35',
}
def get_response(key):
	'''获取起点网的响应数据'''
	base_url = 'https://www.qidian.com/so/'
	
	url = f'{base_url}{quote(key)}.html'
	response = requests.get(url=url,headers=headers)
	return response


def get_link(response):
	'''根据响应获取有效链接'''
	# 获取搜索界面的链接
	key_tree = etree.HTML(response.text)
	link_list = key_tree.xpath('//div[@id="result-list"]//div[@class="book-mid-info"]/h3/a/@href')
	# 根据字数筛选链接 删除不需要的URL
	total_list = key_tree.xpath('//div[@id="result-list"]//div[@class="total"]/p[1]/span/text()')
	del_list = []
	for i in range(len(total_list)):
		if list(total_list[i])[1] == '0':
			del_list.append(i)
	for i in range(len(del_list) - 1, -1, -1):
		del link_list[del_list[i]]	
	return link_list
	
	
def get_data(link):
	'''通过有效链接返回本书的数据'''
	data = {}
	attr_url = f'https:{link}'
	# 请求小说属性页
	attr_response = requests.get(url=attr_url, headers=headers)
	attr_tree = etree.HTML(attr_response.text)
	# 保存小说属性
	data['name'] = attr_tree.xpath('/html/body/div[1]/div[@class="book-detail-wrap center990"]/div[1]/div[2]/h1/em/text()')
	data['author'] = attr_tree.xpath('/html/body/div[1]/div[@class="book-detail-wrap center990"]/div[1]/div[2]/h1//span[1]//text()')
	data['tag'] = attr_tree.xpath('//p[@class="tag"]/span/text()')
	data['outline'] = attr_tree.xpath('/html/body/div[1]/div[@class="book-detail-wrap center990"]/div[3]/div[1]/div/div[1]/div[1]/p/text()')
	if len(data['name']) != 0:
		data['name'] = data['name'][0]
	if len(data['author']) != 0:
		data['author'] = data['author'][0]
	info = ''
	for i in range(len(data['outline'])):
		info += data['outline'][i].strip()
		info += '\n'
	data['outline'] = info
	for section in data['outline']:
		section = section.replace('\u3000', '  ')
	# 提取小说章节信息
	data['chapter_name'] = attr_tree.xpath('//ul[@class="cf"]/li//a/text()')
	data['chapter_url'] = attr_tree.xpath('//ul[@class="cf"]/li//a/@href')
	vip_chapter_list = attr_tree.xpath('//ul[@class="cf"]/li//em/text()')
	free_len = len(data['chapter_name']) - len(vip_chapter_list) - 1
	data['chapter_name'] = data['chapter_name'][ : free_len]
	data['chapter_url'] = data['chapter_url'][ : free_len]
	return data
	
	
def get_content(data):
	'''获取data的content'''
	data['content'] = []
	for i in range(len(data['chapter_url'])):
		content_url = f'https:{data["chapter_url"][i]}'
		content_response = requests.get(url = content_url, headers=headers)
		# 根据响应提取章节内容
		content_tree = etree.HTML(content_response.text)
		section_list = content_tree.xpath('//div[@class="read-content j_readContent"]/p/text()')
		text = ''
		for section in section_list:
			section = section.replace('\u3000', '  ')
			section += '\n'
			text += section
		data['content'].append(text)
	return data
	 

def download_text(data):
	'''下载文本'''
	data = get_content(data)
	filename = f'{data["name"]}.txt'
	with open(filename, 'a', encoding="utf-8") as fp:
		for section in data['content']:
			fp.write(section)
	

def main(key):
	'''得到本书除了content以外的内容'''
	response = get_response(key)
	useful_link = get_link(response)
	data_list = []
	# 得到每本书的内容
	for link in useful_link:
		data = get_data(link)
		data_list.append(data)
	return data_list


if __name__ == '__main__':
	key = input('input key: ')
	while key != 'q':
		data_list = main(key)
		time.sleep(1)
		for data in data_list:
			print(data['chapter_name'])
		download_text(data_list[0])
		key = input('input key: ')
