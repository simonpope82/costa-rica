'use strict';
const C=window.TRIP_CONFIG,LK='trip:'+C.key,STATUSES=['Booked','To book','Idea','Question','In plan'];
const $=s=>document.querySelector(s),m=$('#m');
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const enc=encodeURIComponent;
let doc=null,pending=JSON.parse(localStorage.getItem(LK+':pending')||'{}'),set=JSON.parse(localStorage.getItem(LK+':set')||'{}');
let ui={list:'booking',edit:false,mapF:'all',placeF:'all'};
const saveLocal=()=>{localStorage.setItem(LK+':doc',JSON.stringify(doc));localStorage.setItem(LK+':pending',JSON.stringify(pending));};
const saveSet=()=>localStorage.setItem(LK+':set',JSON.stringify(set));
// ---------- data helpers
const all=t=>Object.values(doc.items).filter(i=>!i.del&&(!t||i.type===t)).sort((a,b)=>(a.o||0)-(b.o||0));
const get=id=>doc.items[id];
function touch(it){it.u=Date.now();doc.items[it.id]=it;pending[it.id]=1;saveLocal();queueSync();}
function upd(id,ch){const it={...get(id),...ch};touch(it);}
function addItem(type,f){const o=Math.max(0,...Object.values(doc.items).map(i=>i.o||0))+1;const it={id:type+Date.now().toString(36)+Math.random().toString(36).slice(2,5),type,o,...f};touch(it);return it;}
function del(id){upd(id,{del:true});}
function setMeta(ch){doc.meta={...doc.meta,...ch,u:Date.now()};pending.__meta=1;saveLocal();queueSync();}
function swap(a,b){const x=get(a),y=get(b);const t=x.o;upd(a,{o:y.o});upd(b,{o:t});}
const days=()=>all('day');const dayOf=n=>days().find(d=>d.day==n);
const stayFor=n=>all('stay').find(s=>!s.backupOf&&n>=s.fromDay&&n<=s.toDay);
const usd=crc=>doc.meta.rate?(crc/doc.meta.rate).toFixed(0):'?';
// ---------- links
function waze(it,label='🚗 Navigate in Waze'){const q=[it.name&&!/^Not chosen|^Ideas:/.test(it.name)?it.name:'',it.area,C.country].filter(Boolean).join(' ');
 const u=it.lat!=null&&it.lat!==''?`https://waze.com/ul?ll=${it.lat},${it.lng}&navigate=yes`:`https://waze.com/ul?q=${enc(q)}&navigate=yes`;
 return `<a class="btn waze" href="${u}" target="_blank" rel="noopener">${label}</a>`;}
function gmap(it){const q=[it.name&&!/^Not chosen|^Ideas:/.test(it.name)?it.name:'',it.area,C.country].filter(Boolean).join(' ');
 const u=it.lat!=null&&it.lat!==''?`https://www.google.com/maps/search/?api=1&query=${it.lat},${it.lng}`:`https://www.google.com/maps/search/?api=1&query=${enc(q)}`;
 return `<a class="btn gm" href="${u}" target="_blank" rel="noopener">🗺️ Maps</a>`;}
