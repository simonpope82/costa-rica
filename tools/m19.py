import json
d=json.load(open('seed.json'));I=d['items']
P={}
def full(k,v):
    v.setdefault('id',k);I[k]=v;P[k]={'full':True}
def upd(k,**kw):
    I[k].update(kw);P[k]={'full':True}
def dele(k):
    I[k]['del']=True;P[k]={'del':True}
def day(k,title,plan,place=None):
    upd(k,title=title,plan=plan)
    if place: I[k]['wx']['place']=place
# past
upd('st_jaco',status='Booked',price='NOK 1,198.45 (paid, Airbnb)',address='Av. Pastor Díaz, Jacó 61101',checkin='Mon 2 Nov, after 14:00',checkout='Tue 3 Nov, by 11:00',lat=9.620140877179761,lng=-84.63444504886866,
    notes='1 night, 2 adults. Host: Jesse. Confirmed + paid on Airbnb. Code: see Airbnb app. Listing: https://www.airbnb.co.uk/rooms/1558712813699243233  Map: https://maps.google.com/maps?daddr=9.620140877179761,-84.63444504886866')
o=max(x.get('o',0) for x in I.values())
full('st_quepos',{'type':'stay','name':'Airbnb: Penthouse 2 Bed Huge Ocean View in Manuel Antonio','area':'Quepos / Manuel Antonio','address':'Ruta 618, Pacifico Colonial, Quepos 60601','checkin':'Tue 3 Nov, after 15:00','checkout':'Thu 5 Nov, by 11:00','price':'NOK 4,185.38 (paid, Airbnb)','fromDay':7,'toDay':8,'status':'Booked','notes':'2 nights, 2 adults. Host: John. Keys via Dani on WhatsApp +506 6270 9343. Code: see Airbnb app.','phone':'+506 6270 9343','backupOf':'','ref':'','lat':9.4085003,'lng':-84.1582085,'link':'https://www.airbnb.co.uk/rooms/1308755228995569676','gpsAsked':True,'parkingAsked':False,'o':19.5,'u':1})
full('sp_jaco',{'type':'spend','date':'2026-11-02','what':'Airbnb Jacó condo, 1 night (2–3 Nov), paid','amount':1198.45,'cur':'NOK','who':'Simon','cat':'hotel','o':o+1,'u':1})
full('sp_quepos',{'type':'spend','date':'2026-11-03','what':'Airbnb Manuel Antonio penthouse, Quepos, 2 nights (3–5 Nov), paid','amount':4185.38,'cur':'NOK','who':'Simon','cat':'hotel','o':o+2,'u':1})
day('day6',I['day6']['title'],"10:00–12:00 Bread-making workshop at Finca El Paraiso ✅ BOOKED. Check out of Cala Lodge by 11:30. Then drive Monteverde → Jacó. Night: Airbnb Ocean View Condo, Jacó ✅ BOOKED (paid).",'Jacó')
day('day7','Jacó → Quepos (Manuel Antonio)',"Check out of the Jacó condo by 11:00. Drive Jacó → Quepos (about 1 h 15). Night: Airbnb Penthouse, Manuel Antonio ✅ BOOKED (check-in after 15:00).",'Quepos')
day('day8','Manuel Antonio','Manuel Antonio day. Night: Airbnb Penthouse, Quepos ✅ BOOKED.','Quepos')
# future
day('day9','Quepos → Puerto Viejo (Caribbean)',"Check out of the penthouse by 11:00. Long drive across the country: Quepos → San José → Ruta 32 → Limón → Puerto Viejo, about 360 km, 6 h 30–7 h. Fog + landslides possible on Braulio Carrillo. Dark at 17:30: drive slowly. Night: Puerto Viejo 🟡 NOT BOOKED.",'Puerto Viejo')
day('day10','Puerto Viejo','Beach day. Punta Cocles beach is 5 min away. Night: Puerto Viejo 🟡 NOT BOOKED.','Puerto Viejo')
day('day11','Puerto Viejo','Beach or Cahuita National Park (20 min, open 8–16, pay at the gate). Night: Puerto Viejo 🟡 NOT BOOKED.','Puerto Viejo')
day('day12','Puerto Viejo','Free day. Idea: Ride The Rainforest horse ride at Punta Cocles (not booked). Night: Puerto Viejo 🟡 NOT BOOKED.','Puerto Viejo')
day('day13','Puerto Viejo → Tortuguero (car + boat)',"Check out. Drive Puerto Viejo → Limón → Guápiles → La Pavona, about 3 h 30. Park the car (secure lot). Boat about 1 h (about 12:45 or 15:15, check times). Night: Tortuguero 🟡 NOT BOOKED.",'Tortuguero')
day('day14','Tortuguero → near San José',"Early canal tour if you want. Boat back to La Pavona (about 06:40 or 08:40, check times). Drive La Pavona → near SJO, about 3 h. Ruta 32: fog + landslides possible. Night: near SJO 🟡 NOT BOOKED.",'SJO / Alajuela')
day('day15','Fly home','Slow morning, pack. Fill up. Return the Vamos car at SJO by about 16:30. Fly KL 760 at 19:30.')
upd('st_pvj',name='Not chosen',area='Puerto Viejo de Talamanca (incl. Punta Cocles)',fromDay=9,toDay=12,status='Not booked',checkin='Thu 5 Nov',checkout='Mon 9 Nov',notes='4 nights, 5–9 Nov.',lat=9.65638,lng=-82.75382)
upd('st_tor',name='Not chosen',area='Tortuguero village',fromDay=13,toDay=13,status='Not booked',checkin='Mon 9 Nov',checkout='Tue 10 Nov',notes='1 night. Idea: Hotel Serendipity. No road: car stays at La Pavona, boat about 1 h.')
upd('st_sjo2',fromDay=14,toDay=14,status='Not booked',checkin='Tue 10 Nov',checkout='Wed 11 Nov',notes='Last night, near the airport. Car back by about 16:30 on 11 Nov.')
upd('todo_st_pvj',name='Hotel 5–9 Nov (4 nights): Puerto Viejo',status='Not booked')
upd('todo_st_tor',name='Hotel 9 Nov (1 night): Tortuguero',status='Not booked')
upd('todo_st_sjo2',name='Hotel 10 Nov (1 night): near SJO',status='Not booked')
upd('t_tortboat',day=13,when='Mon 9 Nov (about 12:45 or 15:15) · back Tue 10 Nov (06:40/08:40)')
upd('todo_t_tortboat',name='Tortuguero: La Pavona parking + boats, 9 Nov / 10 Nov')
upd('t_ride',day=12,when='Sun 8 Nov (idea)',status='Idea',name='Ride The Rainforest (horse riding), Puerto Viejo / Punta Cocles')
upd('todo_t_ride',name='Ride The Rainforest, Sun 8 Nov (idea)')
upd('L3',day=9,route='Quepos → Puerto Viejo (via San José + Ruta 32 + Limón)',km=360,time='6 h 30–7 h',leaveBy='11:00',notes='Long day. Fog + landslides possible on Braulio Carrillo.')
upd('L4',day=13,route='Puerto Viejo → La Pavona (via Limón + Guápiles)',km=200,time='3 h 30',leaveBy='09:00',notes='Car stays at La Pavona secure parking. Boats about 12:45, 15:15 (check).')
upd('L5',day=14,route='La Pavona → near SJO (Ruta 32)',km=150,time='3 h',leaveBy='after the boat (~09:30)',notes='Boat back first: 06:40 or 08:40.')
upd('fuel_c7',name='Leave Quepos full (to check)',day=9,leg='L3'); upd('fuel_c8',name='Limón (to check)',day=9,leg='L3')
upd('fuel_c9',name='Limón (to check)',day=13,leg='L4'); upd('fuel_c10',name='Guápiles (to check)',day=13,leg='L4')
upd('fuel_c11',name='Guápiles (to check)',day=14,leg='L5'); upd('fuel_c12',name='Fill up before returning the car, 11 Nov',day=15,leg='L5')
for k in ['st_tam','st_fr','todo_st_tam','todo_st_fr','todo_c14','question_c19','question_c20','L6','fuel_c5','fuel_c6','place144']: dele(k)
upd('place143',status='In plan',why='Beach, 5–9 Nov')
upd('todo_c15',name='Cahuita: pay at the gate. Tortuguero park ticket (9–10 Nov): online or at the gate')
I['meta' if False else 'day1']  # noop
d['meta']['basics']='Plan changed 5 Nov: Quepos → Puerto Viejo (5–9 Nov) → Tortuguero (9–10 Nov) → near SJO (10–11 Nov) → fly 11 Nov 19:30.'
d['mig'].append({'id':'m19-caribbean-replan','patch':P})
json.dump(d,open('seed.json','w'),ensure_ascii=False,indent=0)
