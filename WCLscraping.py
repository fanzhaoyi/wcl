import numpy as np
import pandas as pd
import os
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup,NavigableString,Tag
from selenium.webdriver.chrome.options import Options
import datetime
import csv


def get_Info_Toprogue(trs):
	#get overall ranking info
	data = []
	#c=[rank,spec,name,guild_realm,contract,keylevel,my_affixes,date_created.split('$')[1],time_used,score,talents,trinkets,soulbinds,conduits,legendaries,url]
	col = ['Rank','Spec', 'Name', 'Guild_realm', 'Contract','Keylevel', 'Affixes','Date', 'Duration', 'Points', 'Talents', 'Trnk', 'Soulbinds', 'Conduits', 'Legendaries', 'Url']
	for tr in trs:
	
		#for tr in t:
		try:
			rank = int(tr.find('td',attrs={'class': 'rank'}).getText())
		except:
			rank = 0

		try:
			players_table = tr.find('div',attrs={'class': 'players-table-name-guild-realm'})
			imgs = players_table.find_all('img')
			try:
				spec = imgs[0].get('class')[-1].split('-')
				spec = spec[-2]+'-'+spec[-1]
			except Exception as e:
				spec = 'null'
				print ('spec:',e)
			#print (spec)
			try:
				contract = imgs[1].get('src').split('_')[-1].split('.')[0]
			except Exception as e:
				name = 'null'
				print ('contract',e)

			try:
			#print (contract)
				name = players_table.find('a',attrs={'class': 'main-table-link'}).getText()
			except Exception as e:
				name = 'null'
				print ('name',e)

			try:
			#print (name)
				url = players_table.find('a',attrs={'class': 'main-table-link'}).get('href')
			except:
				url='null'
				print ('url',e)
			#print (url)

			try:
				guild_realm = players_table.find('div',attrs={'class': 'players-table-guild-and-realm'}).getText().replace('\n', '').replace('\t', '').replace('\r', '')
			#print (guild_realm)
			except Exception as e:
				guild_realm = 'null'
				print ('guild an realm',e)
		except Exception as e:
			spec = 'null'
			contract='null'
			name = 'null'
			url = 'null'
			guild_realm = 'null'
			print ('players_table:',e)

		try:
			keylevel = tr.find('span',attrs={'class': 'klvl-value'}).getText()
		except:
			keylevel = 100

		try:
			my_affixes=[]
			affix_table=tr.find('span',attrs={'class': 'affix-table-icon-container'})
			affixes = affix_table.find_all('img')
			if affixes:
				for affix in affixes:
					my_affixes.append(affix.get('title'))
		except:
			my_affixes=['n','n','n','n']

		try:
			#time_used = tr.find('a',attrs={'class': 'rio-realm-link'}).getText()
			time_used = tr.find('td',attrs={'class': 'main-table-number players-table-duration'}).getText().replace('\n', '').replace('\t', '').replace('\r', '').replace(" ","")
			score = tr.find('td',attrs={'class': 'main-table-number keystone-score primary'}).getText().replace('\n', '').replace('\t', '').replace('\r', '').replace(" ","")
			#print (tr.find('td',attrs={'class': 'fights-table-duration main-table-number primary'}))
			if time_used:
				segs = time_used.split(':')
				if len(segs)==3:
					time_used=segs[0]+':'+segs[1]+':'+segs[2]
				elif len(segs)==2:
					time_used = '00:'+segs[0]+':'+segs[1]
		except:
			score = '0'
			time_used = 'null'

		try:
			date_created = tr.find('td',attrs={'class': 'main-table-number players-table-date'}).getText()
		except:
			date_created='idontknow'

		try:
			talents_table = tr.find('div',attrs={'class': 'talents-container'}).find_all('a')
			talents = [i.get('href').split('/')[-1] for i in talents_table]
		except:
			talents = ['null']

		try:
			trinkets_table = tr.find('div',attrs={'class': 'trinkets-container'}).find_all('a')
			trinkets = [i.get('href').split('/')[-1] for i in trinkets_table]
		except:
			trinkets = ['null']

		try:
			soulbinds_table = tr.find('div',attrs={'class': 'soulbinds-container'}).find_all('a')
			soulbinds = [i.get('href').split('/')[-1] for i in soulbinds_table]
		except:
			soulbinds = ['null']

		try:
			conduits_table = tr.find('div',attrs={'class': 'conduits-container'}).find_all('a')
			conduits = [i.get('href').split('/')[-1] for i in conduits_table]
		except:
			conduits = ['null']

		try:
			legendaries_table = tr.find('div',attrs={'class': 'legendaries-container'}).find_all('a')
			legendaries = [i.get('href').split('/')[-1] for i in legendaries_table]
		except:
			legendaries = ['null']

		# try:
		# 	legendaries_table = tr.find('div',attrs={'class': 'legendaries-container'}).find_all('a')
		# 	legendaries = [i.get('href').split('/')[-1] for i in legendaries_table]
		# except:
		# 	legendaries = ['null']

		#print (rank,spec,name,guild_realm,contract,keylevel,my_affixes,date_created,time_used,talents,trinkets,soulbinds,conduits,legendaries)
		temp=[rank,spec,name,guild_realm,contract,keylevel,my_affixes,date_created.split('$')[1],time_used,score,talents,trinkets,soulbinds,conduits,legendaries,url]
		#print (temp)
		data.append(temp)
	data.append(col)
	return data

