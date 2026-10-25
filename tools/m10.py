import json
P='seed.json';d=json.load(open(P));I=d['items'];mx=max(x.get('o',0) for x in I.values())
def o():
    global mx; mx+=1; return mx
patch={}
def upd(k,**f): I[k].update(f); patch[k]=dict(f)
def new(k,**f): f.update(id=k,o=o(),u=1); I[k]=f; patch[k]={'auto':True}
day1="Tue 27 Oct: train from Ås to Gardermoen (R20/R21 → Oslo S, then Flytoget or regional train; times: check Entur). Sleep at Comfort Hotel Runway ✅. Wed 28 Oct: walk or shuttle to the terminal, be there about 07:30. Fly 09:30. Land 17:30. Taxi to the Hampton (at the airport). No car today. Early night. To do: ask Vamos (next door) for the car at ~08:00?"
upd('day1',plan=day1)
day2="08:30 pick up the car at the Vamos office, across the street from the Hampton (walk over). Drive to Alsacia 30–40 min (Simon asks Vamos on 28 Oct for ~08:00). 09:00–10:30 Hacienda Alsacia (Starbucks) coffee tour ✅ booked. 10:30 drive to Poás (about 45 min). About 11:30 Poás crater, about 1 h (tickets NOT booked yet, last entry 14:00). About 12:30 leave, drive to The Springs (about 3 h 15), arrive about 16:00, before dark."
upd('day2',title="Car → Starbucks farm → Poás volcano → The Springs",plan=day2)
upd('L1',route="Hampton → Hacienda Alsacia → Poás volcano → The Springs",km=155,time="4 h 45",leaveBy="08:30",
 notes="Hampton → Hacienda Alsacia about 17 km / 30–40 min. Alsacia → Poás crater about 22 km / 45 min. Poás → The Springs about 115 km / 3 h 15 (mountain roads, slow). Leave Poás by about 12:30.")
upd('t_alsacia',when="Thu 29 Oct 09:00–10:30",length="1 h 30",price="Paid USD 73.72 (NOK 714.98) for 2",status="Booked",
 notes="✅ Booked, 2 adults. Dulce Nombre, San Isidro, Alajuela. Waze: HACIENDA ALSACIA VISITOR CENTER. Runs rain or shine, no refund. 30–40 min from the Hampton.")
upd('t_poas',when="Thu 29 Oct ~11:00–11:30 (after the coffee tour)",price="US$15 pp + parking about ₡2,000",
 notes="Tickets ONLY on the official SINAC site (fake sites exist). Site was down on 25 Oct: try again. Fixed slot, no refunds. Last entry 14:00. https://serviciosenlinea.sinac.go.cr/")
upd('todo_t_poas',name="Poás volcano tickets (SINAC only), Thu 29 Oct ~11:00–11:30 slot")
upd('todo_t_alsacia',name="Hacienda Alsacia coffee tour, Thu 29 Oct 09:00 ✅",done=True,status="Booked",price="USD 73.72")
new('st_gar',type='stay',name="Comfort Hotel Runway",area="Oslo Airport Gardermoen",address="Hans Gaarders veg 27, 2060 Gardermoen",
 checkin="Tue 27 Oct (from 15:00)",checkout="Wed 28 Oct (by 11:00)",price="NOK 1,529 (pay at the hotel)",fromDay=0,toDay=0,status="Booked",
 notes="1 night before the flight, 2 adults, member price. No breakfast. Free cancellation until 16:00 on 27 Oct. Walk or shuttle to the terminal, be there about 07:30 on 28 Oct.",
 phone="+47 63 94 88 88",backupOf="",ref="",lat=None,lng=None,link="",gpsAsked=False,parkingAsked=False)
new('todo_st_gar',type='todo',name="Hotel 27 Oct (1 night): Comfort Hotel Runway, Gardermoen ✅",done=True,status="Booked",link="st_gar",ref="",price="NOK 1,529",notes="Pay at the hotel.")
new('good_train',type='good',name="Tue 27 Oct: train to the airport",text="Ås → Oslo S: R20 or R21 (about 30 min). Oslo S → Gardermoen: Flytoget (about 20 min) or Vy regional train (cheaper). Times: check Entur app. Hotel check-in from 15:00.")
new('todo_vamos_early',type='todo',name="Wed 28 Oct evening: ask Vamos: car at ~08:00?",done=False,status="To book",link="car",ref="",price="",notes="Office next door to the Hampton. Coffee tour starts 09:00.")
new('sp_gar',type='spend',date="2026-10-27",what="Comfort Hotel Runway, Gardermoen (pay at hotel)",amount=1529,cur="NOK",who="Simon",cat="hotel")
new('sp_alsacia',type='spend',date="2026-10-25",what="Hacienda Alsacia coffee tour, 2 people",amount=714.98,cur="NOK",who="Simon",cat="tour")
d['mig'].append({'id':'m10-gardermoen-alsacia','patch':patch})
json.dump(d,open(P,'w'),ensure_ascii=False,indent=0)
