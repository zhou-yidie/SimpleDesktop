\NeedsTeXFormat{LaTeX2e}

% 目录样式设置
\RequirePackage{setspace}
\ProvidesClass{xuptThesis}[2025/11/12 Xi'an University of Posts and Telecommunications Thesis Class]

% 加载基础类
\LoadClass[12pt,a4paper,twoside]{report}

% 加载必要的宏包
\RequirePackage[top=0.79in,bottom=0.79in,left=1.18in,right=1.18in]{geometry}
\RequirePackage{graphicx}
\RequirePackage{amsmath,amssymb,amsbsy}
\RequirePackage{indentfirst}
\RequirePackage{titlesec}
\RequirePackage{listings}
\RequirePackage{url}
\RequirePackage{array}
\RequirePackage{booktabs} % 用于三线表
\RequirePackage{caption} % 用于控制表格和图表标题格式
\RequirePackage{threeparttable} % 用于在表格下方显示脚注
\RequirePackage{tablefootnote} % 保留兼容性
\RequirePackage{multirow} % 用于合并表格行
\RequirePackage{makecell} % 用于合并表格行

% 创建自动编号的表格脚注命令
\newcounter{autotnotecounter}
\newcommand{\autotnote}[1][]{%
  \stepcounter{autotnotecounter}
  \ifx#1\@empty
    \tnote{\arabic{autotnotecounter}}
  \else
    \tnote{\arabic{autotnotecounter}}
  \fi
}

% 在表格开始时重置计数器
\AtBeginEnvironment{table}{% 当table环境开始时
  \setcounter{autotnotecounter}{0}
}

% 设置表格脚注格式：宋体五号，单倍行间距
\let\oldtablenotes\tablenotes
\renewenvironment{tablenotes}[1][normal]{\begin{oldtablenotes}[#1]\songti\fontsize{10.5pt}{10.5pt}\selectfont\parindent0pt}{\end{oldtablenotes}}
\RequirePackage{fancyhdr}
\RequirePackage{ragged2e} % 提供\justifying命令用于两端对齐
\RequirePackage{tocloft} % 用于目录格式控制
\RequirePackage{hyperref}
\RequirePackage{xcolor}


% 强制使用XeLaTeX编译器 - 必须使用XeLaTeX而不是pdflatex
  \RequirePackage{ifxetex}
  \ifxetex
    % 导入必要的中文支持包 - 完全依赖ctex包的默认配置
    \RequirePackage[UTF8]{ctex}
    \RequirePackage{fontspec}
    
    % 仅设置captionsetup，不修改字体配置
    \AtBeginDocument{
      \captionsetup[table]{
        labelfont={bf},
        textfont={}
      }
      \captionsetup[figure]{
        labelfont={bf},
        textfont={}
      }
    }
  \else
    \PackageError{xuptThesis}{必须使用XeLaTeX编译器编译此文档，pdflatex不支持当前字体配置}{请使用xelatex main.tex}
  \fi


% 定义图表标题的字体命令
\DeclareCaptionFont{songti11}{\songti\fontsize{11pt}{13pt}\selectfont}
\DeclareCaptionFont{songti105}{\songti\fontsize{10.5pt}{13pt}\selectfont}
\DeclareCaptionFont{heiti11}{\heiti\fontsize{11pt}{13pt}\selectfont}

% 设置表格标题格式，在"表"和编号之间添加空格
\captionsetup[table]{
  labelfont={bf,songti11},
  textfont={songti11},
  labelsep=quad,
  skip=1em
}



% 重新设置图表标题字体
\captionsetup[figure]{
  labelfont={bf,songti11},
  textfont={songti11},
  labelsep=quad,
  skip=1em
}
\setmainfont{Times New Roman}[BoldFont=Times New Roman Bold] % 设置英文使用Times New Roman


% 设置三线表单元格间距 - 使用booktabs自带间距，不再使用cellspace包
% \setlength\cellspacetoplimit{3pt}
% \setlength\cellspacebottomlimit{3pt}

% 确保所有正文文本使用12号宋体/Time New Roman，行距20pt，两端对齐
\AtBeginDocument{
  \normalfont
  \fontsize{12pt}{20pt}\selectfont
  \justifying % 两端对齐
  
  % 重新定义plain样式，使章节标题页也显示页眉
  \fancypagestyle{fancy}{% 
    \fancyhf[]{}
    \cfoot{\thepage} % 页码在页脚居中
    \chead{\songti\selectfont\color{gray}\fontsize{10.5pt}{12pt} 西安邮电大学毕业设计（论文）} % 页眉宋体五号字居中
  }
}

% 基本设置
\setlength{\parindent}{2em} % 段落首行左缩进2个汉字符
\linespread{1} % 确保行距设置正确
% 优化自动换行和中文排版
\sloppy
\tolerance=10000
\emergencystretch=3em
\pretolerance=500


% 用户自定义变量
\newcommand{\thesistitle}[1]{\def\@thesistitle{#1}}
\newcommand{\institute}[1]{\def\@institute{#1}}
\newcommand{\major}[1]{\def\@major{#1}}
\newcommand{\class}[1]{\def\@class{#1}}
\newcommand{\studentid}[1]{\def\@studentid{#1}}
\newcommand{\studentname}[1]{\def\@studentname{#1}}
\newcommand{\supervisor}[1]{\def\@supervisor{#1}}
\newcommand{\supervisortitle}[1]{\def\@supervisortitle{#1}}
\newcommand{\startdate}[1]{\def\@startdate{#1}}
\newcommand{\duedate}[1]{\def\@duedate{#1}}
\def\@thesistitle{未设置标题}
\def\@institute{未设置学院}
\def\@major{未设置专业}
\def\@class{未设置班级}
\def\@studentid{未设置学号}
\def\@studentname{未设置学生姓名}
\def\@supervisor{未设置导师姓名}
\def\@supervisortitle{未设置导师职称}
\def\@startdate{未设置起止时间}
\def\@duedate{未设置至时间}

% approval表格相关变量定义
\newcommand{\approvalauthor}[1]{\def\@approvalauthor{#1}}
\newcommand{\approvaltitle}[1]{\def\@approvaltitle{#1}}
\newcommand{\approvaltitlebrief}[1]{\def\@approvaltitlebrief{#1}}
\newcommand{\approvalrequirements}[1]{\def\@approvalrequirements{#1}}
\newcommand{\approvaltasks}[1]{\def\@approvaltasks{#1}}
\newcommand{\approvalprogress}[1]{\def\@approvalprogress{#1}}
\newcommand{\approvalchaircomment}[1]{\def\@approvalchaircomment{#1}}
\newcommand{\approvalchairname}[1]{\def\@approvalchairname{#1}}
\newcommand{\approvaldeptchairname}[1]{\def\@approvaldeptchairname{#1}}
\newcommand{\approvaldeanname}[1]{\def\@approvaldeanname{#1}}
\newcommand{\approvalchairdate}[1]{\def\@approvalchairdate{#1}}
\newcommand{\approvaldeptchairdate}[1]{\def\@approvaldeptchairdate{#1}}
\newcommand{\approvaldeanydate}[1]{\def\@approvaldeanydate{#1}}
\newcommand{\approvaltitletype}[1]{\def\@approvaltitletype{#1}}
\newcommand{\approvaltitlecategory}[1]{\def\@approvaltitlecategory{#1}}
\newcommand{\approvaltitlefrom}[1]{\def\@approvaltitlefrom{#1}}
\newcommand{\approvaljobtitle}[1]{\def\@approvaljobtitle{#1}}
\newcommand{\approvalcollege}[1]{\def\@approvalcollege{#1}}

% 默认值定义
\def\@approvalauthor{未设置}
\def\@approvaltitle{未设置}
\def\@approvaltitlebrief{}
\def\@approvalrequirements{}
\def\@approvaltasks{}
\def\@approvalprogress{}
\def\@approvalchaircomment{}
\def\@approvalchairname{未设置}
\def\@approvaldeptchairname{未设置}
\def\@approvalchairdate{年\hspace{1em}月\hspace{1em}日}
\def\@approvaldeptchairdate{年\hspace{1em}月\hspace{1em}日}
\def\@approvaldeanydate{年\hspace{1em}月\hspace{1em}日}
\def\@approvaltitletype{}
\def\@approvaltitlecategory{}
\def\@approvaltitlefrom{}
\def\@approvaljobtitle{未设置}
\def\@approvalcollege{未设置}

% opening表格相关变量定义
\newcommand{\openingstudent}[1]{\def\@openingstudent{#1}}
\newcommand{\openingstudentid}[1]{\def\@openingstudentid{#1}}
\newcommand{\openingclass}[1]{\def\@openingclass{#1}}
\newcommand{\openingteacher}[1]{\def\@openingteacher{#1}}
\newcommand{\openingtitle}[1]{\def\@openingtitle{#1}}
\newcommand{\openingpurpose}[1]{\def\@openingpurpose{#1}}
\newcommand{\openingbackground}[1]{\def\@openingbackground{#1}}
\newcommand{\openingproblems}[1]{\def\@openingproblems{#1}}
\newcommand{\openingplan}[1]{\def\@openingplan{#1}}
\newcommand{\openingteachcomment}[1]{\def\@openingteachcomment{#1}}

% opening表格变量默认值
\def\@openingstudent{未设置}
\def\@openingstudentid{未设置}
\def\@openingclass{未设置}
\def\@openingteacher{未设置}
\def\@openingtitle{未设置}
\def\@openingpurpose{}
\def\@openingbackground{}
\def\@openingproblems{}
\def\@openingplan{}
\def\@openingteachcomment{}

% score表格相关变量定义
\newcommand{\scorestudent}[1]{\def\@scorestudent{#1}}
\newcommand{\scoresex}[1]{\def\@scoresex{#1}}
\newcommand{\scoresid}[1]{\def\@scoresid{#1}}
\newcommand{\scoremajor}[1]{\def\@scoremajor{#1}}
\newcommand{\scoreclass}[1]{\def\@scoreclass{#1}}
\newcommand{\scorecoursename}[1]{\def\@scorecoursename{#1}}

% score表格变量默认值
\def\@scorestudent{未设置}
\def\@scoresex{未设置}
\def\@scoresid{未设置}
\def\@scoremajor{未设置}
\def\@scoreclass{未设置}
\def\@scorecoursename{未设置}

% 标题格式设置
\titleformat{\chapter}[hang]
  {\normalfont\fontsize{16pt}{20pt}\selectfont\heiti\bfseries\center}{第\thechapter 章}{1em}{}
\titlespacing*{\chapter}{0pt}{-22pt}{7pt}
\titleformat{\section}
  {\normalfont\fontsize{14pt}{20pt}\selectfont\heiti\bfseries}{\thesection}{1em}{}
\titlespacing*{\section}{0pt}{24pt}{6pt}
\titleformat{\subsection}
    {\normalfont\fontsize{12pt}{20pt}\selectfont\heiti\bfseries}{\thesubsection}{1em}{}
\titlespacing*{\subsection}{0pt}{12pt}{6pt}

% 定义封面命令
\newcommand{\makecover}{%
  \begin{titlepage}
    \vspace*{1cm}
    \centering
    % 校徽
    \includegraphics[height=3cm]{figures/title_logo.png}
    \vspace{1cm}
    
    % 标题
    \fontsize{36pt}{43pt}\selectfont\heiti\textbf{毕业设计（论文）}
    \vspace{1cm}
    
    % 表格信息
    \begin{tabular}{lll}
      {\songti\fontsize{16pt}{14pt}\selectfont{题\hspace{2em}目：}}&{\songti\fontsize{14pt}{15pt}\selectfont\underline{\makebox[10cm][c]{\fontspec{Times New Roman}\songti\selectfont\@thesistitle}}} &\\
      {\songti\fontsize{16pt}{14pt}\selectfont{学\hspace{2em}院：}}&{\songti\fontsize{14pt}{15pt}\selectfont\underline{\makebox[10cm][c]{\fontspec{Times New Roman}\songti\selectfont\@institute}}} &\\
      {\songti\fontsize{16pt}{14pt}\selectfont{专\hspace{2em}业：}}&{\songti\fontsize{14pt}{15pt}\selectfont\underline{\makebox[10cm][c]{\fontspec{Times New Roman}\songti\selectfont\@major}}} &\\
      {\songti\fontsize{16pt}{14pt}\selectfont{班\hspace{2em}级：}}&{\songti\fontsize{14pt}{15pt}\selectfont\underline{\makebox[10cm][c]{\fontspec{Times New Roman}\songti\selectfont\@class}}} &\\
      {\songti\fontsize{16pt}{14pt}\selectfont{学\hspace{2em}号：}}&{\songti\fontsize{14pt}{15pt}\selectfont\underline{\makebox[10cm][c]{\fontspec{Times New Roman}\songti\selectfont\@studentid}}} &\\
      {\songti\fontsize{16pt}{14pt}\selectfont{学生姓名：}}&{\songti\fontsize{14pt}{15pt}\selectfont\underline{\makebox[10cm][c]{\fontspec{Times New Roman}\songti\selectfont\@studentname}}} &\\
      {\songti\fontsize{16pt}{14pt}\selectfont{导师姓名：}}&{\songti\fontsize{14pt}{15pt}\selectfont\underline{\makebox[4cm][c]{\fontspec{Times New Roman}\songti\selectfont\@supervisor}}{\songti\fontsize{16pt}{16pt}\selectfont{\makebox[2cm][c]{职称：}}}\hspace{-0.5em}\underline{\makebox[4cm][c]{\fontspec{Times New Roman}\songti\selectfont\@supervisortitle}}} &\\
      {\songti\fontsize{16pt}{14pt}\selectfont{起止时间：}}&{\songti\fontsize{14pt}{15pt}\selectfont\underline{\makebox[4cm][c]{\fontspec{Times New Roman}\songti\selectfont\@startdate}}{\songti\fontsize{16pt}{16pt}\selectfont{\makebox[1cm][c]{至}}}\underline{\makebox[5cm][c]{\fontspec{Times New Roman}\songti\selectfont\@duedate}}} &
    \end{tabular}
    \vspace{3cm}
    
    % 日期
    \centering{{\fontspec{Times New Roman}\fontsize{14pt}{17pt}\selectfont\number\year}{\songti\fontsize{14pt}{17pt}\selectfont 年}{\fontspec{Times New Roman}\fontsize{14pt}{17pt}\selectfont\number\month}{\songti\fontsize{14pt}{17pt}\selectfont 月}{\fontspec{Times New Roman}\fontsize{14pt}{17pt}\selectfont\number\day}{\songti\fontsize{14pt}{17pt}\selectfont 日}}
  \end{titlepage}
}



% 重新定义摘要环境（report类已定义，使用renewenvironment避免冲突）
  \renewenvironment{abstract}
    {
     \clearpage
     \pagestyle{fancy}
     \fancyhf[]{}
     \cfoot{\thepage}
     \pagenumbering{Roman}
     \setcounter{page}{1}
     \vspace{40pt}% 段前40pt
     \begin{center}\bfseries\heiti\fontsize{16pt}{20pt}\selectfont 摘\hspace{2em}要\end{center}% 黑体小三号字，中间空两格

    \songti\fontsize{12pt}{20pt}\selectfont
    \begin{spacing}{2}
    
    }% 正文宋体小四号字，固定行距20pt，所有段落首行缩进
    {
    \end{spacing}
    }


% 关键字环境
\newenvironment{keywords}
  {\vspace{20pt}% 段前20pt
  \noindent\fontsize{12}{20pt}\heiti\selectfont\textbf{关键词：}
  \noindent\fontsize{12}{20pt}\songti\selectfont{
  }
  {}}

% 英文摘要环境定义
\newenvironment{abstracten}
  {
   \clearpage
   \vspace{40pt}% 段前40pt
  \begin{center}\fontspec{Arial}\fontsize{16pt}{20pt}\selectfont{ABSTRACT}\end{center}% Arial体小三号字，居中
 
   \fontspec{Times New Roman}\fontsize{12pt}{20pt}\selectfont

    \justifying% 两端对齐
    \begin{spacing}{2}
   }% Times New Roman字体，行距20pt
   {
    \end{spacing}
   }

% 英文关键词环境定义
  \newenvironment{keywordsen}
    {\vspace{20pt}% 段前20pt
    \noindent\fontspec{Times New Roman}\fontsize{12pt}{20pt}\selectfont\textbf{Keywords:}}
    {}

% 声明页命令
\newcommand{\makedeclaration}{%
  \input{macro/declaration.tex}
}

% 重新定义plain样式，使章节标题页也显示页眉
\fancypagestyle{plain}{% 
  \fancyhf{} % 清空所有页眉页脚
  \chead{\songti\selectfont\color{gray}\fontsize{10.5pt}{12pt} 西安邮电大学毕业设计（论文）} % 宋体五号的标题作为页眉
  \cfoot{\thepage} % 只保留页脚页码
}

% 自定义目录命令
\newcommand{\mytableofcontents}{% 

% 目录 - 使用底层方法彻底移除页眉
\clearpage
\makeatletter % 允许使用@命令
% 保存当前页面样式
\let\oldpagestyle\pagestyle
\let\oldthispagestyle\thispagestyle

% 创建一个完全空白的页面样式
\def\blankpagestyle{%
  \let\@oddhead\@empty
  \let\@evenhead\@empty
  \let\@oddfoot\@empty
  \let\@evenfoot\@empty
  \let\thispagestyle\relax
}

% 使用空白页面样式
\let\pagestyle\blankpagestyle

% 定义更密集的点分隔符命令
\def\densdotfill{%
  \cleaders\hb@xt@.3em{\hss.\hss}\hfill\kern\z@
}

% 设置目录一级标题（每章标题）为黑体小四号字，行间距20pt，添加密集点分隔符
\def\l@chapter##1##2{%
  \vspace{6pt}% 行前空6pt
  \fontsize{12pt}{20pt}\heiti\selectfont\bfseries % 黑体小四号字，行间距20pt
  \hb@xt@\textwidth{%
    \def\tocbasic@gluestrut{}
    \csname tocbasic@gluestrut\endcsname \songti##1
    \densdotfill\hb@xt@\@pnumwidth{\hfil ##2}\par
  }
}

% 设置目录二级及以上标题为宋体，并使用与章节相同的密集点分隔符
\def\l@section##1##2{%
  \fontsize{10.5pt}{14pt}\songti\selectfont % 宋体
  \hb@xt@\textwidth{%
    \def\tocbasic@gluestrut{}
    \csname tocbasic@gluestrut\endcsname\hspace{2em}##1\densdotfill\hb@xt@\@pnumwidth{\hfil ##2}\par
  }
}

\def\l@subsection##1##2{%
  \fontsize{10.5pt}{14pt}\songti\selectfont % 宋体
  \hb@xt@\textwidth{%
    \def\tocbasic@gluestrut{}
    \csname tocbasic@gluestrut\endcsname\hspace{4em}##1\densdotfill\hb@xt@\@pnumwidth{\hfil ##2}\par
  }
}

\def\l@subsubsection##1##2{%
  \fontsize{10.5pt}{14pt}\songti\selectfont % 宋体
  \hb@xt@\textwidth{%
    \def\tocbasic@gluestrut{}
    \csname tocbasic@gluestrut\endcsname\hspace{6em}##1\densdotfill\hb@xt@\@pnumwidth{\hfil ##2}\par
  }
}

% 手动生成目录标题和内容
  \vspace{40pt} % 段前40pt
  \begin{center}
    \fontsize{16pt}{20pt}\selectfont\heiti{目\hspace{2em}录} % 黑体小三号字，行距20pt
  \end{center}
  \vspace{20pt} % 段后20pt
  
  % 重定义\numberline命令为章节编号添加"第"和"章"（只对不含小数点的编号有效），并确保所有序号后都有空格
    \let\oldnumberline\numberline
    \def\numberline##1{%
      \in@{.}{##1}% 检查是否包含点
      \ifin@% 包含点的情况
         ##1\hspace{0.5em}
      \else% 不包含点 - chapter（第X章）
        第##1章\hspace{0.5em}
      \fi
    }
  
  \@starttoc{toc}

% 恢复原始页面样式
\let\pagestyle\oldpagestyle
\let\thispagestyle\oldthispagestyle
\makeatother % 恢复正常命令
\clearpage
}

% -------------------------  结论环境  -------------------------------------------

\makeatletter
\newenvironment{conclusion}{
  \clearpage
  \vspace*{-35pt}% 段前40pt
  \begin{center}\fontsize{16pt}{32pt}\selectfont\heiti{结\hspace{2em}论}\end{center}% 黑体小三号字，居中，标题间空两格
  \addcontentsline{toc}{chapter}{结\hspace{2em}论}
  \vspace{-8pt}% 
  \songti\fontsize{12pt}{20pt}\selectfont% 正文小四号字，行距20pt

}{
 
}
\makeatother

% -------------------------  致谢环境  -------------------------------------------

\makeatletter
\newenvironment{acknowledgements}{
  \clearpage
  \vspace*{-35pt}% 段前40pt
  \begin{center}\fontsize{16pt}{32pt}\selectfont\heiti{致\hspace{2em}谢}\end{center}% 黑体小三号字，居中，标题间空两格
  \addcontentsline{toc}{chapter}{致\hspace{2em}谢}
  \vspace{-8pt}% 
  \songti\fontsize{12pt}{20pt}\selectfont% 正文小四号字，行距20pt
  % ctex包已经设置了默认的中文字体，这里只需要确保行距正确
}{
  \par
}
\makeatother

% 定义表格单元格单倍行距命令
\newcommand{\tablecell}[1]{%
  \begingroup
  \songti\fontsize{11pt}{11pt}\selectfont % 11pt宋体，单倍行距
  %\linespread{1}\selectfont % 确保单倍行距
  #1%
  \endgroup
}

% 重新定义table环境
\let\oldtable\table
\let\endoldtable\endtable

\renewenvironment{table}[1][htbp]{%
  \oldtable[#1]
  \centering
  \renewcommand{\arraystretch}{1.5} % 增加20%的行间距以实现横线与文字间的3pt间距
  \setlength{\arrayrulewidth}{1pt} % 线条宽度
  % 确保表格内所有内容使用单倍行距
  \def\table@single@spacing{1}
  \renewcommand{\baselinestretch}{1}\selectfont
  \let\oldcaption\caption
  \renewcommand{\caption}[1]{%
    \oldcaption{##1}
    \vspace{3pt} % 标题与表格间的间距
  }
}{%
  \vspace{6pt} % 确保脚注与表格有适当间距
  \endoldtable
}

% 定义表头格式命令，确保表头所有列都使用黑体
\newcommand{\tableheader}[1]{\heiti\fontsize{11pt}{13pt}\selectfont #1}

% 参考文献相关命令
\newcommand{\thesisbibliography}[1][references]{%
  \clearpage % 确保从新页开始
  \addcontentsline{toc}{chapter}{参考文献} % 将参考文献添加到目录
  \bibliographystyle{plain}
  \bibliography{#1}
}

% 附录命令，将附录添加到目录中
\newcommand{\thesisappendix}[1][appendix]{%
  \appendix
  \clearpage
  \addcontentsline{toc}{chapter}{附\hspace{2em}录}
  \input{contents/#1.tex}
}

% 附录计数器初始化
\newcounter{appendixcounter}
\setcounter{appendixcounter}{0}

% 自动编号附录命令
\newcommand{\appendixchapter}{%
  \stepcounter{appendixcounter}%
  \ifnum\value{appendixcounter}>26%
    \PackageError{xuptThesis}{附录编号超出Z的范围}{最多支持26个附录（A-Z）}%
  \fi
  \clearpage
  \chapter*{附\hspace{2em}录\hspace{1em}\Alph{appendixcounter}}%
  % \addcontentsline{toc}{chapter}{附\hspace{2em}录\Alph{appendixcounter}}%
}

% 带参数的宋体字体命令，参数为字体大小
\newcommand{\simsun}[1]{%
  \fontsize{#1}{20}\songti\selectfont%
}

% 完成类定义
\endinput