const chip=s=>s?`<span class="chip s-${esc(s).replace(/ /g,'-')}">${esc(s)}</span>`:'';
const editBtn=id=>`<button class="btn" data-ed="${id}">✏️ Edit</button>`;
const kv=(k,v)=>v!==undefined&&v!==null&&v!==''?`<div class="kv"><b>${k}</b> ${esc(v)}</div>`:'';
// ---------- time
function crNow(){const d=new Date(Date.now()+C.utcOffset*3600e3);return d.toISOString().slice(0,10);}
function crClock(){return new Date(Date.now()+C.utcOffset*3600e3).toISOString().slice(11,16);}
function homeTime(hhmm){if(!/^\d\d:\d\d/.test(hhmm||''))return '';let [h,mm]=hhmm.split(':').map(Number);h=(h+C.homeOffsetH)%24;return `${String(h).padStart(2,'0')}:${String(mm).padStart(2,'0')} ${C.homeName}`;}
// ---------- screens
const R={};
R.more=()=>`<h2>☰ All screens</h2><div class="tiles">${[['today','🏠','Today'],['map','🗺️','Map'],['days','📅','Day by day'],['stays','🛏️','Stays'],['car','🚙','Car'],['flights','✈️','Flights'],['places','📍','Places'],['lists','✅','Checklists'],['info','ℹ️','Info + notes'],['settings','⚙️','Sync + export']].map(([h,e,t])=>`<a class="tile" href="#${h}"><b>${e}</b>${t}</a>`).join('')}</div>`;
R.today=()=>{const t=crNow(),ds=days(),first=ds[0],last=ds[ds.length-1];let h='';
 if(first&&t<first.date){const n=Math.ceil((new Date(first.date)-new Date(t))/864e5);
  const tb=[...all('todo').filter(x=>!x.done),...all('stay').filter(s=>s.status==='To book'&&!s.backupOf),...all('tour').filter(x=>x.status==='To book')];
  h+=`<div class="card" style="text-align:center"><div class="big-num">${n}</div><div><b>days to go</b></div><div class="mut">Leave ${esc(first.label)} · CR time now ${crClock()}</div></div>`;
  h+=`<h2>🟡 Still to book / do (${tb.length})</h2>`+tb.map(x=>`<div class="row"><span class="t">${x.type==='stay'?'🛏️ '+esc(x.area):x.type==='tour'?'☕ '+esc(x.name):esc(x.name)}</span>${chip(x.status)}</div>`).join('')+`<a class="btn big pri" href="#lists">Open checklist</a>`;
  return h;}
 const d=ds.find(x=>x.date===t)||(t>last.date?last:first);
 if(t>last.date)h+=`<div class="banner">The trip is over. Showing the last day.</div>`;
 return `<h2>🏠 Today · CR ${crClock()}</h2>`+dayCard(d,true);};
function dayCard(d,full){const s=stayFor(d.day),leg=all('leg').find(l=>l.day==d.day),fu=all('fuel').filter(f=>f.day==d.day);
 const tours=all('tour').filter(x=>x.day==d.day),pl=all('place').filter(p=>p.day==d.day);
 let h=`<div class="card"><h3>Day ${d.day} · ${esc(d.label)} · ${esc(d.title)}</h3><div>${esc(d.plan)}</div><div class="mut">🌅 ${esc(d.sunset||'')}</div>`;
 h+=s?`<div class="card" style="background:#eef6f1"><b>🛏️ Sleep:</b> ${esc(s.area)} ${chip(s.status)}<br>${esc(s.name)} <span class="mut">(night ${d.day-s.fromDay+1} of ${s.toDay-s.fromDay+1})</span><br>${waze(s)}${gmap(s)}</div>`:(d.day==days().length?`<div class="mut">🛫 No hotel tonight. Fly home.</div>`:'');
 if(leg){h+=`<div class="card" style="background:#f0f7ff"><b>🚗 Drive ${esc(leg.name)}:</b> ${esc(leg.route)}<br>${esc(leg.km)} km · ${esc(leg.time)}${leg.leaveBy?` · <b>leave by ${esc(leg.leaveBy)}</b>`:''}<div class="mut">${esc(leg.notes)}</div>`;
  const target=s&&d.day>1&&s.fromDay===d.day?s:(d.day==days().length?get('car'):s);
  if(target)h+=waze(target,"▶️ Start today's drive");
  if(fu.length)h+=`<div style="margin-top:8px"><b>⛽ Fuel stops</b></div>`+fu.map(f=>`<div class="row"><span class="t">${esc(f.name)} <span class="mut">km ${esc(f.km)}</span></span>${waze({...f,area:''},'🚗 Waze')}</div>`).join('');h+='</div>';}
 else h+=`<div class="mut">🚗 No long drive (rest day)</div>`;
 if(tours.length)h+=`<div><b>☕ Tours</b></div>`+tours.map(x=>`<div class="row" style="flex-wrap:wrap"><span class="t"><b>${esc(x.when)}</b> ${esc(x.name)} ${chip(x.status)}<br><span class="mut">${esc(x.length)} · ${esc(x.price)}${/^\d\d:\d\d/.test(x.when)?' · '+homeTime(x.when):''}</span></span>${waze(x,'🚗 Waze')}<button class="sm" data-ed="${x.id}">✏️</button></div>`).join('');
 if(pl.length)h+=`<div><b>📍 Places</b></div>`+pl.map(p=>`<div class="row"><span class="t">${esc(p.name)} ${chip(p.status)}</span>${waze(p,'🚗')}</div>`).join('');
 const food=s?all('food').filter(f=>f.stay===s.id):[];
 if(food.length&&full!==false)h+=`<details><summary><b>🍽️ Food nearby (${food.length})</b></summary>`+food.map(f=>`<div class="row"><span class="t">${f.link?`<a href="${esc(f.link)}" target="_blank">${esc(f.name)}</a>`:esc(f.name)}<br><span class="mut">${esc(f.notes)}</span></span>${gmap(f)}</div>`).join('')+`<div class="mut">Found by the bot on the web, 13 Oct. Not checked by you.</div></details>`;
 h+=`<label>📝 Notes for this day</label><textarea data-note="${d.id}">${esc(d.notes)}</textarea>`;
 h+=`<div>${editBtn(d.id)}<button class="btn" data-addact="${d.day}">＋ Activity</button></div></div>`;return h;}
