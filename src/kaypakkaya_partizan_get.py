from datetime import datetime, timedelta
import os,sys,html2text,cv2
import urllib.parse
import html,re,time,markdown
import rg

n=0

l='https://www.kaypakkayahaber.com/views/ajax'
l2='https://www.kaypakkayahaber.com'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hl=[]
di={'page':'0',
    'view_name':"ns_prod_news_topic",
    'view_display_id':"panel_pane_1",
    'view_args':"231/616385ed-713a-4764-5904-4a64ed03811e",
    'view_path':"taxonomy/term/231",
    'view_base_path':"null",
    'view_dom_id':"a1aa421b63f7fae85431969eff68115a",
    'pager_element':"0"}
if not os.path.exists('000000.list'):
    for a in range(5):
        di['page']=str(a)
        h=rg.rpost(l,di).json()[2]['data']
        f=open('test.htm','w+');f.write(h);f.close()
        h=h.split('<div class="view-content">')[1].split('<h2 class="element-invisible">Sayfalar</h2>')[0]
        h=['%s%s'%(l2,b.split('<a href="')[1].split('"')[0])for b in h.split('<div class="dynamic-formatters-group promo-group clearfix">')[1:]]
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
        if not os.path.exists('test.htm'):f=open('test.htm','w+');f.write(h);f.close()
        h2=h.split('<div class="page-main-content-wrapper clearfix">')[1].split('<div class="page-footer-alpha grid-35 alpha omega">')[0]
        hi=h2.split('<div class="content">')[1].split('</div>')[0]
        h3='</div>'.join(h2.split('<div class="page-main grid-23 alpha">')[1].split('</div>')[:-2])
        h3='%s\n\n%s'%(hi,h3)
        h={'title':h2.split('<div class="panel-pane pane-page-title" >')[1].split('</div>')[0].split('<h1>')[1].split('</h1>')[0],
           'time':'%sT%s:00-04:00'%(h2.split('<span class="post-submitted">Yayınlandı: ')[1].split('<')[0],
                              h2.split('<span class="post-submitted">Güncellendi: ')[1].split(' ')[0]),
           'author':h2.split('<div class="field-item evenfield field-name-field-ns-article-kicker field-type-text field-label-hidden">')[1].split('<')[0],
           'description':h2.split('<div class="field-item evenfield field-name-field-ns-article-lead field-type-text-long field-label-hidden">')[1].split('<')[0],
           'images':[html.unescape(b.split('src="')[1].split('"')[0].split('?')[0])for b in h3.split('<img')[1:]],
           'text':hp.handle(h3),
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

<!--METADATA-->

%s

Source: %s'''%(h['title'].replace('\n',' '),
               h['author'],
               h['time'],
               h['description'],
               repr(['[%s](%s)'%(c.split('/')[-1].split('?')[0].replace('\n',''),c)for c in h['images']]),
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
