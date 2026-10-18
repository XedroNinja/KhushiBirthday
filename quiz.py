"""Builds quiz.json for the never-ending quiz: real, single-line, loving/caring messages, balanced between us.
Each item: [id, who (0 Khushi, 1 Harshil), date, text]. Run after explore.py."""
import pickle,re,json,random
rows=pickle.load(open('rows.pkl','rb'))
K='Khushi Verma'
sysx=re.compile(r'call|omitted|attached|deleted|http|www\.',re.I)
LV=re.compile(r"love|luv|miss|\bcare|cute|pyar|pyari|proud|babu|baby|cutu|thank|sleep well|hug|kiss|beautiful|pretty|smart|sundar|♥|❤|🫶|😘|🥰|🤗",re.I)
triv=re.compile(r"^(good ?(morning|night)|gm|gn|ok+|hmm+|haan|hn|yes|no)\b[^a-z]*$",re.I)
seen=set();pool={0:[],1:[]}
for r in rows:
    t=r[2].strip()
    if '\n' in t or not 18<=len(t)<=88 or sysx.search(t) or triv.match(t) or not LV.search(t):continue
    key=re.sub(r'[^a-z]','',t.lower())
    if len(key)<8 or key in seen:continue
    seen.add(key);pool[0 if r[1]==K else 1].append((r[0].strftime('%Y-%m-%d'),t))
random.seed(11)
n=min(len(pool[0]),len(pool[1]),1400)
items=[]
for w in(0,1):
    random.shuffle(pool[w]);items+=[(w,d,t) for d,t in pool[w][:n]]
random.shuffle(items)
out=[[i,w,d,t] for i,(w,d,t) in enumerate(items)]
open('quiz.json','w',encoding='utf8').write(json.dumps(out,ensure_ascii=False,separators=(',',':')))
print('questions per person',n,'| total messages',len(out),'| questions (x2 types)',len(out)*2)
