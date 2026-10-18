# Builds seed.json (public, no booking refs) from the brief data.
import json,sys,os
items=[];o=[0]
def add(t,**f):
    o[0]+=1; f.update(type=t,id=f.get('id') or f"{t}{o[0]}",o=o[0]); items.append(f); return f
meta={"title":"Costa Rica road trip","travellers":["Simon","Stian"],"start":"2026-10-28","end":"2026-11-11",
 "tz":"Costa Rica UTC−6 · Oslo is 7 h ahead","rate":456.61,"rateNote":"456.61 CRC = 1 USD (10 Oct 2026)",
 "basics":"Route: draft D2 (approved 13 Oct). 14 nights · about 1,180 km, about 32 h driving over 6 days · fuel: to check"}
WX=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"wx.json")))
RT=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","route.json")))
fmt=lambda m:(f"{m//60} h {m%60:02d}" if m%60 else f"{m//60} h")
D=[("Wed 28 Oct","Arrive · taxi","Land 17:30. Taxi to the Hampton (at the airport). No car today. Early night."),
("Thu 29 Oct","Car → Poás volcano → Starbucks farm → The Springs","08:30 Vamos brings the car to the Hampton (hotel delivery 9 USD, to ask Vamos). Leave 08:45 sharp. 09:30 Poás volcano crater (online ticket, fixed slot, to book), about 1 h. 10:30 leave, Poás → Hacienda Alsacia (about 45 min). 11:30 Starbucks farm tour, 1 h 30 + 30 min tasting (to book). Tight: leave the farm by 13:45. Drive to The Springs (about 3 h 30), arrive about 17:15, before dark."),
("Fri 30 Oct","Volcano + waterfall + hot springs","Full-day tour (10 h, pickup from the hotel): La Fortuna waterfall, Maleku lunch, Arenal volcano walk, hot springs. No driving."),
("Sat 31 Oct","Río Celeste (maybe)","Check out of The Springs. Move to hotel 2 in La Fortuna (to book). Idea: Río Celeste waterfall, Tenorio park (1 h 45 each way, 250 steps down). Or a lazy day at the hot springs."),
("Sun 1 Nov","Don Juan coffee + chocolate","Don Juan Arenal tour (2 h; 09:00, 10:00, 14:00 or 15:00). Afternoon: hot springs. No driving."),
("Mon 2 Nov","To Tamarindo","Leave 08:00. Long drive (5 h 30). Afternoon: beach."),
("Tue 3 Nov","Tamarindo beach","Beach, surf, sunset. No driving."),
("Wed 4 Nov","To Fiesta Resort","Leave 09:00, arrive about 14:00. All inclusive: pool + food."),
("Thu 5 Nov","To Tortuguero (car + boat)","Leave 07:00. Via San José + Ruta 32 to La Pavona (5 h 15). Park the car (secure lot). 15:15 boat (12:45 if early), about 1 h."),
("Fri 6 Nov","Tortuguero","Canal boat tour + national park. No car."),
("Sat 7 Nov","To Punta Cocles","06:40 or 08:40 boat back to La Pavona. Drive via Guápiles + Limón (4 h 45)."),
("Sun 8 Nov","Ride The Rainforest","Horse ride on the beach + jungle (Ride The Rainforest, Punta Cocles). Book ahead."),
("Mon 9 Nov","Cahuita","Cahuita National Park (open every day 8–16; about 20 min drive). Beach."),
("Tue 10 Nov","Back to SJO","Long day: leave 07:00 (6 h 30). Ruta 32 over Braulio Carrillo. Fog + landslides possible."),
("Wed 11 Nov","Fly home","Slow morning, pack. Fill up. Car back at SJO by 14:00 (saves a day) or 17:00 (change asked). Fly 19:30.")]
for i,(d,t,p) in enumerate(D,1):
    w=WX[str(i)]
    add("day",id=f"day{i}",day=i,date=f"2026-{'10' if 'Oct' in d else '11'}-{int(d.split()[1]):02d}",label=d,title=t,plan=p,notes="",sunset="Dark about 17:15–17:30",
        wx={"kind":w["kind"],"place":w["place"],"tmax":w["tmax"],"tmin":w["tmin"],"mm":w["mm"],"pop":w["pop"]})
