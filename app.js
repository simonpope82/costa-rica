const K='cr-trip-v1';let id=0;const nid=()=>Date.now().toString(36)+(id++);
let S=JSON.parse(localStorage.getItem(K)||'null');
if(!S){S={tab:'days',edit:false,todo:TODOS.map(t=>({id:nid(),t,d:false})),pack:Object.entries(PACK).map(([g,a])=>({g,items:a.map(t=>({id:nid(),t,s:false,st:false}))})),qs:QS.map(t=>({id:nid(),t,d:false,a:''}))};}
const save=()=>localStorage.setItem(K,JSON.stringify(S));
const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const m=document.getElementById('m');
function mv(a,i,d){const j=i+d;if(j<0||j>=a.length)return;[a[i],a[j]]=[a[j],a[i]];}
function ctl(path,i){return S.edit?`<button class="sm" data-up="${path}:${i}">▲</button><button class="sm" data-dn="${path}:${i}">▼</button><button class="sm" data-del="${path}:${i}">✕</button>`:'';}
function addBox(path,ph){return S.edit?`<div class="add"><input id="in-${path}" placeholder="${ph}"><button data-add="${path}">＋</button></div>`:'';}
function list(path){if(path==='todo')return S.todo;if(path==='qs')return S.qs;return S.pack[+path.slice(1)].items;}
function render(){
document.querySelectorAll('nav button').forEach(b=>b.classList.toggle('on',b.dataset.t===S.tab));
const eb=`<button class="edit" data-edit>${S.edit?'✔ Done':'✏️ Edit'}</button>`;let h='';
if(S.tab==='todo'){const n=S.todo.filter(x=>x.d).length;h=`${eb}<h2>✅ To do (${n}/${S.todo.length})</h2><div class="bar"><i style="width:${S.todo.length?n/S.todo.length*100:0}%"></i></div>`+
S.todo.map((x,i)=>`<div class="row ${x.d?'done':''}"><button class="ck ${x.d?'on':''}" data-tk="todo:${i}">${x.d?'✓':''}</button><span class="t">${esc(x.t)}</span>${ctl('todo',i)}</div>`).join('')+addBox('todo','New to-do');}
if(S.tab==='pack'){h=`${eb}<h2>🎒 Packing</h2><div class="legend">Green = Simon · Orange = Stian</div>`+S.pack.map((g,gi)=>{const p='g'+gi;
return `<h2>${esc(g.g)} <small style="color:#888">${g.items.filter(x=>x.s&&x.st).length}/${g.items.length}</small></h2>`+g.items.map((x,i)=>`<div class="row ${x.s&&x.st?'done':''}"><div><button class="ck ${x.s?'on':''}" data-tk="${p}:${i}:s">${x.s?'✓':''}</button><div class="who">Simon</div></div><div><button class="ck st ${x.st?'on':''}" data-tk="${p}:${i}:st">${x.st?'✓':''}</button><div class="who">Stian</div></div><span class="t">${esc(x.t)}</span>${ctl(p,i)}</div>`).join('')+addBox(p,'Add to '+g.g);}).join('');}
if(S.tab==='info')h='<h2>ℹ️ Good to know</h2>'+INFO.map(([a,b])=>`<div class="card"><h3>${a}</h3>${esc(b)}</div>`).join('');
if(S.tab==='qs'){const n=S.qs.filter(x=>x.d).length;h=`${eb}<h2>❓ Open questions (${n}/${S.qs.length})</h2>`+S.qs.map((x,i)=>`<div class="row ${x.d?'done':''}" style="flex-wrap:wrap"><button class="ck ${x.d?'on':''}" data-tk="qs:${i}">${x.d?'✓':''}</button><span class="t">${esc(x.t)}</span>${ctl('qs',i)}<input class="ans" data-ans="${i}" placeholder="Answer…" value="${esc(x.a)}"></div>`).join('')+addBox('qs','New question');}
if(S.tab==='days')h=DAYS?'<h2>📅 Day by day</h2>'+DAYS.map(dayHtml).join(''):'Loading…';
m.innerHTML=h;}
let DAYS=null;fetch('trip-data.json',{cache:'no-store'}).then(r=>r.json()).then(j=>{DAYS=j.days;render();});
const enc=encodeURIComponent;
function btns(q,lat,lng){const w=lat!=null?`https://waze.com/ul?ll=${lat},${lng}&navigate=yes`:`https://waze.com/ul?q=${enc(q)}&navigate=yes`;
const g=lat!=null?`https://www.google.com/maps/search/?api=1&query=${lat},${lng}`:`https://www.google.com/maps/search/?api=1&query=${enc(q)}`;
return `<a class="go wz" href="${w}" target="_blank">🚗 Waze</a><a class="go gm" href="${g}" target="_blank">🗺️ Maps</a>`;}
function dayHtml(d,i){const s=d.stay;let st='';
if(s){st=s.booked?`<div class="stay">🛏️ <b>${esc(s.name)}</b><br><small>${esc(s.address||'')}</small><br>${btns(s.name+' '+(s.address||s.area),s.lat,s.lng)}</div>`
:`<div class="stay">🛏️ <span class="nb">Not booked yet</span><br>📍 ${esc(s.area)}<br>${btns(s.area.replace(/\(.*\)/,'')+' Costa Rica')}</div>`;}
const r=d.restaurants.length?'<div><b>🍽️ Eat</b>'+d.restaurants.map(x=>{const town=s?s.area.replace(/\(.*\)/,''):'';const u=x.link||`https://www.google.com/maps/search/?api=1&query=${enc(x.name+' '+town+' Costa Rica')}`;return `<div class="rs">• <a href="${u}" target="_blank">${esc(x.name)}</a> <small>${esc(x.note||'')}</small> <a href="https://www.google.com/maps/search/?api=1&query=${enc(x.name+' '+town+' Costa Rica')}" target="_blank">📍</a></div>`}).join('')+'</div>':(s?'<div class="rs"><small>🍽️ Food: TBD (when hotel is booked)</small></div>':'');
return `<div class="day"><h3>${d.emoji} Day ${i+1} · ${esc(d.date)}</h3><div>${esc(d.plan)}</div>${st}${r}</div>`;}
document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;const d=b.dataset;
if(d.t){S.tab=d.t;scrollTo(0,0);}
else if('edit' in d)S.edit=!S.edit;
else if(d.tk){const[p,i,f]=d.tk.split(':');const x=list(p)[+i];const k=f||'d';x[k]=!x[k];}
else if(d.up){const[p,i]=d.up.split(':');mv(list(p),+i,-1);}
else if(d.dn){const[p,i]=d.dn.split(':');mv(list(p),+i,1);}
else if(d.del){const[p,i]=d.del.split(':');const a=list(p);if(confirm('Remove "'+a[+i].t+'"?'))a.splice(+i,1);}
else if(d.add){const inp=document.getElementById('in-'+d.add);const t=inp.value.trim();if(!t)return;const a=list(d.add);a.push(d.add[0]==='g'?{id:nid(),t,s:false,st:false}:{id:nid(),t,d:false,a:''});}
else return;save();render();});
document.addEventListener('input',e=>{if(e.target.dataset.ans!==undefined){S.qs[+e.target.dataset.ans].a=e.target.value;save();}});
document.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.id?.startsWith('in-'))document.querySelector(`[data-add="${e.target.id.slice(3)}"]`).click();});
render();
if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js');
