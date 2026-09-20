from pathlib import Path
p=Path('.report_work/build.py');s=p.read_text()
s=s.replace("if page_no:D.add_page_break()", "if page_no and (level==1 or page_no<6 or title is None):\n  x=D.add_paragraph();x.paragraph_format.space_after=Pt(0);x.paragraph_format.space_before=Pt(0);x.paragraph_format.line_spacing=1;x.add_run().add_break(WD_BREAK.PAGE)")
# Remove break-only paragraphs and transfer page break onto the next block, eliminating blank overflow pages.
pos=s.index("D.save('Отчет_")
s=s[:pos]+'''# Strip all inherited paragraph borders, including the template Title rule.
for style in D.styles:
 for b in list(style.element.xpath('.//w:pBdr')):b.getparent().remove(b)
for x in D.paragraphs:
 for b in list(x._p.xpath('.//w:pBdr')):b.getparent().remove(b)
 if x.text.startswith('Студент группы') or x.text.startswith('Руководитель курсовой') or x.text.startswith('где g'):
  x.alignment=WD_ALIGN_PARAGRAPH.LEFT
for x in list(D.paragraphs):
 if x._p.xpath('.//w:br[@w:type="page"]') and not x.text.strip():
  nxt=x._p.getnext()
  if nxt is not None and nxt.tag==qn('w:p'):
   pp=nxt.find(qn('w:pPr'))
   if pp is None:pp=OxmlElement('w:pPr');nxt.insert(0,pp)
   pp.append(OxmlElement('w:pageBreakBefore'))
   x._p.getparent().remove(x._p)
''' + s[pos:]
p.write_text(s)
