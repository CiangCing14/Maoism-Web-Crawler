from datetime import datetime, timedelta
import os,sys,html2text,cv2,re,html,base64
import urllib.parse,markdown
import rg

n=0

l='https://proletaricomunisti.blogspot.com/'
l2='https://proletaricomunisti.blogspot.com'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hl=[]
ul=l
if not os.path.exists('000000.list'):
    for a in range(5):
        ps=rg.rget(ul).text
        f=open('test.txt','w+');f.write(ps);f.close()
        h=ps.split("<div class='blog-posts hfeed'>")[1].split("<div class='blog-pager' id='blog-pager'>")[0]
        h=['%s%s'%(l,b.split("<a class='timestamp-link' href='https://proletaricomunisti.blogspot.com/")[1].split("'")[0])for b in h.split("<div class='post-outer'>")[1:]]
        hl.extend(h)
        f=open('%s.list'%(str(a).rjust(6).replace(' ','0')),'w+');f.write(repr(h));f.close()
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
def formal(a):
    if'data'==a[:4]:
        return[a,'temp.%s'%a.split(':')[1].split('/')[1].split(';')[0]]
    else:return a
if not os.path.exists('JSON-src'):os.mkdir('JSON-src')
dr=os.listdir('JSON-src')
if len(dr)==0:
    hp=html2text.HTML2Text()
    for a in range(len(hl)):
        h=rg.rget(hl[a]).text
        if not os.path.exists('test.txt'):f=open('test.txt','w+');f.write(h);f.close()
        h2=h.split("<div class='post-outer'>")[1].split("<div class='comments' id='comments'>")[0]
        h={'time':h2.split("<abbr class='published' itemprop='datePublished' title='")[1].split("'")[0],
           'title':html.unescape(h.split("' property='og:title'/>")[0].split("'")[-1]).strip(),
           'description':de if(de:=html.unescape(h.split("' property='og:description'/>")[0].split("'")[-1]).strip())else'None',
           'author':h2.split("<span class='fn' itemprop='author'")[1].split("<span itemprop='name'>")[1].split('</span>')[0],
           'images':[formal(b.split('src="'if'"'in b else"src='")[1].split('"'if'"'in b else"'")[0].split('?')[0])for b in h2.split("<div class='post-header'>")[1].split("<div class='post-footer'>")[0].split('<img ')[1:]],
           'text':hp.handle(h2.split("<div class='post-header'>")[1].split("<div class='post-footer'>")[0]).strip(),
           'source':hl[a]
          }
        h['text']='\n\n'.join([z.replace('\n','').strip()for z in h['text'].split('\n\n')if z])
        for z in h['images']:
            if isinstance(z,list):
                h['text']=h['text'].replace(z[0],z[1])
        if h['time'].split('T')[0]<d:break
        if not os.path.exists(pa:='JSON-src/%s.json'%h['time']):
            print(h)
            f=open(pa,'w+');f.write(repr(h));f.close()
        else:
            if'up'in locals():
                if h['text']!=up:
                    while True:
                        n+=1
                        h['time']='%sT%s:%s'%(h['time'].split('T')[0],
                                                      str(int(h['time'].split('T')[1].split(':')[0])-n),
                                                      ':'.join(h['time'].split('T')[1].split(':')[1:]))
                        if not os.path.exists(pa:='JSON-src/%s.json'%h['time']):
                            break
                    print(h)
                    f=open(pa,'w+');f.write(repr(h));f.close()
                else:print(h['time'],'已经完成下载。')
        n+=1
        up=h['text']
if not os.path.exists('Images'):os.mkdir('Images')
imgs=[]
for a in os.walk('JSON-src'):
    for b in a[2]:
        f=open('JSON-src/%s'%b,'rb');h=eval(f.read().decode('utf-8',errors='ignore'));f.close()
        imgs.append([h['time'].replace(':','-').replace('+','-'),h['images']])
for a in imgs:
    for z in a[1]:
        if isinstance(z,list):
            pa='Images/%s/temp.%s'%(a[0],z[0].split(':')[1].split('/')[1].split(';')[0])
        else:
            pa='Images/%s/%s'%(a[0],urllib.parse.unquote(z).split('/')[-1].split('?')[0])
        if not os.path.exists(pa):
            if not os.path.exists(pa2:='/'.join(pa.split('/')[:-1])):
                os.makedirs(pa2)
            try:
                if isinstance(z,list):
                    im=base64.b64decode(','.join(';'.join(z[0].split('data:')[1].split(';')[1:]).split(',')[1:]))
                else:im=rg.rget(z,st=True).content
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
                if'/'in url:
                    t2='%s%s%s)%s'%(t2,htc[z-1],url.replace('\n','').replace('/'.join(url.replace('\n','').split('/')[:-1]),('../Images/%s'%h['time'].replace(':','-').replace('+','-')if'.webp'not in url else'../ConvertedIMGs/%s'%h['time'].replace(':','-').replace('+','-')).split('?')[0]).replace('.webp','.png').split('?')[0],')'.join(ht[z].split(')')[1:]))
                else:t2='%s%s%s)%s'%(t2,htc[z-1],'%s/%s'%(('../Images/%s'%h['time'].replace(':','-').replace('+','-')if'.webp'not in url else'../ConvertedIMGs/%s'%h['time'].replace(':','-').replace('+','-')),url.replace('\n','')),')'.join(ht[z].split(')')[1:]))
        t3=t2
        t='''# %s

Author: %s

Description: %s

Time: %s

Images: %s

<!--METADATA-->

%s

Source: %s'''%(h['title'].strip().replace('\n',' '),
               h['author'],
               h['description'],
               h['time'],
               repr(['[%s](%s)'%(c.split('/')[-1].split('?')[0].replace('\n',''),c)for c in h['images']if not isinstance(c,list)]),
               t3,
               '[%s](%s)'%(h['source'],h['source']))
        if not os.path.exists(pa1:='MDs/%s.md'%b.split('.json')[0]):
            f=open(pa1,'w+');f.write(t);f.close()
            print(h['time'],'转换为MD完毕。')
        else:print(h['time'],'已经转换为MD。')
        if not os.path.exists(pa:='HTMs/%s.htm'%b.split('.json')[0]):
            f=open(pa,'w+');f.write(markdown.markdown(t));f.close()
            print(h['time'],'转换为HTM完毕。')
        else:print(h['time'],'已经转换为HTM。')
