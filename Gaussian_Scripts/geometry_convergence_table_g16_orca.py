#!/usr/bin/env python3
"""
orca_convergence_table.py

Detect whether the file is from Gaussian or ORCA,
parse geometry optimization convergence data,
and display a nicely formatted table with convergence info.

Author: Muhammad Ali Hashmi + ChatGPT
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

try:
    from rich.console import Console
    from rich.table import Table
    from rich import box
except Exception:
    sys.stderr.write(
        "This script requires the 'rich' package.\n"
        "Install it (user-local is fine) with:\n"
        "  python3 -m pip install --user rich\n"
    )
    raise

console = Console()

# ---------------- HELPER FUNCTIONS ----------------

def detect_program(filepath: str) -> str:
    """
    Detect if the file is Gaussian or ORCA by scanning its contents.
    """
    markers = {
        "gaussian": [
            r"Entering Gaussian System, Link 0=g16",
            r"Gaussian, Inc\.",
            r"Copyright .* Gaussian, Inc\.",
        ],
        "orca": [
            r"\* O\s+R\s+C\s+A \*",
            r"ORCA",
            r"Frank Neese",
            r"Geometry convergence",
        ],
    }
    with open(filepath, "r", errors="ignore") as f:
        for _ in range(5000):  # Read first 5000 lines
            line = f.readline()
            if not line:
                break
            if any(re.search(pat, line) for pat in markers["gaussian"]):
                return "gaussian"
            if any(re.search(pat, line) for pat in markers["orca"]):
                return "orca"
    # Fallback detection based on whole text
    text = Path(filepath).read_text(errors="ignore")
    if re.search(r"Geometry convergence", text):
        return "orca"
    if re.search(r"Item\s+Value\s+Threshold\s+Converged\?", text):
        return "gaussian"
    return "unknown"

def format_float(x: Optional[float], ndp: int = 6) -> str:
    """
    Format a float with fixed decimal places (no scientific notation).
    """
    if x is None:
        return "-"
    return f"{x:.{ndp}f}"

# ---------------- GAUSSIAN PARSER ----------------

def parse_gaussian(text: str) -> List[Dict[str, Any]]:
    """
    Parse Gaussian16 'Item / Value / Threshold / Converged?' tables.
    Returns list of steps, each containing values and convergence flags.
    """
    steps = []

    # Find each "Item Value Threshold Converged?" header
    header_pat = re.compile(r'Item\s+Value\s+Threshold\s+Converged\?', re.M)
    headers = list(header_pat.finditer(text))

    for i, m in enumerate(headers):
        start = m.end()
        end = headers[i+1].start() if i+1 < len(headers) else len(text)
        block = text[start:end]

        # Helper to parse a row from the block
        def row(label: str) -> Optional[Tuple[float, float, bool]]:
            r = re.search(rf'{label}\s+([-\d.]+)\s+([-\d.]+)\s+(YES|NO)', block)
            if r:
                return (float(r.group(1)), float(r.group(2)), r.group(3) == "YES")
            return None

        rows = {
            "max_force": row(r"Maximum Force"),
            "rms_force": row(r"RMS\s+Force"),
            "max_disp":  row(r"Maximum Displacement"),
            "rms_disp":  row(r"RMS\s+Displacement"),
        }

        # Parse Predicted change in Energy
        energy_val: Optional[float] = None
        er = re.search(r'Predicted change in Energy=([-\d.DEded+]+)', block)
        if er:
            sval = er.group(1).replace('D', 'E').replace('d', 'E')
            try:
                energy_val = float(sval)
            except:
                energy_val = None

        steps.append({
            "rows": rows,
            "energy": {"val": energy_val},
        })

    return steps

# ---------------- ORCA PARSER ----------------

def parse_orca(text: str) -> List[Dict[str, Any]]:
    """
    Parse ORCA 'Geometry convergence' tables.
    Handles missing or shortened 'Energy change' lines.
    """
    steps = []
    # Find all Geometry convergence blocks
    cut_points = [m.start() for m in re.finditer(r'Geometry convergence', text)]
    for i, s in enumerate(cut_points):
        e = cut_points[i + 1] if i + 1 < len(cut_points) else len(text)
        block = text[s:e]

        def row3(label: str) -> Optional[Tuple[float, float, bool]]:
            r = re.search(rf'{label}\s+([-\d.]+)\s+([-\d.]+)\s+(YES|NO)', block)
            if r:
                return (float(r.group(1)), float(r.group(2)), r.group(3) == "YES")
            return None

        rows = {
            "rms_grad": row3(r"RMS gradient"),
            "max_grad": row3(r"MAX gradient"),
            "rms_step": row3(r"RMS step"),
            "max_step": row3(r"MAX step"),
        }

        # Parse Energy change
        energy_val: Optional[float] = None
        energy_thr: Optional[float] = None
        energy_conv: Optional[bool] = None

        r_full = re.search(r'Energy change\s+([-\d.]+)\s+([-\d.]+)\s+(YES|NO)', block)
        if r_full:
            energy_val = float(r_full.group(1))
            energy_thr = float(r_full.group(2))
            energy_conv = (r_full.group(3) == "YES")
        else:
            r_short = re.search(r'Energy change\s+([-\d.]+)', block)
            if r_short and r_short.group(1) != "...":
                try:
                    energy_val = float(r_short.group(1))
                except:
                    energy_val = None

        if any(v is not None for v in rows.values()) or energy_val is not None:
            steps.append({
                "rows": rows,
                "energy": {"val": energy_val, "thr": energy_thr, "conv": energy_conv},
            })

    return steps

# ---------------- RENDER FUNCTIONS ----------------

def render_gaussian(steps: List[Dict[str, Any]], filename: str) -> None:
    """
    Display Gaussian convergence table.
    Uses fixed ΔE threshold = 0.00004 for convergence.
    """
    print()  # Blank line before table
    title = f"GAUSSIAN Geometry Optimization Summary of {filename}"
    table = Table(title=title, box=box.HEAVY_HEAD, header_style="bold")

    # Add table columns
    table.add_column("Step", justify="right")
    table.add_column("Max Force", justify="right")
    table.add_column("Conv MF", justify="center")
    table.add_column("RMS Force", justify="right")
    table.add_column("Conv RF", justify="center")
    table.add_column("Max Disp", justify="right")
    table.add_column("Conv MD", justify="center")
    table.add_column("RMS Disp", justify="right")
    table.add_column("Conv RD", justify="center")
    table.add_column("Energy Change", justify="right")
    table.add_column("Conv E", justify="center")

    e_thr = 0.00004  # Fixed threshold for Gaussian ΔE

    for idx, st in enumerate(steps, 1):
        r = st["rows"]
        e_val = st["energy"]["val"]

        def val_cell(tup):
            if not tup:
                return "-"
            val, thr, conv = tup
            s = format_float(val)
            return f"[green]{s}[/green]" if conv else s

        # Energy value cell
        de_conv = None
        if e_val is not None:
            de_conv = abs(e_val) <= e_thr
        de_cell = format_float(e_val)
        if de_conv:
            de_cell = f"[green]{de_cell}[/green]"

        table.add_row(
            str(idx),
            val_cell(r["max_force"]), "YES" if (r["max_force"] and r["max_force"][2]) else "NO" if r["max_force"] else "-",
            val_cell(r["rms_force"]), "YES" if (r["rms_force"] and r["rms_force"][2]) else "NO" if r["rms_force"] else "-",
            val_cell(r["max_disp"]),  "YES" if (r["max_disp"]  and r["max_disp"][2])  else "NO" if r["max_disp"]  else "-",
            val_cell(r["rms_disp"]),  "YES" if (r["rms_disp"]  and r["rms_disp"][2])  else "NO" if r["rms_disp"]  else "-",
            de_cell,
            "YES" if (de_conv is True) else ("NO" if de_conv is False else "-"),
        )

    console.print(table)
    console.print(f"[dim]Note: ΔE threshold (Gaussian) fixed at {e_thr:.6f}[/dim]")

def render_orca(steps: List[Dict[str, Any]], filename: str) -> None:
    """
    Display ORCA convergence table (thresholds read from file).
    """
    print()
    title = f"ORCA Geometry Optimization Summary of {filename}"
    table = Table(title=title, box=box.HEAVY_HEAD, header_style="bold")

    table.add_column("Step", justify="right")
    table.add_column("RMS grad", justify="right")
    table.add_column("Conv RG", justify="center")
    table.add_column("MAX grad", justify="right")
    table.add_column("Conv MG", justify="center")
    table.add_column("RMS step", justify="right")
    table.add_column("Conv RS", justify="center")
    table.add_column("MAX step", justify="right")
    table.add_column("Conv MS", justify="center")
    table.add_column("Energy Change", justify="right")
    table.add_column("Conv E", justify="center")

    for idx, st in enumerate(steps, 1):
        r = st["rows"]
        e = st["energy"]

        def val_cell(tup):
            if not tup:
                return "-"
            val, thr, conv = tup
            s = format_float(val)
            return f"[green]{s}[/green]" if conv else s

        de_val = e.get("val") if e else None
        de_conv = e.get("conv") if e else None

        de_cell = format_float(de_val)
        if de_conv:
            de_cell = f"[green]{de_cell}[/green]"

        table.add_row(
            str(idx),
            val_cell(r["rms_grad"]), "YES" if (r["rms_grad"] and r["rms_grad"][2]) else "NO" if r["rms_grad"] else "-",
            val_cell(r["max_grad"]), "YES" if (r["max_grad"] and r["max_grad"][2]) else "NO" if r["max_grad"] else "-",
            val_cell(r["rms_step"]), "YES" if (r["rms_step"] and r["rms_step"][2]) else "NO" if r["rms_step"] else "-",
            val_cell(r["max_step"]), "YES" if (r["max_step"] and r["max_step"][2]) else "NO" if r["max_step"] else "-",
            de_cell,
            "YES" if (de_conv is True) else ("NO" if de_conv is False else "-"),
        )

    console.print(table)

# ---------------- MAIN ----------------

def main():
    if len(sys.argv) != 2:
        console.print("[red]Usage:[/red] python3 orca_convergence_table.py <output.log|output.out>")
        sys.exit(1)

    filepath = sys.argv[1]
    p = Path(filepath)
    if not p.exists():
        console.print(f"[red]File not found:[/red] {filepath}")
        sys.exit(1)

    program = detect_program(filepath)
    text = p.read_text(errors="ignore")
    fname_only = p.name

    if program == "gaussian":
        steps = parse_gaussian(text)
        if not steps:
            console.print("[yellow]No Gaussian optimization steps detected.[/yellow]")
            sys.exit(0)
        render_gaussian(steps, fname_only)
    elif program == "orca":
        steps = parse_orca(text)
        if not steps:
            console.print("[yellow]No ORCA optimization steps detected.[/yellow]")
            sys.exit(0)
        render_orca(steps, fname_only)
    else:
        console.print("[red]Could not determine whether the file is Gaussian or ORCA output.[/red]")
        sys.exit(2)

if __name__ == "__main__":
    main()