def get_summary_table_info(trs,urls):
	#get team players info
	data = []
	col = ['rank','spec','name','percent','damage','gearlevel','rank_key','active','dps','url']	
	for tr in trs:
		#tr = td
		
		#for tr in t:
		try:
			rank = int(tr.find('td',attrs={'class': 'main-table-performance rank'}).getText())
		except:
			rank = 0

		try:
			players_table = tr.find('td',attrs={'class': 'main-table-name report-table-name'})
			# for node in players_table:
			# 	if isinstance(node,NavigableString):
			# 		node.extract()
			imgs = players_table.find_all('img')

			spec = imgs[0].get('class')[-1].split('-')

			classes = spec[-2]
			spec = spec[-2]+'-'+spec[-1]
			#contract = imgs[1].get('src').split('_')[-1].split('.')[0]

			name = players_table.find('td',attrs={'class': 'tooltip main-table-link'}).getText().replace('\n', '').replace('\t', '').replace('\r', '')
			url = urls+'&source='+tr.get('id').split('-')[-2]
	
			
		except:
			spec = 'null'
			#contract='null'
			name = 'null'
			url = 'null'
			#guild_realm = 'null'

		try:
			score_table = tr.find('td',attrs={'class': 'tooltip report-table-amount main-table-amount sorting_1'})
			percent = tr.find('div',attrs={'class': 'report-amount-percent'}).getText().replace('\n', '').replace('\t', '').replace('\r', '')
			damage =  tr.find('span',attrs={'class': 'report-amount-total'}).getText().replace('\n', '').replace('\t', '').replace('\r', '')
		except:
			percent=0
			damage = 0

		try:
			gearlevel = tr.find('td',attrs={'class': 'main-table-number rank main-table-ilvl tooltip'}).getText().replace('\n', '').replace('\t', '').replace('\r', '')
		except:
			gearlevel = 0

		try:
			rank_key = tr.find('td',attrs={'class': 'main-table-ilvl-performance rank'}).getText().replace('\n', '').replace('\t', '').replace('\r', '')
		except:
			rank_key = 0
		
		try:
			active = tr.find('td',attrs={'class': 'num tooltip main-table-active'}).getText().replace('\n', '').replace('\t', '').replace('\r', '')
		except:
			active = 0

		try:
			dps = tr.find('td',attrs={'class': 'main-table-number primary main-per-second-amount'}).getText().replace('\n', '').replace('\t', '').replace('\r', '')
		except:
			dps = 0
				
		temp=[rank,spec,name,percent,damage,gearlevel,rank_key,active,dps,url]
		#print (temp)
		data.append(temp)
	data.append(col)
	return data

