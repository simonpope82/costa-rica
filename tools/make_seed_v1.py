# Builds seed.json (public, no booking refs) from the brief data.
import json,sys
items=[];o=[0]
def add(t,**f):
    o[0]+=1; f.update(type=t,id=f.get('id') or f"{t}{o[0]}",o=o[0]); items.append(f); return f
meta={"title":"Costa Rica road trip","travellers":["Simon","Stian"],"start":"2026-10-28","end":"2026-11-11",
 "tz":"Costa Rica UTC−6 · Oslo is 7 h ahead","rate":456.61,"rateNote":"456.61 CRC = 1 USD (10 Oct 2026)",
 "basics":"14 nights · about 755 km, about 23 h 30 driving over 8 days · fuel about 125 USD (about 160 USD with local trips)"}
D=[("Wed 28 Oct","Arrive","Land 17:30, car 18:30, early night"),("Thu 29 Oct","Coffee day","09:00 Hacienda Doka tour; 13:00 Rosa Blanca tour + cupping"),
("Fri 30 Oct","Drive","Drive to La Fortuna"),("Sat 31 Oct","Arenal","Volcano park, waterfall, hot springs, hanging bridges"),("Sun 1 Nov","Arenal","Free day or tour"),
("Mon 2 Nov","Drive","Around Lake Arenal via Tilarán. Last 35 km rough gravel. Leave by 09:00"),
("Tue 3 Nov","Cloud forest","Cloud forest reserve, hanging bridges, night walk. Optional Don Juan coffee + chocolate tour"),
("Wed 4 Nov","Drive","Longest drive. Lunch in Jacó"),("Thu 5 Nov","Beach and park","Manuel Antonio National Park (check open days + tickets)"),
("Fri 6 Nov","Beach","Beach, boat or catamaran trip"),("Sat 7 Nov","Drive","Short coast drive"),("Sun 8 Nov","Beach","Marino Ballena park (whale's tail), waterfalls"),
("Mon 9 Nov","Drive","Via San Isidro + Ruta 2. Leave by 09:00. Fill up in San Isidro. Cold at night"),("Tue 10 Nov","Tarrazú coffee","10:30 Coopedota tour, walk from hotel"),
("Wed 11 Nov","Fly home","Leave by 12:30 latest (aim 12:00). Fill up near airport. Car back by 16:30. Fly 19:30")]
for i,(d,t,p) in enumerate(D,1):
    add("day",id=f"day{i}",day=i,date=f"2026-{'10' if 'Oct' in d else '11'}-{int(d.split()[1]):02d}",label=d,title=t,plan=p,notes="",sunset="Dark about 17:15–17:30")
S=[("st_hampton","Hampton by Hilton San Jose Airport","Alajuela (at SJO airport)",1,1,"Booked","1 night, prepaid SEK 1,305, non-refundable. Booking site still says 'Confirming'. Alamo car rental station is at this hotel.","",None,"",None,None),
("st_rb","Finca Rosa Blanca coffee farm","Santa Bárbara de Heredia",2,2,"To book","Junior Suite from about 315 USD/night + 13% tax. Idea: 1 night here + 1 at a backup.","+506 2269 9392",None,"",None,None),
("st_pv","Pura Vida Hotel","Tuetal, Alajuela (4 km from SJO)",1,2,"Idea","99–129 USD/night + 13% tax, breakfast, free airport pickup","", "st_rb","",None,None),
("st_bv","Buena Vista Chic Hotel","Alajuela hills (9 km from SJO)",1,2,"Idea","From about 144 USD/night, breakfast + airport shuttle","","st_rb","",None,None),
("st_lf","Not chosen","La Fortuna / Arenal",3,5,"To book","","",None,"",10.4679,-84.6427),
("st_mv","Not chosen","Monteverde (Santa Elena)",6,7,"To book","","",None,"",10.3167,-84.8256),
("st_ma","Not chosen","Manuel Antonio / Quepos",8,10,"To book","","",None,"",9.43,-84.16),
("st_uv","Not chosen","Uvita / Dominical",11,12,"To book","","",None,"",9.1611,-83.7372),
("st_sm","Ideas: Hotel Valle Verde (in town) or Cedrela Eco Lodge (10 min away)","Santa María de Dota",13,14,"To book","Cold at night","",None,"",None,None)]
for sid,n,a,f,t,st,no,ph,bk,ref,la,lo in S:
    add("stay",id=sid,name=n,area=a,address=("Airport Blvd 1, Alajuela" if sid=="st_hampton" else ""),checkin=("Wed 28 Oct" if sid=="st_hampton" else ""),checkout=("Thu 29 Oct" if sid=="st_hampton" else ""),price=("SEK 1,305 (prepaid)" if sid=="st_hampton" else ""),fromDay=f,toDay=t,status=st,notes=no,phone=ph,backupOf=bk or "",ref=ref,lat=la,lng=lo,link="",gpsAsked=False,parkingAsked=False)
