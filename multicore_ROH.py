#program
#Runs of Homozygosity
#multicore


import datetime,sys 
import threading
import Queue

#VALORI DA CAMBIARE PER IL CALCOLO DELLE ROH BOVINI 54 K
#file_out='ROH_54K_etero0_missing50.txt'
file_out=sys.argv[1]

mini_SNP=15          #numero di snp minimo per ogni ROH
lunghezza_minima=1   #Lunghezza minima delle ROH da mettere nel file finale

maxbuffer=sys.argv[2]          #Numero di "2" massimi dentro una ROH
maxmissing=sys.argv[3]          #Numero di "5" massimi dentro una ROH

maxbuffer=int(sys.argv[2])          #Numero di "2" massimi dentro una ROH
maxmissing=int(sys.argv[3])          #Numero di "5" massimi dentro una ROH

###############################################

output=open(file_out,'w')
output.write('RAZZA ANIMALE CROMOSOMA CONTA INIZIO  FINE DIFFERENZA \n')
Lock = threading.Lock()


def scrivi_out1(razza,animale,prim,ult,cont,crom):
    global mini_SNP,lunghezzza_minima,Lock
    diff=int(ult)-int(prim)
    if cont>mini_SNP and diff/1000000. > lunghezza_minima:
        with Lock:
            output.write('%s %s %s %s %s %s %s \n'%(razza,animale,crom,cont,prim,ult,diff))
            output.flush() #pulire il buffer
        

#caricamento file ped e map editati da me
pedfiles=['/Users/Gabriele/Desktop/prova_multithread_ROH/HD_G2F.ped']
mappa_all=open('/Users/Gabriele/Desktop/prova_multithread_ROH/HD_G2F.map','r')

#pedfiles=['/Users/Gabriele/Desktop/prova_multithread_ROH/bruna_march.ped']
#mappa_all=open('/Users/Gabriele/Desktop/prova_multithread_ROH/bruna_march.map','r')


genotipo=[]
pop={}
ref={}
info={}
name=[]
cromosomi=[]
posizioni=[]
print '####################################################'
print '###### INIZIO PROGRAMMA RUNS OF HOMOZYGOSITY #######'
print '####################################################'
print datetime.datetime.now()
print '--------------------------'

for mapp in mappa_all:
    chro,nam,xx,posiz=mapp.strip().split()
    if not chro.isdigit() or int(chro)<1 or int(chro)>29:
        cromosomi.append('skip')
        posizioni.append('skip')
        continue
    cromosomi.append(chro)
    posizioni.append(posiz)
    name.append(nam)


recode={'11':'1','22':'1','12':'2','21':'2','00':'5'}



def ROH(en,line,cromosomi,posizioni,name):
    
        if en%20==0:print "LETTI:",(en+1),"ANIMALI"
        allpp=[]
        razza,ind,sire,dame,sex,phe,geno=line.strip().split(' ',6) ### Controlla altri separatori
        geno=geno.split()
        genotype=[recode.get(geno[x]+geno[x+1],'!') for x in range(0,len(geno)-1,2)]
        if genotype.count('!'): print "ERRORE NEL CODICE - Questo deve essere un return con errore"
        conta=0;ultimo=0;primo=0;lastcrom='1'
        for letter in range(len(genotype)):
            if cromosomi[letter]=='skip':continue
#            if 98133474 >= int(posizioni[letter])>= 97016802 and cromosomi[letter]=='2':
#                print letter,genotype[letter]
        
                scrivi_out(razza,ind,primo,ultimo,conta,lastcrom)
                conta=0
                lastcrom=cromosomi[letter]
            if conta==0:
                buff=0;primo=0; ultimo=0; missing=0;
                if genotype[letter]=='1':
                    conta+=1
                    primo=posizioni[letter]
                    continue
                else:continue
            if genotype[letter]=='1':
                conta+=1
                ultimo=posizioni[letter]
                continue
            elif genotype[letter]=='2':
                    buff+=1
                    if buff<=maxbuffer and missing<=maxmissing:
                        conta+=1;continue
                    elif buff > maxbuffer:
                        ultimo=posizioni[letter-1]
                        scrivi_out(razza,ind,primo,ultimo,conta,lastcrom)
                        conta=0
                        continue
            elif genotype[letter]=='5':
                    missing+=1
                    if buff<=maxbuffer and missing<=maxmissing:
                        conta+=1;continue
                    elif missing > maxmissing:         
                        ultimo=posizioni[letter-1]
                        scrivi_out(razza,ind,primo,ultimo,conta,lastcrom)
                        conta=0            



class myThread (threading.Thread):
    def __init__(self, riga_animale,en):
        threading.Thread.__init__(self)
        self.name = riga_animale
        self.enu= en

    def run(self):
        #print "Starting"
        ROH(self.enu, self.name, cromosomi,posizioni,name)
        #print "Exiting "    


for pedfile in pedfiles:
    conta=0
    numero_razze={}
    conta_animali=0


threads = []

'''

for en,line in enumerate(open(pedfile)):
    #ROH(en,line,cromosomi,posizioni,name)
    
    #thread.start_new_thread( ROH,(en,line,cromosomi,posizioni,name))
    
    thread = myThread(line,en)
    thread.start()
    #thread.join()
'''





print 'controllo lunghezza dizionario',len(finale_ROH)
#output.close()
print 'CALCOLO ROH FINITO'
print '---TIME---',datetime.datetime.now()
print '--------------------------'
if cromosomi[letter]!=lastcrom:
