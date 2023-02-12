from datetime import datetime, timedelta
import os,sys,html2text,cv2
import urllib.parse
import html,re,time,markdown
import rg

n=0

l='https://socialistiskrevolution.wordpress.com/?infinity=scrolling'
l2='https://socialistiskrevolution.wordpress.com'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hl=[]
if not os.path.exists('000000.list'):
    for a in range(5):
        h=rg.rpost(l,{'action':'infinite_scroll','page':str(a+1)}).json()['html']
        h=[b.split('<a href="')[1].split('"')[0]for b in h.split('<article id="post-')[1:]]
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
print('\n'.join(hl))
if not os.path.exists('JSON-src'):os.mkdir('JSON-src')
dr=os.listdir('JSON-src')
if len(dr)==0:
    hp=html2text.HTML2Text()
    n=0
    for a in range(len(hl)):
        h=rg.rget(hl[a]).text
        if'/category/'in hl[a]:continue
        if not os.path.exists('test.txt'):f=open('test.txt','w+');f.write(h);f.close()
        h2=h
        h=h.split('<div class="entry-content">')[1].split('<div id="jp-post-flair"')[0]
        h={'title':h2.split('<meta property="og:title" content="')[1].split('"')[0].strip(),
           'publish time':h2.split('<meta property="article:published_time" content="')[1].split('"')[0],
           'modified time':h2.split('<meta property="article:modified_time" content="')[1].split('"')[0],
           'description':h2.split('<meta property="og:description" content="')[1].split('"')[0],
           'type':h2.split('<meta property="og:type" content="')[1].split('"')[0],
           'author':h2.split('<span class="author vcard">')[1].split('</span>')[0].split('</a>')[0].split('>')[-1],
           'images':[html.unescape(b.split('src="')[1].split('"')[0].split('?')[0])for b in h.split('<img')[1:]if'src="'in b],
           'text':hp.handle(h),
           'categories':[y.split('<')[0]for y in h2.split('<span class="cat-links">')[1].split('</span>')[0].split('rel="category tag">')[1:]],
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

Type: %s

Categories: %s

<!--METADATA-->

%s

Source: %s'''%(h['title'].replace('\n',' '),
               h['author'],
               h['publish time'],
               h['modified time'],
               h['description'],
               repr(['[%s](%s)'%(c.split('/')[-1].split('?')[0].replace('\n',''),c)for c in h['images']]),
               h['type'],
               repr(h['categories']),
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