R.days=()=>`<h2>📅 Day by day</h2>`+days().map(d=>dayCard(d,true)).join('');
R.stays=()=>`<h2>🛏️ Stays</h2>`+all('stay').filter(s=>!s.backupOf).map(s=>{const b=all('stay').filter(x=>x.backupOf===s.id);
 return `<div class="card"><h3>${esc(s.area)} ${chip(s.status)}</h3><div><b>${esc(s.name)}</b></div>
 ${kv('🌙 Nights',`${dayOf(s.fromDay)?.label} → ${dayOf(s.toDay)?.label} (${s.toDay-s.fromDay+1})`)}${kv('📍 Address',s.address)}${kv('🛰️ GPS',s.lat!=null&&s.lat!==''?s.lat+', '+s.lng:'not set (name search)')}
 ${kv('💵 Price',s.price)}${kv('🔖 Ref',s.ref)}${kv('🕑 Check-in',s.checkin)}${kv('🕚 Check-out',s.checkout)}${kv('📞 Phone',s.phone)}${s.link?`<div><a href="${esc(s.link)}" target="_blank">🔗 Link</a></div>`:''}${kv('📝',s.notes)}
 <div class="row"><button class="ck ${s.gpsAsked?'on':''}" data-tg="${s.id}:gpsAsked">${s.gpsAsked?'✓':''}</button><span class="t">Asked hotel for GPS</span></div>
 <div class="row"><button class="ck ${s.parkingAsked?'on':''}" data-tg="${s.id}:parkingAsked">${s.parkingAsked?'✓':''}</button><span class="t">Asked about safe parking</span></div>
 ${waze(s)}${gmap(s)}${editBtn(s.id)}${b.length?`<div style="margin-top:8px"><b>Backups</b></div>`+b.map(x=>`<div class="card" style="background:#f7f7f7"><b>${esc(x.name)}</b> ${chip(x.status)}<br>${esc(x.area)}<div class="mut">${esc(x.notes)}</div>${waze(x)}${editBtn(x.id)}</div>`).join(''):''}</div>`;}).join('')+`<button class="btn big" data-new="stay">＋ Add stay</button>`;
R.car=()=>{const c=get('car');const fl=all('fuellog'),tl=all('toll');const fc=fl.reduce((a,x)=>a+(+x.cost||0),0),tc=tl.reduce((a,x)=>a+(+x.cost||0),0);
 return `<h2>🚙 Car</h2><div class="card"><h3>${esc(c.name)} ${chip(c.status)}</h3>${kv('🏢 Company',c.company)}${kv('🔖 Ref',c.ref)}${kv('🔑 Pick-up',c.pickup)}${kv('↩️ Return',c.ret)}${kv('📅 Days',c.days)}${kv('🚙 Car',c.car)}${kv('🛡️ Insurance',c.insurance)}${kv('⚠️ Watch out',c.watch)}${kv('🪪 Licence',c.licence)}${kv('💵 Price',c.price)}${kv('💳 Deposit',c.deposit)}${kv('📞 Phone',c.phone)}${waze(c,'🚗 Waze to SJO airport')}${editBtn('car')}</div>
 <h2>⛽ Fuel log</h2><table><tr><th>Date</th><th>Litres</th><th>Cost ₡</th><th>Station</th><th></th></tr>${fl.map(x=>`<tr><td>${esc(x.date)}</td><td>${esc(x.litres)}</td><td>${esc(x.cost)}</td><td>${esc(x.station)}</td><td><button class="sm" data-ed="${x.id}">✏️</button></td></tr>`).join('')}</table><div><b>Total:</b> ₡${fc} ≈ ${usd(fc)} USD</div><button class="btn" data-new="fuellog">＋ Add fuel</button>
 <h2>🛣️ Tolls</h2><table><tr><th>Date</th><th>Where</th><th>Cost ₡</th><th></th></tr>${tl.map(x=>`<tr><td>${esc(x.date)}</td><td>${esc(x.name)}</td><td>${esc(x.cost)}</td><td><button class="sm" data-ed="${x.id}">✏️</button></td></tr>`).join('')}</table><div><b>Total:</b> ₡${tc} ≈ ${usd(tc)} USD</div><button class="btn" data-new="toll">＋ Add toll</button>
 ${all('info').filter(i=>/Fuel|Toll/.test(i.name)).map(i=>`<div class="card"><b>${esc(i.name)}</b><br>${esc(i.text)}</div>`).join('')}`;};
