# Auto Drawer

This Python program is helping to automate the longitudinal and cross-section drawing process using level sheets in the construction field. Every drawings are drawn by the program is saved in .dxf format. There are two data sheet templates in MS Excel format and Libra Calc format. you can use any of the file templates to add your drawing data. please DO NOT change any template's column names or any format before adding the data file to the program.

## Used Tools
  * Python 3.12.1
  * pip 24.0
  * pandas 2.2.1
  * ezdxf 1.1.4

## Setup Before Run
#### Step 01
Create a virtual environment using Python.
$python -m venv venv

Activate the virtual environment
$venv/scripts/activate

#### Step 02
Install required libraries
$pip install pandas==2.2.1, ezdxf==1.1.4, odfpy==1.4.1

#### Step 03
Replace your data file name and location in app.py file

#### Step 04
Run the app.py file, Then the drawing will create the same directory that the app.py file exists.

# Warning.....!!!!
**This Program is Not Completed Yet** In that case there can be find out some bugs.

# TODO list
  * Create a User Interface.
  * Fix bugs.
  * Optimize codes.
