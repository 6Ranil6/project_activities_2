from pathlib import Path
import csv,json,sys,collections,statistics
sys.path.insert(0,str(Path('LLM_as_a_judge').resolve()))
from ad_validator import validate_description
out={}; sets={}
for p in list(Path('data').glob('*.csv'))+list(Path('LLM_as_a_judge/vals').glob('*.csv')):
 with p.open(encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
 d={'n':len(rows),'columns':list(rows[0]),'categories':dict(collections.Counter(r.get('category_name') for r in rows))}; sets[p.name]=set(r.get('item_id') for r in rows)
 d['params_empty']=sum(r.get('params','').strip() in ('','{}','null','nan') for r in rows)
 d['invalid_params']=sum(1 for r in rows if r.get('params') and not r['params'].lstrip().startswith('{'))
 for col in rows[0]:
  if col.endswith('response') or col in ('generated_description','pred_description'):
   vals=[r[col] for r in rows]; results=[validate_description(v) for v in vals]
   d[col]={'nonempty':sum(bool(v.strip()) for v in vals),'pass':sum(r.success for r in results),'avg_words':statistics.mean(len(v.split()) for v in vals),'violations':dict(collections.Counter(v.split(':')[0] for r in results for v in r.violations))}
 out[str(p)]=d
out['intersections']={a+' / '+b:len(sets[a]&sets[b]) for a,b in [('train_with_params.csv','valid_with_params.csv'),('dataset_filtered_with_params_3k.csv','valid_with_params.csv'),('clean_val_qwen_base.csv','valid_with_params.csv')]}
Path('.report_work/stats.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)); print(json.dumps(out,ensure_ascii=False,indent=2))