L=[(1,"SJO → Finca Rosa Blanca",15,"30 min","",[("Delta La Ribera",6)],"None needed."),
(2,"Rosa Blanca ↔ Hacienda Doka",35,"1 h 30","",[("Servicentro Carrizal",7)],"None needed."),
(3,"Rosa Blanca → La Fortuna",135,"3 h 30","",[("Mi Servicentro Naranjo",40),("Delta San Jorge, La Fortuna",119)],"Break at Naranjo. Fill up at Delta San Jorge. Cost about 22 USD."),
(6,"La Fortuna → Monteverde via Tilarán",110,"3 h 30","09:00",[("Servicentro Arenal",46),("Servicentro Tilarán",75)],"Leave full. Tilarán is the last before gravel. Cost about 19 USD."),
(8,"Monteverde → Manuel Antonio",185,"5 h 15","",[("JSM Monteverde",2),("Servicentro Jacó",114),("Gasolinera Paquita, Quepos",178)],"Longest drive. Cost about 31 USD."),
(11,"Quepos → Uvita",65,"1 h 45","",[("Delta Quepos",8),("Servicentro Bahía Ballena, Uvita",64)],"Cost about 11 USD."),
(13,"Uvita → San Isidro → Santa María de Dota",135,"5 h","09:00",[("Servicentro Bahía Ballena",2),("Tanok or Gasotica, San Isidro",50),("Gasolinera Santa María",135)],"Must fill in San Isidro. Gasolinera Santa María on arrival. Cost about 22 USD."),
(15,"Santa María de Dota → SJO",75,"2 h 30","12:30",[("Gas Caribe",59)],"Leave full. Fill up near SJO for car return. Cost about 13 USD.")]
for i,(d,r,km,tm,lb,fs,no) in enumerate(L,1):
    add("leg",id=f"L{i}",name=f"L{i}",day=d,route=r,km=km,time=tm,leaveBy=lb,notes=no)
    for n,k in fs: add("fuel",name=n,day=d,leg=f"L{i}",km=k,lat=None,lng=None)
for f in [("Wed 28 Oct","KL 1198","Oslo → Amsterdam","09:30","11:25"),("Wed 28 Oct","KL 759","Amsterdam → San José (SJO)","12:40","17:30"),
("Wed 11 Nov","KL 760","San José → Amsterdam","19:30","12:50 Thu 12 Nov"),("Thu 12 Nov","KL 1203","Amsterdam → Oslo","14:20","16:10")]:
    add("flight",date=f[0],name=f[1],route=f[2],leaves=f[3],lands=f[4],status="Booked")
add("car",id="car",name="Rental car: Full Size SUV 4x4",company="Vamos Rent-A-Car",ref="",status="Booked",pickup="San José International Airport (SJO), Thu 29 Oct 2026, 12:00",ret="SJO, Thu 12 Nov 2026, 12:00",warn="⚠️ Change return to Wed 11 Nov ~16:30 (flight leaves Wed 11 Nov 19:30)",
 days="14 days (as booked)",car="Full Size SUV 4x4, 2500cc, automatic, petrol. Check 4 big bags fit.",
 insurance="SLI/TPL is required; a credit card can't replace it. Ask for an all-in price with SLI. CDW can sometimes be skipped with a card letter.",
 watch="Returning after 18:30 can cost an extra day. Check grace period. Ask about Quick Pass for tolls. Add Stian as driver?",
 licence="Norwegian licence OK, no international permit. Carry passport.",price="$1,211.18 total",deposit="",phone="",lat=9.9939,lng=-84.2088,area="SJO airport (Juan Santamaría)")
