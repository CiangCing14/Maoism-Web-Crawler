import os,sys,importlib,shutil,time,markdown,re,datetime,hashlib,markdown2odt,pyttsx3
import urllib.parse
import translators.server as tss

ds='/home/a/CiangCing14.github.io/Maoism-Datasets/%s'%str(datetime.date.today())
pds='/home/a/CiangCing14.github.io/Maoism-Datasets/%s'%str(datetime.date.today()+datetime.timedelta(days=-1))
ud='/home/a/CiangCing14.github.io'

ps=[]
for a in os.walk(sys.path[0]):
    for b in a[2]:
        if(fn:='.'.join(b.split('.')[:-1]))[-3:]=='get':
            ps.append(fn)
print('預計要運行的模組：%s'%repr(ps))
for a in ps:
    if not os.path.exists(p:='src/%s'%a.replace('_',' ')[:-4]):
        print('運行模組：%s'%a)
        try:importlib.import_module(a)
        except RuntimeError:
            print('模組“%s”，網絡條件差。'%a)
            pass
        l=[]
        for b in os.walk(sys.path[0]):
            for c in b[2]:
                if b[0]==sys.path[0]:
                    if c[-5:]=='.list'or c=='RecentPostings.md'or c=='test.htm'or c=='test.txt':
                        l.append(c)
        fo=['JSON-src','Images','ConvertedIMGs','MDs','HTMs','__pycache__']
        fol=[b for b in fo if os.path.exists(b)]
        os.makedirs(p)
        for b in l:
            os.rename(b,'%s/%s'%(p,b))
        for b in fol:
            shutil.move(b,'%s/%s'%(p,b))
b1,b2,b3,b4=False,False,False,False
if not os.path.exists('Images'):os.mkdir('Images');b1=True
if not os.path.exists('ConvertedIMGs'):os.mkdir('ConvertedIMGs');b2=True
if not os.path.exists('HTMs'):os.mkdir('HTMs');b3=True
if not os.path.exists('MDs'):os.mkdir('MDs');b4=True
n1,n2=0,0
for a in os.walk(sys.path[0]):
    for b in a[2]:
        if a[0]=='%s/HTMs'%sys.path[0]:
            n1n=int(b.split('-')[-1].split('.')[0])
            if n1n>n1:n1=n1n
for a in os.walk(sys.path[0]):
    for b in a[2]:
        if a[0]=='%s/MDs'%sys.path[0]:
            n2n=int(b.split('-')[-1].split('.')[0])
            if n2n>n2:n2=n1n
print('繼續進程HTMs%d，MDs%d。'%(n1,n2))
for a in os.walk('src'):
    for b in a[2]:
        pa='%s/%s'%(a[0],b)
        if('Images'in a[0])and b1:
            pn=a[0].split('/Images/')[0].split('/')[-1]
            pd=a[0].split('/Images/')[1]
            pa2='Images/%s/%s'%(pn,pd)
            if not os.path.exists(pa2):
                os.makedirs(pa2)
            os.rename(pa,'%s/%s'%(pa2,b))
        elif('ConvertedIMGs'in a[0])and b2:
            pn=a[0].split('/ConvertedIMGs/')[0].split('/')[-1]
            pd=a[0].split('/ConvertedIMGs/')[1]
            pa2='ConvertedIMGs/%s/%s'%(pn,pd)
            if not os.path.exists(pa2):
                os.makedirs(pa2)
            os.rename(pa,'%s/%s'%(pa2,b))
        elif('HTMs'in a[0])and b3:
            pn=a[0].split('/HTMs')[0].split('/')[-1]
            n1+=1
            f=open(pa,'r');tt=f.read();f.close()
            f=open('HTMs/%s-%s.htm'%(b[:-4],str(n1).rjust(6).replace(' ','0')),'w+');f.write(tt.replace('../Images','../Images/%s'%pn).replace('../ConvertedIMGs','../ConvertedIMGs/%s'%pn));f.close()
        elif('MDs'in a[0])and b4:
            pn=a[0].split('/MDs')[0].split('/')[-1]
            n2+=1
            f=open(pa,'r');tt=f.read();f.close()
            f=open('MDs/%s-%s.md'%(b[:-3],str(n2).rjust(6).replace(' ','0')),'w+');f.write(tt.replace('../Images','../Images/%s'%pn).replace('../ConvertedIMGs','../ConvertedIMGs/%s'%pn));f.close()
for a in os.walk('src'):
    if not a[2]:
        try:os.removedirs(a[0])
        except:pass
if os.path.exists(pds):
    f=open('%s/MD5s.txt'%pds,'r');md5s=f.read().split('\n');f.close()
    for a in os.walk('MDs'):
        for b in a[2]:
            f=open(pa:='%s/%s'%(a[0],b),'rb');t=f.read();f.close()
            t=hashlib.md5(t).hexdigest()
            if t in md5s:
                print('清除已經抓取過的新聞：%s。'%b[:-3])
                os.remove(pa)
                for z in os.walk('HTMs'):
                    for v in z[2]:
                        if v[:-11]==b[:-10]:
                            os.remove('%s/%s'%(z[0],v))
