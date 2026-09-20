from pypdf import PdfReader
from pathlib import Path
from docx import Document
import re
f=Path('Отчет_Хаялиев_ИУ6-74Б_Генерация_описаний_Авито.docx');d=Document(f);r=PdfReader(next(Path('.report_work/review4').glob('*.pdf')))
norm=lambda s:re.sub(r'\s+',' ',s).strip()
pages=[norm(p.extract_text()) for p in r.pages];print('PAGES',len(pages))
for p in d.paragraphs:
 if '\t' in p.text and p.text.split('\t')[-1].isdigit():
  h=p.text.split('\t')[0];key='ПРИЛОЖЕНИЕ А' if h.startswith('ПРИЛОЖЕНИЕ') else h
  matches=[i+1 for i,t in enumerate(pages) if i>=4 and norm(key) in t]
  assert matches,h
  for run in p.runs:
   if '\t' in run.text:run.text=run.text.rsplit('\t',1)[0]+'\t'+str(matches[0])
 if p.text.startswith('Отчет '):
  for run in p.runs:run.text=re.sub(r'Отчет \d+ с\.',f'Отчет {len(pages)} с.',run.text)
d.save(f)
for i,t in enumerate(pages):print(i+1,len(t),t[:75])
