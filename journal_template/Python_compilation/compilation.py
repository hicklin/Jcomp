from papers import *
config = ConfigParser.ConfigParser()
config.read("issue_config.ini")

page_orietation = 1

front_matter_objects = []

for fm in eval(config.get('Frontmatters', 'frontmatters')):
    frontmatter = Frontmatter(fm)
    front_matter_objects.append(frontmatter)

current_page = eval(config.get('Frontmatters', 'start_page'))

for fm in front_matter_objects:
    current_page, page_orietation = fm.get_pdf(current_page, page_orietation)

paper_objects = []

for p in eval(config.get('papers', 'papers')):
    paper = Paper(p)
    paper.get_aut_tit()
    paper_objects.append(paper)

papers_page_orientation = page_orietation
current_page = eval(config.get('papers', 'start_page'))

for paper in paper_objects:
    current_page, page_orietation = paper.get_pdf(current_page, page_orietation)
    paper.generate_bib()
    paper.get_self_cite()
    paper.set_self_citation()

page_orietation = papers_page_orientation
current_page = eval(config.get('papers', 'start_page'))

for paper in paper_objects:
    current_page, page_orietation = paper.get_pdf(current_page, page_orietation)

compilation = PdfFileMerger()

for paper in front_matter_objects:
    compilation.append(PdfFileReader(file(eval(config.get('Frontmatters', 'directory')) + paper.file_name + "/" + paper.file_name + ".pdf", 'rb')))

for paper in paper_objects:
    compilation.append(PdfFileReader(file(eval(config.get('papers', 'directory')) + paper.file_name + "/" + paper.file_name + ".pdf", 'rb')))

compilation.write("Xjenza compilation.pdf")