add("info",name="Fuel prices",text="From 3 Oct 2026: Súper 764 CRC/L, Plus 91 719 CRC/L, Diesel 785 CRC/L, same at every station. One tank covers any single drive.")
add("info",name="Tolls",text="Small, on Ruta 27 (e.g. Pozón 570 CRC, Atenas 750 CRC): card, cash or Quick Pass.")
T=[("Hacienda Doka, Sabanilla de Alajuela",2,"09:00","1 h","28 USD (43 with lunch)","To book","Top pick. Old working wet mill + roaster. Mon–Fri 08:00–15:30, Sat–Sun 08:00–14:30. 17 km from Rosa Blanca"),
("Finca Rosa Blanca tour + cupping",2,"13:00","2.5 h","40 USD per person","To book","Organic, own mill. Min 2, max 6. Book ahead: +506 2269 9392"),
("Coopedota, Santa María de Dota",14,"10:30","2 h","10,000–12,500 CRC (22–27 USD)","To book","Co-op from 1960. Tue–Sun 08:30, 10:30, 13:30, 15:30"),
("Starbucks Hacienda Alsacia (next to Doka)",None,"Option","90 min","about 35 USD","Question","Swap for Doka? Polished, corporate"),
("Don Juan Tours, Monteverde",7,"Option, 3 Nov","2 h","45 USD","Idea","Coffee + chocolate + sugar cane")]
for n,d,w,l,p,s,no in T: add("tour",name=n,day=d,when=w,length=l,price=p,status=s,notes=no,lat=None,lng=None,link="")
add("info",name="Coffee: skip",text="Skip: Café Britt (a show, not a working farm) and Hacienda Espíritu Santo (closed since 30 May 2025). Ask farms whether the mill runs in late Oct / early Nov.")
add("info",name="Option: 1 night in Colombia",status="Idea",text="Idea, not decided. Fly Thu 29 Oct SJO → Bogotá or Medellín, back Fri 30 Oct. Costs about 2 road-trip nights. No visa for Norwegians. Yellow fever jab needed to re-enter Costa Rica, at least 10 days before: both need it by about 20 Oct.")
for k,v in [("Entry","No visa for Norwegians, up to 180 days. May be asked for a return ticket (we have one) and about 100 USD per person per month."),
("Driving","Drive on the right. Limits: 40 km/h towns, 60–80 rural, 100 max. Speed cameras, big fines. No driving after dark (dark about 17:30); arrive by 16:30–17:00. Never drive into water you can't see the bottom of. One-lane bridge: the side with the CEDA sign waits. Right on red only if clear and no sign. Seatbelts on."),
("La Fortuna → Monteverde","Last 35 km after Tilarán is gravel, potholes, steep. Slow, 4x4, daylight only."),
("Weather","End of rainy season. October is the wettest; drier in November. Sunny mornings, rainy afternoons. Caribbean side is dry Sep–Oct, wet in Nov (backup if the Pacific is bad)."),
("Money","Colones (CRC). US dollars OK in tourist areas. Cards work almost everywhere."),("Day 1","Land in the dark; night 1 is only 30 min away."),
("Waze","Download Waze offline areas or Google Maps offline maps before the trip.")]:
    add("good",name=k,text=v)
B=[("Flights, ref on Flights screen",True,"Booked"),("4x4 SUV: 28 Oct 18:30 → 11 Nov 16:30, with SLI, grace period, Quick Pass, Stian as driver, 4 bags fit",False,"To book"),
("Credit card coverage letter (only to skip CDW)",False,"To book"),("Hotel 28–29 Oct (2 nights): Finca Rosa Blanca, or 1 night + backup",False,"To book"),
("Hotel 30 Oct – 1 Nov (3 nights): La Fortuna",False,"To book"),("Hotel 2–3 Nov (2 nights): Monteverde",False,"To book"),("Hotel 4–6 Nov (3 nights): Manuel Antonio",False,"To book"),
("Hotel 7–8 Nov (2 nights): Uvita",False,"To book"),("Hotel 9–10 Nov (2 nights): Santa María de Dota",False,"To book"),("Hacienda Doka tour, Thu 29 Oct 09:00",False,"To book"),
("Rosa Blanca tour + cupping, Thu 29 Oct 13:00 (min 2 people)",False,"To book"),("Coopedota tour, Tue 10 Nov 10:30",False,"To book"),
("Park tickets on SINAC online: Manuel Antonio, Arenal, Poás, Marino Ballena",False,"To book"),("Travel insurance for both",False,"To book"),
("Yellow fever jab by about 20 Oct (only if doing Colombia, both)",False,"Question"),("Waze + offline maps downloaded",False,"To book"),("Local SIM or eSIM",False,"To book"),
("Some colones + card for tolls",False,"To book"),("Ask each hotel for GPS location and safe parking",False,"To book"),("Check in online for KL 760 (24 h before)",False,"To book"),
("Check for an online arrival form for Costa Rica",False,"To book")]
for n,d,s in B:
    if n.startswith("4x4 SUV"): add("todo",id="todo_car",name=n,done=True,status="Booked",ref="",price="$1,211.18",notes="Vamos, booked. ⚠️ Return date is wrong (12 Nov 12:00): change to Wed 11 Nov ~16:30.")
    else: add("todo",name=n,done=d,status=s,ref="",price="",notes="")
