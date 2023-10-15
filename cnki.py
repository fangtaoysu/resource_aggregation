import PySimpleGUI as sg
import search_function as sf


def init():
	'''显示窗口'''
	title_list = ['主题', '篇关摘', '关键字', '篇名', '全文', '作者', '第一作者', '通讯作者', '作者单位', '基金', '摘要', '小标题', '参考文献', '分类号', '文献来源', 'DOI']

	layout = [
		[sg.Text(size=(5,5)),],
		[sg.Text(size=(4,1)), sg.Combo(title_list, key='-TITLE1-', size=(8,1)), sg.InputText(enable_events=True, key='-KEY1-'),],
		[sg.Combo(['AND', 'OR', 'NOT'], key='-OPE1-', size=(3,1)), sg.Combo(title_list, key='-TITLE2-', size=(8, 1)), sg.InputText(enable_events=True, key='-KEY2-'),],
		[sg.Combo(['AND', 'OR', 'NOT'], key='-OPE2-', size=(3,1)), sg.Combo(title_list, key='-TITLE3-', size=(8,1)), sg.InputText(enable_events=True, key='-KEY3-'),],
		[sg.Button("检索", key = '-SEARCH-', size=(11,1)),],
	]
	win_cnki = sg.Window('文献搜索', layout, size=(1000,600), font=("楷体", 24))
	event_callbacks = {
		'-SEARCH-': sf.cnki,
		'-KEY1-Return-Key': sf.cnki,
		'-KEY2-Return-Key': sf.cnki,
		'-KEY3-Return-Key': sf.cnki,
	}
	return event_callbacks, win_cnki

def main(*param):
	'''爬取文献的主逻辑'''
	event_callbacks, win_cnki = init()
	while True:
		event, values = win_cnki.read()
		win_cnki['-KEY1-'].bind("<Return>", 'Return-Key')
		win_cnki['-KEY2-'].bind("<Return>", 'Return-Key')
		win_cnki['-KEY3-'].bind("<Return>", 'Return-Key')
		
		# 关闭窗口
		if event is None:
			break
		ope1, ope2 = 1, 1	
		if values['-OPE1-'] == 'AND':
			ope1 = 1
		elif values['-OPE1-'] == 'OR':
			ope1 = 2
		elif values['-OPE1-'] == 'NOT':
			ope1 = 3	
		if values['-OPE2-'] == 'AND':
			ope2 = 1
		elif values['-OPE2-'] == 'OR':
			ope2 = 2
		elif values['-OPE2-'] == 'NOT':
			ope2 = 3
			
		if event in event_callbacks:
			key1 = values['-KEY1-']
			key2 = values['-KEY2-']
			key3 = values['-KEY3-']
			title1 = values['-TITLE1-']
			title2 = values['-TITLE2-']
			title3 = values['-TITLE3-']
			event_callbacks[event](title1, title2, title3, key1, key2, key3, ope1, ope2)
			
	win_cnki.close()
