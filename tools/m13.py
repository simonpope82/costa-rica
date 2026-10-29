import json
P='seed.json';d=json.load(open(P));I=d['items']
ch={
'day2':dict(title="Car → Starbucks farm → Poás volcano → The Springs",plan="08:30 pick up the Vamos car, across the street from the Hampton (walk over). Drive to Hacienda Alsacia, 30–40 min. 09:00 Hacienda Alsacia (Starbucks) coffee tour ✅ booked: 1 h 30 tour + 30 min tasting. About 11:00 leave, drive to Poás (about 45 min–1 h). 12:40 Poás volcano entry ✅ BOOKED (2 adults, GetYourGuide, QR in the app), about 1 h at the crater. About 13:45 leave, drive to The Springs, La Fortuna (about 2 h 30–3 h). Aim to arrive before dark (~17:45)."),
'L1':dict(route="Hampton → Hacienda Alsacia → Poás volcano → The Springs",leaveBy="08:30",notes="Hampton → Hacienda Alsacia about 17 km / 30–40 min. Alsacia → Poás crater about 22 km / 45 min–1 h. Poás → The Springs about 115 km / 2 h 30–3 h (mountain roads, slow). Leave Poás by about 13:45, arrive before dark (~17:45)."),
't_poas':dict(when="Thu 29 Oct 12:40 entry (after the coffee tour)",status="Booked",price="Paid via GetYourGuide (2 adults) + parking about ₡2,000",notes="Booked via GetYourGuide, 12:40, 2 adults, QR in GetYourGuide app. About 1 h at the crater. Code: see Tickets."),
'todo_t_poas':dict(name="Poás volcano tickets, Thu 29 Oct 12:40",done=True,status="Booked",notes="Booked via GetYourGuide, 12:40, 2 adults, QR in GetYourGuide app"),
}
patch={}
for k,v in ch.items(): I[k].update(v);patch[k]=v
d['mig'].append({'id':'m13-poas-booked','patch':patch})
json.dump(d,open(P,'w'),ensure_ascii=False,indent=0)
