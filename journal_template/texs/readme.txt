The Xjenza Online LaTeX template uses biblatex with the biber backend. The
citation style used by Xjenza Online is APA v6.

Installations

	- biblatex    https://www.ctan.org/pkg/biblatex?lang=en
        - biber       http://biblatex-biber.sourceforge.net/

Execution

	- The pdf is generated in the usuall way using PDFLaTeX.

	- To generate the reference section execute biber from terminal
		> biber paper
	  after having already executed PDFLaTeX. This should be followed by another PDFLaTeX
	  If you are using texmaker, you can add the command
		biber %|pdflatex -synctex=1 -interaction=nonstopmode %.tex|evince %.pdf
	  to the
		> Options > Configure TexMaker > Quick Build tab
	  to execute these commands.
