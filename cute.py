"""Builds cute.js: small real details from the chat, shown under each page's charts.
Every quote is looked up in _chat.txt (script stops if one cannot be found). Run after explore.py."""
import pickle,re,json,collections as C,datetime as dt
rows=pickle.load(open('rows.pkl','rb'))
K='Khushi Verma';H='Harshil♥️';nm=lambda w:'khushi' if w==K else 'harshil'
D=lambda d:d.strftime('%Y-%m-%d')
sysx=re.compile(r'call|omitted|attached|deleted|http|Messages and calls')
txt=lambda r:not sysx.search(r[2])
def cut(t):
    t=t.replace('\n',' ').strip()
    return t if len(t)<=150 else t[:150].rsplit(' ',1)[0]+'...'
def Q(d,who,start):
    for r in rows:
        if D(r[0])==d and r[1]==who and r[2].startswith(start):
            return {'k':'q','who':nm(who),'d':d,'t':cut(r[2])}
    raise SystemExit('NOT FOUND '+d+' '+start)
def Fq(r):return {'k':'q','who':nm(r[1]),'d':D(r[0]),'t':cut(r[2])}
F=lambda t:{'k':'f','t':t}
n=lambda x:f'{x:,}'
MO=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
dl=lambda d:f"{int(d[8:])} {MO[int(d[5:7])-1]} {d[:4]}"
C_={}
# calls
fc=next(r for r in rows if re.match(r'^\u200e?(Video|Voice) call, \u200e?\d+',r[2]))
m=re.match(r'^\u200e?(Video|Voice) call, \u200e?(\d+) (\w+)',fc[2])
first_call=F(f"Our first call in the chat: a {m.group(1).lower()} call on {dl(D(fc[0]))}, {m.group(2)} {m.group(3)}.")
gm=lambda w:next(r for r in rows if r[1]==w and re.search(r'good morning',r[2],re.I))
gmk,gmh=gm(K),gm(H)
# streak start
ss=next(r for r in rows if D(r[0])=='2023-10-28' and txt(r))
# busiest month and day
days=C.Counter(D(r[0]) for r in rows);mon=C.Counter(r[0].strftime('%Y-%m') for r in rows);mon.pop('2026-10',None)
bm=mon.most_common(1)[0][0];bmr=next(r for r in rows if r[0].strftime('%Y-%m')==bm and txt(r))
bd=days.most_common(1)[0][0];bdr=[r for r in rows if D(r[0])==bd and txt(r)]
# midnight
mid={w:sum(1 for r in rows if r[1]==w and r[0].hour==0 and r[0].minute==0 and txt(r)) for w in(K,H)}
# hearts
hr=re.compile('[\u2764\u2665\U0001F495\U0001F496\U0001F497\U0001F498\U0001F49E\U0001F493\U0001F49D\U0001FAF6]')
hd=C.Counter();[hd.update({D(r[0]):len(hr.findall(r[2]))}) for r in rows if r[1]==K]
hday,hn=hd.most_common(1)[0]
# quiet run
alld=sorted(days);d0=dt.date.fromisoformat(alld[0]);d1=dt.date.fromisoformat(alld[-1])
sil=[d0+dt.timedelta(i) for i in range((d1-d0).days+1) if str(d0+dt.timedelta(i)) not in days]
best=(0,None);cur=[]
for d in sil+[None]:
    if d and cur and (d-cur[-1]).days==1:cur.append(d)
    elif d and not cur:cur=[d]
    else:
        if len(cur)>best[0]:best=(len(cur),cur[0],cur[-1])
        cur=[d] if d else []