R.flights=()=>{const ref=doc.meta.flightRef;
 return `<h2>✈️ Flights ${chip('Booked')}</h2><div class="card">${kv('🔖 Booking ref',ref||'(shows after sync login)')}<div class="mut">SAS EuroBonus · flown by KLM · 2 bags each · SJO Terminal M</div></div>
 <div class="banner">⏰ Check in online for KL 760 from <b>Tue 10 Nov 19:30</b> CR time (${homeTime('19:30').replace(C.homeName,'')}Wed 11 Nov ${C.homeName}). 24 h before.</div>`+
 all('flight').map(f=>`<div class="card"><h3>${esc(f.name)} · ${esc(f.date)}</h3><div>${esc(f.route)}</div><div>🛫 ${esc(f.leaves)} → 🛬 ${esc(f.lands)} <span class="mut">(local times)</span></div>${editBtn(f.id)}</div>`).join('');};
R.places=()=>{const kinds=['all','beach','coffee','nature','food','nightlife','activity'];let ps=all('place');if(ui.placeF!=='all')ps=ps.filter(p=>p.kind===ui.placeF);
 return `<h2>📍 Places and ideas</h2><div class="tabs">${kinds.map(k=>`<button class="${ui.placeF===k?'on':''}" data-pf="${k}">${k}</button>`).join('')}</div>`+
 ps.map(p=>`<div class="card"><h3>${esc(p.name)} ${chip(p.status)}</h3><div>${esc(p.why)}</div><div class="mut">${esc(p.kind)}${p.day?` · in Day ${p.day}`:''}${p.area?' · '+esc(p.area):''}</div>${p.link?`<a href="${esc(p.link)}" target="_blank">🔗 Link</a><br>`:''}${waze(p)}${editBtn(p.id)}</div>`).join('')+`<button class="btn big" data-new="place">＋ Add place</button>`;};
R.lists=()=>{let h=`<h2>✅ Checklists</h2><div class="tabs"><button class="${ui.list==='booking'?'on':''}" data-lt="booking">📋 Booking</button><button class="${ui.list==='packing'?'on':''}" data-lt="packing">🎒 Packing</button></div>
 <button class="btn" data-editmode>${ui.edit?'✔ Done editing':'✏️ Edit list'}</button>`;
 const ctl=(arr,i)=>ui.edit?`${i>0?`<button class="sm" data-sw="${arr[i].id}:${arr[i-1].id}">▲</button>`:''}${i<arr.length-1?`<button class="sm" data-sw="${arr[i].id}:${arr[i+1].id}">▼</button>`:''}<button class="sm" data-ed="${arr[i].id}">✏️</button><button class="sm" data-del="${arr[i].id}">✕</button>`:'';
 if(ui.list==='booking'){const a=all('todo'),n=a.filter(x=>x.done).length;
  h+=`<div><b>${n} of ${a.length} done</b></div><div class="bar"><i style="width:${a.length?n/a.length*100:0}%"></i></div>`+a.map((x,i)=>`<div class="row ${x.done?'done':''}"><button class="ck ${x.done?'on':''}" data-tg="${x.id}:done">${x.done?'✓':''}</button><span class="t">${esc(x.name)} ${chip(x.status)}${x.ref?`<br><span class="mut">Ref ${esc(x.ref)}</span>`:''}${x.price?`<span class="mut"> · ${esc(x.price)}</span>`:''}${x.notes?`<br><span class="mut">${esc(x.notes)}</span>`:''}</span>${ctl(a,i)}</div>`).join('')+
  `<div class="row"><input id="new-todo" placeholder="New item"><button class="btn pri" data-quick="todo">＋</button></div>`;}
 else{const P=doc.meta.travellers||['A','B'],a=all('pack');const groups=[...new Set(a.map(x=>x.group))];
  h+=P.map((p,pi)=>{const n=a.filter(x=>x.ticks?.[p]).length;return `<div><b>${esc(p)}: ${n} of ${a.length} packed</b></div><div class="bar"><i style="width:${a.length?n/a.length*100:0}%;background:${pi?'#b45309':''}"></i></div>`}).join('');
  h+=groups.map(g=>{const ga=a.filter(x=>x.group===g);return `<h2>${esc(g)}</h2>`+ga.map((x,i)=>`<div class="row">${P.map((p,pi)=>`<div><button class="ck ${pi?'p2':''} ${x.ticks?.[p]?'on':''}" data-pk="${x.id}:${esc(p)}">${x.ticks?.[p]?'✓':''}</button><div class="who">${esc(p)}</div></div>`).join('')}<span class="t">${esc(x.name)}</span>${ctl(ga,i)}</div>`).join('')+
   `<div class="row"><input data-newpack="${esc(g)}" placeholder="Add to ${esc(g)}"><button class="btn pri" data-quickpack="${esc(g)}">＋</button></div>`;}).join('');
  h+=ui.edit?`<div class="row"><input id="new-group" placeholder="New group name"><button class="btn" data-newgroup>＋ Group</button></div>`:'';}
 return h;};
