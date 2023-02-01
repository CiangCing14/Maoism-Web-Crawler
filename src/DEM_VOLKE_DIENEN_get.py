import requests as r
from datetime import datetime, timedelta
import os,sys,html2text,cv2
import urllib.parse
import html,re,markdown
import rg

l='https://www.demvolkedienen.org/index.php/de/?start='
l2='https://www.demvolkedienen.org'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hl=[]
if not os.path.exists('000000.list'):
    for a in range(5):
        h=rg.rget('%s%d'%(l,a*8)).text.split('<div class="page-header">')[1].split('<div class="pagination">')[0]
        h=[['%s/index.php/de/%s'%(l2,b.split('<a href="/index.php/de/')[1].split('"')[0]),b.split('<time datetime="')[1].split('"')[0]]for b in h.split('<h2 class="item-title" itemprop="name">')[1:]if'<time datetime="'in b]
        hl.extend(h)
        f=open('%s.list'%(str(a).rjust(6).replace(' ','0')),'w+');f.write(repr(h));f.close()
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
print('\n'.join([repr(a)for a in hl]))
if not os.path.exists('JSON-src'):os.mkdir('JSON-src')
dr=os.listdir('JSON-src')
if len(dr)==0:
    hp=html2text.HTML2Text()
    for a in range(len(hl)):
        h=rg.rget(hl[a][0]).text
        if not os.path.exists('test.txt'):f=open('test.txt','w+');f.write(h);f.close()
        h='<div class="page-header">'.join(h.split('<div class="page-header">')[1:]).split('<!--End Content-->')[0].split('<div id="aside"')[0]
        h={'title':h.split('itemprop="name">')[1].split('<')[0].strip(),
           'time':hl[a][1],
           'author':hp.handle(h.split(sp)[1].split('</dd>')[0])if(sp:='<dd class="createdby" itemprop="author" itemscope="" itemtype="http://schema.org/Person">')in h else'DEM VOLKE DIENEN',
           'images':[html.unescape((af)if(af:=b.split('src="')[1].split('"')[0].split('?')[0]).find('//')!=-1 else('https://www.demvolkedienen.org%s'%af))for b in h.split('<img')[1:]if'svg'not in b.split('src="')[1].split('"')[0]],
           'text':hp.handle(h.split(sp if(sp:='<div class="pull-left item-image">')in h else'<div itemprop="articleBody">')[1].split('<dl class="article-info muted">')[0].split('<ul class="tags inline">')[0].split('<ul class="pager pagenav">')[0]).replace('](/index.php','](https://www.demvolkedienen.org/index.php'),
           'tags':[y.split('class="label label-info">')[1].split('</a>')[0].strip()for y in h.split(sp)[1].split('</ul>')[0].split('<li class="tag-')[1:]]if(sp:='<ul class="tags inline">')in h else None,
           'category':h.split(sp)[1].split('</dd>')[0].split('>')[1].split('<')[0]if(sp:='<dd class="category-name">')in h else None,
           'source':hl[a][0]
          }
        t2=''
        t4=h['text'].split('(')
        for z in range(len(t4)):
            if z==0:
                t2=t4[z]
            else:
                url=t4[z].split(')')[0]
                t2='%s(%s)%s'%(t2,'%s%s'%(l2,url)if(url[0]in['/','.'])and('http'not in url)else url,')'.join(t4[z].split(')')[1:]))
        h['text']=t2
        if h['time'].split('T')[0]<d:break
        if not os.path.exists(pa:='JSON-src/%s.json'%h['time']):
            print(h)
            f=open(pa,'w+');f.write(repr(h));f.close()
        else:print(h['time'],'已經完成下載。')
if not os.path.exists('Images'):os.mkdir('Images')
imgs=[]
for a in os.walk('JSON-src'):
    for b in a[2]:
        f=open('JSON-src/%s'%b,'r');h=eval(f.read());f.close()
        imgs.extend(h['images'])
for a in imgs:
    if not os.path.exists(pa:='Images/%s'%urllib.parse.unquote(a).split('/')[-1].split('?')[0]):
        im=rg.rget(a,st=True).content
        f=open(pa,'wb+');f.write(im);f.close()
        print(pa,'下載完畢。')
    else:print(pa,'已經完成下載。')
if not os.path.exists('ConvertedIMGs'):os.mkdir('ConvertedIMGs')
for a in os.walk('Images'):
    for b in a[2]:
        if'.webp'==b[-5:]:
            if not os.path.exists(pa:='ConvertedIMGs/%s'%b.replace('.webp','.png')):
                im=cv2.imread('%s/%s'%(a[0],b))
                cv2.imwrite(pa,im)
                print(pa,'轉換完畢。')
            else:
                print(pa,'已經完成轉換。')
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
                t2='%s%s%s)%s'%(t2,htc[z-1],url.replace('\n','').replace('/'.join(url.replace('\n','').split('/')[:-1]),('../Images'if'.webp'not in url else'../ConvertedIMGs').split('?')[0]).replace('.webp','.png').split('?')[0],')'.join(ht[z].split(')')[1:]))
        t3=t2
        t='''# %s

Author: %s

Time: %s

Images: %s

Tags: %s

Category: %s

<!--METADATA-->

%s

Source: %s'''%(h['title'].replace('\n',' '),
               h['author'],
               h['time'],
               repr(['[%s](%s)'%(c.split('/')[-1].split('?')[0].replace('\n',''),c)for c in h['images']]),
               repr(h['tags']),
               repr(h['category']),
               t3,
               '[%s](%s)'%(h['source'],h['source']))
        if not os.path.exists(pa1:='MDs/%s.md'%b.split('.json')[0]):
            f=open(pa1,'w+');f.write(t);f.close()
            print(h['time'],'轉換為MD完畢。')
        else:print(h['time'],'已經轉換為MD。')
        if not os.path.exists(pa:='HTMs/%s.htm'%b.split('.json')[0]):
            f=open(pa,'w+');f.write(markdown.markdown(t));f.close()
            print(h['time'],'轉換為HTM完畢。')
        else:print(h['time'],'已經轉換為HTM。')
