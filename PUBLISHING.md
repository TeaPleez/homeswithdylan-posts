# Scheduling approved posts in Meta Business Suite (proven method, Nov 2026)

Images reach Business Suite through GitHub Pages because Facebook's CSP blocks fetches to other sites but allows iframes:
- Repo: TeaPleez/homeswithdylan-posts (public). Pages: https://teapleez.github.io/homeswithdylan-posts/
- relay.html (repo root) answers postMessage {type:'get', files:[...]} from https://business.facebook.com with the JPEG bytes.
- Slides go in posts/<YYYY-MM-DD>/slide-01.jpg ... (plus post.json). Commit + push to main; Pages redeploys in ~1-2 min.

Browser: the Claude desktop app's built-in browser pane (mcp__remote-devices__Claude_Browser__*), already signed in to Meta Business Suite.

## Steps per post
1. Navigate (force:true) to https://business.facebook.com/latest/composer and wait ~3 s.
2. javascript_exec — hook the file picker:
   window.__lastFileInput=null; const o=HTMLInputElement.prototype.click; if(!window.__hooked){HTMLInputElement.prototype.click=function(){ if(this.type==='file'){window.__lastFileInput=this;return;} return o.apply(this,arguments)}; window.__hooked=true}
3. find "Add photo/video" and left_click it by ref (a REAL click; JS .click() does not trigger it).
4. javascript_exec — load slides via the relay and attach them (replace DATE and N):
   const inp=window.__lastFileInput; const names=[...Array(N)].map((_,i)=>'posts/DATE/slide-'+String(i+1).padStart(2,'0')+'.jpg');
   const items=await new Promise((res,rej)=>{const f=document.createElement('iframe');f.style.display='none';f.src='https://teapleez.github.io/homeswithdylan-posts/relay.html?t='+Date.now();const t=setTimeout(()=>rej(new Error('relay timeout')),20000);window.addEventListener('message',function h(e){if(e.origin!=='https://teapleez.github.io')return;if(e.data.type==='ready'){f.contentWindow.postMessage({type:'get',files:names},'https://teapleez.github.io')}else{clearTimeout(t);window.removeEventListener('message',h);f.remove();e.data.type==='files'?res(e.data.items):rej(new Error(e.data.message))}});document.body.appendChild(f)});
   const dt=new DataTransfer(); for(const it of items) dt.items.add(new File([it.buf],it.name,{type:'image/jpeg'}));
   inp.files=dt.files; if(!document.contains(inp)){inp.style.display='none';document.body.appendChild(inp)}
   inp.dispatchEvent(new Event('input',{bubbles:true})); inp.dispatchEvent(new Event('change',{bubbles:true}));
   await new Promise(r=>setTimeout(r,6000)); (document.body.innerText.match(/1080 x 1350/g)||[]).length   // must equal N
   If the relay 404s, Pages hasn't redeployed yet: wait 60 s and retry (up to ~8 min).
5. Post to: open the "Post to" combobox; if a Facebook Page is listed, tick it too. (As of Nov 18 2026 only Instagram homeswithdylan is connected.)
6. find "dialogue box" (the Text combobox), left_click it, then computer type the full caption. Verify with get_page_text.
7. find the switch "Set date and time" and click it (if it is still off, click the toggle by coordinate after a screenshot).
8. Date: triple_click the date field (placeholder mm/dd/yyyy) to open the calendar, click the day number. Verify value e.g. "Nov 19, 2026".
9. Time: spinbuttons labelled hours / minutes / meridiem. Click hours and type the hour digit(s); click minutes and press ArrowDown/ArrowUp (repeat) until aria-valuenow is right (typing digits does NOT work for minutes); click meridiem and type A or P. Verify via javascript: [...document.querySelectorAll('[role=spinbutton]')].map(e=>e.getAttribute('aria-label')+'='+(e.getAttribute('aria-valuetext')||e.getAttribute('aria-valuenow')))
10. Screenshot to confirm the preview shows the cover slide first, then click the blue "Schedule" button.
11. The composer may sit on "Scheduling your post… / We're having trouble completing your request" — do NOT click Schedule again. Wait ~20 s, then open the Planner (https://business.facebook.com/latest/content_calendar) and confirm the post is shown at the right day/time. Only if it is missing after 2 minutes, redo the post once.
Never publish immediately; never schedule anything without Dylan's OK.
