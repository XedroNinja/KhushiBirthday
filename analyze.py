import re,json,pickle,collections as C,datetime as dt,random
rows=pickle.load(open('rows.pkl','rb'))
K='Khushi Verma';H='Harshil♥️'
nm=lambda w:'khushi' if w==K else 'harshil'
D=lambda d:d.strftime('%Y-%m-%d')
out={}
out['meta']={'total':len(rows),'first':D(rows[0][0]),'last':D(rows[-1][0]),'by':{nm(w):sum(r[1]==w for r in rows) for w in(K,H)}}
days=C.Counter(D(r[0]) for r in rows)
out['daily']=dict(sorted(days.items()))
d0=rows[0][0].date();d1=rows[-1][0].date()
alld=[d0+dt.timedelta(i) for i in range((d1-d0).days+1)]
out['meta']['span_days']=len(alld);out['meta']['active_days']=len(days)
best=cur=0;bs=None;cs=None
for d in alld:
    if D(d) in days:
        if cur==0:cs=d
        cur+=1
        if cur>best:best=cur;bs=cs
    else:cur=0
out['meta']['streak']=best;out['meta']['streak_start']=D(bs)
out['silent_days']=[D(d) for d in alld if D(d) not in days]
mon={}
for r in rows:
    m=r[0].strftime('%Y-%m');mon.setdefault(m,{'khushi':0,'harshil':0})[nm(r[1])]+=1
out['monthly']=dict(sorted(mon.items()))
hm={'khushi':[[0]*24 for _ in range(7)],'harshil':[[0]*24 for _ in range(7)]}
for r in rows:hm[nm(r[1])][r[0].weekday()][r[0].hour]+=1
out['heat']=hm
# calls
cal=[];cm=C.Counter();
for r in rows:
    m=re.match(r'^\u200e?(Video|Voice) call, \u200e?(\d+) (sec|min|hr|hour)',r[2])
    if m:
        n=int(m.group(2));s=n*(1 if m.group(3)=='sec' else 3600 if m.group(3) in('hr','hour') else 60)
        cal.append((r[0],m.group(1),s))
tot=sum(c[2] for c in cal)
lc=max(cal,key=lambda c:c[2])
cmo={}
for d,t,s in cal:
    x=cmo.setdefault(d.strftime('%Y-%m'),{'n':0,'h':0});x['n']+=1;x['h']+=s/3600
out['calls']={'n':len(cal),'video':sum(c[1]=='Video' for c in cal),'hours':round(tot/3600,1),'longest_min':round(lc[2]/60),'longest_date':D(lc[0]),'monthly':{k:{'n':v['n'],'h':round(v['h'],1)} for k,v in sorted(cmo.items())}}
# keyword by month by person
def kw(rx):
    res={'khushi':C.Counter(),'harshil':C.Counter()}
    for r in rows:
        if re.search(rx,r[2],re.I):res[nm(r[1])][r[0].strftime('%Y-%m')]+=1
    return {w:{'total':sum(c.values()),'monthly':dict(sorted(c.items()))} for w,c in res.items()}
RX={'love':r'love you|luv u|love u|i love','miss':r'miss you|miss u|yaad','sorry':r'sorry|maaf','gussa':r'gussa|naraz|naaraz','gm':r'good morning|\bgm\b','gn':r'good night|\bgn\b','khana':r'khana|khaya|khaa liya|kha liya','sojao':r'so ja|sojao|so jao|so jaa','reach':r'reach','dawai':r'dawai|medicine|tablet|dawa\b','paani':r'paani|pani piyo|water','tc':r'take care|tc\b'}
out['kw']={k:kw(v) for k,v in RX.items()};out['rx']=RX
# late night 0-5am
out['night']={w:sum(1 for r in rows if nm(r[1])==w and r[0].hour<5) for w in('khushi','harshil')}
# emojis
em=re.compile('[\U0001F300-\U0001FAFF\u2600-\u27BF\u2764]')
for w in(K,H):
    c=C.Counter(e for r in rows if r[1]==w for e in em.findall(r[2]))
    out.setdefault('emoji',{})[nm(w)]=c.most_common(8)
# who texts first each day, and first-of-year
fd={};
for r in rows:fd.setdefault(D(r[0]),r[1])
out['first_texter']={nm(w):sum(v==w for v in fd.values()) for w in(K,H)}
# comebacks: gaps >=20h
txt=[r for r in rows if not re.search(r'(Video|Voice) call|omitted|attached|deleted',r[2])]
gaps=[]
for a,b in zip(rows,rows[1:]):
    g=(b[0]-a[0]).total_seconds()/3600
    if g>=20:gaps.append((g,a,b))
gaps.sort(key=lambda x:-x[0])
cb=[]
for g,a,b in gaps[:30]:
    nxt=next((r for r in rows if r[0]>=b[0] and not re.search(r'call|omitted|attached|deleted',r[2]) and len(r[2])>3),b)
    cb.append({'hours':round(g),'from':D(a[0]),'back':D(b[0]),'who':nm(b[1]),'text':nxt[2][:90]})
out['comebacks']=cb
out['day1']=[{'who':nm(r[1]),'t':r[2][:80]} for r in rows[:14] if 'omitted' not in r[2] and 'attached' not in r[2]]
# notes pool: Khushi's short sweet lines
pat=re.compile(r'love you|miss you|take care|proud|i am here|mai hu na|you are the best|always with you',re.I)
pool=[r for r in rows if r[1]==K and pat.search(r[2]) and 12<=len(r[2])<=80 and '\n' not in r[2]]
random.seed(7);random.shuffle(pool);pool=sorted(pool[:60],key=lambda r:r[0])
out['notes']=[{'t':r[2],'d':D(r[0])} for r in pool]
# milestone day counts
for k in('2023-11-18','2024-08-01','2023-08-01'):out.setdefault('mile',{})[k]=days.get(k,0)
# trip candidates
tr=C.Counter(D(r[0]) for r in rows if re.search(r'trip|manali|goa|train|flight',r[2],re.I) and '2024-04'<=D(r[0])<='2024-09')
out['trip_cands']=tr.most_common(8)
def first(who,rx,after=0):
    for r in rows:
        if r[1]==who and re.search(rx,r[2],re.I):return r
F=[]
def add(r,tag,u,who):F.append({'who':nm(who),'d':D(r[0]),'t':r[2].strip().replace('\n',' ')[:90],'tag':tag,'u':u})
add(rows[1],'the very first message',"2026-10-05",H)
add(rows[2],'her first words to me',"2026-10-05",K)
add(first(H,r'looking cute'),'the first time I called you cute',"2026-10-06",H)
add(first(H,r'date pe'),'the first time we said "date"',"2026-10-07",H)
add(first(H,r'miss you'),'the first time I said miss you',"2026-10-08",H)
add(first(K,r'miss you|miss u\b'),'her first miss you',"2026-10-09",K)
add(first(H,r'^I love youuu$'),'the first I love you in our chat',"2026-10-10",H)
add(first(K,r'\b(love|luv|lub)\s+(you|u|uu|youu|uuu)\b'),'her first I love you',"2026-10-11",K)
out['firsts']=F
s=json.dumps(out,ensure_ascii=False,separators=(',',':'));open('data.js','w').write('window.DATA='+s+';')
print({k:out[k] for k in('meta','night','first_texter','mile','trip_cands')},out['calls']['n'],out['calls']['hours'],out['calls']['longest_min'],out['emoji'],out['kw']['love'].keys())
for c in cb[:6]:print(c)
for n in out['notes'][:6]:print(n)
