from datetime import datetime, timedelta
import os,sys,html2text,cv2
import urllib.parse,markdown,re
import rg

n=0
pg=['situacao-politica','nacional','luta-pela-terra','internacional','america-latina-2','luta-anti-imperialista','nova-cultura']
l='https://anovademocracia.com.br/'
l2='https://anovademocracia.com.br'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hl={}
no=False
for z in pg:
    if z not in hl:hl[z]=[]
    if not os.path.exists('%s_000000.list'%z):
        no=True
        for a in range(5):
            h=rg.rget('%s/%s/page/%d'%(l,z,a+1)).text
            h=h.split('<h1 class="heading-title-main size-tiny">ÚLTIMAS NOTÍCIAS:</h1>')[1].split('<div class="pagination-inner">')[0]
            h=['%s%s'%(l,b.split('<a href="https://anovademocracia.com.br/')[1].split('"')[0])for b in h.split('<article class="wi-post')[1:]]
            hl[z].extend(h)
            f=open('%s_%s.list'%(z,str(a).rjust(6).replace(' ','0')),'w+');f.write(repr(h));f.close()
if not no:
    for z in pg:
        if z not in hl:hl[z]=[]
        fl=[]
        for a in os.walk(sys.path[0]):
            for b in a[2]:
                if a[0]==sys.path[0]:
                    if b[-4:]=='list':
                        if b[:len(z)]==z:
                            fl.append([int(b[:-5].split('_')[1]),'%s/%s'%(a[0],b)])
        fl.sort(key=lambda x:x[0])
        fl=[a[1]for a in fl]
        for a in fl:
            f=open(a,'r');h=eval(f.read());f.close()
            hl[z].extend(h)
print('\n'.join(hl))
if not os.path.exists('JSON-src'):os.mkdir('JSON-src')
dr=os.listdir('JSON-src')
if len(dr)==0:
    hp=html2text.HTML2Text()
    for u in hl.keys():
        thl=hl[u]
        for a in range(len(thl)):
            h=rg.rget(thl[a]).text
            if not os.path.exists('test.txt'):f=open('test.txt','w+');f.write(h);f.close()
            h2=h.split('<div class="single-body single-section">')[1].split('<span class="share-label">')[0]
            h3=h.split(sp)[1].split('data-src="')[1].split('"')[0]if((sp:='<div class="thumbnail-container">')in h)else None
            h4=h.split(sp)[1].split(sp2)[1].split('</figcaption>')[0]if((sp)and((sp2:='<figcaption class="fox-figcaption">'))in h)else None
            h={'author':h.split('<a class="url fn" itemprop="url" rel="author"')[1].split('>')[1].split('<')[0],
               'publish time':h.split('<meta property="article:published_time" content="')[1].split('"')[0],
               'modified time':h.split('<meta property="article:modified_time" content="')[1].split('"')[0],
               'updated time':h.split('<meta property="og:updated_time" content="')[1].split('"')[0],
               'title':h.split('<meta property="og:title" content="')[1].split('"')[0].strip(),
               'type':h.split('<meta property="og:type" content="')[1].split('"')[0].strip(),
               'description':h.split('<meta property="og:description" content="')[1].split('"')[0].strip(),
               'tags':[c for b in h.split('<meta property="article:tag" content="')[1:]if(c:=b.split('"')[0])],
               'section':h.split('<meta property="article:section" content="')[1].split('"')[0],
               'thumb':h3,
               'thumb caption':h4,
               'images':[('%s%s'%(l2,kl)if l2 not in(kl:=b.split('src="')[1].split('"')[0])else kl)for b in h2.split('<img')[1:]if('src="'in b)],
               'text':hp.handle(h2).strip(),
               'source':thl[a]
              }
            h['text']='\n\n'.join([z.replace('\n','').strip()for z in h['text'].split('\n\n')if z])
            if h3:h['images']=[h3]+h['images']
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
            if h['publish time'].split('T')[0]<d:break
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
        ht=h['thumb'].split('/')[-1].split('?')[0].split('#')[0]
        t='''# %s

Author: %s

Description: %s

Publish Time: %s

Modified Time: %s

Updated Time: %s

Images: %s

Section: %s

Tags: %s

Type: %s

<!--METADATA-->%s%s

%s

Source: %s'''%(h['title'].replace('\n',' '),
               h['author'],
               h['description'],
               h['publish time'],
               h['modified time'],
               h['updated time'],
               repr(['[%s](%s)'%(c.split('/')[-1].split('?')[0].replace('\n',''),c)for c in h['images']]),
               h['section'],
               repr(h['tags']),
               h['type'],
               '\n\n![](%s/%s)'%('../Images/%s'%h['publish time'].replace(':','-').replace('+','-')if'.webp'not in h['thumb'] else'../ConvertedIMGs/%s'%h['publish time'].replace(':','-').replace('+','-'),(ht if not ht[-5:]=='.webp'else'%s.png'%ht[:-5]))if h['thumb']else'',
               '\n\n%s'%h['thumb caption']if h['thumb caption']else'',
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
