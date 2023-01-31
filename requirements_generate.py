import os,sys
r=[]
for a in os.walk(sys.path[0]):
    for b in a[2]:
        if b[-2:]=='py':
            if a[0]==sys.path[0]:continue
            f=open('%s/%s'%(a[0],b),'r');t=f.read();f.close()
            t=t.split('\n')
            for c in t:
                if'from'==c[:4]:
                    t2=c.split('from ')[1].split(' ')[0].split(',')
                elif'import'==c[:6]:
                    t2=c.split('import ')[1].split(' ')[0].split(',')
                for d in t2:
                    d=d.split('.')[0]
                    if d not in r:
                        r.append(d)
t='\n'.join(r)
print(t)
f=open('requirements.txt','w+');f.write(t);f.close()