G={"SJO":(9.9939,-84.2088),"LF":(10.47168,-84.64444),"TAM":(10.2993,-85.8371),"FR":(9.9555,-84.7695),"TOR":(10.5420,-83.5024),"PC":(9.638944,-82.717119)}
S=[("st_hampton","Hampton by Hilton San Jose Airport","Alajuela (at SJO airport)",1,1,"Booked","1 night (Wed 28 Oct only), prepaid SEK 1,305, non-refundable. Confirmed by Trip.com 13 Oct. Check-in after 14:00. Non-refundable. Alamo car rental station is at this hotel. GPS = airport (approx).","",None,"SJO"),
("st_lf","The Springs Resort & Spa","La Fortuna / Arenal (9 km west + 3.5 km north of town)",2,3,"Booked","2 nights: Thu 29 + Fri 30 Oct. Vista Grande Double Queen (2 queen beds). Hot springs included. No breakfast. Paid, non-refundable. Booked on Booking.com 18 Oct: waiting for the hotel confirmation email. https://www.thespringscostarica.com/ · GPS approx (OpenStreetMap).","+506 2401 3300",None,"LF"),
("st_tam","Not chosen","Tamarindo",6,7,"To book","","",None,"TAM"),
("st_fr","Fiesta Resort All Inclusive","El Roble, Chacarita, Puntarenas 5400",8,8,"To book","1 night, all inclusive. GPS approx (El Roble).","",None,"FR"),
("st_tor","Hotel Serendipity","1809 Playa, Tortuguero, Limón",9,10,"To book","No road: car stays at La Pavona, boat about 1 h. GPS = village (approx).","",None,"TOR"),
("st_pvj","Not chosen","Punta Cocles, Puerto Viejo de Talamanca",11,13,"To book","","",None,"PC"),
("st_sjo2","Not chosen","Near SJO (Tuetal / Alajuela hills / Belén)",14,14,"To book","Last night, near the airport.","",None,"SJO"),
("st_pv","Pura Vida Hotel","Tuetal, Alajuela (4 km from SJO)",14,14,"Idea","99–129 USD/night + 13% tax (1 Sep–15 Nov), breakfast, free airport pickup for arrivals","+506 2430 2929","st_sjo2",None),
("st_bv","Buena Vista Chic Hotel","Alajuela hills (9 km from SJO)",14,14,"Idea","From about 144 USD/night, breakfast + airport shuttle","","st_sjo2",None),
("st_rb","Finca Rosa Blanca coffee farm","Santa Bárbara de Heredia",14,14,"Idea","Junior Suite from about 315 USD/night + 13% tax.","+506 2269 9392","st_sjo2",None)]
for sid,n,a,f,t,st,no,ph,bk,g in S:
    la,lo=(G[g] if g else (None,None))
    if sid=="st_rb": la,lo=10.04566,-84.15062
    if sid=="st_lf": la,lo=10.5191,-84.6883
    add("stay",id=sid,name=n,area=a,address=("Airport Blvd 1, Alajuela" if sid=="st_hampton" else ""),checkin={"st_hampton":"Wed 28 Oct","st_lf":"Thu 29 Oct"}.get(sid,""),checkout={"st_hampton":"Thu 29 Oct","st_lf":"Sat 31 Oct"}.get(sid,""),price={"st_hampton":"SEK 1,305 (prepaid)","st_lf":"NOK 7,761.16 (paid, non-refundable)"}.get(sid,""),fromDay=f,toDay=t,status=st,notes=no,phone=ph,backupOf=bk or "",ref="",lat=la,lng=lo,link="",gpsAsked=False,parkingAsked=False)
