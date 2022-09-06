from psychopy import visual, core, event, gui, prefs, sound, monitors, parallel
import shelve, sys
import random
import numpy as np
import traceback
import os
from os import listdir
from os.path import isfile, join
from imp import reload
import myshuffle2
reload(myshuffle2)
from myshuffle2 import xp_shuffle2
reload(sys)
#import #serial
from win32api import GetSystemMetrics
#sys.setdefaultencoding("UTF-8")

execute=list(sys.argv)#argument: practice or not(1 or 0)/ test or not(1 or 0)/end block/start block
sub=int(input('ID:'))#type subject number (even: green-left, red-right; odd: red-left, green-right)
p = parallel.ParallelPort('0x0378')

if str(sub) in listdir("exp2_data_follow_MEG/log_file"):
	jud=input('continues?(y/n)')
	if jud=="n":
		sys.exit()
else:
	os.makedirs("exp2_data_follow_MEG/log_file/"+str(sub))


if sub%12>=6:
	if sub%2==1:
		intr_order=['per','img','exe','execon']
		#self_r=["第一個方塊出現時，你有多專注看方塊？（1-9分）","第一個方塊出現時，你想像的按鍵動作感覺有多真實？（1-9分）","第一個方塊出現時，你多有自信按到正確按鍵？（1-9分）"]
	else:
		intr_order=['per','exe','img','execon']
		#self_r=["第一個方塊出現時，你有多專注看方塊？（1-9分）","第一個方塊出現時，你多有自信按到正確按鍵？（1-9分）","第一個方塊出現時，你想像的按鍵動作感覺有多真實？（1-9分）"]
else:
	if sub%2==0:
		intr_order=['per','img','exe','execon']
		#self_r=["第一個方塊出現時，你有多專注看方塊？（1-9分）","第一個方塊出現時，你想像的按鍵動作感覺有多真實？（1-9分）","第一個方塊出現時，你多有自信按到正確按鍵？（1-9分）"]
	else:
		intr_order=['per','exe','img','execon']
		#self_r=["第一個方塊出現時，你有多專注看方塊？（1-9分）","第一個方塊出現時，你多有自信按到正確按鍵？（1-9分）","第一個方塊出現時，你想像的按鍵動作感覺有多真實？（1-9分）"]
con=intr_order[int(int(execute[3])-1)]
print('the condition is '+con)

if str(sub) in listdir("exp2_data_follow_MEG"):
	onlyfiles = [f for f in listdir("exp2_data_follow_MEG/"+str(sub)) if isfile(join("exp2_data_follow_MEG/"+str(sub), f))]
else:
	os.makedirs("exp2_data_follow_MEG/"+str(sub))
"""
fix_t=np.random.exponential(0.5,36*2)
fix_t=(np.array(fix_t)-min(fix_t))/max(fix_t)+1
fix_t=[round(x,1) for x in fix_t]
np.mean(fix_t)
"""
mon = monitors.Monitor('4MEG')
mon.setSizePix((GetSystemMetrics(0),GetSystemMetrics(1))) #monitor width in pix
mon.setWidth(28)#monitor width in cm
mon.setDistance(33) #monitor distance in cm
mon.saveMon()


