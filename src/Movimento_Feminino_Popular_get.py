from datetime import datetime, timedelta
import os,sys,html2text,cv2,re
import urllib.parse,markdown
import rg

l='https://brasilmfp.blogspot.com/'
l='https://brasilmfp.blogspot.com'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hl=[]
ul=l
if not os.path.exists('000000.list'):
    for a in range(5):
        ps=rg.rget(ul).text
        f=open('test.txt','w+');f.write(ps);f.close()
        h=ps.split("<div class='blog-posts hfeed'>")[1].split("<div class='blog-pager' id='blog-pager'>")[0]
        h=[b.split("<a class='timestamp-link' href='")[1].split("'")[0]for b in h.split("<span class='post-timestamp'>")[1:]]
        hl.extend(h)
        f=open('%s.list'%(str(a).rjust(6).replace(' ','0')),'w+');f.write(repr(h));f.close()
        ul=ps.split("a class='blog-pager-older-link' href='")[1].split("'")[0]
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
        h=h.split("<div class='post-outer'>")[1].split("<div class='comments' id='comments'>")[0]
        h2=hp.handle(h3:=h.split("<div class='post-footer'>")[0]).strip().split('\n')
        h={'time':h.split("<abbr class='published' itemprop='datePublished' title='")[1].split("'")[0],
           'title':h2[0].replace('#','').replace('*','').strip(),
           'author':b if(b:=h.split("<span class='post-author vcard'>")[1].split("<")[0]).strip()else'Movimento Feminino Popular',
           'images':[b.split('src="'if'"'in b else"src='")[1].split('"'if'"'in b else"'")[0].split('?')[0]for b in h3.split('<img ')[1:]],
           'tags':[b.split('<')[0].title()for b in h.split("<span class='post-labels'>")[1].split("</span>")[0].split("rel='tag'>#")[1:]],
           'text':'\n'.join(h2[1:]).strip(),
           'source':hl[a]
          }
        t2=''
        t4=h['text'].split('(')
        for z in range(len(t4)):
            if z==0:
                t2=t4[z]
            else:
                url=t4[z].split(')')[0]
                t2='%s(%s)%s'%(t2,'%s%s'%(l2,url)if('/'in url)and('http'not in url)else url,')'.join(t4[z].split(')')[1:]))
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

<!--METADATA-->

%s

Source: %s'''%(h['title'].strip().replace('\n',' '),
               h['author'],
               h['time'],
               repr(['[%s](%s)'%(c.split('/')[-1].split('?')[0].replace('\n',''),c)for c in h['images']]),
               repr(h['tags']),
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