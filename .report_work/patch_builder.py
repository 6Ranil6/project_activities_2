from pathlib import Path
p=Path('.report_work/build.py');s=p.read_text();s=s.replace("import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt", "from reportlab.pdfgen import canvas\nfrom reportlab.pdfbase import pdfmetrics\nfrom reportlab.pdfbase.ttfonts import TTFont\nimport pypdfium2 as pdfium")
a=s.index("plt.rcParams.update");b=s.index('\npage()\n',a)
s=s[:a]+'''pdfmetrics.registerFont(TTFont('TimesReport','/System/Library/Fonts/Supplemental/Times New Roman.ttf'))
def chart(name,labels,values,maxval):
 c=canvas.Canvas(str(W/(name+'.pdf')),pagesize=(650,290));c.setFont('TimesReport',14)
 left=235;right=600;bottom=38;top=266;step=(top-bottom)/len(labels)
 for i,(lab,val) in enumerate(zip(labels,values)):
  y=top-i*step-step/2;c.setFillColorRGB(0,0,0);c.drawRightString(left-12,y-4,lab)
  c.setFillColorRGB(.38,.49,.58);c.rect(left,y-8,(right-left)*val/maxval,17,fill=1,stroke=0)
  c.setFillColorRGB(0,0,0);c.drawString(left+(right-left)*val/maxval+5,y-4,str(round(val,1)).replace('.',','))
 c.setStrokeColorRGB(.5,.5,.5);c.line(left,bottom,left,top)
 c.setFont('TimesReport',13);c.drawCentredString((left+right)/2,15,'Доля, %');c.save()
 pdf=pdfium.PdfDocument(str(W/(name+'.pdf')));pdf[0].render(scale=2.3).to_pil().save(W/(name+'.png'))
vals=sorted(cats.items(),key=lambda x:x[1],reverse=True)
chart('categories',[a for a,b in vals],[b/300 for a,b in vals],48)
chart('rules',['Базовая VLM','SFT VLM','CLIP + ruGPT'],[86,18,0],100)
''' +s[b:]
s=s.replace('14 источн.','12 источн.')
s=s.replace("for i,r in enumerate(refs[7:],8):","for i,r in enumerate(refs[7:12],8):")
s=s.replace("p('Табличные входы хранятся в комплекте данных [13]. Повторные расчеты состава выборок и прохождения правил зафиксированы при подготовке настоящего отчета [14].')",'')
p.write_text(s)
