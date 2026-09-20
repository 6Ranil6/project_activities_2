from zipfile import ZipFile
from pathlib import Path
from PIL import Image
for name in ['ААА_presentation.pptx','бизнесчасть_проблема_актуальность_аналоги.docx']:
 with ZipFile(name) as z:
  for n in z.namelist():
   if '/media/' in n:
    p=Path('.report_work')/(('slide_' if name.endswith('pptx') else 'biz_')+Path(n).name);p.write_bytes(z.read(n))
    try:
     im=Image.open(p);print(p,im.size)
    except:pass
