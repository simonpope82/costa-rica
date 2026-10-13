# Builds seed.json (public, no booking refs) from the brief data.
import json,sys,os
items=[];o=[0]
def add(t,**f):
    o[0]+=1; f.update(type=t,id=f.get('id') or f"{t}{o[0]}",o=o[0]); items.append(f); return f
meta={"title":"Costa Rica road trip","travellers":["Simon","Stian"],"start":"2026-10-28","end":"2026-11-11",
 "tz":"Costa Rica UTC−6 · Oslo is 7 h ahead","rate":456.61,"rateNote":"456.61 CRC = 1 USD (10 Oct 2026)",
 "basics":"Route: draft C (approved 13 Oct). 14 nights · about 1,040 km, about 30 h driving over 7 days · fuel: to check"}
WX=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"wx.json")))
RT=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","route.json")))
fmt=lambda m:(f"{m//60} h {m%60:02d}" if m%60 else f"{m//60} h")
D=[("Wed 28 Oct","Arrive · taxi","Land 17:30. Taxi to the Hampton (at the airport). No car today. Early night."),
("Thu 29 Oct","Car → Monteverde","12:00 pick up the car (Vamos, SJO). Drive to Monteverde, arrive about 16:00. Last part is rough. Fill up before."),
("Fri 30 Oct","Cloud forest + Don Juan","07:30 cloud forest reserve or hanging bridges. Don Juan coffee + chocolate tour (the original, in Monteverde). No driving."),
("Sat 31 Oct","To La Fortuna","Leave about 09:00 via Tilarán (gravel first). Afternoon: hotel hot springs."),
("Sun 1 Nov","Arenal volcano","Volcano park walk or hanging bridges. No driving."),
("Mon 2 Nov","Tabacón","Tabacón Thermal Resort & Spa. Morning: La Fortuna waterfall."),
("Tue 3 Nov","Break drive","Leave about 10:00. Splits the long drive to the Pacific."),
("Wed 4 Nov","To Manuel Antonio","Leave about 09:00. Afternoon: beach."),
("Thu 5 Nov","National park","07:00 Manuel Antonio National Park (open Wed–Mon 7–15, closed Tue; SINAC tickets). No driving."),
("Fri 6 Nov","To the coffee mountains","Leave about 10:00. Slow mountain road. Cold at night."),
("Sat 7 Nov","Coopedota","10:30 Coopedota tour, walk from the hotel. No driving."),
("Sun 8 Nov","To the Caribbean","Long day: leave 07:00. Via Cartago + Ruta 32. Check Waze for closures."),
("Mon 9 Nov","Cahuita","Cahuita National Park (open every day 8–16; about 20 min drive). Beach + activities."),
("Tue 10 Nov","Back to SJO","Long day: leave 07:30. Ruta 32 over Braulio Carrillo. Fog + landslides possible."),
("Wed 11 Nov","Fly home","Slow morning, pack. Fill up. Car back at SJO (return change asked: 17:00). Fly 19:30.")]
for i,(d,t,p) in enumerate(D,1):
    w=WX[str(i)]
    add("day",id=f"day{i}",day=i,date=f"2026-{'10' if 'Oct' in d else '11'}-{int(d.split()[1]):02d}",label=d,title=t,plan=p,notes="",sunset="Dark about 17:15–17:30",
        wx={"kind":w["kind"],"place":w["place"],"tmax":w["tmax"],"tmin":w["tmin"],"mm":w["mm"],"pop":w["pop"]})