def get_all_dungeon_rogue():
	dungeons = {
				12291: 'De Other Side',#DOS 
				12287: 'Halls of Atonement',#HOA
				12290: 'Mists of Tirna Scithe',#MIST
				12286: 'The Necrotic Wake',#NW
				12289: 'Plaguefall',#PF
				12284: 'Sanguine Depths',#SD
				12285: 'Spires of Ascension',#SOA
				12293: 'Theater of Pain' #TOP
				}
	#url_ = 'https://www.warcraftlogs.com/zone/rankings/25#leaderboards=1&boss=12293&class=Rogue&spec=Melee&faction=2&page='
	
	for dungeon in dungeons:
		# if dungeon == 12289:
		# 	therange = np.arange(5,10,1)
		# else:
		# 	therange = np.arange(10)
		# 	print (therange)

		therange=np.arange(10)
		#look at the first 10 pages
		for page in therange:
			global browser
			keep_looking = True
			above_24 = True	
			browser = webdriver.Chrome()
			has_browser = True

			if not above_24:
				break
			
			while keep_looking:
				try:
					if has_browser == False:
						browser = webdriver.Chrome()
					url = 'https://www.warcraftlogs.com/zone/rankings/25#leaderboards=1&boss='+str(dungeon)+'&class=Rogue&spec=Melee&faction=2&page='+str(page+1)
					#url = url_+str(page+1)
					browser.get(url)
					sleep(5)

					agree = '/html/body/div[2]/div/div/div/div[2]/div/button[3]'
					try:
						browser.find_element_by_xpath(agree).click()
					except Exception as e:
						print (e)
						
					soup = BeautifulSoup(browser.page_source,"lxml")
					table = soup.find('table', attrs={'class': 'summary-table ranking-table players-table dataTable no-footer'})
					table2 = soup.find('table', attrs={'class': 'summary-table ranking-table players-table dataTable no-footer collapsed'})
					
					if table:
						keep_looking = False
					elif table2:
						keep_looking = False
						table = table2
					has_browser = True
				except Exception as e:
					if has_browser==True:
						browser.quit()				
					print ('Reconnecting 1:', e)
					has_browser =False

			trs = []
			urls = []

			for i in range(100):
				tr_id = 'row-'+str(dungeon)+'-'+str((page)*100+i+1)
				tr_temp=table.find('tr',attrs={'id': tr_id})

				if tr_temp:
					for node in tr_temp:
						if isinstance(node,NavigableString):
							node.extract()
				trs.append(tr_temp)	
			print (len(trs),'players found on page',str(page+1))
			data_=get_Info_Toprogue(trs)
			data = data_[:-1]
			print (len(data),'players extracted on page',str(page+1))
			first_col = data_[-1]
			#print (first_col)
			if len(data)==0:
				continue

			for p in range(len(data[:])):
				#url2 = browser.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[2]/div/div[4]/div[1]/table/tbody/tr['+str(p+1)+']/td[2]/div/div[1]/a').get_attribute('href')
				
				the_player = data[p][2]
				the_rank = data[p][0]
				keylevel = int(data[p][5])
				if keylevel<24:
					print ('bingo')
					above_24=False
					data = data[:p]
					break

				keep_looking = True
				attemp2=0
				while keep_looking and attemp2<10:
					try:
						if has_browser == False:
							browser = webdriver.Chrome()
						c_url = 'https://www.warcraftlogs.com'+data[p][-1]
						debug = 'debug1'
						browser.get(c_url)
						sleep(4)
						debug = 'debug2'
						soup = BeautifulSoup(browser.page_source,"lxml")
						debug = 'debug3'
						table = soup.find('table', attrs={'class': 'summary-table report dataTable'})
						debug = 'debug4'
						#table2 = soup.find('table', attrs={'class': 'summary-table ranking-table players-table dataTable no-footer collapsed'})
						
						if table:
							keep_looking = False
							attemp2=11
						# elif table2:
						# 	keep_looking = False
						# 	table = table2
						has_browser = True
					except Exception as e:
						#browser.quit()
						attemp2+=1
						print ('Reconnecting 2:', e,debug,c_url)
						if has_browser==True:
							browser.quit()
						print (data[p])
						debug=''
						has_browser = False
				#summary_table = table
				if attemp2==10:
					data[p].append(['damage_done'])
					data[p].append(['damage_done'])
					data[p].append(['damage_done'])
					print (page,the_rank,the_player,'completed------')
					continue

				summary_table = table.find('tbody')
				the_head = table.find('thead')
				trs1 = summary_table.find_all('tr',attrs={'class': 'odd'})
				trs2 = summary_table.find_all('tr',attrs={'class': 'even'})
				trs = trs1+trs2
				numbers = [t.get('id').split('-')[-2] for t in trs]
				data2 = get_summary_table_info(trs,c_url)

				if len(data2)==0:
					continue

				full_table = []
				keep_looking = True
				attemp3=0
				while keep_looking and attemp3<10:
					try:
						if has_browser == False:
							browser = webdriver.Chrome()
						debug = 'debug1'
						browser.get(c_url+'&phase=-1')

						sleep(3)
						debug = 'debug2'
						summary_table = BeautifulSoup(browser.page_source,"lxml").find('table', attrs={'class': 'summary-table report dataTable'})
						#summary_table2 =  BeautifulSoup(browser.page_source,"lxml").find('table', attrs={'class': 'summary-table ranking-table players-table dataTable no-footer collapsed'})
						debug = 'debug3'
						if summary_table:
							keep_looking = False
							attemp3=11
						# elif table2:
						# 	keep_looking = False
						# 	table = table2
						has_browser = True
					except Exception as e:
						if has_browser==True:
							browser.quit()
						attemp3+=1
						print ('Reconnecting 3:', e,debug,c_url+'&phase=-1')
						debug = ''
						has_browser=False
						#browser.quit()
			
				the_table = summary_table.find('tbody')
				the_head = summary_table.find('thead')
				for node in the_table:
					if isinstance(node,NavigableString):
						node.extract()
				for i in range(len(the_table.contents)):
					for node in the_table.contents[i]:
						if isinstance(node,NavigableString):
							node.extract()
					temp = []
					for j in the_table.contents[i]:
						temp.append(j.getText().replace('\n', '').replace('\t', '').replace('\r', ''))

					full_table.append(temp[:-1]) 	
					#print (the_table.contents[i].getText().replace('\n', '*').replace('\t', '*').replace('\r', '*'))
				col = []
				for node in the_head:
					if isinstance(node,NavigableString):
						node.extract()
				for i in the_head.contents[0]:
					col.append(i.getText().replace('\n', '').replace('\t', '').replace('\r', ''))
				damage_done = [col[:-1]]+full_table
				#print (damage_done)

				data[p].append(damage_done)

				cols = data2[-1]
				data2 = data2[:-1]
				data2=[cols]+data2
				#print (data2)

				data[p].append(data2)

				for d in data2:
					if d[2]==the_player:

						keep_looking = True
						attemp4 = 0
						while keep_looking and attemp4<10:
							try:
								if has_browser==False:							
									browser = webdriver.Chrome()
								debug = 'debug1'
								browser.get(d[-1])
								sleep(4)
								debug = 'debug2'
								summary_table = BeautifulSoup(browser.page_source,"lxml").find('table', attrs={'class': 'summary-table report dataTable'})
								#summary_table2 =  BeautifulSoup(browser.page_source,"lxml").find('table', attrs={'class': 'summary-table ranking-table players-table dataTable no-footer collapsed'})
								debug = 'debug3'
								if summary_table:
									keep_looking = False
									attemp4=11
								# elif table2:
								# 	keep_looking = False
								# 	table = table2
								has_browser=True
							except Exception as e:
								#browser.quit()
								attemp4+=1
								print ('Reconnecting 4: ', e,debug,d[-1])
								debug=''
								if has_browser==True:
									browser.quit()
								has_browser=False

						if attemp4==10:
							data[p].append(['damage_done'])
							print (page,the_rank,the_player,'completed------')

							continue

						full_table = []
						
						the_table = summary_table.find('tbody')
						the_head = summary_table.find('thead')
						for node in the_table:
							if isinstance(node,NavigableString):
								node.extract()
						for i in range(len(the_table.contents)):
							for node in the_table.contents[i]:
								if isinstance(node,NavigableString):
									node.extract()
							temp = []
							for j in the_table.contents[i]:
								temp.append(j.getText().replace('\n', '').replace('\t', '').replace('\r', ''))

							full_table.append(temp[:-1])
							#print (the_table.contents[i].getText().replace('\n', '*').replace('\t', '*').replace('\r', '*'))
						col = []
						for node in the_head:
							if isinstance(node,NavigableString):
								node.extract()
						for i in the_head.contents[0]:
							col.append(i.getText().replace('\n', '').replace('\t', '').replace('\r', ''))
						damage_done = [col[:-1]]+full_table

						data[p].append(damage_done)
			
				print (page,the_rank,the_player,'completed------')
			final_col = first_col+['damage_to_boss','team','damage_done']
			#print (final_col)
			resultpath = 'WarcraftLogs/'+dungeons[dungeon]+'_Rouge_25+/'
			if not os.path.exists(resultpath):
				os.makedirs(resultpath)
				print (resultpath,'created')
			mytime2 = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
			if len(data)>0:
				if len(data[0])==19:
					pd.DataFrame(data).to_csv(resultpath+mytime2+'.csv',header=final_col[:len(data[0])], index=False,encoding="utf_8_sig")
				else:
					pd.DataFrame(data).to_csv(resultpath+mytime2+'_less24.csv',header=final_col[:len(data[0])], index=False,encoding="utf_8_sig")
			if has_browser==True:
				browser.quit()
			has_browser=False


get_all_dungeon_rogue()
