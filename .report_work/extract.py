from pathlib import Path
from zipfile import ZipFile
from lxml import etree
import json
out=Path('.report_work')
for p in Path('.').rglob('*'):
 if p.suffix in ['.docx','.pptx','.odt']:
  with ZipFile(p) as z:
   names= [n for n in z.namelist() if (n=='word/document.xml' or n=='content.xml' or (n.startswith('ppt/slides/slide') and n.endswith('.xml')))]
   names.sort(key=lambda n:int(''.join(filter(str.isdigit,n)) or 0))
   text=[]
   for n in names:
    root=etree.fromstring(z.read(n)); text.append('\nFILE '+n+'\n')
    for el in root.iter():
     if etree.QName(el).localname in ('p',):
      text.append(''.join(el.itertext()) if p.suffix=='.odt' else ''.join(el.xpath('.//*[local-name()="t"]/text()')))
   (out/(p.stem+'.txt')).write_text('\n'.join(text))
for p in Path('aaa-describtion_generation').rglob('*.ipynb'):
 nb=json.loads(p.read_text()); chunks=[]
 for i,c in enumerate(nb['cells']):
  chunks.append(f'CELL {i} '+c['cell_type']+'\n'+''.join(c['source']))
  for o in c.get('outputs',[]):
   chunks.append(''.join(o.get('text',[])))
   chunks.append(''.join(o.get('data',{}).get('text/plain',[])))
 (out/(p.stem+'.txt')).write_text('\n'.join(chunks))