G={"SJO":(9.9939,-84.2088),"MV":(10.31651,-84.82434),"LF":(10.47168,-84.64444),"AT":(9.97949,-84.39903),"MA":(9.40857,-84.15476),"SM":(9.65346,-83.96871),"PV":(9.64965,-82.77509)}
S=[("st_hampton","Hampton by Hilton San Jose Airport","Alajuela (at SJO airport)",1,1,"Booked","1 night (Wed 28 Oct only), prepaid SEK 1,305, non-refundable. Booking site still says 'Confirming'. Alamo car rental station is at this hotel. GPS = airport (approx).","",None,"SJO"),
("st_mv","Not chosen","Monteverde (Santa Elena)",2,3,"To book","","",None,"MV"),
("st_lf","Not chosen (hotel with hot springs)","La Fortuna / Arenal",4,6,"To book","Want: hotel with hot springs. Tabacón itself is an option.","",None,"LF"),
("st_at","Not chosen","Atenas",7,7,"To book","Break night.","",None,"AT"),
("st_ma","Not chosen","Manuel Antonio / Quepos",8,9,"To book","","",None,"MA"),
("st_sm","Ideas: Hotel Valle Verde (in town) or Cedrela Eco Lodge (10 min away)","Santa María de Dota",10,11,"To book","Cold at night","",None,"SM"),
("st_pvj","Not chosen","Puerto Viejo de Talamanca",12,13,"To book","","",None,"PV"),
("st_sjo2","Not chosen","Near SJO (Tuetal / Alajuela hills / Belén)",14,14,"To book","Last night, near the airport.","",None,"SJO"),
("st_pv","Pura Vida Hotel","Tuetal, Alajuela (4 km from SJO)",14,14,"Idea","99–129 USD/night + 13% tax (1 Sep–15 Nov), breakfast, free airport pickup for arrivals","+506 2430 2929","st_sjo2",None),
("st_bv","Buena Vista Chic Hotel","Alajuela hills (9 km from SJO)",14,14,"Idea","From about 144 USD/night, breakfast + airport shuttle","","st_sjo2",None),
("st_rb","Finca Rosa Blanca coffee farm","Santa Bárbara de Heredia",14,14,"Idea","Junior Suite from about 315 USD/night + 13% tax.","+506 2269 9392","st_sjo2",None)]
for sid,n,a,f,t,st,no,ph,bk,g in S:
    la,lo=(G[g] if g else (None,None))
    if sid=="st_rb": la,lo=10.04566,-84.15062
    add("stay",id=sid,name=n,area=a,address=("Airport Blvd 1, Alajuela" if sid=="st_hampton" else ""),checkin=("Wed 28 Oct" if sid=="st_hampton" else ""),checkout=("Thu 29 Oct" if sid=="st_hampton" else ""),price=("SEK 1,305 (prepaid)" if sid=="st_hampton" else ""),fromDay=f,toDay=t,status=st,notes=no,phone=ph,backupOf=bk or "",ref="",lat=la,lng=lo,link="",gpsAsked=False,parkingAsked=False)
L=[(2,"L1","SJO → Monteverde","12:00",[("Servicentro El Roble (to check)",None),("JSM Monteverde (on arrival)",None)],"Fill up before the rough last part."),
(4,"L2","Monteverde → La Fortuna via Tilarán","09:00",[("JSM Monteverde (leave full)",None),("Servicentro Tilarán",None),("Servicentro Arenal",None),("Delta San Jorge, La Fortuna",None)],"Gravel first part. Daylight only."),
(7,"L3","La Fortuna → Atenas","10:00",[("Gasolinera La Fortuna (leave full)",None),("Stop on the way: to check",None)],""),
(8,"L4","Atenas → Manuel Antonio","09:00",[("Servicentro Jacó",None),("Gasolinera Parrita",None),("Gasolinera Paquita, Quepos",None)],""),
(10,"L5","Manuel Antonio → Santa María de Dota","10:00",[("Fill up in Quepos (to check)",None),("Gasolinera Santa María (on arrival)",None)],"Slow mountain road."),
(12,"L6","Santa María de Dota → Puerto Viejo","07:00",[("Gasolinera Santa María (leave full)",None),("Cartago (to check)",None),("Limón (to check)",None)],"Long day. Check Waze for Ruta 32 closures."),
(14,"L7","Puerto Viejo → near SJO","07:30",[("Leave full in Puerto Viejo (to check)",None),("Guápiles (to check)",None),("Near SJO (to check)",None)],"Long day. Fog + landslides possible on Braulio Carrillo.")]
for d,lid,r,lb,fs,no in L:
    k=RT[lid];add("leg",id=lid,name=lid,day=d,route=r,km=k["km"],time=fmt(k["min"]),leaveBy=lb,notes=no)
    for n,km in fs: add("fuel",name=n,day=d,leg=lid,km=km,lat=None,lng=None)
