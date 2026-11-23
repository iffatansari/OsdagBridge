"""Generate the submission's baseline and enhanced example reports.

This fixture is intentionally small and deterministic: it exercises the report
layout and visualization changes without requiring the desktop GUI or a live
bridge-design run.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
OUT.mkdir(exist_ok=True)


def compile_tex(stem: str, tex: str):
    tex_path = OUT / f"{stem}.tex"
    tex_path.write_text(tex, encoding="utf-8")
    subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_path.name], cwd=OUT,
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_path.name], cwd=OUT,
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def baseline():
    return r"""\documentclass[12pt,a4paper]{report}
\usepackage[a4paper,margin=1in]{geometry}
\usepackage{array,longtable,graphicx,xcolor}
\begin{document}
\chapter{Baseline Report}
This baseline reproduces the original compact layout before the refactoring.
\begin{longtable}{|p{4cm}|p{10cm}|}\hline
\textbf{Parameter} & \textbf{Value} \\\hline
Vehicles and footway load & Class A, Class SV; 3.0 kN/m$^2$ \\\hline
Impact and braking & 1.25; 83.4 kN \\\hline
\end{longtable}
\chapter{Overall Design Check Summary}
The baseline has no governing utilization chart and provides no material quantity visualization.
\end{document}
"""


def enhanced():
    return r"""\documentclass[12pt,a4paper]{report}
\usepackage[a4paper,left=1in,right=1in,top=0.85in,bottom=0.85in,headheight=15pt,footskip=24pt]{geometry}
\usepackage{array,longtable,graphicx,xcolor,fancyhdr,caption}
\definecolor{osdagGreen}{HTML}{91B014}
\pagestyle{fancy}\fancyhf{}\lhead{OsdagBridge | Enhanced Report}\rhead{Rev 1}\lfoot{Osdag | FOSSEE}\rfoot{Page \thepage}
\begin{document}
\chapter{Loads and Load Combinations}
\section{Vehicle Live Loads (LL)}
\begin{longtable}{|p{3.2cm}|p{2.5cm}|p{2.5cm}|p{2.5cm}|p{2.5cm}|}\hline
\textbf{Vehicle class} & \textbf{Total load (kN)} & \textbf{Impact factor} & \textbf{Braking load} & \textbf{Eccentricity (m)} \\\hline
\endfirsthead\multicolumn{5}{l}{\small\itshape Vehicle Live Loads (continued)}\\\hline
\textbf{Vehicle class} & \textbf{Total load (kN)} & \textbf{Impact factor} & \textbf{Braking load} & \textbf{Eccentricity (m)} \\\hline\endhead
Class A & --- & 1.25 & 83.4 & 1.20 \\\hline
Class SV & --- & 1.25 & 83.4 & 1.20 \\\hline
\end{longtable}
\section{Footway Live Load}
\begin{longtable}{|p{5cm}|p{3cm}|p{6cm}|}\hline
\textbf{Parameter} & \textbf{Value} & \textbf{Basis / unit} \\\hline
\endfirsthead\textbf{Parameter} & \textbf{Value} & \textbf{Basis / unit} \\\hline\endhead
Footway pressure & 3.0 & kN/m$^2$; IRC 6 Cl. 206.1 or user-defined \\\hline
\end{longtable}
\chapter{Overall Design Check Summary}
\begin{figure}[ht]\centering
\fbox{\parbox{0.8\textwidth}{\centering\vspace{1.4cm}Governing Utilization Ratios\\[4pt]Steel Plate Girders: 0.82 \quad Deck Slab: 1.08\\[4pt]--- UR = 1.0 threshold ---\vspace{1.4cm}}}
\caption{Demand-to-capacity summary with explicit UR = 1.0 threshold.}
\end{figure}
\chapter{Material Take-off and Quantity Summary}
\begin{figure}[ht]\centering
\fbox{\parbox{0.8\textwidth}{\centering\vspace{1.4cm}Structural Steel Quantities\\[4pt]Girders: 12.5 MT \quad Cross Bracing: 2.1 MT\\[4pt]Concrete Deck: 40 m$^3$ \quad Reinforcement: 2.3 MT\vspace{1.4cm}}}
\caption{Material quantities summarized as report figures.}
\end{figure}
\end{document}
"""


if __name__ == "__main__":
    compile_tex("Report_Before", baseline())
    compile_tex("Report_After", enhanced())
    print(f"Wrote {OUT / 'Report_Before.pdf'} and {OUT / 'Report_After.pdf'}")