L=[(2,"L1","Hampton → Poás volcano → Hacienda Alsacia → The Springs","08:45",[("Fill up near SJO (to check)",None),("La Fortuna (on arrival, to check)",None)],"Hampton → Poás crater about 36 km / 1 h–1 h 30. Poás → Hacienda Alsacia about 22 km / 45 min–1 h. Alsacia → The Springs about 119 km / 3 h 30 (mountain roads, slow). Tight: leave the farm by 13:45."),
(6,"L2","La Fortuna → Tamarindo","08:00",[("La Fortuna (leave full)",None),("Liberia (to check)",None)],"Long drive."),
(8,"L3","Tamarindo → Fiesta Resort (Puntarenas)","09:00",[("Tamarindo (leave full)",None),("Nicoya or Ruta 1 (to check)",None)],""),
(9,"L4","Fiesta Resort → La Pavona (via San José + Ruta 32)","07:00",[("Leave full (to check)",None),("Guápiles (to check)",None)],"Car stays at La Pavona secure parking (about 20–23 USD/night). Boats about 07:00, 09:15, 11:15, 12:45, 15:15, 16:15."),
(11,"L5","La Pavona → Punta Cocles","09:30",[("Guápiles (to check)",None),("Limón (to check)",None)],"Boat back first: 06:40 or 08:40."),
(14,"L6","Punta Cocles → near SJO","07:00",[("Leave full in Puerto Viejo (to check)",None),("Guápiles (to check)",None)],"Long day. Fog + landslides possible on Braulio Carrillo.")]
for d,lid,r,lb,fs,no in L:
    k=RT[lid];add("leg",id=lid,name=lid,day=d,route=r,km=k["km"],time=fmt(k["min"]),leaveBy=lb,notes=no)
    for n,km in fs: add("fuel",name=n,day=d,leg=lid,km=km,lat=None,lng=None)
for f in [("Wed 28 Oct","KL 1198","Oslo → Amsterdam","09:30","11:25"),("Wed 28 Oct","KL 759","Amsterdam → San José (SJO)","12:40","17:30"),
("Wed 11 Nov","KL 760","San José → Amsterdam","19:30","12:50 Thu 12 Nov"),("Thu 12 Nov","KL 1203","Amsterdam → Oslo","14:20","16:10")]:
    add("flight",date=f[0],name=f[1],route=f[2],leaves=f[3],lands=f[4],status="Booked")
add("car",id="car",name="Rental car: Full Size SUV 4x4",company="Vamos Rent-A-Car",ref="",status="Booked",pickup="As booked: San José International Airport (SJO), Thu 29 Oct 2026, 12:00 (Vamos wrote 10 Oct by mistake: waiting for Vamos). Plan: 08:30 delivery to the Hampton (9 USD), to ask Vamos.",ret="As booked: SJO, Thu 12 Nov 2026, 12:00",warn="⚠️ Return change asked: Wed 11 Nov 17:00 at SJO. Email sent, waiting for Vamos.",
 days="14 days as booked (13 needed)",car="Full Size SUV 4x4, 2500cc, automatic, petrol. Check 4 big bags fit.",
 insurance="SLI/TPL is required; a credit card can't replace it. Ask for an all-in price with SLI. CDW can sometimes be skipped with a card letter.",
 watch="Returning after 18:30 can cost an extra day. Check grace period. Ask about Quick Pass for tolls. Add Stian as driver?",
 licence="Norwegian licence OK, no international permit. Carry passport.",price="$1,211.18 total",deposit="",phone="",lat=9.9939,lng=-84.2088,area="SJO airport (Juan Santamaría)")
