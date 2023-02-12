from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
import os,sys,html2text,cv2
import urllib.parse
import html,re,markdown
import rg

n=0

d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
td=str(datetime.today()).split(' ')[0]
y1=int(td.split('-')[0])
y2=int(d.split('-')[0])
m1=int(td.split('-')[1])
m2=int(d.split('-')[1])
if y1!=y2 or m1!=m2:
    y=y1-y2
    if y==0:
        tl=['%d/%s'%(y1,str(m1-a).rjust(2).replace(' ','0'))for a in range(m1-m2+1)]
    else:
        tl=['%d/%s'%(y1,str(m1-a).rjust(2).replace(' ','0'))for a in range(m1)]
        for a in range(y-1):
            for b in range(12):
                tl.append('%d/%s'%(y1-a-1,str(12-b).rjust(2).replace(' ','0')))
        tl.extend(['%d/%s'%(y1-y,str(12-a).rjust(2).replace(' ','0'))for a in range(13-m2)])
else:tl=['%d/%s'%(y1,str(m1).rjust(2).replace(' ','0'))]
print(tl)
l='https://philippinerevolution.nu/'
l2='https://philippinerevolution.nu'
hl=[]
ed=[]
a=0
if not os.path.exists('000000.list'):
    while a<5:
        for b in tl:
            if b not in ed:ed.append(b)
            else:continue
            n=0
            while True:
                n+=1
                h=rg.rget(li:='%s%s/page/%d'%(l,b,n)).text
                if'<body class="error404">'in h:
                    break
                h=h.split('<div class="archives">')[1].split('<div class="pagination">')[0]
                h=[c.split('"')[0]for c in h.split('<a class="archiveitem" href="')[1:]]
                f=open('%s.list'%(str(a).rjust(6).replace(' ','0')),'w+');f.write(repr(h));f.close()
                hl.extend(h)
                a+=1
                if a==5:break;break;break
        dt=datetime.strptime('%s/01 00:00:00'%b, '20%y/%m/%d %H:%M:%S')
        ft=dt-relativedelta(months=1)
        tl.append('/'.join(str(ft).split('-')[:2]))
else:
    fl=[]
    for a in os.walk(sys.path[0]):
        for b in a[2]:
            if a[0]==sys.path[0]:
                if b[-4:]=='list':
                    fl.append([int(b[:-5]),'%s/%s'%(a[0],b)])
    fl.sort(key=lambda x:x[0])
    fl=[a[1]for a in fl]
    for a in fl:
        f=open(a,'r');h=eval(f.read());f.close()
        hl.extend(h)
print('\n'.join(hl))
if not os.path.exists('JSON-src'):os.mkdir('JSON-src')
dr=os.listdir('JSON-src')
if len(dr)==0:
    hp=html2text.HTML2Text()
    n=0
    for a in range(len(hl)):
        h=rg.rget(hl[a]).text
        if not os.path.exists('test.txt'):f=open('test.txt','w+');f.write(h);f.close()
        if(sp:='<div class="article__image article')in h:
            h2='>'.join(h.split(sp)[1].split('>')[1:]).split('</div>')[0]
        elif(sp:='<div class="ablogo">')in h:
            h2=h.split(sp)[1].split('</div>')[0]
        else:
            raise TypeError
        h3='</div>'.join(h.split("<div class='article__content'>")[1].split('<div class="sb_hide_show">')[0].split('</div>')[:-1])
        h2='%s\n%s'%(h2,h3)
        h={'title':h.split('<meta property="og:title" content="')[1].split('"')[0].strip(),
           'description':h.split(sp)[1].split('"')[0].strip()if(sp:='<meta property="og:description" content="')in h else None,
           'type':h.split('<meta property="og:type" content="')[1].split('"')[0].strip(),
           'publish time':h.split('<meta property="article:published_time" content="')[1].split('"')[0],
           'modified time':h.split(sp)[1].split('"')[0]if(sp:='<meta property="article:modified_time" content="')in h else'None',
           'author':h.split('<meta name="author" content="')[1].split('"')[0],
           'images':[html.unescape(b.split('src="')[1].split('"')[0].split('?')[0]).strip()for b in h2.split('<img')[1:]],
           'text':hp.handle(h2),
           'categories':[b.split('<')[0]for b in h.split(sp)[1].split('</div>')[0].split('rel="tag">')[1:]]if(sp:='<div class="article__categories">')in h else None,
           'source':hl[a]
          }
        h['text']='\n\n'.join([z.replace('\n','').strip()for z in h['text'].split('\n\n')if z])
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
        dd=h['publish time']
        if dd<d:break
        if not os.path.exists(pa:='JSON-src/%s.json'%h['publish time']):
            print(h)
            f=open(pa,'w+');f.write(repr(h));f.close()
        else:
            if'up'in locals():
                if h['text']!=up:
                    while True:
                        h['publish time']='%sT%s:%s'%(h['publish time'].split('T')[0],
                                                      str(int(h['publish time'].split('T')[1].split(':')[0])+1),
                                                      ':'.join(h['publish time'].split('T')[1].split(':')[1:]))
                        if not os.path.exists(pa:='JSON-src/%s.json'%h['publish time']):
                            break
                    print(h)
                    f=open(pa,'w+');f.write(repr(h));f.close()
                else:print(h['publish time'],'已经完成下载。')
        n+=1
        up=h['text']
        n+=1
