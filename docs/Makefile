# LaTeX -*-Makefile-*-
#
# $HEADER$
# 

# MAIN_TEX: In order to build your document, fill in the MAIN_TEX
# macro with the name of your main .tex file -- the one that you
# invoke LaTeX on.

MAIN_TEX	= 	main.tex

# OTHER_SRC_FILES: Put in the names of all the other .tex files that
# this document depends on in the OTHER_SRC_FILES macro.  This is
# ensure that whenever one of the "other" files changes, "make" will
# rebuild your paper.

OTHER_SRC_FILES	= 	

# BibTeX sources.  The bibliography will automatically be re-generated
# if these files change.

BIBTEX_SOURCES = biblio.bib

# xfig figures.  Will be converted to .eps and .pdf as necessary.

#FIG_FILES	= 

# Files that alredy exist as .png.  Will be converted to .eps and .pdf
# as necessary.

PNG_FILES	= 

# Files that alredy exist as .eps.  Will be converted to .pdf as
# necessary.

EPS_FILES	= 

# Required commands and options

LATEX		= latex
PDFLATEX	= pdflatex
DVIPS		= dvips
MAKEINDEX	= makeindex
BIBTEX		= bibtex
#FIG2DEV		= fig2dev
PNGTOPNM	= pngtopnm
PNMTOPS		= pnmtops
EPS2PDF		= epstopdf
PS2PDF          = ps2pdf
PS2PDF_OPTIONS  = -sPaperSize=letter -dAutoFilterGrayImages=false \
		-dGrayDownSample=false -sGrayImageFilter=LZWEncode \
		-dAutoFilterColorImages=false -sColorImageFilter=LZWEncode \
		-dColorDownSample=false -dEmbedAllFonts=true \
		-dSubsetFonts=true
DISTILL         = distill
DISTILL_OPTIONS = -v -pagesize 612 792 pts -encodegray on -graycompr lzw \
		-graydownsample off -grayacs off -graydepth 8 \
		-subsetfonts on -embedallfonts on -pairs
PSNUP           = psnup

#########################################################################
#
# You should not need to edit below this line
#
#########################################################################

.SUFFIXES:	.tex .dvi .ps .pdf .fig .eps .png

MAIN_DVI	= $(MAIN_TEX:.tex=.dvi)
MAIN_PS		= $(MAIN_TEX:.tex=.ps)
MAIN_PDF	= $(MAIN_TEX:.tex=.pdf)
MAIN_BBL	= $(MAIN_TEX:.tex=.bbl)
MAIN_BASENAME	= $(MAIN_TEX:.tex=)
EPS_PNG_FILES	= $(PNG_FILES:.png=.eps)
EPS_FIG_FILES	= $(FIG_FILES:.fig=.eps)
PDF_FIG_FILES	= $(FIG_FILES:.fig=.pdf)
PDF_EPS_FILES	= $(EPS_FILES:.eps=.pdf)

#
# Some common target names
# Note that the default target is "ps"
#

pdf: $(MAIN_PDF)
ps: $(MAIN_PS) 

#
# Make the dependencies so that things build when they need to
#

$(MAIN_PS): $(MAIN_DVI)
$(MAIN_DVI): $(MAIN_TEX) $(CITE_TEX) $(OTHER_SRC_FILES) $(EPS_FIG_FILES) $(EPS_FILES) $(MAIN_BBL)
$(MAIN_PDF): $(MAIN_TEX) $(CITE_TEX) $(OTHER_SRC_FILES) $(PDF_FIG_FILES) $(PNG_FILES) $(MAIN_BBL) $(PDF_EPS_FILES)

#
# Search strings
#

REFERENCES = "(There were undefined references|Rerun to get (cross-references|the bars) right|No file *[aux|toc|lof|lot])"
NEEDINDEX = "Writing index file"
RERUNBIB = "No file.*\.bbl|LaTeX Warning: Citation|LaTeX Warning: Label\(s\) may"

#
# General rules
#

.eps.pdf:
	@if ( `which $(DISTILL) > /dev/null 2>&1` ); then \
		cmd="$(DISTILL) $(DISTILL_OPTIONS) $*.eps $*.pdf" ; \
                echo $$cmd ; \
                eval $$cmd ;\
	elif ( which $(EPS2PDF) > /dev/null 2>&1 ); then \
		cmd="$(EPS2PDF) $(EPS2PDF_OPTIONS) $*.eps " ; \
                echo $$cmd ; \
                eval $$cmd ;\
	elif ( which $(PS2PDF) > /dev/null 2>&1 ); then \
		cmd="$(PS2PDF) $(PS2PDF_OPTIONS) $*.eps $*.pdf" ; \
                echo $$cmd ; \
                eval $$cmd ;\
	else \
		echo "Cannot find ps to pdf converter :-("; \
	fi

.png.eps:
	$(PNGTOPNM) $< | $(PNMTOPS) -noturn > $*.eps

# Only run bibtex if latex has already been run (i.e., if there is
# already a .aux file).  If .aux file does not exist, then bibtex will
# be run during the .tex.dvi / .tex.pdf rules.  We don't run latex
# here to generate the .aux file because a) we don't know whether to
# run latex or pdflatex, and b) the dependencies are wrong for
# pdflatex because we may need to generate some pdf images first.

$(MAIN_BBL): $(BIBTEX_SOURCES)
	@if (test -f $(MAIN_BASENAME).aux); then \
		echo "### Running BibTex"; \
		$(BIBTEX) $(MAIN_BASENAME); \
	fi

# Macro to handle when running "latex" fails -- ensure to kill the
# .aux and .dvi files so that the next time we run "make", the
# .tex.dvi rule fires, not the .bbl or .dvi.ps rule.

