import json
P='seed.json';d=json.load(open(P));I=d['items'];mx=max(x.get('o',0) for x in I.values())
B=(10.7322,-85.0596)
ch={
'day3':dict(title="Free day at The Springs",plan="Rest day. Pools + hot springs at The Springs. (The big tour is now Sat 31 Oct.) No driving."),
'day4':dict(title="Big tour → drive to Río Celeste",plan="Early check-out, bags in the car. 07:00 Red Lava tour: hanging bridges, lava walk, lunch, La Fortuna waterfall, hot springs. Back about 17:30. Then drive La Fortuna → Bijagua (Río Celeste): 97 km, about 1 h 45. Dark from 17:30: drive slowly. Night near Río Celeste: TO BOOK.",wx=dict(I['day4']['wx'],place="La Fortuna → Bijagua")),
'day5':dict(title="Río Celeste waterfall → Tamarindo?",plan="Go early to Tenorio park (Río Celeste waterfall, about 3 h walk, 250 steps). Then drive Bijagua → Tamarindo: 151 km, about 3 h. Night 1 Nov: TO DECIDE (Tamarindo, or a 2nd night at Río Celeste).",wx=dict(I['day5']['wx'],place="Bijagua / Río Celeste")),
'day6':dict(title="Tamarindo",plan="Beach. (If you stayed a 2nd night at Río Celeste: leave 08:00, drive 3 h to Tamarindo.)"),
't_volc':dict(name="Red Lava full day: hanging bridges, Arenal lava walk, La Fortuna waterfall, hot springs",day=4,when="Sat 31 Oct, 07:00 – about 17:30",length="11 h",price="USD 307.38 for 2 (paid)",status="Booked",notes="Meet: Red Lava office, La Fortuna bus terminal (or ask them for pickup at The Springs). Lunch + hot springs + 1 drink included. Free cancel until 24 h before. Code: see Tickets. Tel +506 2479-8004 / +506 8868-5500. https://redlavatours.com/tour/full-day-hanging-bridges-arenal-volcano-la-fortuna-waterfall-and-hotsprings/"),
't_rc':dict(day=5,when="Sun 1 Nov, morning",status="In plan",length="About 3 h walk, self-drive",notes="250 steps down. From Bijagua about 25 min to the park. Park ticket about 12 USD pp (buy on SINAC)."),
't_dja':dict(status="Idea",notes="Dropped for now: you leave La Fortuna on 31 Oct."),
'st_lf2':dict(name="Not chosen (near Río Celeste)",area="Río Celeste / Bijagua",checkin="Sat 31 Oct",checkout="Sun 1 Nov",fromDay=4,toDay=4,status="To book",notes="1 night, 2 beds. Arrive about 19:30 after the tour. Ideas: Celeste Mountain Lodge (~USD 130–150), Tenorio Lodge (2 queen beds, ~USD 195–225 with breakfast), Hideaway Rio Celeste (luxury, ~USD 420 for 2 queens).",lat=B[0],lng=B[1]),
'todo_st_lf2':dict(name="Hotel 31 Oct (1 night): near Río Celeste (Bijagua), 2 beds"),
'question_c18':dict(answer="Yes: after the tour on 31 Oct, sleep near Río Celeste. Waterfall on 1 Nov.",done=True),
'L2':dict(day=5,route="Bijagua (Río Celeste) → Tamarindo",km=151,time="3 h",leaveBy="after the waterfall (~13:00)",notes=""),
'fuel_c3':dict(name="La Fortuna (leave full on 31 Oct)",day=4,leg="L1b"),
}
patch={}
for k,v in ch.items(): I[k].update(v);patch[k]=v
if 'todo_t_dja' in I: del I['todo_t_dja'];patch['todo_t_dja']={'del':True}
mx+=1;I['L1b']=dict(id='L1b',name='L1b',day=4,route='La Fortuna → Bijagua (Río Celeste)',km=97,time='1 h 45',leaveBy='after the tour (~17:30)',notes='In the dark. Slow, watch for potholes.',type='leg',o=I['L2']['o']-0.5,u=1);patch['L1b']={'auto':True}
mx+=1;I['question_nov1']=dict(id='question_nov1',name="Night of 1 Nov: Tamarindo (then 3 nights there), or a 2nd night at Río Celeste?",done=False,answer="",type='question',o=mx,u=1);patch['question_nov1']={'auto':True}
mx+=1;I['todo_t_rl']=dict(id='todo_t_rl',name="Red Lava full-day tour, Sat 31 Oct 07:00",done=True,status="Booked",link="t_volc",ref="",price="USD 307.38",notes="",type='todo',o=mx,u=1);patch['todo_t_rl']={'auto':True}
d['mig'].append({'id':'m12-redlava-rioceleste','patch':patch})
json.dump(d,open(P,'w'),ensure_ascii=False,indent=0)
