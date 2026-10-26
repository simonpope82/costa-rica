'use strict';
// Tickets wallet. ALL data stays on this phone (localStorage + IndexedDB). Never synced, never in the repo.
(function(){
const TK='trip:tickets:v1',TY={flight:['✈️','Flight'],hotel:['🛏️','Hotel'],car:['🚙','Car'],tour:['☕','Tour'],park:['🌋','Park'],other:['🎟️','Other']};
const SEED=[['flight','Flights KL1198 → SJO','2026-10-28','09:30'],['hotel','Hampton Inn SJO','2026-10-28',''],['car','Vamos car','2026-10-29','08:30'],['tour','Alsacia coffee tour','2026-10-29','09:00'],['park','Poás volcano','2026-10-29','11:30'],['hotel','The Springs (29–31 Oct)','2026-10-29','16:00']];
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let T=JSON.parse(localStorage.getItem(TK)||'null');
if(!T){T=SEED.map((s,i)=>({id:'t'+i,type:s[0],title:s[1],date:s[2],time:s[3],code:'',qr:'',note:''}));save();}
function save(){localStorage.setItem(TK,JSON.stringify(T));}
// IndexedDB for images
const dbp=new Promise((ok,no)=>{const r=indexedDB.open('trip-tickets',1);r.onupgradeneeded=()=>r.result.createObjectStore('img');r.onsuccess=()=>ok(r.result);r.onerror=no;});
const idb=(mode,fn)=>dbp.then(db=>new Promise((ok,no)=>{const t=db.transaction('img',mode);const r=fn(t.objectStore('img'));t.oncomplete=()=>ok(r&&r.result);t.onerror=no;}));
const getImg=id=>idb('readonly',s=>s.get(id)),putImg=(id,v)=>idb('readwrite',s=>s.put(v,id)),delImg=id=>idb('readwrite',s=>s.delete(id));
const sorted=()=>[...T].sort((a,b)=>(a.date+(a.time||'99')).localeCompare(b.date+(b.time||'99')));
const fmt=t=>{if(!t.date)return 'No date';const d=new Date(t.date+'T12:00');return d.toLocaleDateString('en-GB',{weekday:'short',day:'numeric',month:'short'})+(t.time?' · '+t.time:'');};
function qrSvg(txt){try{const q=qrcode(0,'M');q.addData(txt);q.make();return q.createSvgTag({cellSize:8,margin:2,scalable:true});}catch(x){return '';}}
R.tickets=()=>{setTimeout(thumbs,0);return `<h2>🎟️ Tickets</h2><div class="banner">🔒 Only on this phone</div>`+
 sorted().map(t=>`<div class="card tk" data-tko="${t.id}"><div class="tkh"><span class="tki">${TY[t.type]?.[0]||'🎟️'}</span><div class="t"><h3>${e(t.title)}</h3><div class="mut">${e(fmt(t))}</div>${t.note?`<div class="mut">📍 ${e(t.note)}</div>`:''}</div><button class="sm" data-tke="${t.id}" aria-label="Edit">✏️</button></div>
 ${t.code?`<button class="tkc" data-tkc="${e(t.code)}">${e(t.code)} <small>📋</small></button>`:`<button class="tkc empty" data-tke="${t.id}">＋ Add code</button>`}
 <div class="tkimg" id="ti-${t.id}"></div>${t.qr?`<div class="tkqr">${qrSvg(t.qr)}</div>`:''}</div>`).join('')+
 `<button class="btn pri big" data-tke="new">＋ New ticket</button>
 <div class="card"><h3>💾 Backup</h3><div class="mut">Save a file. Keep it private.</div><button class="btn" data-tkx>⬇️ Save</button><label class="btn">⬆️ Load<input type="file" id="tkimp" accept=".json" hidden></label></div>`;};
async function thumbs(){for(const t of T){const el=document.getElementById('ti-'+t.id);if(!el)continue;const b=await getImg(t.id).catch(()=>null);if(b){el.innerHTML=`<img alt="" src="${URL.createObjectURL(b)}">`;}}}
async function full(id){const t=T.find(x=>x.id===id);const b=await getImg(id).catch(()=>null);if(!b&&!t.qr&&!t.code)return;
 const d=document.createElement('div');d.className='tkfull';d.innerHTML=`<div class="tkft">${TY[t.type]?.[0]||''} ${e(t.title)}</div>${b?`<img src="${URL.createObjectURL(b)}">`:''}${t.qr?`<div class="tkqr big">${qrSvg(t.qr)}</div>`:''}${t.code?`<div class="tkfc">${e(t.code)}</div>`:''}<div class="tkfh">☀️ Screen bright · Tap to close</div>`;
 d.onclick=()=>{d.remove();try{wl&&wl.release()}catch(x){}};document.body.appendChild(d);let wl=null;try{wl=await navigator.wakeLock?.request('screen')}catch(x){}}
function edit(id){const t=id==='new'?{id:'t'+Date.now().toString(36),type:'tour',title:'',date:'',time:'',code:'',qr:'',note:'',isNew:1}:T.find(x=>x.id===id);
 const sh=document.getElementById('sheet');sh.innerHTML=`<h2>🎟️ Ticket</h2><div class="tkty">${Object.entries(TY).map(([k,v])=>`<label><input type="radio" name="tkt" value="${k}" ${t.type===k?'checked':''}><span>${v[0]}<br>${v[1]}</span></label>`).join('')}</div>
 <label>Name<input id="tk-title" value="${e(t.title)}"></label><label>Date<input id="tk-date" type="date" value="${e(t.date)}"></label><label>Time<input id="tk-time" type="time" value="${e(t.time)}"></label>
 <label>Code<input id="tk-code" value="${e(t.code)}" autocapitalize="characters"></label>
 <label class="btn">📷 Photo of ticket<input id="tk-img" type="file" accept="image/*" hidden></label><span id="tk-imgok" class="mut"></span><button class="btn" data-tkdi>🗑️ Photo</button>
 <label>Make QR from text (optional)<input id="tk-qr" value="${e(t.qr)}"></label>
 <div><button class="btn pri" data-tks>✅ Save</button><button class="btn" data-tkcl>Close</button>${t.isNew?'':'<button class="btn" data-tkd>🗑️ Delete</button>'}</div>`;
 document.getElementById('ov').classList.remove('hide');let img=null,rm=false;
 sh.querySelector('#tk-img').onchange=ev=>{img=ev.target.files[0];rm=false;sh.querySelector('#tk-imgok').textContent=img?'✅ Photo ready':'';};
 sh.querySelector('[data-tkdi]').onclick=()=>{rm=true;img=null;sh.querySelector('#tk-imgok').textContent='Photo will be removed';};
 const cl=()=>{document.getElementById('ov').classList.add('hide');sh.innerHTML='';render();};
 sh.querySelector('[data-tkcl]').onclick=cl;
 sh.querySelector('[data-tkd]')?.addEventListener('click',async()=>{if(!confirm('Delete ticket?'))return;T=T.filter(x=>x.id!==t.id);save();await delImg(t.id).catch(()=>{});cl();});
 sh.querySelector('[data-tks]').onclick=async()=>{const v=s=>sh.querySelector(s).value.trim();
  Object.assign(t,{type:(sh.querySelector('[name=tkt]:checked')||{}).value||'other',title:v('#tk-title')||'Ticket',date:v('#tk-date'),time:v('#tk-time'),code:v('#tk-code'),qr:v('#tk-qr')});
  if(t.isNew){delete t.isNew;T.push(t);}save();if(img)await putImg(t.id,img);else if(rm)await delImg(t.id).catch(()=>{});cl();};}
const b64=b=>new Promise(ok=>{const r=new FileReader();r.onload=()=>ok(r.result);r.readAsDataURL(b);});
async function exp(){const imgs={};for(const t of T){const b=await getImg(t.id).catch(()=>null);if(b)imgs[t.id]=await b64(b);}
 const blob=new Blob([JSON.stringify({kind:'trip-tickets',v:1,tickets:T,imgs})],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='tickets-backup.json';a.click();}
async function imp(f){try{const j=JSON.parse(await f.text());if(j.kind!=='trip-tickets')throw 0;T=j.tickets;save();for(const[id,u]of Object.entries(j.imgs||{}))await putImg(id,await (await fetch(u)).blob());render();alert('✅ Loaded');}catch(x){alert('Not a ticket file');}}
document.addEventListener('click',ev=>{const b=ev.target.closest('[data-tke],[data-tkc],[data-tkx],[data-tko]');if(!b||b.closest('#sheet'))return;
 if(b.dataset.tke){ev.stopPropagation();return edit(b.dataset.tke);}
 if(b.dataset.tkc!==undefined){ev.stopPropagation();navigator.clipboard?.writeText(b.dataset.tkc);b.classList.add('ok');setTimeout(()=>b.classList.remove('ok'),1200);return;}
 if(b.dataset.tkx!==undefined)return exp();
 if(b.dataset.tko)full(b.dataset.tko);},true);
// One-tap import: #tickets-import=<base64url UTF-8 JSON {tickets:[...], remove:[titles]}>. Fragment never reaches a server.
async function hashImp(){const h=location.hash;if(!h.startsWith('#tickets-import='))return;
 try{let b=h.slice(16).replace(/-/g,'+').replace(/_/g,'/');while(b.length%4)b+='=';const j=JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(b),c=>c.charCodeAt(0))));
  const rm=new Set(j.remove||[]);const gone=T.filter(x=>rm.has(x.title));T=T.filter(x=>!rm.has(x.title));for(const g of gone)await delImg(g.id).catch(()=>{});let n=0;
  for(const t of j.tickets||[]){const key=(t.match||t.title);let c=T.find(x=>x.title===key||x.title===t.title);const {match,img,...f}=t;
   if(c)Object.assign(c,f);else{c={id:'t'+Date.now().toString(36)+(n),type:'other',title:'',date:'',time:'',code:'',qr:'',note:'',...f};T.push(c);}n++;
   if(img)await putImg(c.id,await (await fetch(img)).blob());}
  save();history.replaceState(null,'',location.pathname+location.search+'#tickets');if(window.render)render();setTimeout(()=>alert('✅ '+n+' tickets added'),300);}
 catch(x){history.replaceState(null,'',location.pathname+'#tickets');alert('Import link not valid');}}
addEventListener('hashchange',hashImp);setTimeout(hashImp,0);
document.addEventListener('change',ev=>{if(ev.target.id==='tkimp'&&ev.target.files[0])imp(ev.target.files[0]);});
})();
