%%% -----------------------------------------------------------------------
% Dissertation.tex 2025/11/17 version V1.2
%%% -----------------------------------------------------------------------
% This is the official ieee style template for graduate thesis/dissertation at Towson University
% Modified and refined by Yixin Chen, November, 2025
% Any issues or questions contact Yixin Chen via ychen6@students.towson.edu
% Compile this with pdflatex
% Check latest update via this read only link https://www.overleaf.com/read/gbxnfhvxdthj#202aff
%%% -----------------------------------------------------------------------
%% Importance Notice and Tips:
% This template has already make sure the line spacing, margins and most of the format settings are correct.
% But the student will have to make sure the followings
% 
% ``At least two sentences in each paragraph.''
% 
% Also, try to better arrange your figures/tables. LaTeX does not guarantee this.
% whenever you include a figure/table
% makesure you are adding [htbp] as \begin{figure/table}[htbp]
% this will help with the figures/tables and arrange them at the place in text as precisely as possible
% but you still need to slightly adjust the place where you need to include the figure/table
% make sure your figures/tables do not interrupt the paragraphs
% 
% for the chapter headings and figure/table captions, always capitalize the first character to make sure the format of SmallCap can be applied correctly
% 
% when you need to write quotation marks in LaTeX, use `` as the beginning and '' as the ending. e.g., ``example quotation''
% 
% This is a rare case. If there is a single number or character at the end of a paragraph, use a ~ mark to connect them. e.g., ``xxxxxxxx and here is the last objective~i.''
% in this way, ~ will be rendered as a space and make sure the last character ``i'' will not be isolated in a new line.
%%% -----------------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{TUgrad}[2025/07/30 Towson University graduate thesis/dissertation LaTeX class by Yixin Chen]
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax
\LoadClass[12pt]{report}
\widowpenalty=10000
\clubpenalty=10000
%%% -----------------------------------------------------------------------
\RequirePackage[
  paperwidth=8.5in,
  paperheight=11in,
  left=1.5in,
  right=1in,
  top=1in,
  bottom=1.1in
]{geometry}
%%% -----------------------------------------------------------------------
\RequirePackage{amsmath,amsthm}
\RequirePackage{mathptmx}
\RequirePackage{silence}
\WarningFilter{microtype}{Unable to apply patch}
\RequirePackage[english]{babel}
%%% -----------------------------------------------------------------------
\renewcommand{\thechapter}{\Roman{chapter}}
\renewcommand{\thesection}{\Alph{section}.}
\renewcommand{\thesubsection}{\arabic{subsection})}
\renewcommand{\thesubsubsection}{\alph{subsubsection})}
%%% -----------------------------------------------------------------------
\RequirePackage{titlesec}
\titlespacing*{\chapter}{0pt}{-30pt}{24pt}
\titlespacing*{\section}{0pt}{0em}{0em}
\titlespacing*{\subsection}{0.25in}{0em}{0em}
\titlespacing*{\subsubsection}{0.5in}{0em}{0em}
\setlength{\parskip}{0pt}
\titleformat{\chapter}[display]
  {\normalfont\normalsize\centering}
  {\scshape{Chapter} \thechapter.}
  {0pt}
  {\vspace{24pt}\normalsize\scshape}
\titleformat{name=\chapter,numberless}
  {\normalfont\normalsize\centering}
  {}
  {0pt}
  {\normalsize\scshape}
\titleformat{\section}
  {\normalfont\normalsize}
  {\textit\thesection}{0.5em}{\textit}
\titleformat{\subsection}[runin]
  {\normalfont\normalsize}
  {\textit\thesubsection}{0.5em}{\textit}[: \quad]
\titleformat{\subsubsection}[runin]
  {\normalfont\normalsize}
  {\textit\thesubsubsection}{0.5em}{\textit}[: \quad]
%%% -----------------------------------------------------------------------
% Define the page heading to be page number only.
\newcommand{\properpagestyle}{
	   \pagestyle{myheadings}\markboth{}{}\markright{}}
