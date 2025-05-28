OMERO Multi-Shape ROI Importer
=========================================

Description:
------------
This Python script connects to an OMERO server and imports multiple types of ROIs 
(Regions of Interest) from a CSV file into OMERO images. Supported ROI types include 
rectangles, polygons, ellipses, and lines. Each ROI is added to the specified image 
and is set to be visible across all Z layers.

Features:
---------
- Connects securely to an OMERO server using user credentials.
- Lists available OMERO groups and allows group switching.
- Supports importing rectangular, polygonal, elliptical, and linear ROIs.
- Reads ROIs from a well-structured CSV file.
- Adds ROIs to images on OMERO and displays confirmation messages.

CSV File Format:
----------------
The CSV file must contain the following columns depending on the ROI type:

- Rectangle:
  - `image_id`, `type` (must be "rectangle"), `X`, `Y`, `Width`, `Height`, `text` (optional)
- Polygon:
  - `image_id`, `type` (must be "polygon"), `X_points` (comma-separated integers), `Y_points` (comma-separated integers), `text` (optional)
- Ellipse:
  - `image_id`, `type` (must be "ellipse"), `X`, `Y`, `Width`, `Height`, `text` (optional)
- Line:
  - `image_id`, `type` (must be "line"), `X1`, `Y1`, `X2`, `Y2`, `text` (optional)

Make sure your CSV file adheres to this format before running the script.

Requirements:
-------------
The script requires the following Python libraries:
- ezomero
- pandas
- omero-gateway
- tkinter (included in most Python distributions)

Installation:
-------------
Before running the script, install the required packages:

pip install ezomero
pip install pandas
pip install omero-py


If `tkinter` is missing (common on some Linux distributions), install it manually:

sudo apt-get install python3-tk


Usage:
------
1. Run the script:
python importcsv.py
2. Enter the OMERO server host, username, and password.
3. Select the OMERO group to use.
4. Select the CSV file with ROI data.
5. The script will process the CSV and upload ROIs to the specified images.
6. Confirmation messages will appear once ROIs are successfully added.

Author:
-------
This script was developed by **Daurys De Alba**.
- Email: daurysdealbaherra@gmail.com
- Email: DeAlbaD@si.edu
