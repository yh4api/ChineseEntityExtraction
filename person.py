# -*- coding: utf-8 -*-
#usage: python person para1
import re
import sys
from testInputPerson import *

def zh_sentence_split(text):
	text = text.replace('，','COMMACATEGORY')
	text = text.replace('。','COMMACATEGORY')
	text = text.replace('；','COMMACATEGORY')
	text = text.replace('、','COMMACATEGORY')
	text = text.replace('（','COMMACATEGORY')
	text = text.replace('）','COMMACATEGORY')
	return text.split("COMMACATEGORY")

jobTitle = """總統 | 少尉 | 文官 | 主任 | 主委 | 仕宦 | 司長 | 丞 | 吏 | 有司 | 次長 | 百夫長 | 行政長官 | 委員長 | 官 | 官吏 | 官兒 | 官長 | 官宦 | 官員 | 官僚 | 官職 | 治民官 | 股長 | 長官 | 政務官 | 科長 | 恩相 | 特任官 | 祕書長 | 秘書長 | 區長 | 國務卿 | 國務秘書 | 執政官 | 紳宦 | 組長 | 幹事 | 僚 | 勳爵 | 頭人 | 頭頭兒 | 廳長 | 官人 | 大元帥 | 上將 | 大帥 | 大將 | 中將 | 五星上將 | 元戎 | 元帥 | 少將 | 主帥 | 主將 | 名將 | 帥 | 特級上將 | 副司令 | 參謀總長 | 將官 | 將帥 | 將軍 | 統帥 | 小將 | 隊長 | 副隊長 | 領導人 | 教宗 | 教皇 | 總裁 | 副總裁 | 執行長 | 外交官 | 領事 | 內政部長 | 分局長 | 父母官 | 司法部長 | 外長 | 市長 | 布政使 | 民政局長 | 交通部長 | 列車長 | 地方官 | 州官 | 州牧 | 州長 | 老總 | 考試院長 | 行政院長 | 行政部長 | 局長 | 村長 | 系主任 | 車長 | 邦伯 | 里長 | 事務長 | 典獄長 | 協理 | 奉天省長 | 宜蘭縣長 | 所長 | 牧守 | 社長 | 社會處長 | 保正 | 保長 | 度支使司 | 建設廳長 | 省主席 | 省長 | 酋長 | 庭長 | 站長 | 財政部長 | 財政廳長 | 財經首長 | 郡守 | 郡候 | 院長 | 高雄縣長 | 副所長 | 副社長 | 副院長 | 副廠長 | 副總 | 副議長 | 商務部長 | 國防部長 | 教育局長 | 教育長 | 教育部長 | 教育廳長 | 理事長 | 船長 | 部長 | 部會首長 | 頂頭上司 | 單于 | 郵政局長 | 鄉長 | 園長 | 幹事長 | 督令 | 督撫 | 節度使 | 經濟部長 | 艇長 | 董事長 | 農官 | 農林廳長 | 監察院長 | 廠長 | 樂官 | 課長 | 輪機長 | 機長 | 縣長 | 館長 | 總務組長 | 總幹事 | 總經理 | 總辦 | 艦長 | 議長 | 警政署長 | 警務局長 | 警務部長 | 警察局長 | 護士長 | 鐵路局長 | 鐵路管理局 | 驛丞 | 鹽運使 | 經理 | 市民 | 候選人 | 主辦人 | 主席 | 參選人 | 發言人 | 創始人 | 創辦人 | 學家 | 主嫌 | 老師 | 教授 | 畫家 | 作家 | 醫師 | 名醫 | 廚師 | 大廚 | 委員 | 球員 | 好手 | 選手 | 影星 | 音樂家 | 導演 | 醫生 | 元老 | 主持人 | 歌手 | 代言人 | 部長 | 立委 | 藝人 | 設計師 | 獎得主 | 議員"""
family_member= """女兒 | 兒子 | 獨生女 | 獨生子 | 妻子 | 祖父 | 祖母 | 父親 | 母親 | 長女"""

family_name = """甘 丁 刁 卜 上官 千 尹 介 元 公孫 卞 孔 尤 巴 戈 文 方 毛 牛 王 王孫 冉 包 古 司 司空 司徒 司馬 史 左 申 白 時 伍 仲 任 匡 吉 安 曲 朱 江 牟 何 余 吳 呂 宋 巫 李 杜 沈 汪 谷 貝 辛 邢 阮 邵 卓 周 孟 官 屈 岳 房 易 林 武 邱 金 侯 俞 姜 姚 施 柯 段 洪 紀 胡 范 倪 唐 夏 孫 徐 柴 秦 翁 袁 軒轅 郝 馬 高 涂 寇 崔 庾 張 戚 曹 梅 畢 莫 莊 許 連 郭 陳 陸 陶 章 麥 傅 單 彭 曾 游 湯 童 費 賀 鈕 項 馮 黃 愛新覺羅 楊 浦 萬 梁 葉 董 虞 詹 賈 鄒 雷 廖 甄 翟 蒲 裴 褚 趙 齊 劉 歐 歐陽 潘 蔣 蔡 衛 諸葛 鄭 鄧 鞏 魯 黎 盧 穆 蕭 賴 錢 駱 霍 鲍 龍 勵 戴 璩 繆 薛 謝 賽 鍾 韓 瞿 聶 藍 闕 顏 魏 鄺 龐 羅 嚴 蘇 饒 顧 龔 程 狄 梁 隋 辜 岑 裘 苗 郎 韋 庹 焦 符 艾 佘 溫 柳 權 樊 展 桑 康 習 海"""