R.info=()=>{const q=all('question'),n=q.filter(x=>x.done).length;
 return `<h2>ℹ️ Good to know</h2>`+all('good').map(g=>`<div class="card"><h3>${esc(g.name)}</h3>${esc(g.text)}<br><button class="sm" data-ed="${g.id}">✏️</button></div>`).join('')+
 all('info').filter(i=>!/Fuel|Toll/.test(i.name)).map(i=>`<div class="card"><h3>${esc(i.name)} ${chip(i.status)}</h3>${esc(i.text)}<br><button class="sm" data-ed="${i.id}">✏️</button></div>`).join('')+
 `<h2>❓ Open questions (${n} of ${q.length} answered)</h2>`+q.map(x=>`<div class="row ${x.done?'done':''}" style="flex-wrap:wrap"><button class="ck ${x.done?'on':''}" data-tg="${x.id}:done">${x.done?'✓':''}</button><span class="t">${esc(x.name)}</span><button class="sm" data-ed="${x.id}">✏️</button><input data-ans="${x.id}" placeholder="Answer…" value="${esc(x.answer)}"></div>`).join('')+
 `<div class="row"><input id="new-question" placeholder="New question"><button class="btn pri" data-quick="question">＋</button></div>`+
 `<h2>📝 Notes per day</h2>`+days().map(d=>`<label>Day ${d.day} · ${esc(d.label)} · ${esc(d.title)}</label><textarea data-note="${d.id}">${esc(d.notes)}</textarea>`).join('');};
R.settings=()=>`<h2>⚙️ Sync, export, settings</h2><div class="card"><h3>🔄 Sync between phones</h3>
 <div class="mut">Status: ${esc(syncState)}</div><label>Trip password</label><input id="pw" type="password" value="${esc(set.pw||'')}" placeholder="Shared password"><label>Sync server</label><input id="srv" value="${esc(set.srv||C.syncUrl)}">
 <button class="btn pri" data-savesync>Save + sync now</button></div>
 <div class="card"><h3>🔤 Text</h3><button class="btn" data-font>${set.lexend?'Use normal font':'Use Lexend (dyslexia-friendly)'}</button></div>
 <div class="card"><h3>💱 Rate</h3><label>CRC per 1 USD</label><input id="rate" inputmode="decimal" value="${esc(doc.meta.rate)}"><button class="btn" data-rate>Save rate</button><div class="mut">${esc(doc.meta.rateNote||'')}</div></div>
 <div class="card"><h3>📤 Share + backup</h3><button class="btn" data-export>⬇️ Export JSON</button><label>Import JSON (replaces nothing, merges newer)</label><input type="file" id="imp" accept=".json,application/json"><button class="btn" data-share>🔗 Share link</button><button class="btn" data-print>🖨️ Print / PDF (all days)</button></div>
 <div class="mut">${esc(doc.meta.basics||'')}<br>${esc(doc.meta.tz||'')}</div>`;