add("info",name="Fuel prices",text="From 3 Oct 2026: Súper 764 CRC/L, Plus 91 719 CRC/L, Diesel 785 CRC/L, same at every station. One tank covers any single drive.")
add("info",name="Tolls",text="Small, on Ruta 27 (e.g. Pozón 570 CRC, Atenas 750 CRC): card, cash or Quick Pass.")
T=[("t_doka","Hacienda Doka, Sabanilla de Alajuela",None,"Option","1 h","28 USD (43 with lunch)","Idea","Old working wet mill + roaster.",10.09771,-84.20952),
("t_rb","Finca Rosa Blanca tour + cupping",None,"Option","2.5 h","40 USD per person","Idea","Organic, own mill. +506 2269 9392",10.04566,-84.15062),
("t_volc","Arenal volcano + La Fortuna waterfall + hot springs (GetYourGuide)",3,"Fri 30 Oct, pickup (time at booking)","10 h","about 95–105 USD pp","To book","Pickup in La Fortuna. Lunch, park fees, hot springs + 1 cocktail included. https://www.getyourguide.com/la-fortuna-l1904/arenal-volcano-la-fortuna-waterfall-and-hot-springs-tour-t192264/",10.4627,-84.7032),
("t_dja","Don Juan Arenal coffee + chocolate (La Fortuna)",5,"Sun 1 Nov 09:00/10:00/14:00/15:00","2 h","50 USD pp","To book","The La Fortuna farm (not Monteverde). Free pickup from most town hotels. https://donjuantoursarenal.com/",10.4840,-84.6420),
("t_rc","Río Celeste waterfall (Tenorio park)",4,"Sat 31 Oct (maybe)","6 h tour or self-drive","Tour from 165 USD; park ticket about 32 USD","Idea","250 steps down. 1 h 45 each way from La Fortuna. https://www.getyourguide.com/bijagua-de-upala-l215361/rio-celeste-fossen-luksustur-sertifisert-guide-lunsj-t1381037/",10.7158,-84.9969),
("t_tortboat","Tortuguero: La Pavona parking + boats",9,"Thu 5 Nov (15:15 boat) · back Sat 7 Nov (06:40/08:40)","about 1 h each way","Boat about 8–10 USD pp each way; parking about 20–23 USD/night","To book","Book boat + parking bundle (pavonaparking.com or smithtortugueroboats.com). Times change with the river: confirm.",10.4517,-83.5960),
("t_ride","Ride The Rainforest (horse riding), Punta Cocles",12,"Sun 8 Nov","1–2.5 h","from about 65 USD/h","To book","Guided horse rides, beach + jungle. +506 6192 8939 · ridetherainforest.com",9.638944,-82.717119)]
for tid,n,d,w,l,p,s_,no,la,lo in T: add("tour",id=tid,name=n,day=d,when=w,length=l,price=p,status=s_,notes=no,lat=la,lng=lo,link="")
add("info",name="Coffee: skip",text="Skip: Café Britt (a show, not a working farm) and Hacienda Espíritu Santo (closed since 30 May 2025). Ask farms whether the mill runs in late Oct / early Nov.")
add("info",name="Option: 1 night in Colombia",status="Idea",text="Idea, not decided. Fly Thu 29 Oct SJO → Bogotá or Medellín, back Fri 30 Oct. Costs about 2 road-trip nights. No visa for Norwegians. Yellow fever jab needed to re-enter Costa Rica, at least 10 days before: both need it by about 20 Oct.")
for k,v in [("Entry","No visa for Norwegians, up to 180 days. May be asked for a return ticket (we have one) and about 100 USD per person per month."),
("Driving","Drive on the right. Limits: 40 km/h towns, 60–80 rural, 100 max. Speed cameras, big fines. No driving after dark (dark about 17:30); arrive by 16:30–17:00. Never drive into water you can't see the bottom of. One-lane bridge: the side with the CEDA sign waits. Right on red only if clear and no sign. Seatbelts on."),
("Tortuguero","No road. Park at La Pavona (secure, staffed lot), boat about 1 h. Take only a small bag. No valuables in the car."),
("Weather","End of rainy season. October is the wettest; drier in November. Sunny mornings, rainy afternoons. Caribbean side is dry Sep–Oct, wet in Nov (backup if the Pacific is bad)."),
("Money","Colones (CRC). US dollars OK in tourist areas. Cards work almost everywhere."),("Day 1","Land in the dark. Taxi to the Hampton at the airport. Car on 29 Oct."),
("Waze","Download Waze offline areas or Google Maps offline maps before the trip.")]:
    add("good",name=k,text=v)
