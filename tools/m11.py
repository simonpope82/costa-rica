import json
P='seed.json';d=json.load(open(P));I=d['items'];mx=max(x.get('o',0) for x in I.values())
patch={}
for k,v in list(I.items()):
    if v.get('type')=='pack': del I[k]; patch[k]={'del':True}
L={"👕 Clothes":["Light rain jacket or poncho","Quick-dry T-shirts (5–6)","2 hiking shorts or light trousers","1 long-sleeve shirt (mosquitoes, sun)","Swimwear (hot springs, beach)","Thin fleece (Poás ~10°C)","Evening clothes"],
"👟 Shoes":["Waterproof hiking shoes (worn in)","Sandals or water shoes","Quick-dry socks (6+)"],
"💊 Health":["Insect repellent (DEET)","Sunscreen and cap","Plasters, painkillers, stomach tablets","Own medicines"],
"🎒 Gear":["Daypack with rain cover","Dry bags or zip bags (phone, passport)","Water bottle","Head torch (Tortuguero)","Power bank","US plug adapter","Binoculars"],
"🛂 Papers & money":["Passport","Driving licence","Card with no foreign fees","US$200–300 each in small notes ($1/$5/$10/$20)","Travel insurance"]}
n=0
for g,items in L.items():
    for name in items:
        n+=1;mx+=1;k=f'pk11_{n}'
        I[k]=dict(id=k,type='pack',group=g,name=name,ticks={'Simon':False,'Stian':False},o=mx,u=1);patch[k]={'auto':True}
mx+=1
I['good_cash']=dict(id='good_cash',type='good',name="💵 Cash tip",text="Dollars are OK almost everywhere. Use cash for tips, parking, sodas, fruit stands and boats. Get some colones (₡) from a bank ATM at the airport.",o=mx,u=1);patch['good_cash']={'auto':True}
d['mig'].append({'id':'m11-packing','patch':patch})
json.dump(d,open(P,'w'),ensure_ascii=False,indent=0)
