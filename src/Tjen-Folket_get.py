from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import os,sys,html2text,cv2
import urllib.parse
import html,re,markdown
import rg

l='https://tjen-folket.no/index.php/page/'
l2='https://tjen-folket.no'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hl=[]
with sync_playwright()as playwright:
    br=playwright.firefox.launch(headless=False)
    co=br.new_context()
    pag=co.new_page()
    if not os.path.exists('000000.list'):
        for a in range(5):
            pag.goto('%s%d'%(l,a+1))
            h=pag.content().split('<div id="primary" class="content-area">')[1].split('<div class="archive-pagination">')[0]
            h=[b.split('<a href="')[1].split('"')[0]for b in h.split('<article class="post-grid post-')[1:]]
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
        for a in range(len(hl)):
            pag.goto(hl[a])
            h=pag.content()
            if not os.path.exists('test.txt'):f=open('test.txt','w+');f.write(h);f.close()
            h2=h
            h='<div class="pdfprnt-buttons pdfprnt-buttons-post pdfprnt-top-right">'.join('>'.join(h.split('<article data-scroll="')[1].split('>')[1:]).split('<div class="pdfprnt-buttons pdfprnt-buttons-post pdfprnt-top-right">')[:-1])
            im=[html.unescape(b.split('src="')[1].split('"')[0].split('?')[0])for b in h.split('<img')[1:]]
            h={'title':h2.split('<meta property="og:title" content="')[1].split('"')[0],
               'description':h2.split('<meta property="og:description" content="')[1].split('"')[0],
               'publish time':h2.split('<meta property="article:published_time" content="')[1].split('"')[0],
               'modified time':h2.split('<meta property="article:modified_time" content="')[1].split('"')[0],
               'author':'Tjen Folket Media',
               'images':im,
               'text':hp.handle('<p><img src="%s" width="800px" /></p>%s'%(im[0],'</div>'.join(h.split('<div class="pdfprnt-buttons pdfprnt-buttons-post pdfprnt-top-right">')[1].split('</div>')[1:]))),
               'tags':[y.split('<')[0].strip()for y in h.split(sp)[1].split('</section>')[0].split('rel="tag" data-wpel-link="internal">')[1:]]if(sp:='<section class="post-tags">')in h else None,
               'category':h2.split(sp)[1].split('rel="category tag" data-wpel-link="internal">')[1].split('<')[0]if(sp:='<div class="meta-category">')in h2 else None,
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
            if h['publish time'].split('T')[0]<d:break
            if not os.path.exists(pa:='JSON-src/%s.json'%h['publish time']):
                print(h)
                f=open(pa,'w+');f.write(repr(h));f.close()
            else:print(h['publish time'],'已經完成下載。')
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

Publish Time: %s

Modified Time: %s

Images: %s

Tags: %s

Category: %s

<!--METADATA-->

%s

Source: %s'''%(h['title'].replace('\n',' '),
               h['author'],
               h['description'],
               h['publish time'],
               h['modified time'],
               repr(['[%s](%s)'%(c.split('/')[-1].split('?')[0].replace('\n',''),c)for c in h['images']]),
               repr(h['tags']),
               repr(h['category']),
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
            co.close()
            br.close()