B=[("Flights, ref on Flights screen",True,"Booked",None),("4x4 SUV (Vamos): 29 Oct 12:00 → return change to 11 Nov 17:00 asked. With SLI? Quick Pass, Stian as driver, 4 bags fit",True,"Booked","car"),
("Credit card coverage letter (only to skip CDW)",False,"To book",None),
("Hotel 28 Oct (1 night): Hampton by Hilton SJO Airport",True,"Booked","st_hampton"),
("Hotel 29–30 Oct (2 nights): The Springs Resort & Spa, La Fortuna",True,"Booked","st_lf"),
("Hotel 2–3 Nov (2 nights): Tamarindo",False,"To book","st_tam"),
("Hotel 4 Nov (1 night): Fiesta Resort All Inclusive",False,"To book","st_fr"),
("Hotel 5–6 Nov (2 nights): Hotel Serendipity, Tortuguero",False,"To book","st_tor"),
("Hotel 7–9 Nov (3 nights): Punta Cocles",False,"To book","st_pvj"),("Hotel 10 Nov (1 night): near SJO",False,"To book","st_sjo2"),
("Volcano + waterfall + hot springs tour, Fri 30 Oct",False,"To book","t_volc"),("Don Juan Arenal tour, Sun 1 Nov",False,"To book","t_dja"),
("Tortuguero: La Pavona parking + boats, 5 Nov / 7 Nov",False,"To book","t_tortboat"),("Ride The Rainforest, Sun 8 Nov",False,"To book","t_ride"),
("Cancel Coopedota tour 7 Nov if booked",False,"Question",None),
("Cahuita: pay at the gate. Tortuguero park ticket: online or at the gate",False,"To book",None),("Travel insurance for both",False,"To book",None),
("Waze + offline maps downloaded",False,"To book",None),("Local SIM or eSIM",False,"To book",None),
("Some colones + card for tolls",False,"To book",None),("Ask each hotel for GPS location and safe parking",False,"To book",None),("Check in online for KL 760 (24 h before)",False,"To book",None),
("Check for an online arrival form for Costa Rica",False,"To book",None)]
for n,d,s_,lk in B:
    add("todo",id=("todo_"+lk if lk else None),name=n,done=d,status=s_,link=lk or "",ref="",price=("$1,211.18" if lk=="car" else ""),notes=("Return date: change to Wed 11 Nov 17:00 asked (email sent, waiting for Vamos)." if lk=="car" else ""))
P={"Documents and money":["Passport (6+ months left is safest)","Norwegian driving licence (both, if Stian drives)","Credit card in the driver's name (for the car deposit)","Debit card + backup card","Some US dollars in cash","Card coverage letter (if skipping CDW)","Travel insurance details","E-ticket and booking refs (also offline on phone)","Copies of passport and licence (photo on phone + paper)","Yellow fever certificate (only if Colombia)"],
"Tech":["Phone + charger","Power bank","Plug adapter for Costa Rica (US-type plugs, 120 V: check chargers say 100–240 V)","Car phone holder","Car USB charger + cable","Headphones","Head torch (night walks)"],
"Clothes":["Rain jacket (October is the wettest month)","Warm layer / fleece (cool evenings, plane)","Long trousers (hiking, mosquitoes)","Light quick-dry shirts and shorts","Swimwear","Walking shoes or light hiking boots (mud)","Sandals / flip-flops","Cap or sun hat","Clothes for a nice dinner"],
"Health and comfort":["Personal medicines (enough for the whole trip)","Insect repellent (strong, DEET)","Sunscreen (reef-safe for the beaches)","Sunglasses","Small first aid kit + plasters","Travel sickness tablets (lots of curvy roads)","Stomach tablets","Hand sanitiser"],
"Day trips":["Small daypack","Dry bag (rafting, boat trips, rain)","Water bottle","Binoculars (birds, sloths, whales)","Snorkel mask (optional)","Quick-dry towel"]}
for g,a in P.items():
    for n in a: add("pack",group=g,name=n,ticks={"Simon":False,"Stian":False})
for q in ["Río Celeste on Sat 31 Oct: go, or rest day?","Last night near SJO, or drive from Punta Cocles on 11 Nov (leave 06:30)?","Budget per night? One room or two?","Add Stian as a driver?","Must-dos: zip-line, rafting, hot springs, whales, fishing, surfing?","Do the 1 night in Colombia?","Fiesta Resort: is 1 night enough?"]:
    add("question",name=q,done=False,answer="")
