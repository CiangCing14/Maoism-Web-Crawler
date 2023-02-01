from datetime import datetime, timedelta
import os,sys,html2text,cv2,re
import urllib.parse,json,markdown
import rg

def english2time(a):
    d=re.findall('\d+',a)
    return'%s-%s-%sT%s:%s:00'%(d[0].rjust(4).replace(' ','0'),d[1].rjust(2).replace(' ','0'),d[2].rjust(2).replace(' ','0'),d[3].rjust(2).replace(' ','0'),d[4].rjust(2).replace(' ','0'))

l='https://mlmmlm.icu/index.php?title=Special:%E7%94%A8%E6%88%B7%E8%B4%A1%E7%8C%AE/Admin'
l2='https://mlmmlm.icu'
d=str(datetime.today()-timedelta(days=1)).split(' ')[0]
hl=[]
ul=l
hp=html2text.HTML2Text()
if not os.path.exists('000000.list'):
    for a in range(5):
        ps=rg.rget(ul).text
        if'<div class="mw-pager-navigation-bar">'not in ps:break
        hz=ps.split("<section class='mw-pager-body'>")[1].split('</section>')[0]
        hz=[[english2time(b.split('class="mw-changeslist-date"')[1].split('>')[1].split('<')[0]),hp.handle('</a>'.join(b.split('class="mw-changeslist-date"')[1].split('</a>')[1:])).strip(),ul]for b in hz.split('<li data-mw-revid="')[1:]if'class="mw-changeslist-date"'in b]
        hl.extend(hz)
        f=open('%s.list'%(str(a).rjust(6).replace(' ','0')),'w+');f.write(repr(hz));f.close()
        ul=hp.handle('%s%s'%(l2,ps.split('<div class="mw-pager-navigation-bar">')[1].split('class="mw-nextlink">后50个</a>')[0].split('<a href="')[-1].split('"')[0])).strip()
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
    for a in range(len(hl)):
        h={'time':hl[a][0],
           'text':hl[a][1],
           'source':hl[a][2]
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
        else:print(h['time'],'已經完成整理。')
if not os.path.exists('MDs'):os.mkdir('MDs')
if not os.path.exists('HTMs'):os.mkdir('HTMs')
n=0
for a in os.walk('JSON-src'):
    for b in a[2]:
        n+=1
        f=open('%s/%s'%(a[0],b));h=eval(f.read());f.close()
        t='''# MLMMLM.ICU Time: %s

<!--METADATA-->

%s

Source: %s'''%(h['time'],
               h['text'],
               '[%s](%s)'%(h['source'],h['source']))
        if not os.path.exists(pa1:='MDs/%s.md'%b.split('.json')[0]):
            f=open(pa1,'w+');f.write(t);f.close()
            print(h['time'],'轉換為MD完畢。')
        else:print(h['time'],'已經轉換為MD。')
        if not os.path.exists(pa:='HTMs/%s.htm'%b.split('.json')[0]):
            f=open(pa,'w+');f.write(markdown.markdown(t));f.close()
            print(h['time'],'轉換為HTM完畢。')
        else:print(h['time'],'已經轉換為HTM。')