for f in [("Wed 28 Oct","KL 1198","Oslo → Amsterdam","09:30","11:25"),("Wed 28 Oct","KL 759","Amsterdam → San José (SJO)","12:40","17:30"),
("Wed 11 Nov","KL 760","San José → Amsterdam","19:30","12:50 Thu 12 Nov"),("Thu 12 Nov","KL 1203","Amsterdam → Oslo","14:20","16:10")]:
    add("flight",date=f[0],name=f[1],route=f[2],leaves=f[3],lands=f[4],status="Booked")
add("car",id="car",name="Rental car: Full Size SUV 4x4",company="Vamos Rent-A-Car",ref="",status="Booked",pickup="San José International Airport (SJO), Thu 29 Oct 2026, 12:00",ret="As booked: SJO, Thu 12 Nov 2026, 12:00",warn="⚠️ Return change asked: Wed 11 Nov 17:00 at SJO. Email sent, waiting for Vamos.",
 days="14 days as booked (13 needed)",car="Full Size SUV 4x4, 2500cc, automatic, petrol. Check 4 big bags fit.",
 insurance="SLI/TPL is required; a credit card can't replace it. Ask for an all-in price with SLI. CDW can sometimes be skipped with a card letter.",
 watch="Returning after 18:30 can cost an extra day. Check grace period. Ask about Quick Pass for tolls. Add Stian as driver?",
 licence="Norwegian licence OK, no international permit. Carry passport.",price="$1,211.18 total",deposit="",phone="",lat=9.9939,lng=-84.2088,area="SJO airport (Juan Santamaría)")
add("info",name="Fuel prices",text="From 3 Oct 2026: Súper 764 CRC/L, Plus 91 719 CRC/L, Diesel 785 CRC/L, same at every station. One tank covers any single drive.")
add("info",name="Tolls",text="Small, on Ruta 27 (e.g. Pozón 570 CRC, Atenas 750 CRC): card, cash or Quick Pass.")
T=[("t_doka","Hacienda Doka, Sabanilla de Alajuela",None,"Option","1 h","28 USD (43 with lunch)","Idea","Not in draft C. Old working wet mill + roaster.",10.09771,-84.20952),
("t_rb","Finca Rosa Blanca tour + cupping",None,"Option","2.5 h","40 USD per person","Idea","Not in draft C. Organic, own mill. +506 2269 9392",10.04566,-84.15062),
("t_coop","Coopedota, Santa María de Dota",11,"10:30 Sat 7 Nov","2 h","10,000–12,500 CRC (22–27 USD)","To book","Co-op from 1960. Tue–Sun 08:30, 10:30, 13:30, 15:30. Walk from the hotel.",9.65346,-83.96871),
("t_als","Starbucks Hacienda Alsacia (next to Doka)",None,"Option","90 min","about 35 USD","Question","Polished, corporate",None,None),
("t_dj","Don Juan Tours, Monteverde",3,"Fri 30 Oct","2 h","45 USD","To book","Coffee + chocolate + sugar cane. The original Don Juan (Monteverde).",10.31651,-84.82434),
("t_tab","Tabacón Thermal Resort & Spa",6,"Mon 2 Nov","Day","Price to check","To book","Day pass, or stay there.",10.4938,-84.7247)]
for tid,n,d,w,l,p,s_,no,la,lo in T: add("tour",id=tid,name=n,day=d,when=w,length=l,price=p,status=s_,notes=no,lat=la,lng=lo,link="")
add("info",name="Coffee: skip",text="Skip: Café Britt (a show, not a working farm) and Hacienda Espíritu Santo (closed since 30 May 2025). Ask farms whether the mill runs in late Oct / early Nov.")
add("info",name="Option: 1 night in Colombia",status="Idea",text="Idea, not decided. Fly Thu 29 Oct SJO → Bogotá or Medellín, back Fri 30 Oct. Costs about 2 road-trip nights. No visa for Norwegians. Yellow fever jab needed to re-enter Costa Rica, at least 10 days before: both need it by about 20 Oct.")
for k,v in [("Entry","No visa for Norwegians, up to 180 days. May be asked for a return ticket (we have one) and about 100 USD per person per month."),
("Driving","Drive on the right. Limits: 40 km/h towns, 60–80 rural, 100 max. Speed cameras, big fines. No driving after dark (dark about 17:30); arrive by 16:30–17:00. Never drive into water you can't see the bottom of. One-lane bridge: the side with the CEDA sign waits. Right on red only if clear and no sign. Seatbelts on."),
("La Fortuna → Monteverde","Last 35 km after Tilarán is gravel, potholes, steep. Slow, 4x4, daylight only."),
("Weather","End of rainy season. October is the wettest; drier in November. Sunny mornings, rainy afternoons. Caribbean side is dry Sep–Oct, wet in Nov (backup if the Pacific is bad)."),
("Money","Colones (CRC). US dollars OK in tourist areas. Cards work almost everywhere."),("Day 1","Land in the dark. Taxi to the Hampton at the airport. Car on 29 Oct."),
("Waze","Download Waze offline areas or Google Maps offline maps before the trip.")]:
    add("good",name=k,text=v)
