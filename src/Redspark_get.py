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
l='https://www.redspark.nu/en/'
l2='https://www.redspark.nu'
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
                if'error-404 not-found'in h:
                    break
                h=h.split('<div class="article-container">')[1].split('<ul class="default-wp-page clearfix">')[0]
                h=['https://www.redspark.nu/en/%s'%c.split('<h2 class="entry-title">')[1].split('<a href="https://www.redspark.nu/en/')[1].split('"')[0]for c in h.split('<article id="post-')[1:]]
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
    for a in range(len(hl)):
        h=rg.rget(hl[a]).text
        if not os.path.exists('test.txt'):f=open('test.txt','w+');f.write(h);f.close()
        h='>'.join(h.split('<article id="post-')[1].split('>')[1:]).split('<ul class="default-wp-page clearfix">')[0]
        h2='%s%s'%(h.split('<span class="cat-links">')[0],'</span></div>'.join(h.split('<span class="cat-links">')[1].split('</span></div>')[1:]))
        h2='%s%s'%(h2.split('<header class="entry-header">')[0],'</span></div>'.join(h2.split('<span class="tag-links">')[1].split('</span></div>')[1:]))
        h={'title':h.split('class="entry-title">')[1].split('<')[0].strip(),
           'publish time':h.split('<time class="entry-date published" datetime="')[1].split('"')[0],
           'update time':h.split('<time class="updated" datetime="')[1].split('"')[0],
           'author':h.split('<span class="author vcard">')[1].split('title="')[1].split('"')[0],
           'images':[html.unescape(b.split('src="')[1].split('"')[0].split('?')[0])for b in h.split('<img')[1:]],
           'text':hp.handle(h2),
           'tags':[b.split('<')[0]for b in h.split(sp)[1].split('</span>')[0].split('rel="tag">')[1:]]if(sp:='<span class="tag-links">')in h else None,
           'categories':[b.split('<')[0]for b in h.split(sp)[1].split('</span>')[0].split('rel="category tag">')[1:]]if(sp:='<span class="cat-links">')in h else None,
           'source':hl[a]
          }
        h['text']='\n\n'.join([z.replace('\n','').strip()for z in h['text'].split('\n\n')if z]);h['text']=re.sub('#(\w)','\\#\\1',h['text'])
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
                        n+=1
                        h['publish time']='%sT%s:%s'%(h['publish time'].split('T')[0],
                                                      str(int(h['publish time'].split('T')[1].split(':')[0])-n),
                                                      ':'.join(h['publish time'].split('T')[1].split(':')[1:]))
                        if not os.path.exists(pa:='JSON-src/%s.json'%h['publish time']):
                            break
                    print(h)
                    f=open(pa,'w+');f.write(repr(h));f.close()
                else:print(h['publish time'],'?????????????????????')
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
            print(pa,'???????????????')
        else:print(pa,'?????????????????????')
if not os.path.exists('ConvertedIMGs'):os.mkdir('ConvertedIMGs')
for a in os.walk('Images'):
    for b in a[2]:
        if'.webp'==b[-5:]:
            if not os.path.exists(pa:='%s/%s'%(a[0].replace('Images','ConvertedIMGs'),b.replace('.webp','.png'))):
                if not os.path.exists(pa2:='/'.join(pa.split('/')[:-1])):
                    os.makedirs(pa2)
                im=cv2.imread('%s/%s'%(a[0],b))
                cv2.imwrite(pa,im)
                print(pa,'???????????????')
            else:
                print(pa,'?????????????????????')
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

Update Time: %s

Images: %s

Tags: %s

Categories: %s

<!--METADATA-->

%s

Source: %s'''%(h['title'].replace('\n',' '),
               h['author'],
               h['publish time'],
               h['update time'],
               repr(['[%s](%s)'%(c.split('/')[-1].split('?')[0].replace('\n',''),c)for c in h['images']]),
               repr(h['tags']),
               repr(h['categories']),
               t3,
               '[%s](%s)'%(h['source'],h['source']))
        if not os.path.exists(pa1:='MDs/%s.md'%b.split('.json')[0]):
            f=open(pa1,'w+');f.write(t);f.close()
            print(h['publish time'],'?????????MD?????????')
        else:print(h['publish time'],'???????????????MD???')
        if not os.path.exists(pa:='HTMs/%s.htm'%b.split('.json')[0]):
            f=open(pa,'w+');f.write(markdown.markdown(t));f.close()
            print(h['publish time'],'?????????HTM?????????')
        else:print(h['publish time'],'???????????????HTM???')