// ---------- map
let lmap=null;
R.map=()=>`<h2>🗺️ Map</h2><div class="tabs">${[['all','All'],['sleep','🛏️ Sleep'],['coffee','☕ Coffee'],['ideas','💡 Ideas']].map(([k,t])=>`<button class="${ui.mapF===k?'on':''}" data-mf="${k}">${t}</button>`).join('')}</div><div id="map"></div><div id="nogps" class="mut"></div>`;
function drawMap(){if(!window.L){$('#map').innerHTML='<div class="banner">Map needs internet the first time.</div>';return;}
 lmap=L.map('map').setView([9.9,-84.2],8);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'© OpenStreetMap'}).addTo(lmap);
 const f=ui.mapF,types=f==='sleep'?['stay']:f==='coffee'?['tour']:f==='ideas'?['place']:['stay','tour','place','fuel','car'];
 const its=all().filter(i=>types.includes(i.type)&&!(i.type==='stay'&&i.backupOf));let no=0;
 its.forEach(i=>{if(i.lat==null||i.lat===''){no++;return;}const e={stay:'🛏️',tour:'☕',place:'📍',fuel:'⛽',car:'✈️'}[i.type];
  L.marker([+i.lat,+i.lng],{icon:L.divIcon({html:`<div style="font-size:28px">${e}</div>`,className:'',iconSize:[30,30]})}).addTo(lmap).bindPopup(`<b>${esc(i.type==='stay'?i.area:i.name)}</b><br>${chip(i.status)}<br>${waze(i)}`);});
 const route=[get('car'),...all('stay').filter(s=>!s.backupOf).sort((a,b)=>a.fromDay-b.fromDay),get('car')].filter(s=>s&&s.lat!=null&&s.lat!=='').map(s=>[+s.lat,+s.lng]);
 if(f!=='ideas'&&route.length>1)L.polyline(route,{color:'#0a6b45',weight:5,opacity:.7,dashArray:'8 8'}).addTo(lmap);
 $('#nogps').textContent=no?`${no} items have no GPS yet, so they are not on the map. Add GPS with ✏️ Edit. Route line is straight lines between towns.`:'Route line is straight lines between towns.';}
// ---------- editor
const F={day:'label,title,plan,sunset,notes',stay:'name,area,status,fromDay:n,toDay:n,address,gps,price,ref,checkin,checkout,phone,link,notes',leg:'name,day:day,route,km:n,time,leaveBy,notes',fuel:'name,day:day,km:n,gps',
 flight:'date,name,route,leaves,lands',car:'name,status,company,ref,pickup,ret,days,car,insurance,watch,licence,price,deposit,phone,gps',tour:'name,day:day,when,length,price,status,link,gps,notes',
 place:'name,area,kind:kind,why,status,day:day,link,gps',todo:'name,status,ref,price,notes',pack:'name,group',question:'name,answer',good:'name,text',info:'name,text,status',food:'name,link,notes,gps',fuellog:'date,litres:n,cost:n,station',toll:'date,name,cost:n'};
