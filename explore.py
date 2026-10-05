import re,collections,datetime as dt
P=re.compile(r'^\u200e?\[(\d+)/(\d+)/(\d+),\s+(\d+):(\d+):(\d+)\s*([AP]M)\]\s+([^:]+?):\s(.*)$')
rows=[];cur=None
for l in open('_chat.txt',encoding='utf8'):
    l=l.rstrip('\r\n')
    m=P.match(l)
    if m:
        mo,d,y,h,mi,s,ap,who,t=m.groups();h=int(h)%12+(12 if ap=='PM' else 0)
        cur=[dt.datetime(2000+int(y),int(mo),int(d),h,int(mi),int(s)),who,t];rows.append(cur)
    elif cur: cur[2]+='\n'+l
print(len(rows),collections.Counter(r[1] for r in rows))
import pickle;pickle.dump(rows,open('rows.pkl','wb'))
def cnt(k,who=None):
    return collections.Counter(r[1] for r in rows if re.search(k,r[2],re.I))
for k in ['good morning|gm\\b','good night|gn\\b','miss you|miss u|yaad','love you|luv u|love u|i love','sorry|maaf','gussa|naraz|naaraz','ragebait|rage bait','trip|manali|goa','khana|khaya','so ja|sojao','bye','block','bhai|jaan|baby|babu|cutu|shona']:
    print(k,dict(cnt(k)))
print(collections.Counter(r[2].split(',')[0] for r in rows if re.match(r'.*(Video|Voice) call',r[2])))
for k in ['2023-11-18','2024-08-01','2023-08-01']:
    x=[r for r in rows if r[0].strftime('%Y-%m-%d')==k];print(k,len(x),[r[2][:50] for r in x[:6]])