aft=['chinese','english']
if not os.path.exists('index.htm'):
    ht=''
    n=0
    for a in os.walk('HTMs'):
        a[2].sort()
        for b in a[2]:
            f=open('%s/%s'%(a[0],b),'r');t=f.read();f.close()
            t=t.split('\n')
            tn=[]
            nn=0
            for o in t:
                tn.append(o if nn==0 else o.replace('h1','h2'))
                nn+=1
            t='\n'.join(tn)
            ht='%s%s%s'%(ht,'\n\n<!--NEWS-->\n\n'if n!=0 else'',t)
            n+=1
    ht=ht.replace('src="../Images','src="Images')
    ht=ht.replace('src="../ConvertedIMGs','src="ConvertedIMGs')
    f=open('index.htm','w+');f.write('<html><head><style>%s</style></head><body><img src="Head_Image.jpg" /><h1>Marxism-Leninism-Maoism News</h1><h1>马列毛主义新闻</h1><p><a href="index.pdf">[This lan. PDF]</a><a href="index.odt">[This lan. ODT]</a></p><p>Please select your language 请选择你的语言:</p><p><a href="index.htm">Origin</a> | %s</p>%s</body></html>'%('img{height: auto; width: auto\9; width:100%;}',' | '.join(['<a href="index_%s.htm">%s</a>'%(a,a.title())for a in aft]),ht));f.close()
if not os.path.exists('index.md'):
    ht=''
    n=0
    for a in os.walk('MDs'):
        a[2].sort()
        for b in a[2]:
            f=open('%s/%s'%(a[0],b),'r');t=f.read();f.close()
            t=t.split('\n\n')
            tn=[]
            nn=0
            for o in t:
                tn.append((o if nn==0 else o.replace('# ','## ')).replace('\n',' '))
                nn+=1
            t='\n\n'.join(tn).strip()
            ht='%s%s%s'%(ht,'\n\n<!--NEWS-->\n\n'if n!=0 else'',t)
            n+=1
    ht=ht.replace('(../Images/','(Images/').replace('(../ConvertedIMGs/','(ConvertedIMGs/')
    f=open('index.md','w+');f.write(ht);f.close()
if not os.path.exists('index.odt'):
    markdown2odt.run('index.md','Origin')
if not os.path.exists('index.pdf'):
    os.system('soffice --headless --convert-to pdf index.odt')
def trans_cycle(t,de,sr):
    time.sleep(1)
    return trans(t,de,sr)
def trans(t,de='zh',sr='auto'):
    try:return tss.google(t,sr,de)
    except tss.TranslatorError:return t
    else:return trans_cycle(t,de,sr)
