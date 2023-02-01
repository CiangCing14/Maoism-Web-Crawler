from datetime import datetime, timedelta
import os,sys,html2text,cv2,re
import urllib.parse,json,markdown
import rg

l='http://dazibaorojo08.blogspot.com/'
l2='http://dazibaorojo08.blogspot.com'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hl=[]
ul=l
if not os.path.exists('000000.list'):
    for a in range(5):
        ps=rg.rget(ul).text
        f=open('test.txt','w+');f.write(ps);f.close()
        h=ps.split("<div class='blog-posts hfeed'>")[1].split("<div class='blog-pager' id='blog-pager'>")[0]
        hz=[]
        hz.extend([b.split("<a class='timestamp-link' href='")[1].split("'")[0]for b in h.split('<div class="date-outer">')[1:]])
        hl.extend(hz)
        f=open('%s.list'%(str(a).rjust(6).replace(' ','0')),'w+');f.write(repr(hz));f.close()
        ul=ps.split("<a class='blog-pager-older-link' href='")[1].split("'")[0]
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
        h3='</div>'.join('>'.join(h.split("<div class='post-body entry-content' id='post-body-")[1].split('>')[1:]).split("<div class='post-footer'>")[0].split('</div>')[:-1])
        h={'time':h.split("<abbr class='published' itemprop='datePublished' title='")[1].split("'")[0],
           'title':hp.handle(h.split("' property='og:title'/>")[0].split("'")[-1]).strip(),
           'description':hp.handle(h.split("' property='og:description'/>")[0].split("'")[-1]).strip(),
           'author':h.split("<span class='post-author vcard'>")[1].split("<span itemprop='name'>")[1].split("<")[0],
           'images':[b.split('src="'if'"'in b else"src='")[1].split('"'if'"'in b else"'")[0].split('?')[0]for b in h3.split('<img ')[1:]],
           'text':hp.handle(h3),
           'source':hl[a]
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

Description: %s

Time: %s

Images: %s

<!--METADATA-->

%s

Source: %s'''%(h['title'].replace('\n',' '),
               h['author'],
               h['description'],
               h['time'],
               repr(['[%s](%s)'%(c.split('/')[-1].split('?')[0].replace('\n',''),c)for c in h['images']]),
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
