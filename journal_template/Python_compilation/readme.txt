***************************
*** Instruction for use ***
***************************

Make sure that the tex files are sorted as indicated below

Folder contents
***************

Drafts: Copy of the different versions sent to authors.
Finalised: Soft link to the LaTeX generated pdf after author requests no more changes.
frontmatter: tex files of the frontmatter.
Origial: Original material submitted by the authors separated in folders by paper.
Python_compilation: This file together with "issue_config.ini", "papers.py", "compilation.py" and the "selfCite" folder.
texs: Folders named using two digits, example "04", according to the submission order of the paper. The folders contain all the LaTeX files
      required for compilation with the exception of the .sty and the preamble.tex file. These are located in the folder "packages" located
      in the same level as the papers' folders. The "paper" folder located at the level is a template for a paper.


Modify journal specific variables
*********************************

 * Open "issue_config.ini" and modify the journal specific variables.
 * Note: Under [papers] - "directory" is the relative location from the "compilation.py" file to the papers' tex files.
                        - "papers" is an array (example: ['00', '03', '01', '02']) in order of how the papers should be printed
                                   in the final compilation.
                        - "start_page" is printed page number of the first page from the papers section.
         Under [Frontmatters] - "directory" is the relative location from the "compilation.py" file to the frontmatter's tex files.
                              - "frontmatters" is an array (usually: ['EditorialBoard', 'Rules']) containing, in order, the frontmatter tex files
                              - "start_page" is printed page number, in roman, of the first page from the frontmatter section.
 * run "python compilation.py" from the terminal and wait for the magic to happen!