B=[("Flights, ref on Flights screen",True,"Booked",None),("4x4 SUV (Vamos): 29 Oct 12:00 → return change to 11 Nov 17:00 asked. With SLI? Quick Pass, Stian as driver, 4 bags fit",True,"Booked","car"),
("Credit card coverage letter (only to skip CDW)",False,"To book",None),
("Hotel 28 Oct (1 night): Hampton by Hilton SJO Airport",True,"Booked","st_hampton"),("Hotel 29–30 Oct (2 nights): Monteverde",False,"To book","st_mv"),
("Hotel 31 Oct – 2 Nov (3 nights): La Fortuna, with hot springs",False,"To book","st_lf"),("Hotel 3 Nov (1 night): Atenas",False,"To book","st_at"),
("Hotel 4–5 Nov (2 nights): Manuel Antonio",False,"To book","st_ma"),("Hotel 6–7 Nov (2 nights): Santa María de Dota",False,"To book","st_sm"),
("Hotel 8–9 Nov (2 nights): Puerto Viejo",False,"To book","st_pvj"),("Hotel 10 Nov (1 night): near SJO",False,"To book","st_sjo2"),
("Don Juan tour, Monteverde, Fri 30 Oct",False,"To book","t_dj"),("Tabacón, Mon 2 Nov",False,"To book","t_tab"),("Coopedota tour, Sat 7 Nov 10:30",False,"To book","t_coop"),
("Park tickets on SINAC online: Manuel Antonio (Thu 5 Nov), Arenal. Cahuita: pay at the gate",False,"To book",None),("Travel insurance for both",False,"To book",None),
("Waze + offline maps downloaded",False,"To book",None),("Local SIM or eSIM",False,"To book",None),
("Some colones + card for tolls",False,"To book",None),("Ask each hotel for GPS location and safe parking",False,"To book",None),("Check in online for KL 760 (24 h before)",False,"To book",None),
("Check for an online arrival form for Costa Rica",False,"To book",None)]
for n,d,s_,lk in B:
    add("todo",id=("todo_"+lk if lk else None),name=n,done=d,status=s_,link=lk or "",ref="",price=("$1,211.18" if lk=="car" else ""),notes=("Return date: change to Wed 11 Nov 17:00 asked (email sent, waiting for Vamos)." if lk=="car" else ""))
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
("Jacó","For variety (on the 4 Nov drive)","In plan","food"),("Monteverde","Cloud forest, coffee a must","In plan","nature"),("Puerto Viejo de Talamanca","Beach and activities","In plan","beach"),
("Tamarindo","Best for surfing","Idea","beach"),("Drake Bay","Only reachable by boat or plane","Idea","nature"),("La Fortuna","Volcano scenery","In plan","nature"),
("Playa Conchal","Snorkelling and scuba","Idea","beach"),("Pacuare River","White water rafting, kayak","Idea","activity"),('"Tico beach" (local favourite)',"Name to check","Question","beach")]
gps={"Monteverde":(10.31651,-84.82434),"La Fortuna":(10.47168,-84.64444),"Puerto Viejo de Talamanca":(9.64965,-82.77509),"Papagayo Peninsula":(10.52735,-85.74737),"Nosara":(9.97837,-85.6279),"San José":(9.9333,-84.0833),"Jacó":(9.6144,-84.6286)}
for n,w,s,k in PL:
    la,lo=gps.get(n,(None,None)); add("place",name=n,why=w,status=s,kind=k,area="",lat=la,lng=lo,link="",day=None)
