from datetime import datetime, timedelta
import os,sys,html2text,cv2
import urllib.parse,time,html,markdown,re
import rg

l='https://serviralpuebloperiodico.wordpress.com/page/'
l2='https://serviralpuebloperiodico.wordpress.com'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hl=[]
if not os.path.exists('000000.list'):
    for a in range(5):
        h=rg.rget('%s%d'%(l,a+1)).text.split('<ul class="wp-block-post-template is-layout-flow">')[1].split('<div class="wp-block-group is-layout-constrained">')[0]
        h=[b.split('<a href="')[1].split('"')[0]for b in h.split('<li class="wp-block-post post-')[1:]]
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
        if not os.path.exists('test.txt'):f=open('test.txt','w+');f.write(h);f.close()
        h2='>'.join(h.split('<div class="entry-content wp-block-post-content')[1].split('>')[1:]).split('<div id="atatags')[0].split('<div id="jp-post-flair"')[0]
        h={'title':h.split('<meta property="og:title" content="')[1].split('"')[0].strip(),
           'publish time':h.split('<meta property="article:published_time" content="')[1].split('"')[0],
           'modified time':h.split('<meta property="article:modified_time" content="')[1].split('"')[0],
           'description':h.split('<meta property="og:description" content="')[1].split('"')[0],
           'type':h.split('<meta property="og:type" content="')[1].split('"')[0],
           'author':'SERVIR AL PUEBLO',
           'images':[html.unescape(b.split('src="')[1].split('"')[0].split('?')[0])for b in h2.split('<img')[1:]if'src="'in b],
           'text':hp.handle(h2).strip(),
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
        else:print(h['publish time'],'已經完成下載。')
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
            print(pa,'下載完畢。')
        else:print(pa,'已經完成下載。')
if not os.path.exists('ConvertedIMGs'):os.mkdir('ConvertedIMGs')
for a in os.walk('Images'):
    for b in a[2]:
        if'.webp'==b[-5:]:
            if not os.path.exists(pa:='%s/%s'%(a[0].replace('Images','ConvertedIMGs'),b.replace('.webp','.png'))):
                if not os.path.exists(pa2:='/'.join(pa.split('/')[:-1])):
                    os.makedirs(pa2)
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
                t2='%s%s%s)%s'%(t2,htc[z-1],url.replace('\n','').replace('/'.join(url.replace('\n','').split('/')[:-1]),('../Images/%s'%h['publish time'].replace(':','-').replace('+','-')if'.webp'not in url else'../ConvertedIMGs/%s'%h['publish time'].replace(':','-').replace('+','-')).split('?')[0]).replace('.webp','.png').split('?')[0],')'.join(ht[z].split(')')[1:]))
        t3=t2
        t='''# %s

Author: %s

Publish Time: %s

Modified Time: %s

Description: %s

Images: %s

Type: %s

<!--METADATA-->

%s

Source: %s'''%(h['title'].replace('\n',' '),
               h['author'],
               h['publish time'],
               h['modified time'],
               h['description'],
               repr(['[%s](%s)'%(c.split('/')[-1].split('?')[0].replace('\n',''),c)for c in h['images']]),
               h['type'],
               t3,
               '[%s](%s)'%(h['source'],h['source']))
        if not os.path.exists(pa1:='MDs/%s.md'%b.split('.json')[0]):
            f=open(pa1,'w+');f.write(t);f.close()
            print(h['publish time'],'轉換為MD完畢。')
        else:print(h['publish time'],'已經轉換為MD。')
        if not os.path.exists(pa:='HTMs/%s.htm'%b.split('.json')[0]):
            f=open(pa,'w+');f.write(markdown.markdown(t));f.close()
            print(h['publish time'],'轉換為HTM完畢。')
        else:print(h['publish time'],'已經轉換為HTM。')