const LBL={fromDay:'First night (day no.)',toDay:'Last night (day no.)',ret:'Return',leaveBy:'Leave by',kind:'Type',why:'Why go',day:'Day',cost:'Cost (₡)',gps:'GPS (lat, lng)'};
function openEd(id,type,preset){const it=id?get(id):{type,...preset};const fs=F[it.type].split(',');let h=`<h2>✏️ ${id?'Edit':'Add'}</h2>`;
 for(const f of fs){const[k,t]=f.split(':');const lab=LBL[k]||k[0].toUpperCase()+k.slice(1);
  if(k==='status')h+=`<label>Status</label><select data-f="status"><option></option>${STATUSES.map(s=>`<option ${it.status===s?'selected':''}>${s}</option>`).join('')}</select>`;
  else if(t==='day')h+=`<label>${lab}</label><select data-f="day" data-num><option value="">— none —</option>${days().map(d=>`<option value="${d.day}" ${it.day==d.day?'selected':''}>Day ${d.day} · ${esc(d.label)}</option>`).join('')}</select>`;
  else if(t==='kind')h+=`<label>${lab}</label><select data-f="kind">${['beach','coffee','nature','food','nightlife','activity'].map(s=>`<option ${it.kind===s?'selected':''}>${s}</option>`).join('')}</select>`;
  else if(k==='gps')h+=`<label>${lab}</label><input data-gps value="${it.lat!=null&&it.lat!==''?it.lat+', '+it.lng:''}" placeholder="Paste coordinates or a Google Maps link"><button class="btn" data-here>📍 Use my location</button>`;
  else if(/plan|notes|text|insurance|watch|why|answer/.test(k))h+=`<label>${lab}</label><textarea data-f="${k}">${esc(it[k])}</textarea>`;
  else h+=`<label>${lab}</label><input data-f="${k}" ${t==='n'?'data-num inputmode="decimal"':''} value="${esc(it[k])}">`;}
 h+=`<div><button class="btn pri" data-sv>💾 Save</button><button class="btn" data-cx>Cancel</button>${id?`<button class="btn" style="background:#fee2e2" data-dl>🗑️ Delete</button>`:''}</div>`;
 const sh=$('#sheet');sh.innerHTML=h;$('#ov').classList.remove('hide');sh.scrollTop=0;
 sh.onclick=e=>{const b=e.target.closest('button');if(!b)return;
  if('cx' in b.dataset)close();
  if('dl' in b.dataset){if(confirm('Delete this?')){del(id);close();}}
  if('here' in b.dataset)navigator.geolocation?.getCurrentPosition(p=>{sh.querySelector('[data-gps]').value=p.coords.latitude.toFixed(6)+', '+p.coords.longitude.toFixed(6)},()=>alert('No location. Allow location in settings.'));
  if('sv' in b.dataset){const ch={};sh.querySelectorAll('[data-f]').forEach(i=>{let v=i.value;if(i.hasAttribute('data-num'))v=v===''?null:+v;ch[i.dataset.f]=v;});
   const g=sh.querySelector('[data-gps]');if(g){const p=parseGps(g.value);if(g.value.trim()&&!p){alert('Could not read GPS. Use "9.99, -84.20" or a Google Maps link.');return;}ch.lat=p?p[0]:null;ch.lng=p?p[1]:null;}
   if(id)upd(id,ch);else addItem(it.type,{...preset,...ch});close();}};}
function close(){$('#ov').classList.add('hide');render();}
function parseGps(s){s=decodeURIComponent(s||'');let r=s.match(/!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)/)||s.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/)||s.match(/(-?\d{1,2}\.\d+)\s*,\s*(-?\d{1,3}\.\d+)/);return r?[+r[1],+r[2]]:null;}
// ---------- sync
let syncState='local only',syncT=null,syncing=false;
function setSync(s,ok){syncState=s;const e=$('#sync');e.textContent=ok===true?'🟢 Synced':ok===false?'🔴 '+s:'🟡 '+s;}
function queueSync(){clearTimeout(syncT);syncT=setTimeout(sync,1200);setSync('Not synced yet');}
function mergeIn(r){for(const[id,it]of Object.entries(r.items||{})){const c=doc.items[id];if(!c||((it.u||0)>(c.u||0)))doc.items[id]=it;}
 if(r.meta&&(r.meta.u||0)>(doc.meta.u||0))doc.meta=r.meta;}
async function sync(){if(!set.pw){setSync('Set password',false);return;}if(syncing){queueSync();return;}syncing=true;
 const ids=Object.keys(pending);const body={items:{}};ids.forEach(i=>{if(i==='__meta')body.meta=doc.meta;else if(doc.items[i])body.items[i]=doc.items[i];});
 try{const r=await fetch((set.srv||C.syncUrl)+'/api/sync',{method:'POST',headers:{'content-type':'application/json','x-trip-key':set.pw},body:JSON.stringify(body)});
  if(r.status===401){setSync('Wrong password',false);syncing=false;return;}if(!r.ok)throw new Error(r.status);
  const j=await r.json();ids.forEach(i=>{if(i==='__meta'||!doc.items[i]||(j.items[i]&&j.items[i].u>=doc.items[i].u)||i==='__meta')delete pending[i];});
  mergeIn(j);saveLocal();setSync('Synced',Object.keys(pending).length?undefined:true);if(!document.activeElement||!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName))render();}
 catch(e){setSync(navigator.onLine?'Server asleep or down, retrying':'Offline, saved on phone',false);setTimeout(sync,20000);}
 syncing=false;}