des=['zh','en']
lans={'chinese':'中文','english':'English'}
for y in range(len(des)):
    if not os.path.exists('index_%s.md'%aft[y]):
        f=open('index.md','r');t=f.read();f.close()
        t=t.split('<!--NEWS-->')
        tl=len(t)
        print('讀入%d個新聞。'%tl)
        ne=[]
        for a in t:
            a=a.strip()
            n={}
            n['text']='\n'.join(a.split('<!--METADATA-->')[1].split('\n')[:-1]).strip()
            n['source']=a.split('\n')[-1].split('Source: ')[1] 
            n['title']=a.split('\n')[0][2:]
            n['meta']={}
            tt='\n'.join(a.split('<!--METADATA-->')[0].split('\n')[1:]).strip().split('\n\n')
            for b in tt:
                n['meta'][b.split(': ')[0].lower()]=': '.join(b.split(': ')[1:])
            ne.append(n)
        mt={}
        print('翻譯元數據標識。')
        ks=[]
        for a in ne:
            for b in list(a['meta'].keys()):
                if b not in ks:ks.append(b)
        ksl=len(ks)
        nz=0
        for a in ks:
            mt[a]=trans(a,de=des[y],sr='en')if(des[y]!='en')else a
            print(nz+1,'/',ksl)
            nz+=1
        nec=[]
        for a in range(len(ne)):
            src='auto'
            if(ne[a]['source'].find('https://maozhuyi.home.blog')!=-1)or(ne[a]['source'].find('https://mlmmlm.icu')!=-1):
                src='zh'
            nl=ne[a]['text'].split('\n')
            nll=len(nl)
            ft=['']
            n=0
            while True:
                if n>=nll:break
                ft[-1]=nl[n]if n==0 else'%s\n%s'%(ft[-1],nl[n])
                if len(ft[-1])>5000:
                    ft[-1]='\n'.join(ft[-1].split('\n')[:-1])
                    ft.append('')
                n+=1
            print([len(b)for b in ft])
            ftl=len(ft)
            for b in range(ftl):
                ft[b]=[[c.split(')')[0],c.split(')')[1]]if')'in c else c for c in ft[b].split('(')]
            for b in range(ftl):
                if b==0:
                    print('第%d個新聞開始翻譯。'%(a+1))
                ftbl=len(ft[b])
                for c in range(ftbl):
                    if isinstance(ft[b][c],str):
                        ft[b][c]=trans(ft[b][c],de=des[y],sr=src)if ft[b][c]else''
                    else:
                        ft[b][c][1]=trans(ft[b][c][1],de=des[y],sr=src)if ft[b][c][1]else''
                        ft[b][c]=')'.join(ft[b][c])
                    print('ftb: ',c+1,'/',ftbl)
                ft[b]='('.join(ft[b])
                print('ft: ',b+1,'/',ftl)
            ft='\n'.join(ft).replace(']（图片/','](Images/').replace('）',')').replace('！','!').replace('【','[').replace('】',']').replace('（','(')
            n={}
            n['text']=ft
            n['source']=ne[a]['source']
            n['title']=ne[a]['title']
            print('翻譯標題。')
            n['title']=trans(n['title'],de=des[y],sr=src)
            n['meta']=ne[a]['meta']
            if'description'in n['meta']:print('翻譯簡介。');n['meta']['description']=trans(n['meta']['description'],de=des[y],sr=src)
            if'head description'in n['meta']:print('翻譯頭部簡介。');n['meta']['head description']=trans(n['meta']['head description'],de=des[y],sr=src)
            nk=list(n['meta'].keys())
            for b in nk:
                n['meta'][mt[b].title()]=n['meta'][b]
                del n['meta'][b]
            nec.append(n)
        mds=[]
        for a in nec:
            md='''# %s

%s

<!--METADATA-->

%s

News Source: %s'''%(a['title'],
                    '\n\n'.join(['%s: %s'%(b,a['meta'][b])for b in a['meta'].keys()]),
                    re.sub('\\n####(\S)','\\n#### \\1',a['text']),
                    a['source'])
            mds.append(md)
        fmd='\n\n<!--NEWS-->\n\n'.join(mds)
        f=open('index_%s.md'%aft[y],'w+');f.write(re.sub('\\n[ ]+([#]+)[ ]+','\\n\\1 ',fmd.replace('这是给予的(','](').replace('! ','!')));f.close()
    if not os.path.exists('index_%s.htm'%aft[y]):
        f=open('index_%s.md'%aft[y],'r');fmd=f.read();f.close()
        f=open('index_%s.htm'%aft[y],'w+');f.write('<html><head><style>%s</style></head><body><img src="Head_Image.jpg" /><h1>Marxism-Leninism-Maoism News</h1><h1>马列毛主义新闻</h1><p><a href="index_%s.pdf">[This lan. PDF]</a><a href="index_%s.odt">[This lan. ODT]</a></p><p>Please select your language 请选择你的语言:</p><p><a href="index.htm">Origin</a> | %s</p>%s</body></html>'%('img{height: auto; width: auto\9; width:100%;}',aft[y],aft[y],' | '.join(['<a href="index_%s.htm">%s</a>'%(a,a.title())for a in aft]),markdown.markdown(fmd)));f.close()
    if not os.path.exists('index_%s.odt'%aft[y]):
        markdown2odt.run('index_%s.md'%aft[y],lans[aft[y]])
    if not os.path.exists('index_%s.pdf'%aft[y]):
        os.system('soffice --headless --convert-to pdf %s'%('index_%s.odt'%aft[y]))
l=['HTMs','MDs','__pycache__','src','ConvertedIMGs','Images','index.md','index.htm','index.odt','index.pdf']
l2=['Head_Image.jpg']
if not os.path.exists(ds):
    os.makedirs(ds)
    l.extend(['index_%s.md'%a for a in aft])
    l.extend(['index_%s.htm'%a for a in aft])
    l.extend(['index_%s.odt'%a for a in aft])
    l.extend(['index_%s.pdf'%a for a in aft])
    for a in l:
        if os.path.exists(a):
            shutil.move(a,'%s/%s'%(ds,a))
    for a in l2:
        shutil.copyfile(a,'%s/%s'%(ds,a))
    for a in os.walk('%s/HTMs'%ds):
        for b in a[2]:
            f=open(pa:='%s/%s'%(a[0],b),'r');t=f.read();f.close()
            if'<html>'not in t:t='<html>\n<head><style>%s</style></head>\n<body>\n%s\n</body>\n</html>'%('img{height: auto; width: auto\9; width:100%;}',t)
            os.remove(pa)
            f=open('%s%s'%(pa.replace(':','-').replace('+','-'),'.bak'if pa[-4:]!='.bak'else''),'w+');f.write(t);f.close()
    for a in os.walk('%s/MDs'%ds):
        for b in a[2]:
            os.rename('%s/%s'%(a[0],b),'%s/%s%s'%(a[0],b.replace(':','-').replace('+','-'),'.bak'if pa[-4:]!='.bak'else''))
if not os.path.exists(pa:='%s/MD5s.txt'%ds):
    md5s=[]
    for a in os.walk('%s/MDs'%(ds)):
        for b in a[2]:
            f=open('%s/%s'%(a[0],b),'rb');t=f.read();f.close()
            t=hashlib.md5(t).hexdigest()
            md5s.append(t)
    f=open(pa,'w+');f.write('\n'.join(md5s));f.close()
    os.system("cd %s&&git add .&&git commit -m 'Add files via upload'&&git push"%ud)
