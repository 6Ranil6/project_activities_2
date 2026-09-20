from pypdf import PdfReader
from pathlib import Path
from docx import Document
import re,json
f=Path('Отчет_Хаялиев_ИУ6-74Б_Генерация_описаний_Авито.docx');d=Document(f);r=PdfReader(next(Path('.report_work/render4').glob('*.pdf')))
normalize=lambda s: re.sub(r'\s+',' ',s).strip()
pages=[normalize(p.extract_text()) for p in r.pages];print('PAGES',len(pages));mapping={}
for h in json.loads(Path('.report_work/headings.json').read_text()):
 key='ПРИЛОЖЕНИЕ А' if h.startswith('ПРИЛОЖЕНИЕ') else h
 matches=[i+1 for i,t in enumerate(pages) if i>=4 and normalize(key) in t]
 if not matches:raise ValueError(h)
 mapping[h]=matches[0]
for p in d.paragraphs:
 if '\t' in p.text:
  h=p.text.split('\t')[0]
  if h in mapping:
   for run in p.runs:
    if '\t' in run.text:run.text=run.text.rsplit('\t',1)[0]+'\t'+str(mapping[h])
 if p.text.startswith('Отчет 33 с.'):
  p.runs[0].text=p.runs[0].text.replace('33 с.',str(len(pages))+' с.')
d.save(f);Path('.report_work/page_map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2));print(json.dumps(mapping,ensure_ascii=False,indent=2))