// ---------- events
document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b||b.closest('#sheet'))return;const d=b.dataset;
 if(d.ed)return openEd(d.ed);if(d.new)return openEd(null,d.new,{status:'Idea'});
 if(d.addact)return openEd(null,'tour',{day:+d.addact,status:'Idea'});
 if(d.tg){const[id,k]=d.tg.split(':');upd(id,{[k]:!get(id)[k]});}
 else if(d.pk){const[id,p]=d.pk.split(':');const t={...(get(id).ticks||{})};t[p]=!t[p];upd(id,{ticks:t});}
 else if(d.sw){const[a,c]=d.sw.split(':');swap(a,c);}
 else if(d.del){if(confirm('Remove "'+get(d.del).name+'"?'))del(d.del);}
 else if(d.lt){ui.list=d.lt;}else if('editmode' in d){ui.edit=!ui.edit;}
 else if(d.pf){ui.placeF=d.pf;}else if(d.mf){ui.mapF=d.mf;}
 else if(d.quick){const i=$('#new-'+d.quick);if(!i.value.trim())return;addItem(d.quick,d.quick==='todo'?{name:i.value.trim(),done:false,status:'To book'}:{name:i.value.trim(),done:false,answer:''});}
 else if(d.quickpack){const i=document.querySelector(`[data-newpack="${CSS.escape(d.quickpack)}"]`);if(!i.value.trim())return;addItem('pack',{group:d.quickpack,name:i.value.trim(),ticks:{}});}
 else if('newgroup' in d){const g=$('#new-group').value.trim();if(!g)return;addItem('pack',{group:g,name:'New item',ticks:{}});}
 else if('savesync' in d){set.pw=$('#pw').value.trim();set.srv=$('#srv').value.trim();saveSet();sync();}
 else if('font' in d){set.lexend=!set.lexend;saveSet();applyFont();}
 else if('rate' in d){const v=parseFloat($('#rate').value);if(v>0)setMeta({rate:v});}
 else if('export' in d){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(doc,null,1)],{type:'application/json'}));a.download=C.key+'-'+crNow()+'.json';a.click();return;}
 else if('share' in d){const u=location.href.split('#')[0];navigator.share?navigator.share({title:doc.meta.title,url:u}):(navigator.clipboard?.writeText(u),alert('Link copied: '+u));return;}
 else if('print' in d){location.hash='days';setTimeout(()=>print(),400);return;}
 else return;render();});
document.addEventListener('change',e=>{const t=e.target;
 if(t.dataset.note!==undefined)upd(t.dataset.note,{notes:t.value});
 if(t.dataset.ans!==undefined)upd(t.dataset.ans,{answer:t.value});
 if(t.id==='imp'&&t.files[0])t.files[0].text().then(x=>{try{const j=JSON.parse(x);for(const it of Object.values(j.items||{})){const c=doc.items[it.id];if(!c||(it.u||0)>(c.u||0)){doc.items[it.id]=it;pending[it.id]=1;}}saveLocal();queueSync();render();alert('Imported');}catch(err){alert('Not a valid file')}});});
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.tagName==='INPUT'){const b=e.target.parentElement.querySelector('button.pri');if(b&&!e.target.closest('#sheet'))b.click();}});
$('#ov').addEventListener('click',e=>{if(e.target.id==='ov')close();});
function applyFont(){document.body.classList.toggle('lexend',!!set.lexend);if(set.lexend&&!$('#lexend')){const l=document.createElement('link');l.id='lexend';l.rel='stylesheet';l.href='https://fonts.googleapis.com/css2?family=Lexend:wght@400;700&display=swap';document.head.appendChild(l);}}
function render(){const r=(location.hash||'#today').slice(1);const f=R[r]||R.today;const y=scrollY;
 document.querySelectorAll('nav a').forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+r));
 if(lmap){lmap.remove();lmap=null;}m.innerHTML=f();if(r==='map')drawMap();if(render.last===r)scrollTo(0,y);else scrollTo(0,0);render.last=r;}
addEventListener('hashchange',render);addEventListener('online',sync);setInterval(()=>{if(!document.hidden)sync()},30000);document.addEventListener('visibilitychange',()=>{if(!document.hidden)sync()});
(async()=>{applyFont();$('#ttl').textContent=C.flag+' '+C.country;
 doc=JSON.parse(localStorage.getItem(LK+':doc')||'null');
 if(!doc){try{doc=await (await fetch('seed.json',{cache:'no-store'})).json();}catch(e){m.innerHTML='<div class="banner">No data yet. Open once with internet.</div>';return;}saveLocal();}
 render();sync();if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js');})();