P={"Documents and money":["Passport (6+ months left is safest)","Norwegian driving licence (both, if Stian drives)","Credit card in the driver's name (for the car deposit)","Debit card + backup card","Some US dollars in cash","Card coverage letter (if skipping CDW)","Travel insurance details","E-ticket and booking refs (also offline on phone)","Copies of passport and licence (photo on phone + paper)","Yellow fever certificate (only if Colombia)"],
"Tech":["Phone + charger","Power bank","Plug adapter for Costa Rica (US-type plugs, 120 V: check chargers say 100–240 V)","Car phone holder","Car USB charger + cable","Headphones","Head torch (night walk in Monteverde)"],
"Clothes":["Rain jacket (October is the wettest month)","Warm layer / fleece (Monteverde and Dota are cold at night)","Long trousers (hiking, mosquitoes)","Light quick-dry shirts and shorts","Swimwear","Walking shoes or light hiking boots (mud)","Sandals / flip-flops","Cap or sun hat","Clothes for a nice dinner"],
"Health and comfort":["Personal medicines (enough for the whole trip)","Insect repellent (strong, DEET)","Sunscreen (reef-safe for the beaches)","Sunglasses","Small first aid kit + plasters","Travel sickness tablets (lots of curvy roads)","Stomach tablets","Hand sanitiser"],
"Day trips":["Small daypack","Dry bag (rafting, boat trips, rain)","Water bottle","Binoculars (birds, sloths, whales)","Snorkel mask (optional)","Quick-dry towel"]}
for g,a in P.items():
    for n in a: add("pack",group=g,name=n,ticks={"Simon":False,"Stian":False})
for q in ["29 Oct: Doka + Rosa Blanca cupping, or Alsacia instead of Doka?","Last night: Santa María de Dota (2 h 30 to SJO) or closer to the airport?","Budget per night? One room or two?","Add Stian as a driver?","Must-dos: zip-line, rafting, hot springs, whales, fishing, surfing?","Caribbean detour (Puerto Viejo / Cahuita) if bad weather?","Keep Coopedota in the plan?","Do the 1 night in Colombia?","Will the coffee mills be running in late Oct / early Nov?"]:
    add("question",name=q,done=False,answer="")
PL=[("Papagayo Peninsula","Hotels and food (pricey but nice)","Idea","food"),("San José","Culture and nightlife","Idea","nightlife"),("Nosara","Yoga and spa","Idea","activity"),
("Jacó","For variety (lunch stop on 4 Nov)","In plan","food"),("Monteverde","Cloud forest, coffee a must","In plan","nature"),("Puerto Viejo de Talamanca","Beach and activities","Idea","beach"),
("Tamarindo","Best for surfing","Idea","beach"),("Drake Bay","Only reachable by boat or plane","Idea","nature"),("La Fortuna","Volcano scenery","In plan","nature"),
("Playa Conchal","Snorkelling and scuba","Idea","beach"),("Pacuare River","White water rafting, kayak","Idea","activity"),('"Tico beach" (local favourite)',"Name to check","Question","beach")]
gps={"Monteverde":(10.3167,-84.8256),"La Fortuna":(10.4679,-84.6427)}
for n,w,s,k in PL:
    la,lo=gps.get(n,(None,None)); add("place",name=n,why=w,status=s,kind=k,area="",lat=la,lng=lo,link="",day=None)
