import markdown,cv2,datetime,re
from PIL import Image
import urllib.parse,shutil,os
import html
def run(mdf,lan):
    if os.path.exists('sample2'):shutil.rmtree('sample2')
    shutil.copytree('sample','sample2')
    f=open('sample/content.xml','r');te=f.read();f.close()
    f=open(mdf,'r');t=f.read();f.close()
    t=markdown.markdown(t.replace('<http','(http'))
    t=t.replace('<h1>','<text:h text:style-name="P9" text:outline-level="1"><text:span text:style-name="T3">').replace('</h1>','</text:span></text:h>')
    t=t.replace('<h2>','<text:h text:style-name="P10" text:outline-level="2"><text:span text:style-name="T3">').replace('</h2>','</text:span></text:h>')
    t=t.replace('<h3>','<text:h text:style-name="P11" text:outline-level="3"><text:span text:style-name="T3">').replace('</h3>','</text:span></text:h>')
    t=t.replace('<h4>','<text:h text:style-name="P12" text:outline-level="4"><text:span text:style-name="T3">').replace('</h4>','</text:span></text:h>')
    t=t.replace('<p>','<text:p text:style-name="P4">').replace('</p>','</text:p>')
    t=t.split('<a href="')
    tt=''
    for a in range(len(t)):
        if a==0:tt=t[a]
        else:
            url=t[a].split('"')[0].split('?')[0]
            tt='%s<text:a xlink:type="simple" xlink:href="%s" text:style-name="Internet_20_link" text:visited-style-name="Visited_20_Internet_20_Link">%s</text:a>%s'%(tt,url,'>'.join(t[a].split('</a>')[0].split('>')[1:]),t[a].split('</a>')[1])
    t=tt
    t=t.split('<img')
    tt=''
    def gett(a):
        ty={'png':'png','jpg':'jpeg','jpeg':'jpeg','bmp':'bmp','gif':'gif'}
        af=a.split('.')[-1]
        if af not in ty:
            im=Image.open(urllib.parse.unquote(a))
            return ty[im.format.lower()]
        return ty[af]
    for a in range(len(t)):
        if a==0:tt=t[a]
        else:
            url=t[a].split('src="')[1].split('"')[0]
            try:
                im=Image.open(urllib.parse.unquote(url))
                wt=6.9236
                w0=im.size[0]
                h0=im.size[1]
                ht=h0/w0*wt
                tt='%s<draw:frame draw:style-name="fr1" draw:name="Image%d" text:anchor-type="as-char" svg:width="%sin" svg:height="%sin" draw:z-index="0"><draw:image xlink:href="../%s" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad" draw:mime-type="image/%s"/></draw:frame>'%(tt,a+1,str(round(wt,6)),str(round(ht,6)),url,gett(url))
            except:pass
            aft='"'.join(t[a].split('src="')[1].split('"')[1:])
            if aft[:3]==' />':aft=aft[3:]
            else:raise TypeError
            tt='%s%s'%(tt,aft)
    t=tt
    t=t.replace('<em>','<text:span text:style-name="T4">').replace('</em>','</text:span>')
    t=t.replace('<strong>','<text:span text:style-name="T3">').replace('</strong>','</text:span>')
    t=t.replace('<hr />','<text:p text:style-name="Horizontal_20_Line"/>')
    t=t.replace('<blockquote>','<text:p text:style-name="Quotations">').replace('</blockquote>','</text:p>')
    t=t.replace('>','>\n').strip()
    t='%s\n<text:p><text:soft-page-break/></text:p>%s\n%s'%(te.split('<text:p text:style-name="P2"/><text:h text:style-name="P9" text:outline-level="1"><text:soft-page-break/>#<text:span text:style-name="T2">新闻标题</text:span>')[0],t,'</office:text></office:body>%s'%te.split('</office:text></office:body>')[1])
    t=t.replace('<https：//prensachiripilko.blogspot.com/>','https://prensachiripilko.blogspot.com/').replace('<text:p text:style-name="P7">','')
    t=html.unescape(t)
    t=t.replace('%LAN%',lan)
    dt=str(datetime.date.today()).split('T')[0].split(' ')[0].split('-')
    t=t.replace('%YY%',dt[0])
    t=t.replace('%MO%',dt[1].rjust(2).replace(' ','0'))
    t=t.replace('%DA%',dt[2].rjust(2).replace(' ','0'))
    t=t.replace(' & ',' &amp; ')
    f=open('sample2/content.xml','w+');f.write(t);f.close()
    os.system('cd sample2;7z a a.zip .')
    shutil.move('sample2/a.zip','%s.odt'%'.'.join(mdf.split('.')[:-1]))
    shutil.rmtree('sample2')