%%% -----------------------------------------------------------------------
% Disallow page breaks at hyphens
\brokenpenalty=10000
% Disallow hyphens
\hyphenpenalty=10000
\exhyphenpenalty=10000
\tolerance=1000
\emergencystretch=2em
\sloppy
%%% -----------------------------------------------------------------------
% Redefine the macro used for footnotes to use single spacing
\long\def\@footnotetext#1{\insert\footins{\singlespacing\normalsize
    \interlinepenalty\interfootnotelinepenalty
    \splittopskip\footnotesep
    \splitmaxdepth \dp\strutbox \floatingpenalty \@MM
    \hsize\columnwidth \@parboxrestore
   \edef\@currentlabel{\csname p@footnote\endcsname\@thefnmark}\@makefntext
    {\rule{\z@}{\footnotesep}\ignorespaces
      #1\strut}}}
%%% -----------------------------------------------------------------------
% help showing original Latin characters with pdflatex
\UseRawInputEncoding
\RequirePackage{microtype}
\RequirePackage[titles]{tocloft}
\RequirePackage{ragged2e}
\RequirePackage{fancyhdr}
\setlength{\headheight}{14.5pt}
\RequirePackage{epsfig}
\RequirePackage{epstopdf}
\RequirePackage{graphicx}
\RequirePackage{stfloats}
\RequirePackage{float}
\RequirePackage{indentfirst}
\RequirePackage[hyphens]{url}
\RequirePackage{hyperref}
\RequirePackage{cleveref}
\RequirePackage{cite}
%%% -----------------------------------------------------------------------
% algorithm needed packages
\RequirePackage{algorithm,algpseudocode}
%%% -----------------------------------------------------------------------
% adjusting the settings for subcaptions to avoid double parentheses
\RequirePackage[justification=centering,figurewithin=none,tablewithin=none]{caption}
\RequirePackage{subcaption}
\captionsetup[figure]{labelsep=period, name=Fig.,
  justification=justified}
\captionsetup[subfigure]{labelformat=simple, labelsep=period}
\captionsetup[table]{
  justification=centering,
  labelsep=newline,
  singlelinecheck=false,
  name=Table,
  labelfont=sc,
  textfont=sc,
  skip=2pt}
\renewcommand{\thetable}{\Roman{table}}
\renewcommand{\thefigure}{\arabic{figure}}
%%% -----------------------------------------------------------------------
\RequirePackage{booktabs}
\RequirePackage{diagbox}
\RequirePackage{array}
\RequirePackage{subeqnarray}
\RequirePackage{multirow, tabularx}
\RequirePackage{makecell}
\RequirePackage{threeparttable}
\DeclareMathOperator*{\argmax}{argmax}
\DeclareMathOperator*{\argmin}{argmin}
%%% -----------------------------------------------------------------------
\RequirePackage{xcolor}
\RequirePackage{newlfont}
\RequirePackage{etoolbox}
% Fuzz --------------------------------------------------------------------
\hfuzz2pt % Don't bother to report over-full boxes if over-edge is < 2pt
%%% -----------------------------------------------------------------------
\RequirePackage{lipsum}
\RequirePackage{bm}
\newcommand{\eqn}[1]{{Equation~(\ref{#1})}}
\newcommand{\fig}[1]{{Fig.~\ref{#1}}}
\newcommand{\tbl}[1]{{Table~\ref{#1}}}
\newcommand{\rom}[1]{{ (\romannum{#1}).}}
% MATH -------------------------------------------------------------------
\newcommand{\A}{{\cal A}}
\newcommand{\h}{{\cal H}}
\newcommand{\s}{{\cal S}}
\newcommand{\W}{{\cal W}}
\newcommand{\BH}{\mathbf B(\cal H)}
\newcommand{\KH}{\cal K(\cal H)}
\newcommand{\Real}{\mathbb R}
\newcommand{\Complex}{\mathbb C}
\newcommand{\Field}{\mathbb F}
\newcommand{\RPlus}{[0,\infty)}
%
\newcommand{\norm}[1]{\left\Vert#1\right\Vert}
\newcommand{\essnorm}[1]{\norm{#1}_{\text{\rm\normalshape ess}}}
\newcommand{\abs}[1]{\left\vert#1\right\vert}
\newcommand{\set}[1]{\left\{#1\right\}}
\newcommand{\seq}[1]{\left<#1\right>}
\newcommand{\eps}{\varepsilon}
\newcommand{\To}{\longrightarrow}
\newcommand{\RE}{\operatorname{Re}}
\newcommand{\IM}{\operatorname{Im}}
\newcommand{\Poly}{{\cal{P}}(E)}
\newcommand{\EssD}{{\cal{D}}}
% THEOREMS ----------------------------------------------------------------
\theoremstyle{plain}
\newtheorem{thm}{Theorem}[section]
\newtheorem{cor}[thm]{Corollary}
\newtheorem{lem}[thm]{Lemma}
\newtheorem{prop}[thm]{Proposition}
%
\theoremstyle{definition}
\newtheorem{defn}{Definition}[section]
%
\theoremstyle{remark}
\newtheorem{rem}{Remark}[section]
%
\numberwithin{equation}{section}
\renewcommand{\theequation}{\thesection.\arabic{equation}}
%%% -----------------------------------------------------------------------
% default no ack page
% use \useack to activate
\newif\ifackpage \ackpagefalse
\def\useack{\ackpagetrue}
% default no abbrevations page
% use \useabbr to activate
\newif\ifabbrspage \abbrspagefalse
\def\useabbr{\abbrspagetrue}
%%% -----------------------------------------------------------------------
\def\no@breaks#1{{\def\\{ \ignorespaces}#1}}    % disallow explicit line breaks
%%% -----------------------------------------------------------------------
\newcommand{\thesistitle}[1]{\def\@thesistitle{#1}}
\newcommand{\authorname}[1]{\def\@authorname{#1}}
\newcommand{\submissiontype}[1]{\def\@submissiontype{#1}}
\newcommand{\degreename}[1]{\def\@degreename{#1}}
\newcommand{\departmentname}[1]{\def\@departmentname{#1}}
\newcommand{\graduationdate}[1]{\def\@graduationdate{#1}}
\def\@thesistitle{    
    TITLE OF THESIS/DISSERTATION TYPED IN CAPITAL LETTERS \\
    (DOUBLE SPACED AND CENTERED) \\
    (INVERSE PYRAMID)
}
\def\@authorname{(Student's Name Here)}
\def\@submissiontype{dissertation}
\def\@degreename{Doctor of Philosophy}
\def\@departmentname{Department of Computer and Information Sciences}
\def\@graduationdate{(Month Year of Graduation)}
\newcommand{\ThesisTitle}{\@thesistitle}
\newcommand{\AuthorName}{\@authorname}
\newcommand{\SubmissionType}{\@submissiontype}
\newcommand{\DegreeName}{\@degreename}
\newcommand{\DepartmentName}{\@departmentname}
\newcommand{\GraduationDate}{\@graduationdate}
\newcommand{\ifdissertation}[2]{%
  \ifdefstring{\@submissiontype}{dissertation}{#1}{#2}}
%%% -----------------------------------------------------------------------
\RequirePackage[absolute,overlay]{textpos}
\RequirePackage{setspace}
\def\titlep{%
	\thispagestyle{empty}%
    \newpage\clearpage
        \begin{center}
            \singlespacing
            \textbf{TOWSON UNIVERSITY} \\
            \textbf{COLLEGE OF GRADUATE STUDIES}
        \end{center}
    \begin{textblock*}{\textwidth}(1.5in,1.86in)
    	\begin{center}
            \setstretch{2}
            \textbf{\MakeUppercase\ThesisTitle}
        \end{center}
    \end{textblock*}
    \begin{textblock*}{\textwidth}(1.5in,4in)
        \begin{center}
            \setstretch{2}
            \vspace{1em}
            \textbf{by} \\ \vspace{1.6em}
            \textbf{\AuthorName} \\ 
            \setstretch{1.42}
            \textbf{A \SubmissionType} \\
            \textbf{Presented to the faculty} \\
            \textbf{of Towson University} \\
            \textbf{in partial fulfillment} \\
            \textbf{of the requirements for the degree} \\
            \textbf{\DegreeName} \\
            \textbf{\DepartmentName} \\ \vspace{1.78em}
            \textbf{Towson University,}\\
            \textbf{Towson, Maryland}\\
            \textbf{21252} \\ \vspace{1.78em}
            \textbf{\GraduationDate}
        \end{center}
    \end{textblock*}
    \newpage}
%%% -----------------------------------------------------------------------
\def\beforepreface{
    \RaggedRight
	\pagenumbering{roman}
	\pagestyle{plain}
	\titlep
    \clearpage
    \setstretch{2}
    \setlength{\parindent}{0.5in}
	\input{Pages/A-Preliminary/1-approval}
    \clearpage
    \ifackpage
	\input{Pages/A-Preliminary/2-acknowledgments}
    \clearpage\fi
    \setlength{\parindent}{0in}
	\input{Pages/A-Preliminary/3-abstract}
    \clearpage
% -------------------------------------------------------------------------
	\tableofcontents
    \newpage
    \phantomsection
    \addcontentsline{toc}{chapter}{List of Tables}\listoftables
    \newpage
    \phantomsection
    \addcontentsline{toc}{chapter}{List of Figures}\listoffigures
    \newpage
    \ifabbrspage
    \phantomsection
    \addcontentsline{toc}{chapter}{Keys to Symbols, Abbreviations, or Nomenclature}
    \setlength{\parindent}{0in}
    \input{Pages/A-Preliminary/4-abbreviations}
    \newpage\fi
    \setlength{\parindent}{0.5in}}
%%% -----------------------------------------------------------------------
\def\prefacesection#1{%
	 \chapter*{#1}}
%%% -----------------------------------------------------------------------
\def\afterpreface{\newpage
    \fancyhf{}
    \renewcommand{\headrulewidth}{0pt}
    \makeatletter
    \let\ps@plain\ps@fancy
    \makeatother
    \rhead{\thepage}
    \pagenumbering{arabic}
    \properpagestyle
    \setlength{\parindent}{0.5in}}
%%% -----------------------------------------------------------------------
\let\@biblio\thebibliography
\renewcommand{\thebibliography}[1]{%
	\newpage
    \renewcommand\cftchapafterpnum{\vskip0em}
    \renewcommand\bibname{References}
    \phantomsection
	\addcontentsline{toc}{chapter}{References}
	\@biblio{#1}}
%%% -----------------------------------------------------------------------
\let\@ldbibliography\bibliography
\renewcommand{\bibliography}[1]{\@ldbibliography{#1}}
%%% -----------------------------------------------------------------------
\def\@addcontentsline#1#2#3{\if@filesw \begingroup
\let\label\@gobble \let\index\@gobble \let\glossary\@gobble
\def\protect##1{\string\string\string##1\string\space
   \space}\@temptokena{\thepage}%
\edef\@tempa{\immediate\write
\@auxout{\string\@writefile{#1}{\protect
     \contentsline{#2}{#3}{\the\@temptokena}}}}\@tempa
   \if@nobreak \ifvmode\nobreak\fi\fi\endgroup\fi}
\def\tableofcontents{\@restonecolfalse\if@twocolumn\@restonecoltrue\onecolumn
 \fi\chapter*{Table of Contents \@mkboth{CONTENTS}{CONTENTS}}
 \begingroup
 \setstretch{2}
  \@starttoc{toc}
  \endgroup
  \relax}
%%% -----------------------------------------------------------------------
\renewcommand{\contentsname}{TABLE OF CONTENTS}
\renewcommand{\cftdotsep}{1}
\renewcommand{\cftpartleader}{\cftdotfill{\cftdotsep}} % for parts
\renewcommand{\cftchapleader}{\cftdotfill{\cftdotsep}} % for chapters
\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}} % for sections
% no bold in any headings
\renewcommand{\cftchapfont}{\normalfont}
\renewcommand{\cftchappagefont}{\normalfont}
\renewcommand{\cftsecfont}{\normalfont}
\renewcommand{\cftsecpagefont}{\normalfont}
\renewcommand{\cftsubsecfont}{\normalfont}
\renewcommand{\cftsubsecpagefont}{\normalfont}
% indenting
\cftsetindents{chapter}{0em}{5.4em}
\cftsetindents{section}{3.4em}{1.5em}
\cftsetindents{subsection}{6em}{1.5em}
\cftsetindents{subsubsection}{8.6em}{1.5em}
\cftsetindents{figure}{0em}{2.5em}
\renewcommand\cftfigpresnum{Fig.\ }
\newlength\fighanglength
\settowidth\fighanglength{\cftfigpresnum}
\addtolength\cftfignumwidth{\fighanglength}
\cftsetindents{table}{0em}{2.5em}
\renewcommand\cfttabpresnum{Table\ }
\newlength\tabhanglength
\settowidth\tabhanglength{\cfttabpresnum}
\addtolength\cfttabnumwidth{\tabhanglength}
\newcommand{\etal}{{\em et al.~}}
%%% -----------------------------------------------------------------------
%% default without numbering headings
% uncomment \usenumbering to activate, or comment to deactivate
\def\usenumbering{
  \renewcommand{\thechapter}{\Roman{chapter}}
  \renewcommand{\thesection}{\arabic{chapter}.\arabic{section}}
  \renewcommand{\thesubsection}{\arabic{chapter}.\arabic{section}.\arabic{subsection}}
  \renewcommand{\thesubsubsection}{\arabic{chapter}.\arabic{section}.\arabic{subsection}.\arabic{subsubsection}}
  \cftsetindents{section}{3.4em}{2em}
  \cftsetindents{subsection}{6em}{3em}
  \cftsetindents{subsubsection}{8.6em}{3.6em}}
%%% -----------------------------------------------------------------------
\renewcommand\cftchappresnum{Chapter~}
\renewcommand\cftchapaftersnum{.}
\settowidth{\cftchapnumwidth}{Chapter~999}
\setlength{\cftbeforechapskip}{0pt}
\setlength{\cftbeforesecskip}{0pt}
\setlength{\cftbeforesubsecskip}{0pt}
%%% -----------------------------------------------------------------------
\let\oldappendix\appendix
\renewcommand{\appendix}{%
  \oldappendix
  \setlength{\parindent}{0in}
  \titleformat{\chapter}[display]
      {\normalfont\normalsize\centering}
      {\scshape{Appendix} \thechapter}
      {0pt}
      {\vspace{1.5em}\normalsize\scshape}
  \addtocontents{toc} % Update \cftchappresnum within the .toc
    {\protect\renewcommand{\protect\cftchappresnum}{Appendix }
     \protect\renewcommand{\protect\cftchapaftersnum}{}}}
%%% -----------------------------------------------------------------------
\RequirePackage{pdflscape}
\newenvironment{landscapepage}{
  \clearpage
  \begin{landscape}
  \thispagestyle{plain}
}{
  \end{landscape}
  \clearpage }
%%% -----------------------------------------------------------------------
\newcommand{\red}[1]{\textcolor{red}{\bf #1}}
\newcommand{\blue}[1]{\textcolor{blue}{\bf #1}}
%%% -----------------------------------------------------------------------
\setcounter{tocdepth}{4}
\setcounter{secnumdepth}{4}
%%% -----------------------------------------------------------------------
% Start out normal
\properpagestyle
%%% -----------------------------------------------------------------------
\RequirePackage{enumitem}
\setlist[itemize]{
  topsep=0pt,
  partopsep=0pt,
  itemsep=0pt,
  parsep=0pt,
  labelindent=0.3in,
  labelsep=0.2in,
  leftmargin=0.5in
}