# Restaurants (bot web research 13 Oct 2026, not from the brief) for the brief's sleep areas
F=[("st_lf","Don Rufino","https://donrufino.com/","Costa Rican, smart dinner. Book."),("st_lf","Soda La Hormiga","","Cheap local food"),("st_lf","Arenal Puesta del Sol","https://www.arenalpuestadelsol.com/","Volcano view. Book."),
("st_mv","Taco Taco","","Mexican, busy, fun"),("st_mv","Don Luis","https://donluiscr.com/","Steak + pizza"),("st_mv","The Green Restaurant","","Healthy, good steaks"),
("st_ma","Claro Que Sí","","Seafood (Hotel Si Como No)"),("st_ma","Ronny's Place","","Sunset view"),("st_ma","ARBOL","https://arbolrestaurant.com/","Smart dinner, adults only"),("st_ma","Soda Sánchez (Quepos)","","Cheap local food"),
("st_uv","Mestizo","","Peru/Japan, ceviche"),("st_uv","Al Chile Que Sí","","Sunset view, cocktails"),("st_uv","Kinsu","","Casado, cheap"),
("st_sm","Café Coopedota","https://www.coopedota.com/","Coffee + local food"),("st_sm","Pizzería Las Tejas","","Pizza"),("st_sm","Restaurante y Pesca La Teja","","Trout")]
town={"st_lf":"La Fortuna","st_mv":"Santa Elena Monteverde","st_ma":"Manuel Antonio","st_uv":"Uvita","st_sm":"Santa María de Dota"}
for s,n,u,no in F: add("food",stay=s,name=n,link=u,notes=no,area=town[s],lat=None,lng=None)
add("spend",id="sp_hampton",date="2026-10-13",what="Hampton by Hilton SJO, night 1",amount=1305,cur="SEK",who="Simon",cat="hotel")
add("spend",id="sp_car",date="2026-10-13",what="Vamos car rental, 14 days (paid by Simon, assumed)",amount=1211.18,cur="USD",who="Simon",cat="car")
NEW={"st_hampton","st_rb","sp_hampton"}
NEW2={"car","todo_car","sp_car"}
# Colombia removed (Simon, 13 Oct)
items[:]=[i for i in items if "Colombia" not in json.dumps(i,ensure_ascii=False)]
DEL=set()
for it in items: it["u"]=1791900000000 if it["id"] in DEL else 1791000000000 if it["id"] in NEW2 else (1760352000000 if it["id"] in NEW else 1)
# Keep ids stable with the first published seed (tools/seed-v1.json), so phones don't get duplicates
import os
here=os.path.dirname(os.path.abspath(__file__))
v1=json.load(open(os.path.join(here,"seed-v1.json")))["items"]
key=lambda i:(i["type"],i.get("name"),i.get("group"),i.get("day"),i.get("label"),i.get("area"),i.get("leg"),i.get("stay"))
oldmap={key(i):i for i in v1.values()}
oldmap_name={(i["type"],i.get("name")):i for i in v1.values()}
seen=set()
for it in items:
    if it.get("del"): continue
    o=oldmap.get(key(it)) or (oldmap_name.get(("todo",v1[next(k for k,v in v1.items() if v["type"]=="todo" and v["name"].startswith("4x4 SUV"))]["name"])) if it["id"]=="todo_car" else None) or oldmap_name.get((it["type"],it.get("name")))
    if o and o["id"] not in seen and it["id"] not in ("st_hampton","sp_hampton","sp_car"):
        it["id"]=o["id"]; it["o"]=o["o"]; seen.add(o["id"])
# tombstone ids from v1 that are gone, and ids that only existed in the 13 Oct seeds (372d481, cd4f07a)
cur={i["id"] for i in items}
gone=[k for k in v1 if k not in cur]
for f in ("seed-372d481.json","seed-cd4f07a.json"):
    p=os.path.join(here,f)
    if os.path.exists(p):
        for k in json.load(open(p))["items"]:
            if k not in cur and k not in gone: gone.append(k)
for k in gone:
    items.append({"id":k,"type":(v1.get(k) or {}).get("type","x"),"o":0,"del":True,"u":1791900000000})
for it in items:
    if it["id"] in ("info60","todo82","pack98","question136"): it["u"]=1791900000000
# ids reused with other content in the 13 Oct seeds: force the right content
for f in ("seed-372d481.json","seed-cd4f07a.json"):
    p=os.path.join(here,f)
    if os.path.exists(p):
        old=json.load(open(p))["items"]
        for it in items:
            o=old.get(it["id"])
            if o and not it.get("del") and o.get("name")!=it.get("name") or (o and o.get("type")!=it.get("type")): it["u"]=max(it.get("u",1),1791900000000)
json.dump({"v":1,"meta":meta,"items":{i["id"]:i for i in items}},open(sys.argv[1],"w"),ensure_ascii=False,indent=0)
print(len(items))
