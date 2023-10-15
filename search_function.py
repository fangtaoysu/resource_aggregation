import PySimpleGUI as sg
import crawl_music as cm
import crawl_novel as cn
import crawl_cnki as cc
import webbrowser


def crawl_content(style, key):
	'''实现搜索资源'''
	if not key:
		# 显示输入为空的提示框
		words = '输入值为空呢，亲~'
		show_tips(words, 2)

	else:
		# 指引用户
		words = '在搜呢..\n大概需要10~20s的等待^-^\n在此期间不要瞎搞，会死程序的:)'
		show_tips(words, 2)
		
		music_list = []
		novel_list = []

		if style == '小说':
			novel_list = cn.main(key)		
		if novel_list:
			show_novel(novel_list)
		if style == '音乐':
			music_list = cm.main(key)
		if music_list:
			show_music(music_list)
			
			
def cnki(title1, title2, title3, key1, key2, key3, set_ope1, set_ope2):
	'''单独处理cnki的逻辑'''
	if key1 or key2 or key3:
		data_list = cc.main(title1, title2, title3, key1, key2, key3, set_ope1, set_ope2)
		show_literature(data_list)
	else:
		words = '输入值为空呢，亲~'
		show_tips(words, 2)
		
		
def  show_literature(data_list):
	'''显示爬到的文献'''
	index = 0
	all_listbox = []
	for data in data_list:
		row = [
			sg.Text(f'{index+1}.'),
			sg.Text(f'《{data["title"]}》'),
			sg.Text(f'author:{data["authors"]}'),
			sg.Text(f'[{data["keywords"]}]'),
			sg.Button("摘要", key=f'-ABSTRACT-{index}'),
			sg.Button("更多信息", key=f'-MORE-INFO-{index}'),
			sg.Button("在线阅读", key=f'-READ-{index}'),
		]
		all_listbox.append(row)
		index += 1
	literature_layout = [[sg.Column(all_listbox, size=(800, 500), pad=(0, 0),scrollable=True,vertical_scroll_only=False)]]
	control_literature(literature_layout, data_list)
	
	
def control_literature(literature_layout, data_list):
	'''控制show文献窗口的逻辑'''
	win_literature = sg.Window('文献', literature_layout, font=("楷体", 16))
	while True:
		event, values = win_literature.read(timeout=10)
		
		for i in range(len(data_list)):
			data = data_list[i]
			key = f'-ABSTRACT-{i}'
			if event == key:
				sg.popup_scrolled(data['abstract'], font=("楷体", 18))
			key = f'-MORE-INFO-{i}'
			if event == key:
				content = merge_content(data)
				sg.popup_scrolled(content, font=("楷体", 18))
			key = f'-READ-{i}'
			if event == key:
				url = cc.get_url(data['title'])
				open_url(url)

		if event is None:
			win_literature.close()
			break
		
def merge_content(data):
	'''合并文献爬取的更多信息'''
	orgs = f'作者单位：{data["orgs"]}'
	funds = f'资金赞助：{data["funds"]}'
	album = f'专辑：{data["album"]}'
	special = f'专题：{data["special"]}'
	class_number = f'分类号：{data["class_number"]}'
	content = f'{orgs}\n{funds}\n{album}\n{special}\n{class_number}'
	return content
	

def show_novel(novel_list):
	'''将novel_list的内容显示出来'''
	index = 0
	novel_layout = []
	for data in novel_list:
		row = [
			sg.Text(f'《{data["name"]}》'),
			sg.Text(f'@{data["author"]}'),
			sg.Text(data['tag']),
			sg.Button('介绍', key = f'-INTRO-{index}'),
			sg.Button('在线阅读', key = f'-READ-{index}'),
			sg.Button('下载', key = f'-DOWNLOAD-{index}'),
		]
		novel_layout.append(row)
		index += 1
	control_novel(novel_layout, novel_list)
	
	
