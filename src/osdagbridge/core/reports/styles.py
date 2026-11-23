"""Centralized visual and layout theme for OsdagBridge PDF reports.

All report chapters should consume these values rather than embedding independent
font, spacing, colour, or table-layout decisions.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class ReportTheme:
    accent: str = "91B014"
    accent_dark: str = "5D7600"
    pass_colour: str = "2E7D32"
    fail_colour: str = "C62828"
    header_fill: str = "EAF2C8"
    border_colour: str = "7A7A7A"
    body_font_size: str = "12pt"
    page_margin: str = "1in"
    head_height: str = "15pt"
    foot_skip: str = "24pt"
    table_col_pad: str = "5pt"
    row_stretch: str = "1.16"
    extra_row_height: str = "1.2pt"
    table_bottom_guard: str = "7\\baselineskip"

THEME = ReportTheme()

DOCUMENT_GEOMETRY = (
    f"a4paper, left={THEME.page_margin}, right={THEME.page_margin}, "
    f"top=0.85in, bottom=0.85in, headheight={THEME.head_height}, "
    f"footskip={THEME.foot_skip}"
)


def latex_layout_preamble() -> str:
    """Return packages and global layout controls used by every report."""
    return rf"""
% Centralized OsdagBridge report theme (styles.py)
\usepackage[{DOCUMENT_GEOMETRY}]{{geometry}}
\usepackage{{graphicx}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{booktabs}}
\usepackage{{array}}
\usepackage{{tabularx}}
\usepackage{{float}}
\usepackage{{fancyhdr}}
\usepackage[hidelinks]{{hyperref}}
\usepackage{{xcolor}}
\usepackage{{setspace}}
\usepackage{{enumitem}}
\usepackage{{caption}}
\usepackage{{subcaption}}
\usepackage{{multirow}}
\usepackage{{colortbl}}
\usepackage{{longtable}}
\usepackage{{titlesec}}
\usepackage{{titletoc}}
\usepackage{{lastpage}}
\usepackage{{makecell}}
\usepackage{{etoolbox}}
\usepackage{{needspace}}
\numberwithin{{table}}{{chapter}}
\numberwithin{{figure}}{{chapter}}
\setlength{{\tabcolsep}}{{{THEME.table_col_pad}}}
\renewcommand{{\arraystretch}}{{{THEME.row_stretch}}}
\setlength{{\LTleft}}{{\fill}}
\setlength{{\LTright}}{{\fill}}
\setlength{{\LTpre}}{{0pt}}
\setlength{{\LTpost}}{{8pt}}
\setlength{{\arrayrulewidth}}{{0.5pt}}
\setlength{{\extrarowheight}}{{{THEME.extra_row_height}}}
% Keep captions, headings, and the first table rows away from the footer.
\BeforeBeginEnvironment{{table}}{{\needspace{{{THEME.table_bottom_guard}}}}}
\BeforeBeginEnvironment{{longtable}}{{\needspace{{{THEME.table_bottom_guard}}}}}
\definecolor{{osdagGreen}}{{HTML}}{{{THEME.accent}}}
\definecolor{{osdagGreenDark}}{{HTML}}{{{THEME.accent_dark}}}
\definecolor{{reportPass}}{{HTML}}{{{THEME.pass_colour}}}
\definecolor{{reportFail}}{{HTML}}{{{THEME.fail_colour}}}
\definecolor{{reportHeader}}{{HTML}}{{{THEME.header_fill}}}
\newcolumntype{{L}}[1]{{>{{\raggedright\arraybackslash}}p{{#1}}}}
\newcolumntype{{C}}[1]{{>{{\centering\arraybackslash}}p{{#1}}}}
\newcolumntype{{R}}[1]{{>{{\raggedleft\arraybackslash}}p{{#1}}}}
\setlist{{topsep=3pt,itemsep=2pt,parsep=0pt}}
\setstretch{{1.12}}
"""


def longtable_header(header_tex: str) -> str:
    """Return a repeated longtable header block for first and later pages."""
    return ("\\endfirsthead\n"
            "\\multicolumn{7}{l}{\\small\\itshape Continued from previous page}\\\\\n"
            "\\hline\n" + header_tex +
            "\\\\\n\\hline\n\\endhead\n")
