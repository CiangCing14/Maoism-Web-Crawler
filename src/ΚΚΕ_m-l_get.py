from datetime import datetime, timedelta
import os,sys,html2text,cv2
import urllib.parse
import html,re,time,markdown
import rg

n=0

def greek2date1(a):
    d=re.findall('\d+',a)
    dd=d[0]
    y=d[1]
    mo=a.split(' ')[1]
    m=['ΓΕΝΑΡΗ','ΦΛΕΒΑΡΗ','ΜΑΡΤΗ','ΑΠΡΙΛΗ','ΜΑΗ','ΙΟΥΝΗ','ΙΟΥΛΗ','ΑΥΓΟΥΣΤΟΥ','ΣΕΠΤΕΜΒΡΗ','ΟΚΤΩΒΡΗ','ΝΟΕΜΒΡΗ','ΔΕΚΕΜΒΡΗ']
    for b in range(len(m)):
        if mo==m[b]:
            mo=b+1
    return'-'.join([y,str(mo).rjust(2).replace(' ','0'),dd.rjust(2).replace(' ','0')])

def greek2date2(a):
    d=re.findall('\d+',a)
    dd=d[0]
    y=d[1]
    mo=a.split(' ')[1]
    m=['Γενάρη','Φλεβάρη','Μάρτη','Απρίλη','Μάη','Ιούνη','Ιούλη','Αύγουστού','Σεπτέμβρη','Οκτώβρη','Νοέμβρη','Δεκέμβρη']
    error=True
    for b in range(len(m)):
        if mo==m[b]:
            error=False
            mo=b+1
    if error:raise TypeError
    return'-'.join([y,str(mo).rjust(2).replace(' ','0'),dd.rjust(2).replace(' ','0')])

l='https://www.kkeml.gr/umbraco/surface/ArticlesList/Get?latest=true&page='
l2='https://www.kkeml.gr'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hl=[]
if not os.path.exists('000000.list'):
    for a in range(5):
        h=rg.rget('%s%d'%(l,a+1)).text
        h=[['%s%s'%(l2,b.split('<a href="')[1].split('"')[0]),
            '%s%s'%(l2,b.split('<img src="')[1].split('"')[0].split('?')[0])]for b in h.split('<div class="row pb-4">')[1:]]
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
    n=0
    ed=''
    for a in range(len(hl)):
        h=rg.rget(hl[a][0]).text
        if not os.path.exists('test.txt'):f=open('test.txt','w+');f.write(h);f.close()
        if'<img src="/Assets/General/Images/kkeml-logo.jpg" alt="KKE(ml) CPG(m-l)" style="width:100%" />'in h:
            h2='</div>'.join(h.split('<div class="row mx-0 mt-5">')[1].split('<div class="col-md-3')[0].split('</div>')[:-1])
            h2='<p><img src="%s"></p>%s'%(hl[a][1],h2)
            h={'title':h.split('<meta property="og:title" content="')[1].split('"')[0].strip(),
               'time':greek2date1(h.split('<div class="page-title">')[1].split('</div>')[0].split('<span>')[1].split('</span>')[0].strip()),
               'description':h.split('<meta property="og:description" content="')[1].split('"')[0],
               'type':h.split('<meta property="og:type" content="')[1].split('"')[0],
               'author':'ΚΚΕ(μ-λ)',
               'images':[html.unescape(b.split('src="')[1].split('"')[0].split('?')[0])for b in h2.split('<img')[1:]],
               'text':hp.handle(h2),
               'source':hl[a][0]
              }
            h['text']='\n\n'.join([z.replace('\n','').strip()for z in h['text'].split('\n\n')if z]);h['text']=re.sub('#(\w)','\\#\\1',h['text'])
        elif'<img src="/Assets/24-news/images/ps_logo.jpg" alt="Προλεταριακή Σημαία Proletariaki Simea" style="width:100%" />'in h:
            h2=h.split('<div class=" mt-4">')[1].split('<div class="row">')[0]
            h={'title':h.split('<meta property="og:title" content="')[1].split('"')[0].strip(),
               'time':greek2date2(' '.join(h.split('style="color:black;"><strong>')[1].split('</strong>')[0].split(' ')[1:4])),
               'description':h.split('<meta property="og:description" content="')[1].split('"')[0],
               'type':h.split('<meta property="og:type" content="')[1].split('"')[0],
               'author':'ΚΚΕ(μ-λ)',
               'images':[html.unescape(b.split('src="')[1].split('"')[0].split('?')[0])for b in h2.split('<img')[1:]],
               'text':hp.handle(h2),
               'source':hl[a][0]
              }
            h['text']='\n\n'.join([z.replace('\n','').strip()for z in h['text'].split('\n\n')if z]);h['text']=re.sub('#(\w)','\\#\\1',h['text'])
        else:raise TypeError
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
        for z in range(len(h['images'])):
            if h['images'][z][:4]!='http'and(':'not in h['images'][z]):
                h['images'][z]='%s%s'%(l2,h['images'][z])
        dd=h['time']
        if ed:
            if ed!=dd:
                n=0
        h['time']='%sT%s:00:00-04:00'%(h['time'],str(99-n).rjust(2).replace(' ','0'))
        ed=dd
        if dd<d:break
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
        n+=1
if not os.path.exists('Images'):os.mkdir('Images')
imgs=[]
for a in os.walk('JSON-src'):
    for b in a[2]:
        f=open('JSON-src/%s'%b,'r');h=eval(f.read());f.close()
        imgs.append([h['time'].replace(':','-').replace('+','-'),h['images']])
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
                t2='%s%s%s)%s'%(t2,htc[z-1],url.replace('\n','').replace('/'.join(url.replace('\n','').split('/')[:-1]),('../Images/%s'%h['time'].replace(':','-').replace('+','-')if'.webp'not in url else'../ConvertedIMGs/%s'%h['time'].replace(':','-').replace('+','-')).split('?')[0]).replace('.webp','.png').split('?')[0],')'.join(ht[z].split(')')[1:]))
        t3=t2
        t='''# %s

Author: %s

Time: %s

Description: %s

Images: %s

Type: %s

<!--METADATA-->

%s

Source: %s'''%(h['title'].replace('\n',' '),
               h['author'],
               h['time'],
               h['description'],
               repr(['[%s](%s)'%(c.split('/')[-1].split('?')[0].replace('\n',''),c)for c in h['images']]),
               h['type'],
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