if not os.path.exists('Images'):os.mkdir('Images')
imgs=[]
for a in os.walk('JSON-src'):
    for b in a[2]:
        f=open('JSON-src/%s'%b,'r');h=eval(f.read());f.close()
        imgs.append([h['publish time'].replace(':','-').replace('+','-'),h['images']])
for a in imgs:
    for z in a[1]:
        if not os.path.exists(pa:='Images/%s/%s'%(a[0],urllib.parse.unquote(z).split('/')[-1].split('?')[0])):
            if not os.path.exists(pa2:='/'.join(pa.split('/')[:-1])):
                os.makedirs(pa2)
            try:im=rg.rget(z,st=True).content
            except:continue
            f=open(pa,'wb+');f.write(im);f.close()
            print(pa,'下载完毕。')
        else:print(pa,'已经完成下载。')
if not os.path.exists('ConvertedIMGs'):os.mkdir('ConvertedIMGs')
for a in os.walk('Images'):
    for b in a[2]:
        if'.webp'==b[-5:]:
            if not os.path.exists(pa:='%s/%s'%(a[0].replace('Images','ConvertedIMGs'),b.replace('.webp','.png'))):
                if not os.path.exists(pa2:='/'.join(pa.split('/')[:-1])):
                    os.makedirs(pa2)
                im=cv2.imread('%s/%s'%(a[0],b))
                cv2.imwrite(pa,im)
                print(pa,'转换完毕。')
            else:
                print(pa,'已经完成转换。')
if not os.path.exists('MDs'):os.mkdir('MDs')
if not os.path.exists('HTMs'):os.mkdir('HTMs')
for a in os.walk('JSON-src'):
    for b in a[2]:
        t=''
        f=open('%s/%s'%(a[0],b));h=eval(f.read());f.close()
        ht=re.split('!\[[\w\W]*?]\(',h['text'])
        htc=re.findall('!\[[\w\W]*?]\(',h['text'])
        t2=''
        for z in range(len(ht)):
            if z==0:
                t2=ht[z]
            else:
                url=ht[z].split(')')[0]
                t2='%s%s%s)%s'%(t2,htc[z-1],url.replace('\n','').replace('/'.join(url.replace('\n','').split('/')[:-1]),('../Images/%s'%h['publish time'].replace(':','-').replace('+','-')if'.webp'not in url else'../ConvertedIMGs/%s'%h['publish time'].replace(':','-').replace('+','-')).split('?')[0]).replace('.webp','.png').split('?')[0],')'.join(ht[z].split(')')[1:]))
        t3=t2
        t='''# %s

Author: %s

Publish Time: %s

Modified Time: %s

Description: %s

Images: %s

Categories: %s

Type: %s

<!--METADATA-->

%s

Source: %s'''%(h['title'].replace('\n',' '),
               h['author'],
               h['publish time'],
               h['modified time'],
               co if(co:=h['description'])else'None',
               repr(['[%s](%s)'%(c.split('/')[-1].split('?')[0].replace('\n',''),c)for c in h['images']]),
               repr(h['categories']),
               h['type'],
               t3,
               '[%s](%s)'%(h['source'],h['source']))
        if not os.path.exists(pa1:='MDs/%s.md'%b.split('.json')[0]):
            f=open(pa1,'w+');f.write(t);f.close()
            print(h['publish time'],'转换为MD完毕。')
        else:print(h['publish time'],'已经转换为MD。')
        if not os.path.exists(pa:='HTMs/%s.htm'%b.split('.json')[0]):
            f=open(pa,'w+');f.write(markdown.markdown(t));f.close()
            print(h['publish time'],'转换为HTM完毕。')
        else:print(h['publish time'],'已经转换为HTM。')
