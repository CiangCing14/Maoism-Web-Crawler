from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import os,sys,html2text,cv2
import urllib.parse
import html,re
from PyPDF2 import PdfReader
from PyPDF2 import PdfFileReader
import docx
import markdown
import rg

n=0

def getMetaData(doc):
    metadata = {}
    prop = doc.core_properties
    metadata["author"] = prop.author
    metadata["category"] = prop.category
    metadata["comments"] = prop.comments
    metadata["content_status"] = prop.content_status
    metadata["created"] = prop.created
    metadata["identifier"] = prop.identifier
    metadata["keywords"] = prop.keywords
    metadata["last_modified_by"] = prop.last_modified_by
    metadata["language"] = prop.language
    metadata["modified"] = prop.modified
    metadata["subject"] = prop.subject
    metadata["title"] = prop.title
    metadata["version"] = prop.version
    return metadata

l='http://www.sholajawid.org/update/index_tazaha.html'
l2='http://www.sholajawid.org'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hl=[]
with sync_playwright()as playwright:
    br=playwright.firefox.launch(headless=False)
    co=br.new_context()
    pag=co.new_page()
    if not os.path.exists('000000.list'):
        h=rg.rget(l).text.split('<h3 align="center" class="headerstyle style17 style25 style85">')[1].split('<p class="clear" align="right">&nbsp;</p>')[0]
        h=[[c.split('"')[0]for c in b.split('<a href="')[1:]]for b in h.split('<span class="style177">*******************</span>')]
        h2=[]
        for a in h:
            for b in a:
                h2.append(b)
        h=h2
        hl.extend(h2)
        f=open('000000.list','w+');f.write(repr(h));f.close()
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
    hl2=[]
    for a in hl:
        if a not in hl2:
            if a not in['../index.html','index_asnaad_tarikhi.html','shomaraha_Haay_sholajawid.html']:
                if'file:///'not in a:
                    hl2.append(a.replace('..',l2))
    hl=hl2
    ts=[]
    hl2=[]
    for a in hl:
        if(b:=a.split('/')[-1].split('.')[-1])not in ts:
            if not b:continue
            if b in['6150','orgdocx','orgpdf','com']:print(a);continue
            ts.append(b)
    for a in hl:
        if a.split('/')[-1].split('.')[-1]not in['orgdocx','orgpdf','com']:
            if l2 in a:
                hl2.append(a)
    hl=hl2[:25]
    print('**********')
    print('\n'.join(hl))
    print(ts)
    ll=len('2022-12-22T22:12:26+04:30')
    if not os.path.exists('JSON-src'):os.mkdir('JSON-src')
    dr=os.listdir('JSON-src')
    if len(dr)==0:
        hp=html2text.HTML2Text()
        n=0
        n2=0
        for a in range(len(hl)):
            if hl[a][-4:]=='.pdf':
                h=rg.rget(hl[a],1000,True).content
                f=open('temp.pdf','wb+');f.write(h);f.close()
                try:rd=(pd:=PdfReader('temp.pdf')).pages
                except:
                    print(hl[a],'错误。')
                    continue
                lrd=len(rd)
                for a2 in range(lrd):
                    if a2==0:
                        tt=rd[a2].extract_text()
                    else:
                        tt='%s\n\n===== Page %s =====\n\n%s'%(tt,str(a2).rjust(6).replace(' ','0'),rd[a2].extract_text())
                    if a2+1==lrd:
                        tt='%s\n\n===== Page %s ====='%(tt,str(a2+1).rjust(6).replace(' ','0'))
                h=tt.strip()
                h={'title':h.split('\n')[0],
                   'time':str(pd.metadata.creation_date).replace(' ','T'),
                   'author':pd.metadata.author,
                   'images':[],
                   'text':'\n'.join(h.split('\n')[1:]),
                   'source':hl[a]}
                h['text']='\n\n'.join([z.replace('\n','').strip()for z in h['text'].split('\n\n')if z])
                os.remove('temp.pdf')
                if h['time']=='None':
                    h['time']=str(n2).rjust(ll).replace(' ','0')
                    n2+=1
            elif hl[a][-5:]=='.html':
                pag.goto(hl[a])
                h=pag.content()
                if not os.path.exists('test.txt'):f=open('test.txt','w+');f.write(h);f.close()
                h2=h
                h='>'.join(h.split('<div id="main">')[1].split('class="headerstyle')[1].split('>')[1:]).split('<div id="sidebar">')[0]
                h3=h.split('\n')
                tr=False
                nn=0
                for b in range(len(h3)):
                    reg=re.search('[\u0600-\u06FF]+',h3[b])
                    if reg:
                        tr=True
                    if tr:
                        if nn==0:
                            h=h3[b]
                        else:
                            h='%s\n%s'%(h,h3[b])
                        nn+=1
                t=hp.handle(h).strip()
                h={'title':t.split('\n')[0].replace('#','').replace('**','').strip(),
                   'time':'%s-01-01T00:00:00+04:30'%(str(2000-n).rjust(4).replace(' ','0')),
                   'author':h2.split('<meta name="author" content="')[1].split('"')[0],
                   'images':[html.unescape(b.split('src="')[1].split('"')[0].split('?')[0])for b in t.split('<img')[1:]],
                   'text':'\n'.join(t.split('\n')[1:]).strip(),
                   'source':hl[a]
                  }
                h['text']='\n\n'.join([z.replace('\n','').strip()for z in h['text'].split('\n\n')if z])
                n+=1
            elif hl[a][-5:]=='.docx'or hl[a][-4:]in('.doc','.dot'):
                af='.docx'if hl[a][-5:]=='.docx'else hl[a][-4:]
                h=rg.rget(hl[a],1000,True).content
                if not h:
                    print(hl[a],'错误。')
                    continue
                f=open('temp%s'%af,'wb+');f.write(h);f.close()
                if af=='.docx':
                    doc=docx.Document('temp%s'%af)
                    md=getMetaData(doc)
                os.system('libreoffice --headless --convert-to htm temp%s'%af)
                f=open('temp.htm','r');h2=f.read().strip();f.close()
                t=hp.handle(h2).strip()
                h={'title':t.split('\n')[0].replace('#','').replace('**','').strip(),
                   'time':str(md['created']).replace(' ','T')if af=='.docx'else'%s-01-01T00:00:00+04:30'%(str(2000-n).rjust(4).replace(' ','0')),
                   'author':str(md['author'])if af=='.docx'else'Unknown',
                   'images':[html.unescape(b.split('src="')[1].split('"')[0].split('?')[0])for b in h2.split('<img')[1:]],
                   'text':'\n'.join(t.split('\n')[1:]).strip(),
                   'source':hl[a]
                  }
                h['text']='\n\n'.join([z.replace('\n','').strip()for z in h['text'].split('\n\n')if z])
                print(h)
                os.remove('temp%s'%af)
                os.remove('temp.htm')
                if af!='.docx':n+=1
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
            else:
                if'up'in locals():
                    if h['text']!=up:
                        while True:
                            h['time']='%sT%s:%s'%(h['time'].split('T')[0],
                                                          str(int(h['time'].split('T')[1].split(':')[0])+1),
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
            t4=h['title']
            if t4[:2]=='![':
                url=t4.split('](')[1].split(')')[0]
                t4=t4.replace(url,'../Images/%s'%url)
            h['title']=t4.strip()
            t='''# %s

Author: %s

Time: %s

Images: %s

<!--METADATA-->

%s

Source: %s'''%(h['title'].replace('\n',' '),
                   h['author'],
                   h['time'],
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
