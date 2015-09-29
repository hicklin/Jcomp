import fileinput
import re
# from issue_settings import *
import os
import subprocess
from PyPDF2 import PdfFileReader, PdfFileMerger
import ConfigParser

class Paper(object):
    def __init__(self, file_name):
	config = ConfigParser.ConfigParser()
        config.read("issue_config.ini")
        self.dir = eval(config.get('papers', 'directory'))
        self.file_name = file_name
        self.author = None
        self.title = None
        self.first_page = 0
        self.last_page = 1
        self.journal = eval(config.get('bib', 'journal'))
        self.year = eval(config.get('bib', 'year'))
        self.volume = eval(config.get('bib', 'volume'))
        self.number = eval(config.get('bib', 'number'))
        self.citation = None

    def get_aut_tit(self):
        tex = open(self.dir + self.file_name + "/" + self.file_name + ".tex", "r").read()
        # get authors
        author = re.search(r"author\{(.+)\}", tex).group(1)
        annotations = re.findall(r"(\$\^[\{\d \,\}]+\$)", author)
        for annotation in annotations:
            author = author.replace(annotation, "")
	author = author.replace("*", "")
        # get title
        author = re.sub(r'(, )', ", and ", author)
        tit = re.search(r"title\{(.+)\}", tex)
        self.author = author
        # tit = re.sub(r" (\\)\w", "\\", tit.group(1))
        self.title = tit.group(1)

    def set_page_number(self, page_orientation):
        for line in fileinput.input(self.dir + self.file_name + "/" + self.file_name + ".tex", inplace=True):
            if re.search(r'(setcounter\{pagna\}\{\d+\})', line):
                print re.sub(r'(setcounter\{pagna\}\{\d+\})', "setcounter{pagna}{" + str(self.first_page) + "}", line),
            elif re.search(r'(setcounter\{page\}\{\d+\})', line):
                print re.sub(r'(setcounter\{page\}\{\d+\})', "setcounter{page}{" + str(page_orientation) + "}", line),
            else:
                print line,


    def generate_bib(self):
        bib = open("selfCite/self" + self.file_name + ".bib", "w")
        bib.write("@Article{self,\n\
			author = {" + self.author + "},\n\
            title = {},\n\
			journal = {" + self.journal + "},\n\
			year = {" + self.year + "},\n\
			volume = {" + self.volume + "},\n\
            pages = {" + str(self.first_page) + "--" + str(self.last_page) + "}\n}")
            # Removed on request from iuseppe (20150727)
            # title = {" + self.title + "},\n\
            # number = {" + self.number + "},\n\

    def get_self_cite(self):
        os.chdir("selfCite")
        for line in fileinput.input("selfCitation.tex", inplace=True):
            print re.sub(r'(bibliography\{.+\})', "bibliography{self" + self.file_name + ".bib}", line),
        subprocess.call("pdflatex -synctex=1 -interaction=nonstopmode selfCitation.tex", shell=True)
        subprocess.call("bibtex selfCitation.aux", shell=True)
        self_bib = open("selfCitation.bbl", "r").read()
        os.chdir("../")
        self_cite = re.search(r'\{self\}(.+)\\end\{thebibliography\}', self_bib.replace('\n', ''))
        self.citation = self_cite.group(1)

        # self_cite = re.search(r'\{self\}(.+)\\end\{thebibliography\}', self_bib.replace('\n', '')).group(1)
        # replace_cite = re.search(r'(\\newblock[^)]*)\\newblock', self_cite).group(1)
        # self_cite.replace(replace_cite, '')
        # self.citation = self_cite
        # # self_cite = re.search(r'\{self\}(.+)\\end\{thebibliography\}', self_bib.replace('\n', '')).group(1)
        # # self.citation = re.sub(r'(\\newblock[^)]*)\\newblock', "\\\\newblock", self_cite)

    def get_pdf(self, current_page, page_orientation):
        self.first_page = current_page
        self.set_page_number(page_orientation)
        cwd = os.getcwd()
        os.chdir(self.dir + self.file_name)
        subprocess.call("pdflatex -synctex=1 -interaction=nonstopmode " + self.file_name + ".tex", shell=True)
        subprocess.call("biber " + self.file_name, shell=True)
        subprocess.call("pdflatex -synctex=1 -interaction=nonstopmode " + self.file_name + ".tex", shell=True)
        paper_pages = PdfFileReader(open(self.file_name + ".pdf", "rb")).getNumPages()
        os.chdir(cwd)
        current_page = self.first_page + paper_pages
        self.last_page = current_page - 1
        page_orientation += paper_pages
        return current_page, page_orientation

    def set_self_citation(self):
        for line in fileinput.input(self.dir + self.file_name + "/" + self.file_name + ".tex", inplace=True):
            regex = re.search(r'selfCitation\{(.+)\}', line)
            if regex:
                l = line.replace(regex.group(1), str(self.citation))
                print l,
            else:
                l = line
                print l,

class Frontmatter(object):
    def __init__(self, file_name):
	config = ConfigParser.ConfigParser()
        config.read("issue_config.ini")
        self.dir = eval(config.get('Frontmatters', 'directory'))
        self.file_name = file_name
        self.first_page = 0

    def set_page_number(self, page_orientation):
        for line in fileinput.input(self.dir + self.file_name + "/" + self.file_name + ".tex", inplace=True):
            if re.search(r'(setcounter\{pagna\}\{\d+\})', line):
                print re.sub(r'(setcounter\{pagna\}\{\d+\})', "setcounter{pagna}{" + str(self.first_page) + "}", line),
            elif re.search(r'(setcounter\{page\}\{\d+\})', line):
                print re.sub(r'(setcounter\{page\}\{\d+\})', "setcounter{page}{" + str(page_orientation) + "}", line),
            else:
                print line,

    def get_pdf(self, current_page, page_orientation):
        self.first_page = current_page
        self.set_page_number(page_orientation)
        cwd = os.getcwd()
        os.chdir(self.dir + self.file_name)
        subprocess.call("pdflatex -synctex=1 -interaction=nonstopmode " + self.file_name + ".tex", shell=True)
        paper_pages = PdfFileReader(open(self.file_name + ".pdf", "rb")).getNumPages()
        os.chdir(cwd)
        current_page = self.first_page + paper_pages
        page_orientation += paper_pages
        return current_page, page_orientation