temporal = "週一 星期一 禮拜一 週二 星期二 禮拜二 週三 星期三 禮拜三 週四 星期四 禮拜四 週五 星期五 禮拜五 週六 星期六 禮拜六 週日 星期日 禮拜日 禮拜天 星期天 今天 昨天 明天 早上 下午 今早 昨晚 今晚 今\( 昨\("

cue_verbs = "指出 表示 接受 出席 是"
cur_words = temporal+" "+cue_verbs
jobTitles = jobTitle.split(" | ")
jobTitles += family_member.split(" | ")
job_title_exp = "r'("
job_title_exp = ""

job_title_exp += "|".join(jobTitles)
#job_title_exp += ")'"
jt_comp = re.compile(r'('+job_title_exp+')')
fns = family_name.split()
cur_word_exp="|".join(cur_words.split())
cur_word_comp = re.compile(r'('+cur_word_exp+')') 

cand = []
NERList = []

inL = sys.stdin.readline().strip()

while inL:
	if inL.startswith("-i"):
		text = zh_sentence_split(inL[2:])
	elif inL == "exit":
		break
	else:
		try:
			#text = zh_sentence_split(eval(sys.argv[1]))
			text = zh_sentence_split(eval(inL))
		except:
			print "input doesn't exist; try next one"
			inL = sys.stdin.readline().strip()
			continue
	#for t in text:
	#print t
	for t in text:
		#print t
		#m = jt_comp.search(t) 
		#print m==None
		#if m != None:
		for m in jt_comp.finditer(t):
			fn_bi_behind = t[m.end():m.end()+6]
			fn_behind = t[m.end():m.end()+3]
			#print fn_bi_behind, fn_behind
			if fn_bi_behind in fns:
				check = 0
				if cur_word_comp.match(t[m.end()+9:])!=None:
					check = 1
					NERList.append(t[m.end():m.end()+9])
				elif cur_word_comp.match(t[m.end()+12:])!=None:
					check = 1
					NERList.append(t[m.end():m.end()+12])
				if not check:
					cand.append(t[m.end():m.end()+9]) #LLF
					cand.append(t[m.end():m.end()+12])#LLFF
			elif fn_behind in fns:
				check = 0
				#print re.match(r'$', t[m.end()+9:]) == None
				if cur_word_comp.match(t[m.end()+6:])!=None:
					check = 1
					NERList.append(t[m.end():m.end()+6])
				elif cur_word_comp.match(t[m.end()+9:])!=None or re.match(r'$', t[m.end()+9:])!=None:
					check = 1
					NERList.append(t[m.end():m.end()+9])
#			print NERList
				if not check:
					cand.append(t[m.end():m.end()+6]) #LF
					cand.append(t[m.end():m.end()+9]) #LFF
			#LLFF
			fn_bi_ahead = t[m.start()-12:m.start()-6]
			if fn_bi_ahead in fns:
				cand.append(t[m.start()-12:m.start()])
			#LLF
			fn_bi_ahead = t[m.start()-9:m.start()-3]
			if fn_bi_ahead in fns:
				cand.append(t[m.start()-9:m.start()])
			#LFF
			
			fn_ahead = t[m.start()-9:m.start()-6]
			if fn_bi_ahead in fns:
				cand.append(t[m.start()-9:m.start()])

			#LF
			fn_ahead = t[m.start()-6:m.start()-3]
			if fn_bi_ahead in fns:
				cand.append(t[m.start()-6:m.start()])
#		for c in cand:
#			print c

	cand = list(set(cand))
	cand.sort(key=len, reverse=True)
	print "candidate list"
	new_ner = []
	for cid, c in enumerate(cand):
		#print cid, c
		count = 0
		flag = 0
		for t in text:
			#if t.find(c)!=-1:
			#	count += 1
			count+= t.count(c)
		for n in new_ner:
			if n.find(c, 0) != -1:
				flag = 1
				break
		if not flag and count >= 2:
			new_ner.append(c)
		elif not flag:
			print c
	print "sure list"
	for n in set(NERList+new_ner):
		print n
	
	cand = []
	NERList = []
	inL = sys.stdin.readline().strip()
