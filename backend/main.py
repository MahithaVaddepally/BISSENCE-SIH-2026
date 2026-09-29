from pathlib import Path
import json,re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
ROOT=Path(__file__).resolve().parents[1]
def load(name): return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))
app=FastAPI(title='BISSENCE BIS Knowledge Gateway',version='0.2.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])
class Query(BaseModel): query:str; language:str='English'
class Product(BaseModel): product_name:str; material:str=''; category:str=''; sector:str=''; intended_use:str=''
class HUID(BaseModel): huid:str

def score(record,query):
 terms=set(re.findall(r'[a-z0-9]+',query.lower()))
 text=' '.join([record.get('is_number',''),record.get('title',''),record.get('category',''),' '.join(record.get('keywords',[])),record.get('summary','')]).lower()
 return sum(1 for term in terms if term in text)/max(1,len(terms))
@app.get('/standards')
def standards(q:str=''):
 data=load('standards.json')
 return sorted([dict(x,score=round(score(x,q),2)) for x in data if not q or score(x,q)>0],key=lambda x:x['score'],reverse=True)
@app.get('/standards/{id}')
def standard(id:str): return next((x for x in load('standards.json') if x['id']==id),{'error':'Standard not found'})
@app.post('/chat')
def chat(body:Query):
 results=sorted([(score(x,body.query),x) for x in load('standards.json')],key=lambda p:p[0],reverse=True)
 if not results or results[0][0]==0:
  return {'answer':'I could not match that product to a source yet. Add the product type and intended use, or search the standards library.','applicable_standards':[],'evidence':[],'grounded':False,'language':body.language}
 bestscore,best=results[0]
 related=[x for sc,x in results[1:3] if sc>0]
 evid=[]
 for record in [best,*related]:
  for doc in record.get('source_documents',[])[:1]:
   evid.append({'standard':record['is_number'],'title':record['title'],'source':doc['title'],'url':doc['url'],'materials':record.get('materials',[]),'tests':record.get('tests',[])})
 return {'answer':best['summary'],'applicable_standards':[dict(x,score=round(sc,2)) for sc,x in results if sc>0][:3],'materials':best.get('materials',[]),'tests':best.get('tests',[]),'evidence':evid,'grounded':bool(evid),'language':body.language,'disclaimer':'Prototype retrieval from product manuals and BIS pages; check the latest standard text, amendments and QCO.'}
@app.post('/recommend')
def recommend(p:Product):
 q=' '.join([p.product_name,p.material,p.category,p.intended_use,p.sector]); results=sorted([(score(x,q),x) for x in load('standards.json')],key=lambda z:z[0],reverse=True); matches=[dict(x,score=round(sc,2)) for sc,x in results if sc>0][:3]
 return {'product':p.model_dump(),'applicable_standards':matches,'materials':matches[0].get('materials',[]) if matches else [],'tests':matches[0].get('tests',[]) if matches else [],'certification':matches[0].get('certification','Check applicable QCO and current BIS scheme') if matches else 'Insufficient evidence: identify the product and intended use','grounded':bool(matches)}
@app.post('/verify-huid')
def verify(body:HUID):
 rec=next((x for x in load('hallmark.json') if x['huid'].upper()==body.huid.upper()),None)
 return {'found':bool(rec),'record':rec,'note':'Illustrative prototype data. Verify HUID using the official BIS Care app.'}
@app.get('/labs')
def labs(state:str='',q:str=''):
 data=load('labs.json'); return [x for x in data if (not state or state.lower() in x['state'].lower()) and (not q or q.lower() in str(x).lower())]
@app.get('/stats')
def stats(): return {'standards_searched':1284,'ai_conversations':326,'certification_requests':148,'hallmark_verifications':72,'mode':'illustrative demo data'}
