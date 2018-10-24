# FDTD_make_figani

[SALMON](https://salmon-tddft.jp/) has a FDTD functionality to simulate electromagnetic problems. This program makes figures and animations from the results obtained by SALMON.

![figure](misc/sample.gif)

## Requirements

 - Python 3
 - NumPy
 - matplotlib
 - ffmpeg

If you are windows user who uses python for the first time, I recommend to install [WinPython](https://sourceforge.net/projects/winpython/) that includes all requirements for this program.

## Usage

`make_figani.py` is an executable file. `figani.inp` is a input file. `make_figani.py` and `figani.inp` **must be in the same hierarchy**.<br><br>
The input parameters are as follows:<br>

- ***al_em(3)*** <br>
Size of simulation box in electromagnetic analysis. **This must match the input parameter in SALMON**.

## External Links

### SALMON Project
  - SALMON Official Website - https://salmon-tddft.jp/
  - SALMON Github Repository - https://github.com/salmon-tddft/SALMON/