try:
	win = visual.Window((1920,1080),monitor='4MEG', allowGUI=True,
					color=(0,0,0), fullscr = True,\
					units='deg', screen=1,gammaErrorPolicy='ignore')
	st_size = 1.5
	blknum = 3
	#st_size=100
	r=visual.Rect(win,width=st_size, height=st_size, \
			lineColor=[-1,-1,-1],fillColor=[1,1,1])
	tri_sqr=visual.Rect(win,width=12, height=6, units='deg', pos=(0, 19),\
			lineColor=[1,1,1],fillColor=[1,1,1])

	key=['comma','period','slash']
	key=['left','down','right']
	key=['9','8','7']
	key_pos=['left','middle','right']
	trig_order=['per','img','exe','execon']

	#ser = #serial.#serial("COM5", 115200, timeout=1)

	#ser.write(b"ff")

	if sub%6==1:
		color=[(-1,-1,1),(1,-1,-1),(-1,1,-1)]#blue/red/green
	elif sub%6==2:
	    color=[(1,-1,-1),(-1,-1,1),(-1,1,-1)]#red/blue/green
	elif sub%6==3:
		color=[(-1,-1,1),(-1,1,-1),(1,-1,-1)]#blue/green/red
	elif sub%6==4:
	    color=[(-1,1,-1),(-1,-1,1),(1,-1,-1)]#green/blue/red
	elif sub%6==5:
	    color=[(1,-1,-1),(-1,1,-1),(-1,-1,1)]#red/green/blue
	else:
	    color=[(-1,1,-1),(1,-1,-1),(-1,-1,1)]#green/red/blue
	irrelevant=(1,1,1)


	#ser.write(b"00")

	ck = core.Clock()

	LH=visual.Line(win, \
			start=(-st_size/4,0), end=(st_size/4,0),\
			fillColor=(0,0,1),lineColor=(-1,-1,-1))
	LV=visual.Line(win, \
			start=(0,-st_size/4), end=(0,st_size/4),\
			fillColor=(0,0,1),lineColor=(-1,-1,-1))

	mask=visual.GratingStim(win,size=st_size)#,blendmode='add')

	"""
	img=visual.TextStim(win, color=(-1.0, -1.0, -1.0),height=st_size, text='imagery')
	exe=visual.TextStim(win, color=(-1.0, -1.0, -1.0),height=st_size, text='execution')
	correct=visual.TextStim(win, color=(-1.0, -1.0, -1.0),height=st_size, text='correct')
	wrong=visual.TextStim(win, color=(-1.0, -1.0, -1.0),height=st_size, text='wrong')
	late=visual.TextStim(win, color=(-1.0, -1.0, -1.0),height=st_size, text='late response')
	"""

	prac = visual.TextStim(win, text = "顏色按鍵配對", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	test = visual.TextStim(win, text = "實驗階段", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	febk = visual.TextStim(win, text = "按鍵正確", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	img = visual.TextStim(win, text = "想像按鍵", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	exe = visual.TextStim(win, text = "實際按鍵", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	execon = visual.TextStim(win, text = "覺察按鍵", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	per = visual.TextStim(win, text = "注意手指", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	rest = visual.TextStim(win, text = "休息", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	rest_a = visual.TextStim(win, text = "休息（按任意鍵繼續）", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	complete = visual.TextStim(win, text = "完成顏色按鍵配對", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	warn = visual.TextStim(win, text = "請勿按鍵", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	start = visual.TextStim(win, text = "正式開始", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	PRA = visual.TextStim(win, text = "練習", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	p2cont = visual.TextStim(win, text = "準備好按左手小拇指繼續", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	att_withProgram = visual.TextStim(win, text = "在注意手指時，\n是否會自動產生按鍵的衝動？", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)
	if intr_order[1]=='img':
		eval = [visual.TextStim(win, text = "第一個方塊出現時，你有多注意\n顏色對應到的手指？（1-7分）", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True),\
		visual.TextStim(win, text = "第一個方塊出現時，你想像的按鍵動作\n感覺有多真實？（1-7分）", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True),\
		visual.TextStim(win, text = "第一個方塊出現時，你多有自信\n按到正確按鍵？（1-7分）", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True),\
		visual.TextStim(win, text = "第一個方塊出現時，你的按鍵動作\n感覺有多清楚？（1-7分）", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)]
	else:
		eval = [visual.TextStim(win, text = "第一個方塊出現時，你有多注意\n顏色對應到的手指？（1-7分）", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True),\
		visual.TextStim(win, text = "第一個方塊出現時，你多有自信\n按到正確按鍵？（1-7分）", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True),\
		visual.TextStim(win, text = "第一個方塊出現時，你想像的按鍵動作\n感覺有多真實？（1-7分）", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True),\
		visual.TextStim(win, text = "第一個方塊出現時，你的按鍵動作\n感覺有多清楚？（1-7分）", units = 'deg', height = st_size/1.5,color=(-1,-1,-1),bold=True)]
	#IV list
	cond_order=[1,1,1,0,0,0,0,0,0]*4
	color_order=color*12
	answer_order=key*12
	position_order=key_pos*12
	p_fix_t=[0.075, 0.15, 0.225, 0.3]*9
	fixa_time=0.3

	#DV list
	pre_motor_type=[]
	rt_pre=[]
	acc_pre=[]
	false_response_per=[]
	false_response_img=[]

	rt_test=[]
	acc_test=[]
	repeat=[]

	irrelevant_rt=[]

	whole_color=[]
	whole_position_order=[]
	whole_motor_type=[]
	whole_fix=[]
	self_evaluation=[]

	#extra data
	practice_left=[]
	practice_middle=[]
	practice_right=[]
	practice_left_img=[]
	practice_middle_img=[]
	practice_right_img=[]
	practice_left_exe=[]
	practice_middle_exe=[]
	practice_right_exe=[]
	att_ProgramPercent_t = []
	time_limit=1
	p.setData(0)
	#for practice
	if execute[1]=='1':
		correct_l=0
		correct_r=0
		correct_m=0
		pra_rt=[]
		pra_acc=[]
		pra_pos=[]
		pra_con=[]
		pra_color=[]
		pra_clock=[]
		win.mouseVisible = False
		prac.draw()
		win.flip()
		event.waitKeys(keyList=['space'])
		cri=5#the criterion of how many consecutive correct response

		prc_prctice=0
		sequence=list(range(12))
		random.shuffle(sequence)
		time_vec_l=[]
		time_vec_m=[]
		time_vec_r=[]
		#the rule is .... 1.repeat: color can not be same as later one 2.non-repeat: the second one can not be samee as later one
		while correct_l<cri or correct_r<cri or correct_m<cri:
			prc_prctice+=1
			key_an=[]
			key_previous=[]
			press_count = 0
			LH.draw()
			LV.draw()
			win.flip()
			core.wait(fixa_time-0.2)
			dis=sequence[prc_prctice%12]%3
			r.fillColor=color[dis]
			r.draw()
			tri_sqr.draw()
			p.setData(2)
			win.flip()

			event.clearEvents()
			p.setData(0)
			t1=ck.getTime()
			t0=ck.getTime()
			while t1-t0<time_limit:
				t1=ck.getTime()
				key_an_each=event.getKeys(key+['escape'],timeStamped=ck)
				if key_an_each!=[]:

					press_count+=1
					key_an = key_an_each

			if press_count>1:
				febk.setText("方塊出現後請勿按鍵超過一次")
				if dis==0:
					correct_l=0
					practice_left.append('multiple response')
				elif dis==2:
					correct_r=0
					practice_right.append('multiple response')
				else:
					correct_m=0
					practice_middle.append('multiple response')

			elif press_count==1:
				if key_an[0][0]=='escape':
					break
				elif key_an[0][0]==key[dis]:
					p.setData(4)
					febk.setText("按鍵正確")
					pra_acc.append(1)
					pra_rt.append(key_an[0][1]-t0)
					pra_pos.append(key_pos[dis])
					pra_con.append(con)
					pra_color.append(color[dis])
					pra_clock.append([key_an[0][1],t0])
					if dis==0:
						correct_l+=1
						practice_left.append(1)
						time_vec_l.append(key_an[0][1]-t0)
					elif dis==2:
						correct_r+=1
						practice_right.append(1)
						time_vec_r.append(key_an[0][1]-t0)
					else:
						correct_m+=1
						practice_middle.append(1)
						time_vec_m.append(key_an[0][1]-t0)
				else:
					p.setData(12)
					febk.setText("按鍵錯誤")
					pra_acc.append(0)
					pra_rt.append(key_an[0][1]-t0)
					pra_pos.append(key_pos[dis])
					pra_con.append(con)
					pra_color.append(color[dis])
					pra_clock.append([key_an[0][1],t0])
					if dis==0:
					    correct_l=0
					    if key_an[0][0]==key_previous:
					        practice_left.append('error from previous')
					    else:
					        practice_left.append(0)
					elif dis==2:
					    correct_r=0
					    if key_an[0][0]==key_previous:
					        practice_right.append('error from previous')
					    else:
					        practice_right.append(0)
					else:
					    correct_m=0
					    if key_an[0][0]==key_previous:
					        practice_middle.append('error from previous')
					    else:
					        practice_middle.append(0)

			else:
				febk.setText("請在方塊消失前按鍵")
				pra_acc.append('no response')
				pra_rt.append(99)
				pra_pos.append(key_pos[dis])
				pra_con.append(con)
				pra_color.append(color[dis])
				pra_clock.append([t0])
				if dis==0:
					correct_l=0
					practice_left.append('no response')
				elif dis==2:
					correct_r=0
					practice_right.append('no response')
				else:
					correct_m=0
					practice_middle.append('no response')

			key_previous=key[dis]
			febk.draw()
			win.flip()
			p.setData(0)
			core.wait(1)

			if correct_l>=cri and correct_r>=cri and correct_m>=cri:
			    complete.draw()
			    win.flip()
			    core.wait(1)
			elif prc_prctice%12==0:
			    random.shuffle(sequence)
			    rest_a.draw()
			    win.flip()
			    event.waitKeys()
		d_log = shelve.open("exp2_data_follow_MEG/log_file/"+str(sub)+"/"+con+"_practice")
		d_log['rt']=pra_rt
		d_log['acc']=pra_acc
		d_log['pos']=pra_pos
		d_log['color']=pra_color
		d_log['condition']=pra_con
		d_log['clock']=pra_clock
		d_log.close()

	if execute[2]=='1':
		t_start=ck.getTime()
		if execute[1]=='0':
			d = shelve.open("exp2_data_follow_MEG/"+str(sub)+"/"+con)
			practice_left=d['left_practice_accuracy']
			practice_right=d['right_practice_accuracy']
			practice_middle=d['middle_practice_accuracy']
			time_vec_l=d['left_practice_time']
			time_vec_r=d['right_practice_time']
			time_vec_m=d['middle_practice_time']
			if execute[4]!='1':
				rt_pre=d['pre_execution_rt']
				acc_pre=d['pre_execution_accuracy']
				false_response_per=d['pre_perception_false_response']
				false_response_img=d['pre_imagery_false_response']
				rt_test=d['post_execution_rt']
				acc_test=d['post_execution_accuracy']
				pre_motor_type=d['pre_motor_type']
				repeat=d['repeat_or_not']
				irrelevant_rt=d['irrelevant_rt']
				whole_color=d['whole_color_order']
				whole_motor_type=d['whole_motor_type_order']
				whole_position_order=d['whole_position_order']
				whole_fix=d['whole_fixation_time']
				self_evaluation=d['self evaluation']
			d.close()
		#time_vec=[np.mean(time_vec_l),np.mean(time_vec_m),np.mean(time_vec_r)]
		cri=5

		for block in range(int(execute[4]),blknum+1):
			log_rt=[]
			log_acc=[]
			log_resp=[]
			log_finger=[]
			log_con=[]
			log_type=[]
			log_color=[]
			log_clock=[]
			log_block=[]
			log_pre_fixation_time=[]

			color01=0
			color02=0
			color10=0
			color12=0
			color20=0
			color21=0

			while color01!=color02 or color10!=color12 or color21!=color20 or color01==0:
				second_color_order, order,color01,color02,color10,color12,color21,color20=xp_shuffle2(4,color)

			#random.shuffle(fix_t)
		    #practice tr
			#second_color_order,order=xp_shuffle(5,color)
			#random.shuffle(fix_t)
			win.mouseVisible = False
			if block==1:
				test.draw()
				win.flip()
				core.wait(1)

				exec("%s.draw()" %con)
				win.flip()
				event.clearEvents()
				event.waitKeys(keyList=['space'])

				PRA.draw()
				win.flip()
				event.clearEvents()
				key_t = event.waitKeys(keyList=['space','1'])
				for pre in range(len(color)*2):
					key_an = None
					r.fillColor=color[pre%len(color)]
					t1=0
					tx=0
					LH.draw()
					LV.draw()
					win.flip()
					event.clearEvents()
					core.wait(fixa_time)
					r.draw()
					win.flip()
					#===============對到這=============
					if con[:3]=='exe':
						t1=ck.getTime()
						t0=ck.getTime()
						while t1-t0<time_limit:
							t1=ck.getTime()
							key_an_each=event.getKeys(key+['escape'],timeStamped=ck)
							if key_an_each!=[]:
								#press_count+=1
								key_an = key_an_each
						win.flip()
						core.wait(random.choice(p_fix_t))
					else:
						t0=ck.getTime()
						key_an=event.waitKeys(time_limit,key+['escape'],timeStamped=ck)
						win.flip()
						if key_an!=None:
						    warn.draw()
						    win.flip()
						    core.wait(1)
						else:
							key_an=event.waitKeys(random.choice(p_fix_t),key+['escape'],timeStamped=ck)
							if key_an!=None:
							    warn.draw()
							    win.flip()
							    core.wait(1)


						if key_an!=None and key_an[0][0]=='escape':
						        break

					LH.draw()
					LV.draw()
					win.flip()
					event.clearEvents()
					core.wait(fixa_time)
					r.fillColor=color[pre%3-pre%2]
					r.draw()
					win.flip()

					t0=ck.getTime()
					key_an=event.waitKeys(time_limit+1,key+['escape'],timeStamped=ck)

					if key_an!=None and key_an[0][0]=='escape':
					    break


					win.flip()
					core.wait(1)
					LH.draw()
					LV.draw()
					win.flip()
					core.wait(fixa_time)
					r.fillColor=irrelevant
					r.draw()
					win.flip()
					event.clearEvents()
					t0=ck.getTime()
					key_an=event.waitKeys(keyList=['1', 'escape'],timeStamped=ck)
					if key_an!=None:
						if key_an[0][0]=='escape':
						    break
						else:
							win.flip()
							core.wait(random.choice(p_fix_t))
				start.draw()
				win.flip()
				key_t = event.waitKeys(keyList=['space','1'])

			#real test
			answer=0
			ff=0
			p2cont.draw()
			win.flip()
			event.waitKeys(keyList=['1'])

			for pre in order:
			    #pre trial

				core.wait(0.8)

				key_an=None
				win.mouseVisible = False
				LH.draw()
				LV.draw()
				win.flip()
				event.clearEvents()
				core.wait(fixa_time)

				r.fillColor=color_order[pre]
				whole_color.append(color_order[pre])
				whole_position_order.append(position_order[pre])
				r.draw()
				tri_sqr.draw()
				#p.setData(4)##ser.write(str(trig_order.index(con)+1)+'2')
				p.setData(2**(trig_order.index(con)+4)+1)
				#ser.write(b"01")
				win.flip()
				p.setData(0)


				if con[:3]=='exe':
					t1=ck.getTime()
					t0=ck.getTime()
					while t1-t0<time_limit:
						t1=ck.getTime()
						key_an_each=event.getKeys(key+['escape'],timeStamped=ck)
						if key_an_each!=[]:

							#press_count+=1
							key_an = key_an_each
							if key_an[0][0]!='escape':
							    #p.setData(12)#int(key_an[0][0]==answer_order[pre])*4+16)#
								p.setData(64+128*(1-int(key_an[0][0]==answer_order[pre])))
								#ser.write(b'e'+str(int(key_an[0][0]==answer_order[pre])))
					#ser.write(b"00")
					win.flip()
					p.setData(0)
					core.wait(p_fix_t[pre])
				else:

					t0=ck.getTime()
					key_an=event.waitKeys(time_limit,key+['escape'],timeStamped=ck)
					#ser.write(b"00")
					win.flip()
					if key_an!=None :
						warn.draw()
						win.flip()
						core.wait(1)
					else:
						key_an=event.waitKeys(p_fix_t[pre],key+['escape'],timeStamped=ck)
						if key_an!=None :
							if key_an[0][0]!='escape':
							    p.setData(16+32)#trig_order.index(con)*100+3*(2-int(key_an[0][0]==answer_order[pre])))##ser.write(b'e'+str(int(key_an[0][0]==answer_order[pre])))8
							warn.draw()
							win.flip()
							core.wait(1)
				if key_an!=None and key_an[0][0]=='escape':
					break
				elif con[:3]=='exe':
					pre_motor_type.append(con)
					whole_motor_type.append(con)
					if key_an!=None :
					    rt_pre.append(key_an[0][1]-t0)
					    acc_pre.append(key_an[0][0]==answer_order[pre])
					    if key_an[0][0]!=answer_order[pre] and key_an[0][0]==answer:
					        acc_pre[-1]='error from previous'

					elif key_an==None:
					    rt_pre.append(99)
					    acc_pre.append('no response')
				else:
					pre_motor_type.append(con)
					whole_motor_type.append(con)
					if key_an!=None :
					    exec("false_response_%s.append(1)" %con)
					elif key_an==None:
					    exec("false_response_%s.append(0)" %con)



				if key_an!=None and key_an[0][0]=='escape':
						break

				log_pre_fixation_time.append(ff+0.8)
				log_color.append(color_order[pre])
				log_finger.append(position_order[pre])
				if key_an!=None:
					log_resp.append(key_an[0][0])
					log_rt.append(key_an[0][1]-t0)
					log_acc.append(key_an[0][0]==answer_order[pre])
					log_clock.append([key_an[0][1],t0])
				else:
					log_resp.append('no response')
					log_rt.append(99)
					log_acc.append(con[:3]!='exe')
					log_clock.append([t0])
				log_con.append(con)
				log_type.append('pre_trial')
				log_block.append(block)
				#test trials
				key_an=[]

				whole_fix.append(ff+0.8)
				whole_motor_type.append('exe')
				repeat.append(cond_order[pre])

				LH.draw()
				LV.draw()
				win.flip()


				event.clearEvents()
				core.wait(fixa_time)

				second_color=second_color_order[order.index(pre)]
				r.fillColor=second_color
				answer=key[color.index(second_color)]

				r.draw()
				tri_sqr.draw()
				#ser.write(b"10")
				#p.setData(8*(cond_order[pre]+1))##ser.write(str(trig_order.index(con)+1)+str(cond_order[pre]))
				p.setData(2**(trig_order.index(con)+4)+2**(1+2*(1-cond_order[pre])))
				win.flip()
				p.setData(0)

				t0=ck.getTime()
				key_an=event.waitKeys(time_limit+1,key+['escape'],timeStamped=ck)
				#ser.write(b"00")
				if key_an!=None:
					if key_an[0][0]=='escape':
						break

					else :
						#p.setData(20+cond_order[pre]*4)

						p.setData(2**(trig_order.index(con)+4)+2**(1+2*(1-cond_order[pre]))+int(key_an[0][0]==answer)*4+\
						(int(key_an[0][0]!=answer))*cond_order[pre]*12+\
						(int(key_an[0][0]!=answer))*(1-cond_order[pre])*(-4))

						rt_test.append(key_an[0][1]-t0)
						acc_test.append(key_an[0][0]==answer)
						print(key_an[0][0]==answer,key_an[0][1]-t0)#online check
						if key_an[0][0]!=answer and key_an[0][0]==answer_order[pre]:
						    acc_test[-1]='error from previous'

				else:
				    rt_test.append(99)
				    acc_test.append('no response')

				whole_color.append(second_color)
				whole_position_order.append(key_pos[color.index(second_color)])

				whole_fix.append(p_fix_t[pre])

				log_pre_fixation_time.append(p_fix_t[pre])
				log_color.append(second_color)
				log_finger.append(key_pos[color.index(second_color)])
				if key_an!=None:
					log_resp.append(key_an[0][0])
					log_rt.append(key_an[0][1]-t0)
					log_acc.append(key_an[0][0]==answer)
					log_clock.append([key_an[0][1],t0])
				else:
					log_resp.append('no response')
					log_rt.append(99)
					log_acc.append(False)
					log_clock.append([t0])

				log_con.append(con)
				log_type.append('post_'+'non-'*(1-cond_order[pre])+'repeat')
				log_block.append(block)

				ff=random.choice(p_fix_t)
				win.flip()
				#ser.write(b"00")99987987
				core.wait(ff+0.5)
				p.setData(0)
				LH.draw()
				LV.draw()
				win.flip()
				core.wait(fixa_time)
				r.fillColor=irrelevant
				r.draw()
				win.flip()
				event.clearEvents()
				t0=ck.getTime()
				key_an=event.waitKeys(keyList=['1', 'escape'],timeStamped=ck)
				if key_an!=None:
					if key_an[0][0]=='escape':
					    break
					else:
						irrelevant_rt.append(key_an[0][1]-t0)
						ff=random.choice(p_fix_t)
						win.flip()
						core.wait(ff)
				whole_fix.append(ff+0.5)
				whole_color.append([1,1,1])
				whole_position_order.append('irrelevant')
				whole_motor_type.append('exe')

				log_pre_fixation_time.append(ff+0.5)
				log_color.append([1,1,1])
				log_finger.append('l_little')
				if key_an!=None:
					log_resp.append(key_an[0][0])
					log_rt.append(key_an[0][1]-t0)
					log_acc.append(key_an[0][0]=='1')
					log_clock.append([key_an[0][1],t0])
				else:
					log_resp.append('no response')
					log_rt.append(99)
					log_acc.append(False)
					log_clock.append([t0])

				log_con.append(con)
				log_type.append('irrelevant')
				log_block.append(block)

			    #mask.setcolor=


			if key_an!=None and key_an[0][0]=='escape':
			    break
			else:
				rest.draw()
				win.flip()
				event.waitKeys(keyList=['space'])

				d_log = shelve.open("exp2_data_follow_MEG/log_file/"+str(sub)+"/"+con+"_0"+str(block))
				d_log['rt']=log_rt
				d_log['acc']=log_acc
				d_log['pos']=log_finger
				d_log['color']=log_color
				d_log['condition']=log_con
				d_log['clock']=log_clock
				d_log['type']=log_type
				d_log['response']=log_resp
				d_log['pre_fix']=log_pre_fixation_time
				d_log['block']=log_block
				d_log.close()


				eval[int(int(execute[3])-1)].draw()
				win.flip()
				while True:
					ev_key=event.waitKeys(keyList=[str(i) for i in range(1,10)])
					if ev_key[0] in [str(i) for i in range(1,10)]:
						break
				self_evaluation.append(float(ev_key[0]))
				if con=='per':
					att_withProgram.draw()
					win.flip()
					while True:
						keyProgram = event.waitKeys(keyList=[str(i) for i in range(0,10)])
						if keyProgram[0] in [str(i) for i in range(0,10)]:
							break
					att_ProgramPercent = float(keyProgram[0])
					att_ProgramPercent_t.append(att_ProgramPercent)
					win.flip()
				if block!=blknum:
					rest.draw()
					win.flip()#marker measurement
					event.waitKeys()
					win.flip()


				t_end = ck.getTime()
				print((t_end-t_start)/60, "minutes")

except Exception:
    traceback.print_exc()

finally:
	win.close()
	d_log.close()
	p.setData(0)
	try:
		d = shelve.open("exp2_data_follow_MEG/"+str(sub)+"/"+con)
		win.close()
		#ser.close()
		if execute[1]=='1':
			d['left_practice_accuracy']=practice_left
			d['right_practice_accuracy']=practice_right
			d['middle_practice_accuracy']=practice_middle
			d['left_practice_time']=time_vec_l
			d['right_practice_time']=time_vec_r
			d['middle_practice_time']=time_vec_m
		if execute[2]=='1':
			d['pre_execution_rt']=rt_pre
			d['pre_execution_accuracy']=acc_pre
			d['pre_perception_false_response']=false_response_per
			d['pre_imagery_false_response']=false_response_img
			d['post_execution_rt']=rt_test
			d['post_execution_accuracy']=acc_test
			d['pre_motor_type']=pre_motor_type
			d['repeat_or_not']=repeat
			d['irrelevant_rt']=irrelevant_rt
			d['whole_color_order']=whole_color
			d['whole_position_order']=whole_position_order
			d['whole_motor_type_order']=whole_motor_type
			d['whole_fixation_time']=whole_fix
			d['self evaluation']=self_evaluation
			if con == 'per':
				d['attend effector % with program'] = att_ProgramPercent_t
	finally:
		d.close()