def control_novel(novel_layout, novel_list):
	'''控制小说展示逻辑'''
	win_novel = sg.Window('小说', novel_layout, font=("楷体", 16))	
	
	while True:
		event, values = win_novel.read()
		
		for i in range(len(novel_list)):
			data = novel_list[i]
			# 处理小说介绍事件 - 显示介绍
			keyname = f'-INTRO-{i}'
			if event == keyname:
				sg.popup_scrolled(data['outline'], font=("楷体", 18))
			# 处理小说在线阅读事件 - 阅读内容
			keyname = f'-READ-{i}'
			if event == keyname:
				open_url(data['chapter_url'][0])
			# 处理小说下载事件 - 下载文本
			keyname = f'-DOWNLOAD-{i}'
			if event == keyname:
				sg.popup_ok('下崽中...', auto_close=True, auto_close_duration=1)
				# 优化下载体验，实现队列下载
				win_novel.perform_long_operation(lambda: cn.download_text(data), '-DOWNLOAD-FINISH-')
		
		if event == '-DOWNLOAD-FINISH-':
			sg.popup_ok('下好了', auto_close=True, auto_close_duration=2)
		
		if event == None:
			win_novel.close()
			break
	
	
def show_music(music_list):
	'''将music_list的内容展示出来'''
	index = 0
	music_layout = []
	all_listbox = []
	for data in music_list:
		row = [
			sg.Text(str(index+1)),
			# 实现多个下载，暂时不需要
			# sg.Checkbox('', enable_events=True, key='-CHOICE'),
			sg.Text(f'《{data["song"]}》'),
			sg.Text(f'@{data["singer"]}'),
			sg.Button('在线听', key=f'-LISTEN-{index}'),
			sg.Button('下载', key=f'-DOWNLOAD-{index}'),
			]
		all_listbox.append(row)
		index += 1
	
	music_layout = [[sg.Column(all_listbox, size=(800, 500), pad=(0, 0),scrollable=True,vertical_scroll_only=True)]]
	control_music(music_layout, music_list)
	
	
def control_music(music_layout, music_list):
	'''控制show音乐窗口的逻辑'''
	win_music = sg.Window('音乐', music_layout, font=("楷体", 16))
	while True:
		event, values = win_music.read()
		for i in range(len(music_list)):
			data = music_list[i]
			keyname = f'-DOWNLOAD-{i}'
			# 处理下载音乐事件
			if event == keyname:
				if not data['link']:
					words = '本首歌曲只能在线听哟~'
					show_tips(words, 2)
					break
				words = '在下载哟~骚安勿躁\n如果出现"未响应"也不要慌张\n文件会保存在本程序的目录下'
				show_tips(words, 3)
				# 优化下载体验，实现队列下载
				win_music.perform_long_operation(lambda: cm.download_music(data, i), '-DOWNLOAD-FINDISH-')
			keyname = f'-LISTEN-{i}'
			# 处理在线听事件
			if event == keyname:		
				open_url(data['url'])
		
		if event == '-DOWNLAOD-FINISH-':
			words = '下好了'
			show_tips(words, 2)			
			
		if event == None:
			win_music.close()
			break

def open_url(url):
	'''打开一个网页'''
	if not url:
		words = '没找到呢~试试别的吧'
		show_tips(words, 2)
		return
	webbrowser.open_new_tab(url)


def show_tips(words, s):
	'''根据words和秒数定制一个提示窗口'''
	sg.popup_ok(words, auto_close=True, auto_close_duration=s, font=("仿宋", 14))


if __name__ == "__main__":
	key1, key2, key3 = "", "", ""
	key1 = input("input key1: ")
	if input("need second key(y/n)?: ") == "y":
		key2 = input("input key2: ")
		if input("need third key(y/n)?: ") == "y":
			key3 = input("input key3: ")
	while key1 != 'q':
		cnki(key1, key2, key3)
		key1 = input("input key1: ")
	if input("need second key(y/n)?: ") == "y":
		key2 = input("input key2: ")
		if input("need third key(y/n)?: ") == "y":
			key3 = input("input key3: ")
