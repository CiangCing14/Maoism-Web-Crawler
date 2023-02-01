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
                    print(hl[a],'錯誤。')
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
                   'time':'%s-01-01T00:00:00'%(str(2000-n).rjust(4).replace(' ','0')),
                   'author':h2.split('<meta name="author" content="')[1].split('"')[0],
                   'images':[html.unescape(b.split('src="')[1].split('"')[0].split('?')[0])for b in t.split('<img')[1:]],
                   'text':'\n'.join(t.split('\n')[1:]).strip(),
                   'source':hl[a]
                  }
                n+=1
            elif hl[a][-5:]=='.docx'or hl[a][-4:]in('.doc','.dot'):
                af='.docx'if hl[a][-5:]=='.docx'else hl[a][-4:]
                h=rg.rget(hl[a],1000,True).content
                if not h:
                    print(hl[a],'錯誤。')
                    continue
                f=open('temp%s'%af,'wb+');f.write(h);f.close()
                if af=='.docx':
                    doc=docx.Document('temp%s'%af)
                    md=getMetaData(doc)
                os.system('libreoffice --headless --convert-to htm temp%s'%af)
                f=open('temp.htm','r');h2=f.read().strip();f.close()
                t=hp.handle(h2).strip()
                h={'title':t.split('\n')[0].replace('#','').replace('**','').strip(),
                   'time':str(md['created']).replace(' ','T')if af=='.docx'else'%s-01-01T00:00:00'%(str(2000-n).rjust(4).replace(' ','0')),
                   'author':str(md['author'])if af=='.docx'else'Unknown',
                   'images':[html.unescape(b.split('src="')[1].split('"')[0].split('?')[0])for b in h2.split('<img')[1:]],
                   'text':'\n'.join(t.split('\n')[1:]).strip(),
                   'source':hl[a]
                  }
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
            else:print(h['time'],'已經完成下載。')
    if not os.path.exists('Images'):os.mkdir('Images')
    imgs=[]
    for a in os.walk(sys.path[0]):
        for b in a[2]:
            if b[-4:]in['.gif','.jpg','.png','.bmp']or b[-5:]=='.webp':
                if not os.path.exists(b):continue
                if b=='Head_Image.jpg':continue
                os.rename(b,'Images/%s'%b)
                print(b,'移動完畢。')
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
                print(h['time'],'轉換為MD完畢。')
            else:print(h['time'],'已經轉換為MD。')
            if not os.path.exists(pa:='HTMs/%s.htm'%b.split('.json')[0]):
                f=open(pa,'w+');f.write(markdown.markdown(t));f.close()
                print(h['time'],'轉換為HTM完畢。')
            else:print(h['time'],'已經轉換為HTM。')
