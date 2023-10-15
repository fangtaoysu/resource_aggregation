import PySimpleGUI as sg
from init import Home


# 创建一个home对象
home = Home()
# 创建窗口
win_root = sg.Window('资源搜索', home.layout, size=(1000,600), font=("楷体", 24))

while True:
	# 点击右上角，event=None
	# values：字典
	event, values = win_root.read(timeout=10)
	# input绑定回车，支持输入后完成后回车搜索
	win_root['-INPUT-'].bind("<Return>", 'Return-Key')
	
	# 关闭窗口
	if event is None:
		break
		
	# 按下搜索按钮，打开页面
	if event in home.event_callbacks:
		#win_root.Hide()
		key = values['-INPUT-']
		style = values['-STYLE-']
		home.event_callbacks[event](style, key)
		#win_root.UnHide()
		

# 关闭窗口
win_root.close()