PL=[("Papagayo Peninsula","Hotels and food (pricey but nice)","Idea","food"),("San José","Culture and nightlife","Idea","nightlife"),("Nosara","Yoga and spa","Idea","activity"),
("Jacó","For variety","Idea","food"),("Monteverde","Cloud forest (dropped in D2)","Idea","nature"),("Puerto Viejo de Talamanca","Beach and activities","In plan","beach"),
("Tamarindo","Best for surfing","In plan","beach"),("Drake Bay","Only reachable by boat or plane","Idea","nature"),("La Fortuna","Volcano scenery","In plan","nature"),
("Playa Conchal","Snorkelling and scuba","Idea","beach"),("Pacuare River","White water rafting, kayak","Idea","activity"),('"Tico beach" (local favourite)',"Name to check","Question","beach")]
gps={"Monteverde":(10.31651,-84.82434),"La Fortuna":(10.47168,-84.64444),"Puerto Viejo de Talamanca":(9.64965,-82.77509),"Papagayo Peninsula":(10.52735,-85.74737),"Nosara":(9.97837,-85.6279),"Tamarindo":(10.2993,-85.8371),"San José":(9.9333,-84.0833),"Jacó":(9.6144,-84.6286)}
for n,w,s,k in PL:
    la,lo=gps.get(n,(None,None)); add("place",name=n,why=w,status=s,kind=k,area="",lat=la,lng=lo,link="",day=None)
# Restaurants (bot web research 13 Oct 2026, not from the brief) for the brief's sleep areas
F=[("st_lf","Don Rufino","https://donrufino.com/","Costa Rican, smart dinner. Book."),("st_lf","Soda La Hormiga","","Cheap local food"),("st_lf","Arenal Puesta del Sol","https://www.arenalpuestadelsol.com/","Volcano view. Book.")]
town={"st_lf":"La Fortuna"}
for s,n,u,no in F: add("food",stay=s,name=n,link=u,notes=no,area=town[s],lat=None,lng=None)
add("spend",id="sp_hampton",date="2026-10-13",what="Hampton by Hilton SJO, night 1",amount=1305,cur="SEK",who="Simon",cat="hotel")
add("spend",id="sp_car",date="2026-10-13",what="Vamos car rental, 14 days (paid by Simon, assumed)",amount=1211.18,cur="USD",who="Simon",cat="car")
# Hacienda Alsacia on day 2 (Simon, 18 Oct). Added at the end so other items keep their order.
add("tour",id="t_alsacia",name="Hacienda Alsacia (Starbucks coffee farm), Poás",day=2,when="Thu 29 Oct ~11:30 (tours 08:00–15:00)",length="1 h 30 + 30 min tasting",price="about 30–36 USD pp",status="To book",notes="Real coffee farm on Poás volcano: coffee trees, nursery, wet mill, roaster + tasting. Visitor centre 8–16, café to 18. About 45 min from Poás. Book online: https://starbuckscoffeefarm.com/en/",lat=10.1013,lng=-84.2009,link="")
add("tour",id="t_poas",name="Poás Volcano National Park (crater)",day=2,when="Thu 29 Oct ~09:30 (fixed slot)",length="about 1 h",price="16.95 USD pp + parking about ₡2,000",status="To book",notes="Tickets ONLY online (SINAC SICORE), fixed time slot. No refunds, even for fog. Open 08:00–16:00, last entry 14:00. Mornings are clearer. https://serviciosenlinea.sinac.go.cr/",lat=10.1960,lng=-84.2316,link="")
add("todo",id="todo_t_poas",name="Poás volcano tickets (SINAC online), Thu 29 Oct ~09:30 slot",done=False,status="To book",link="t_poas",ref="",price="",notes="")
add("todo",id="todo_vamos_delivery",name="Ask Vamos: deliver the car to the Hampton Thu 29 Oct 08:30 (9 USD). Email about Wed 21 Oct",done=False,status="Question",link="",ref="",price="",notes="https://vamosrentacar.com/faq/")
add("todo",id="todo_t_alsacia",name="Hacienda Alsacia (Starbucks farm) tour, Thu 29 Oct ~11:30",done=False,status="To book",link="t_alsacia",ref="",price="",notes="")
# The Springs booked for 29-30 Oct (Simon, 18 Oct); 31 Oct-1 Nov still to book. o=17.5 keeps it next to st_lf.
add("stay",id="st_lf2",name="Not chosen (hotel 2)",area="La Fortuna / Arenal",address="",checkin="Sat 31 Oct",checkout="Mon 2 Nov",price="",fromDay=4,toDay=5,status="To book",notes="2 nights: Sat 31 Oct + Sun 1 Nov. The Springs covers only 29 + 30 Oct.",phone="",backupOf="",ref="",lat=10.47168,lng=-84.64444,link="",gpsAsked=False,parkingAsked=False)["o"]=17.5
add("todo",id="todo_st_lf2",name="Hotel 31 Oct – 1 Nov (2 nights): La Fortuna, hotel 2",done=False,status="To book",link="st_lf2",ref="",price="",notes="")["o"]=71.5
add("spend",id="sp_springs",date="2026-10-18",what="The Springs Resort & Spa, 2 nights (29–30 Oct), Booking.com, paid",amount=7761.16,cur="NOK",who="Simon",cat="hotel")
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
C=json.load(open(os.path.join(here,"seed-C.json")))["items"];p5={}
for k,it in final.items():
    b=C.get(k)
    if not b or b.get("type")!=it["type"] or b.get("name")!=it.get("name"): p5[k]={"auto":True}
    else:
        ch={f:v for f,v in it.items() if (f not in KEEP or (f=="notes" and it["type"]=="leg")) and b.get(f)!=v}
        if ch: p5[k]=ch
