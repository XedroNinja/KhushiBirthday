"""Builds diary.json: every day of the chat, for the in-site diary and 'On this day'. Run after explore.py."""
import pickle,re,json
rows=pickle.load(open('rows.pkl','rb'))
K='Khushi Verma'
def conv(t):
    t=t.replace('\u200e','').strip()
    if re.search(r'Messages and calls are end-to-end',t):return None
    m=re.match(r'<attached: .*?-(AUDIO|PHOTO|STICKER|VIDEO|GIF)-',t)
    if m:return {'AUDIO':'voice note','PHOTO':'photo','STICKER':'sticker','VIDEO':'video','GIF':'GIF'}[m.group(1)],1
    if re.match(r'^(image|video|audio|sticker|GIF) omitted$',t):return {'image':'photo','video':'video','audio':'voice note','sticker':'sticker','GIF':'GIF'}[t.split()[0]],1
    m=re.match(r'^(Voice|Video) call, (\d+) (sec|min|hr)',t)
    if m:return f'{m.group(1)} call, {m.group(2)} {m.group(3)}',1
    if re.match(r'^(Missed )?(voice |video )?(Voice |Video )?call|^(Voice|Video|Group) call',t,re.I):return 'Missed call',1
    if 'deleted this message' in t or 'message was deleted' in t:return 'message deleted',1
    return t[:400],0
D={}
for r in rows:
    c=conv(r[2])
    if not c:continue
    e=[r[0].strftime('%H%M'),0 if r[1]==K else 1,c[0]]
    if c[1]:e.append(1)
    D.setdefault(r[0].strftime('%Y-%m-%d'),[]).append(e)
s=json.dumps(D,ensure_ascii=False,separators=(',',':'))
open('diary.json','w',encoding='utf8').write(s)
print(len(D),'days',round(len(s.encode())/1e6,2),'MB')
