from datetime import datetime, timedelta
import os,sys,html2text,cv2
import urllib.parse
import html,re,time,markdown,json
import rg

n=0

def english2date(a):
    d=re.findall('\d+',a)
    y=d[0]
    dd=d[1]
    mo=a.split(' ')[1]
    m=['January','February','March','April','May','June','July','August','September','October','November','December']
    for b in range(len(m)):
        if mo==m[b]:
            mo=b+1
    return'-'.join([y,str(mo).rjust(2).replace(' ','0'),dd.rjust(2).replace(' ','0')])

l='https://www.bannedthought.net/RecentPostings.htm'
l2='https://www.bannedthought.net'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hp=html2text.HTML2Text()
hl=[]
if not os.path.exists(pa:='RecentPostings.md.bin'):
    h=rg.rget(l,60)
    h.encoding='utf-8'
    h=h.text
    h=h.split('''<br>
<hr>
<br>''')[1].split('</blockquote>')[0]
    h=[hp.handle(b.split('</li>')[0]).strip()for b in h.split('<li>')[1:]]
    hl.extend(h)
    f=open(pa,'w+');f.write(repr(h));f.close()
else:
    f=open(pa,'r');h=eval(f.read());f.close()
    hl.extend(h)
print('\n'.join(hl))
if not os.path.exists('JSON-src'):os.mkdir('JSON-src')
dr=os.listdir('JSON-src')
if len(dr)==0:
    n=0
    ed=''
    for a in range(len(hl)):
        h=hl[a]
        h={'time':english2date(h.split(' — ')[0]),
           'text':' — '.join(h.split(' — ')[1:]),
           'source':l
          }
        h['text']='\n\n'.join([z.replace('\n','').strip()for z in h['text'].split('\n\n')if z])
        ht=h['text']
        t2=ht.split('](')
        t3=''
        for c in range(len(t2)):
            if c==0:
                t3=t2[c]
            else:
                t3='%s](%s)%s'%(t3,
                                'https://www.bannedthought.net/%s'%u if'http'!=(u:=t2[c].split(')')[0])[:4]else u,
                                ')'.join(t2[c].split(')')[1:]))
        h['text']=t3
        t2=''
        t4=h['text'].split('(')
        for z in range(len(t4)):
            if z==0:
                t2=t4[z]
            else:
                if')'in t4[z]:
                    url=t4[z].split(')')[0];hc=True
                else:
                    url=t4[z];hc=False
                t2='%s(%s%s%s'%(t2,'%s%s'%(l2,url)if(url[0]in['/','.'])and('http'not in url)else url,')'if hc else'',')'.join(t4[z].split(')')[1:]))
        h['text']=t2
        dd=h['time']
        if ed:
            if ed!=dd:
                n=0
        h['time']='%sT%s:00:00-04:00'%(h['time'],str(99-n).rjust(2).replace(' ','0'))
        ed=dd
        if dd<d:break
        if not os.path.exists(pa:='JSON-src/%s.json'%h['time']):
            print(h)
            f=open(pa,'w+');f.write(repr(h));f.close()
        else:
            if'up'in locals():
                if h['text']!=up:
                    while True:
                        h['time']='%sT%s:%s'%(h['time'].split('T')[0],
                                                      str(int(h['time'].split('T')[1].split(':')[0])+1),
                                                      ':'.join(h['time'].split('T')[1].split(':')[1:]))
                        if not os.path.exists(pa:='JSON-src/%s.json'%h['time']):
                            break
                    print(h)
                    f=open(pa,'w+');f.write(repr(h));f.close()
                else:print(h['time'],'已经完成下载。')
        n+=1
        up=h['text']
        n+=1
if not os.path.exists('MDs'):os.mkdir('MDs')
if not os.path.exists('HTMs'):os.mkdir('HTMs')
for a in os.walk('JSON-src'):
    for b in a[2]:
        f=open('%s/%s'%(a[0],b),'rb');h=eval(f.read().decode(errors='ignore'));f.close()
        t='''# BANNEDTHOUGHT - Time: %s

<!--METADATA-->

%s

Source: %s'''%(h['time'],
               h['text'],
               '[%s](%s)'%(h['source'],h['source']))
        if not os.path.exists(pa1:='MDs/%s.md'%b.split('.json')[0]):
            f=open(pa1,'w+');f.write(t);f.close()
            print(h['time'],'转换为MD完毕。')
        else:print(h['time'],'已经转换为MD。')
        if not os.path.exists(pa:='HTMs/%s.htm'%b.split('.json')[0]):
            f=open(pa,'w+');f.write(markdown.markdown(t));f.close()
            print(h['time'],'转换为HTM完毕。')
        else:print(h['time'],'已经转换为HTM。')