qn,qa,qb=best
after=next(r for r in rows if r[0].date()>qb and txt(r))
# thresholds, words
n100=sum(1 for v in days.values() if v>=100);n500=sum(1 for v in days.values() if v>=500)
words={w:sum(len(r[2].split()) for r in rows if r[1]==w and txt(r)) for w in(K,H)}
fl=lambda d:[r for r in rows if D(r[0])==d and txt(r)]
C_['Day one']=[Q('2023-06-29',K,'Oho kisi ne nhi bola'),first_call]
C_['Every single day']=[F(f"The 543-day streak began on 28 Oct 2023. The first thing said that day:"),Fq(ss)]
C_['Our months']=[F(f"{MO[int(bm[5:])-1]} {bm[:4]} was our loudest month. It began with:"),Fq(bmr)]
C_['When we talk']=[F(f"Messages sent in the very first minute after midnight: Khushi {mid[K]}, Harshil {mid[H]}. Like this, on New Year 2024:"),Q('2024-01-01',K,'I’ve gotten so much more')]
C_['Late nights']=[Q('2023-11-22',K,'Sleep well and properly'),Q('2025-09-24',K,'So jaaa babu')]
C_['Calls']=[first_call]
C_['Good mornings, good nights']=[F(f"Our first \"good morning\"s: hers on {dl(D(gmk[0]))}, mine on {dl(D(gmh[0]))}." if D(gmk[0])!=D(gmh[0]) else f"We both said our first \"good morning\" on the same day, {dl(D(gmk[0]))}."),Q('2024-06-18',K,'Good morning baby'),Q('2023-11-16',H,'good night khushi')]
fd={}
for r in rows:fd.setdefault(D(r[0]),r[1])
def run(w):
    b=(0,'');c=0;st=''
    prev=None
    for d in sorted(fd):
        if prev and (dt.date.fromisoformat(d)-dt.date.fromisoformat(prev)).days!=1:c=0
        prev=d
        if fd[d]==w:
            if c==0:st=d
            c+=1
            if c>b[0]:b=(c,st)
        else:c=0
    return b
rk,rh=run(K),run(H)
C_['Who says hi first']=[F(f"Most days in a row that Khushi sent the first message: {rk[0]}, starting {dl(rk[1])}."),F(f"Mine: {rh[0]}, starting {dl(rh[1])}.")]
C_['How she looks after me']=[Q('2024-07-31',K,'So jao baby thoda aaram'),Q('2024-09-10',K,'Please take care'),Q('2025-11-23',K,'Please jake so jana')]
C_['I love you, I miss you']=[Q('2023-11-09',H,'i miss you more'),Q('2023-11-30',K,'I miss you toooo'),Q('2023-11-02',H,'i do miss your khi khi')]
C_['Hearts and emojis']=[F(f"Her most-hearted day: {dl(hday)}, with {n(hn)} hearts in her messages.")]
C_['Sorry and gussa']=[Q('2024-07-21',K,'Koi sorry ki need nhi babu'),Q('2024-07-09',K,'Hnji sorry baby')]
C_['The quiet days']=[F(f"Our longest quiet stretch was {qn} days, {dl(str(qa))} to {dl(str(qb))}. Then we were back.")]
C_['Dates that matter']=[F("The first I love you from each of us:"),Q('2024-06-03',H,'I love youuu'),Q('2024-06-16',K,'I love you too')]
C_['Every day, in color']=[F(f"Days with 100 or more messages: {n(n100)}. With 200 or more: {n(sum(1 for v in days.values() if v>=200))}. Our record: {n(max(days.values()))} in one day.")]
C_['Busiest days, fastest replies']=[F(f"On our busiest day, {dl(bd)}, the first message was:"),Fq(bdr[0]),F("And the last:"),Fq(bdr[-1])]
C_['Year by year']=[F('How the next two new years began with her:'),Q('2025-01-01',K,'I love you too babbyy'),Q('2026-01-01',K,'Happy new year harshil')]
C_['Her clock, my clock']=[F(f"She sent {n(sum(1 for r in rows if r[1]==K and r[0].hour<5 and txt(r)))} messages between 12 and 5 am. I sent {n(sum(1 for r in rows if r[1]==H and r[0].hour<5 and txt(r)))}.")]
C_['The whole thing']=[F(f"Words typed in the chat: Khushi {n(words[K])}, Harshil {n(words[H])}.")]
json.dump(C_,open('cute.json','w'),ensure_ascii=False,indent=1)
open('cute.js','w',encoding='utf8').write('window.CUTE='+json.dumps(C_,ensure_ascii=False,separators=(',',':'))+';')
for k,v in C_.items():print(k,'|',' || '.join((x['t'] if x['k']=='f' else x['who'][:1]+':'+x['t'])[:90] for x in v))