# Restaurants (bot web research 13 Oct 2026, not from the brief) for the brief's sleep areas
F=[("st_lf","Don Rufino","https://donrufino.com/","Costa Rican, smart dinner. Book."),("st_lf","Soda La Hormiga","","Cheap local food"),("st_lf","Arenal Puesta del Sol","https://www.arenalpuestadelsol.com/","Volcano view. Book."),
("st_mv","Taco Taco","","Mexican, busy, fun"),("st_mv","Don Luis","https://donluiscr.com/","Steak + pizza"),("st_mv","The Green Restaurant","","Healthy, good steaks"),
("st_ma","Claro Que Sí","","Seafood (Hotel Si Como No)"),("st_ma","Ronny's Place","","Sunset view"),("st_ma","ARBOL","https://arbolrestaurant.com/","Smart dinner, adults only"),("st_ma","Soda Sánchez (Quepos)","","Cheap local food"),
("st_uv","Mestizo","","Peru/Japan, ceviche"),("st_uv","Al Chile Que Sí","","Sunset view, cocktails"),("st_uv","Kinsu","","Casado, cheap"),
("st_sm","Café Coopedota","https://www.coopedota.com/","Coffee + local food"),("st_sm","Pizzería Las Tejas","","Pizza"),("st_sm","Restaurante y Pesca La Teja","","Trout")]
town={"st_lf":"La Fortuna","st_mv":"Santa Elena Monteverde","st_ma":"Manuel Antonio","st_uv":"Uvita","st_sm":"Santa María de Dota"}
F=[x for x in F if x[0]!="st_uv"]
for s,n,u,no in F: add("food",stay=s,name=n,link=u,notes=no,area=town[s],lat=None,lng=None)
add("spend",id="sp_hampton",date="2026-10-13",what="Hampton by Hilton SJO, night 1",amount=1305,cur="SEK",who="Simon",cat="hotel")
add("spend",id="sp_car",date="2026-10-13",what="Vamos car rental, 14 days (paid by Simon, assumed)",amount=1211.18,cur="USD",who="Simon",cat="car")
# Colombia removed (Simon, 13 Oct)
items[:]=[i for i in items if "Colombia" not in json.dumps(i,ensure_ascii=False)]
here=os.path.dirname(os.path.abspath(__file__))
v1=json.load(open(os.path.join(here,"seed-v1.json")))["items"]
olds=[json.load(open(os.path.join(here,f)))["items"] for f in ("seed-372d481.json","seed-cd4f07a.json")]
import re
auto=lambda i:re.fullmatch(i["type"]+r"\d+",i["id"]) is not None
key=lambda i:(i["type"],i.get("name"),i.get("group"),i.get("day"),i.get("label"),i.get("area"),i.get("leg"),i.get("stay"))
oldmap={key(i):i for i in v1.values()};seen=set();n=0
for it in items:
    if not auto(it): continue
    o=oldmap.get(key(it))
    if o and o["id"] not in seen: it["id"]=o["id"];it["o"]=o["o"];seen.add(o["id"])
    else: n+=1;it["id"]=f"{it['type']}_c{n}"
for it in items: it["u"]=1
final={i["id"]:i for i in items}
# migration patch for phones that already have data: only fields we changed; keep user ticks/answers/notes
FORCE={"st_hampton","car","todo_car","todo_st_hampton","st_lf","st_at","st_pvj","st_sjo2","L1","L2","L3","L4","L5","L6","L7"}
KEEP={"done","ticks","answer","notes","gpsAsked","parkingAsked","u","o"}
patch={}
for k,it in final.items():
    b=v1.get(k);collide=any(k in O and (O[k].get("name")!=it.get("name") or O[k].get("type")!=it.get("type")) for O in olds)
    if k in FORCE: patch[k]={"full":True}
    elif not b or collide or b.get("type")!=it["type"] or b.get("name")!=it.get("name"): patch[k]={"auto":True}
    else:
        ch={f:v for f,v in it.items() if f not in ("u","o") and b.get(f)!=v and (f not in KEEP or it["type"]=="day" and False)}
        if ch: patch[k]=ch
gone=set(v1)|set().union(*[set(O) for O in olds])
for k in gone-set(final): patch[k]={"del":True}
json.dump({"v":1,"meta":meta,"mig":{"id":"m3-draftC","patch":patch},"items":final},open(sys.argv[1],"w"),ensure_ascii=False,indent=0)
print(len(final),"items;",len(patch),"patches;",sum(1 for p in patch.values() if p.get("del")),"deletes")