for k in set(C)-set(final): p5[k]={"del":True}
D2=json.load(open(os.path.join(here,"seed-D2.json")))["items"];p6={}
for k,it in final.items():
    b=D2.get(k)
    if not b or b.get("type")!=it["type"] or b.get("name")!=it.get("name"): p6[k]={"auto":True}
    else:
        ch={f:v for f,v in it.items() if (f not in KEEP or (f=="notes" and it["type"]=="leg")) and b.get(f)!=v}
        if ch: p6[k]=ch
for k in set(D2)-set(final): p6[k]={"del":True}
print("m6 patch:",json.dumps(p6,ensure_ascii=False))
M6=json.load(open(os.path.join(here,"seed-m6.json")))["items"];p7={}
for k,it in final.items():
    b=M6.get(k)
    if not b or b.get("type")!=it["type"] or b.get("name")!=it.get("name"): p7[k]={"auto":True}
    else:
        ch={f:v for f,v in it.items() if (f not in KEEP or (f=="notes" and it["type"] in ("leg","stay"))) and b.get(f)!=v}
        if ch: p7[k]=ch
for k in set(M6)-set(final): p7[k]={"del":True}
print("m7 patch:",json.dumps(p7,ensure_ascii=False))
M7=json.load(open(os.path.join(here,"seed-m7.json")))["items"];p8={}
for k,it in final.items():
    b=M7.get(k)
    if not b or b.get("type")!=it["type"] or b.get("name")!=it.get("name"): p8[k]={"auto":True}
    else:
        ch={f:v for f,v in it.items() if (f not in KEEP or (f=="notes" and it["type"] in ("leg","stay","tour"))) and b.get(f)!=v}
        if ch: p8[k]=ch
for k in set(M7)-set(final): p8[k]={"del":True}
print("m8 patch:",json.dumps(p8,ensure_ascii=False))
json.dump({"v":1,"meta":meta,"mig":[{"id":"m3-draftC","patch":patch},{"id":"m4-hampton-ok","patch":{"st_hampton":{"notes":final["st_hampton"]["notes"]}}},{"id":"m5-draftD2","patch":p5},{"id":"m6-alsacia","patch":p6},{"id":"m7-springs","patch":p7},{"id":"m8-poas","patch":p8}],"items":final},open(sys.argv[1],"w"),ensure_ascii=False,indent=0)
print(len(final),"items;",len(patch),"patches;",sum(1 for p in patch.values() if p.get("del")),"deletes")