DVI_FAIL = ($(RM) $(MAIN_BASENAME).aux $(MAIN_BASENAME).dvi && false)

# Main workhorse for .tex -> .dvi.  Run latex, makeindex, and bibtex
# as necessary.

.tex.dvi:
	@echo "### Running LaTeX (1)"
	$(LATEX) $* || $(DVI_FAIL)
	@if (egrep $(REFERENCES) $*.log > /dev/null); then \
		echo "### Running LaTeX to fix references (2)"; \
		($(LATEX) $*) || $(DVI_FAIL); \
	fi
	@if (egrep $(NEEDINDEX) $*.log >/dev/null); then \
		echo "### Running makeindex to generate index"; \
		$(MAKEINDEX) $*; \
		echo "### Running LaTeX after generating index"; \
		($(LATEX) $*) || $(DVI_FAIL); \
	fi
	@if (egrep $(RERUNBIB) $*.log >/dev/null); then \
		echo "### Running BibTex because references changed"; \
		$(BIBTEX) $(MAIN_BASENAME); \
		echo "### Running LaTeX after generating bibtex"; \
		($(LATEX) $*) || $(DVI_FAIL); \
	fi
	@if (egrep $(REFERENCES) $*.log > /dev/null); then \
		echo "### Running LaTeX to fix references (3)"; \
		($(LATEX) $*) || $(DVI_FAIL); \
	fi
	@if (egrep $(REFERENCES) $*.log > /dev/null); then \
		echo "### Running LaTeX to fix references (4)"; \
		($(LATEX) $*) || $(DVI_FAIL); \
	fi

.dvi.ps:
	$(DVIPS) -P pdf -t letter -o $*.ps $*

# Macro to handle when running "latex" fails -- ensure to kill the
# .aux file so that the next time we run "make", the .tex.pdf rule
# fires, not the .bbl rule.

PDF_FAIL = ($(RM) $(MAIN_BASENAME).aux && false)

# Main workhorse for .tex -> .pdf.  Run latex, makeindex, and bibtex
# as necessary.  Essentially the same as .tex.dvi, except
# s/latex/pdflatex/ig.

.tex.pdf:
	$(PDFLATEX) $* || $(PDF_FAIL)	
	$(BIBTEX) $(MAIN_BASENAME)
	$(PDFLATEX) $* || $(PDF_FAIL)
	$(PDFLATEX) $* || $(PDF_FAIL)

# 	@echo "### Running pdfLaTeX (1)"
# 	$(PDFLATEX) $* || $(PDF_FAIL)
# 	@if (egrep $(REFERENCES) $*.log > /dev/null); then \
# 		echo "### Running pdfLaTeX to fix references (2)"; \
# 		($(PDFLATEX) $*) || $(PDF_FAIL); \
# 	fi
# 	@if (egrep $(NEEDINDEX) $*.log >/dev/null); then \
# 		echo "### Running makeindex to generate index"; \
# 		$(MAKEINDEX) $*; \
# 		echo "### Running pdfLaTeX after generating index"; \
# 		($(PDFLATEX) $*) || $(PDF_FAIL); \
# 	fi
# 	@if (egrep $(RERUNBIB) $*.log >/dev/null); then \
# 		echo "### Running BibTex because references changed"; \
# 		$(BIBTEX) $(MAIN_BASENAME); \
# 		echo "### Running pdfLaTeX after generating bibtex"; \
# 		($(PDFLATEX) $*) || $(PDF_FAIL); \
# 	fi
# 	@if (egrep $(REFERENCES) $*.log > /dev/null); then \
# 		echo "### Running pdfLaTeX to fix references (3)"; \
# 		($(PDFLATEX) $*) || $(PDF_FAIL); \
# 	fi
# 	@if (egrep $(REFERENCES) $*.log > /dev/null); then \
# 		echo "### Running pdfLaTeX to fix references (4)"; \
# 		($(PDFLATEX) $*) || $(PDF_FAIL); \
# 	fi

#
# graphs
#

Graph: graphs
graph: graphs
graphs:
	(cd results/la-myri; ./geplot)

#
# Just for fun
#

RUN_PSNUP = $(PSNUP) -d -b2 -m10 -pletter
1: $(MAIN_PS)
	num_pages="`psnup -1 $(MAIN_PS) bogus.ps 2>&1 | grep Wrote | cut -dW -f2- | awk '{ print $$2 }'`"; \
	$(RM) bogus.ps; \
	$(RUN_PSNUP) -$$num_pages $(MAIN_PS) one-page.ps; \
	if test "$$?" != "0"; then \
	  num_pages="`expr $$num_pages + 1`"; \
	  $(RUN_PSNUP) -$$num_pages $(MAIN_PS) one-page.ps; \
	fi; \
	if test "$$?" != "0"; then \
	  num_pages="`expr $$num_pages + 1`"; \
	  $(RUN_PSNUP) -$$num_pages $(MAIN_PS) one-page.ps; \
	fi; \
	if test "$$?" != "0"; then \
	  num_pages="`expr $$num_pages + 1`"; \
	  $(RUN_PSNUP) -$$num_pages $(MAIN_PS) one-page.ps; \
	fi
	$(RUN_PS2PDF) one-page.ps
	$(RM) one-page.ps

#
# Standard targets
#

clean:
	$(RM) *~ *.bak *%
	$(RM) *.log *.aux *.dvi *.blg *.toc *.bbl *.lof *.lot \
		*.idx *.ilg *.int *.out */*.aux \
		$(EPS_PNG_FILES) $(EPS_FIG_FILES) $(PDF_FIG_FILES) \
		 $(PDF_EPS_FILES)

distclean: clean
	$(RM) $(MAIN_PS) $(MAIN_DVI) $(MAIN_PDF)
