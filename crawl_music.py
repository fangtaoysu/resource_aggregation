# 网址相同，查看【负载】的【表单数据】
from urllib.request import Request, urlopen, urlretrieve
from urllib.parse import urlencode
import json


def create_request(i, key):
	'''为页面定制请求'''
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35',
		'X-Requested-With':'XMLHttpRequest',
	}
	url = 'https://dev.iw233.cn/Music1/'
	# netease:网易，kugou:酷狗，qq：QQ
	music_type = ['netease', 'kugou', 'qq']
	
	data = {
		'input': key,
		'filter': 'name',
		'type': music_type[i],
		'page': '1',
	}
	data = urlencode(data).encode('utf-8')
	request = Request(url, data, headers)
	return request
	

def get_dict(request):
	'''通过请求得到数据字典'''
	response = urlopen(request)
	content = response.read().decode('utf-8')
	obj = json.loads(content, encoding='utf-8')
	return obj['data']
	
def deal_data(data_list, obj_list):
	'''解析字典，得到想要数据（歌名，歌手，歌词，下载地址）'''
	for obj in obj_list:
		info = {}
		# 歌名
		info['song'] = obj['title']
		# 歌手
		info['singer'] = obj['author']
		# 歌词
		info['content'] = obj['lrc']
		# 下载链接
		info['link'] = obj['url']
		# 源地址
		info['url'] = obj['link']
		data_list.append(info)
	return data_list

def main(key):
	data_list = []
	for i in range(3):
		request = create_request(i, key)
		obj_list = get_dict(request)
		data_list = deal_data(data_list, obj_list)
	return data_list
	
	
def download_music(data, i):
	url_music = data['link']
	filename = f'{data["song"]}-{data["singer"]}.mp3'
	urlretrieve(url_music, filename)
		

if __name__ == '__main__':
	key = input('input key: ')
	while key != 'q':
		data_list = main(key)
		for data in data_list:
			print(data['song'] + data['singer'])

		key = input('input key: ')
