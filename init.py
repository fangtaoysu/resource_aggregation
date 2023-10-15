import PySimpleGUI as sg
from search_function import crawl_content
from cnki import main


class Home():
	'''初始化主界面信息'''
	
	def __init__(self):
		
		# 设置主题
		sg.theme('BluePurple')
		# 界面布局 一级列表从上往下，二级列表从左往右
		# key的规范写法：-KEYNAME-
		# 为元素添加事件 enable_events=True, key='-KEYNAME-'
		self.layout = [
			[sg.Text(size=(5,5)),],
			[sg.InputText(enable_events=True, key='-INPUT-'),sg.Spin(["小说", "音乐"], key='-STYLE-'),sg.Button("搜索", key='-SEARCH-')],
			[sg.Text(),],
			[sg.Text(size=(24,1)),sg.Button("搜索文献", key="-LITERATURE-")],
		]

		# 事件与方法绑定
		self.event_callbacks = {
			'-SEARCH-': crawl_content,
			'-INPUT-Return-Key': crawl_content,
			'-LITERATURE-': main,
		}
