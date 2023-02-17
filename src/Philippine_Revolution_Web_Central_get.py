from datetime import datetime, timedelta
import os,sys,html2text,cv2
import urllib.parse,markdown,re,html
import rg

n=0

def english2date(a):
    d=re.findall('\d+',a)
    dd=d[0]
    y=d[1]
    mo=a.split(' ')[0].title()
    m=['January','February','March','April','May','June','July','August','September','October','November','December']
    for b in range(len(m)):
        if mo==m[b]:
            mo=b+1
    return'-'.join([y,str(mo).rjust(2).replace(' ','0'),dd.rjust(2).replace(' ','0')])

pg=['category/about-us','statements','angbayan','category/publications','category/resources']
l='https://philippinerevolution.nu/'
l2='https://philippinerevolution.nu'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hl={}
no=False
for z in pg:
    if z not in hl:hl[z]=[]
    z2=z.replace('/','-')
    if not os.path.exists('%s_000000.list'%z2):
        no=True
        for a in range(5):
            h=rg.rget('%s/%s/page/%d'%(l,z,a+1)).text
            h=h.split('<div class="archives">')[1].split('<div class="pagination">')[0]
            h=[b.split('"')[0]for b in h.split('<a class="archiveitem" href="')[1:]]
            hl[z].extend(h)
            f=open('%s_%s.list'%(z2,str(a).rjust(6).replace(' ','0')),'w+');f.write(repr(h));f.close()
if not no:
    for z in pg:
        if z not in hl:hl[z]=[]
        z2=z.replace('/','-')
        fl=[]
        for a in os.walk(sys.path[0]):
            for b in a[2]:
                if a[0]==sys.path[0]:
                    if b[-4:]=='list':
                        if b[:len(z2)]==z2:
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
    n=0
    ed=''
    for u in hl.keys():
        thl=hl[u]
        for a in range(len(thl)):
            print(thl[a])
            h=rg.rget(thl[a]).text
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
               'publish time':(h.split(sp)[1].split('"')[0]if(sp:='<meta property="article:published_time" content="')in h else english2date(h.split('<div class="article__date">')[1].split('</div>')[0].strip())).strip(),
               'modified time':h.split(sp)[1].split('"')[0]if(sp:='<meta property="article:modified_time" content="')in h else'None',
               'author':h.split(sp)[1].split('"')[0]if(sp:='<meta name="author" content="')in h else'Philippine Revolution Web Central',
               'images':[html.unescape(b.split('src="')[1].split('"')[0].split('?')[0]).strip()for b in h2.split('<img')[1:]],
               'text':hp.handle(h2),
               'categories':[b.split('<')[0]for b in h.split(sp)[1].split('</div>')[0].split('rel="tag">')[1:]]if(sp:='<div class="article__categories">')in h else None,
               'source':thl[a]
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
            if len(dd)==10:
                if ed:
                    if ed!=dd:
                        n=0
                h['publish time']='%sT%s:00:00-04:00'%(h['publish time'],str(99-n).rjust(2).replace(' ','0'))
                ed=dd
            if dd<d:break
            if not os.path.exists(pa:='JSON-src/%s.json'%h['publish time']):
                print(h)
                f=open(pa,'w+');f.write(repr(h));f.close()
            else:
                if'up'in locals():
                    if h['text']!=up:
                        while True:
                            n+=1
                            h['publish time']='%sT%s:%s'%(h['publish time'].split('T')[0],
                                                          str(int(h['publish time'].split('T')[1].split(':')[0])-n),
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
