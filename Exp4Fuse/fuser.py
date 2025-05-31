import json
from pyserini.search import LuceneSearcher,LuceneImpactSearcher
from tqdm import tqdm
import numpy as np
import random

class Fuser:
    def __init__(self,ratio=60):
        self.ratio=ratio
        
    def fuse(self,topics,hypothesis_documents,embedding):
        searcher=LuceneSearcher.from_prebuilt_index(embedding)
        with open('original_rank', 'w')  as f:
        for i in range(len(hypothesis_documents)):
            qid=hypothesis_documents[i][0]
            question=hypothesis_documents[i][1]
            hits = searcher.search(question, k=1000)
            rank = 0
            for hit in hits:
                rank += 1
                f.write(f'{qid} Q0 {hit.docid} {rank} {hit.score} rank\n')
        with open('hypothesis_documents_rank', 'w')  as f:
        for i in range(len(hypothesis_documents)):
            qid=hypothesis_documents[i][0]
            question=question*5
            question=question+hypothesis_documents[i][2]
            hits = searcher.search(question, k=1000)
            rank = 0
            for hit in hits:
                rank += 1
                f.write(f'{qid} Q0 {hit.docid} {rank} {hit.score} rank\n')
        with open('hypothesis_documents_rank', 'r') as file:
            hy1 = file.readlines()      
            hy=[[int(x.split()[0]),x.split()[1],int(x.split()[2]),int(x.split()[3]),x.split()[4],x.split()[5]] for x in hy1]
        with open('original_rank', 'r') as file:
            ori1 = file.readlines()
            ori=[[int(x.split()[0]),x.split()[1],int(x.split()[2]),int(x.split()[3]),x.split()[4],x.split()[5]] for x in ori1]
        with open('Exp4Fuse_rank', 'w')  as f:
            for i in range(len(topics)):
                dictTem={}
                for j in range(len(hy)):
                    if topics[i][0]==hy[j][0]:
                        try:
                            dictTem[hy[j][2]]['score1']=1/(ratio+hy[j][3])
                        except KeyError:
                            dictTem[hy[j][2]]={}
                            dictTem[hy[j][2]]['score1']=1/(ratio+hy[j][3])              
                for j in range(len(ori)):
                    if dl19_topics[i][0]==ori[j][0]:
                        try:
                            dictTem[ori[j][2]]['score3']=1/(ratio+ori[j][3])
                        except KeyError:
                            dictTem[ori[j][2]]={}
                            dictTem[ori[j][2]]['score3']=1/(ratio+ori[j][3])  
                for passage in dictTem.keys():
                    num=len(dictTem[passage])/10+1
                    score_sum=0
                    for scores in dictTem[passage].keys():
                        score_sum+=dictTem[passage][scores]
                    dictTem[passage]=num*score_sum
                rank=0
                for key, value in sorted(dictTem.items(), key=lambda item: item[1],reverse=True):   
                    rank+=1
                    if rank<=1000:
                        passageinfo=[dl19_hy[i][0],'Q0',key,rank,value,'rank']
                        topicnum=dl19_topics[i][0]
                        f.write(f'{topicnum} Q0 {key} {rank} {value} rank\n')
