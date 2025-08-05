import os
import numpy as np
import tifffile
import pandas as pd

CSV_PATH = "/net/tscratch/people/plgjkosciukiewi/bbbc021/BBBC021_v1_image.csv"
DATA_DIR = "/net/tscratch/people/plgjkosciukiewi/bbbc021/extracted_bbbc021/"
OUTPUT_DIR = "/net/tscratch/people/plgjkosciukiewi/bbbc021/OUT_BBC"

metadata = pd.read_csv(CSV_PATH)

for _, row in metadata.iterrows():
    Image_PathName_DAPI = row["Image_PathName_DAPI"]
    Image_PathName_Tubulin = row["Image_PathName_Tubulin"]
    Image_PathName_Actin = row["Image_PathName_Actin"]

    Image_FileName_DAPI = row["Image_FileName_DAPI"]
    Image_FileName_Tubulin = row["Image_FileName_Tubulin"]
    Image_FileName_Actin = row["Image_FileName_Actin"]

    image_dapi_path = os.path.join(DATA_DIR, Image_PathName_DAPI, Image_FileName_DAPI)
    image_tubulin_path = os.path.join(DATA_DIR, Image_PathName_Tubulin, Image_FileName_Tubulin)
    image_actin_path = os.path.join(DATA_DIR, Image_PathName_Actin, Image_FileName_Actin)

    try:
        image_dapi = tifffile.imread(image_dapi_path)
        image_tubulin = tifffile.imread(image_tubulin_path)
        image_actin = tifffile.imread(image_actin_path)
    except FileNotFoundError as e:
        print(f"Skipping due to missing file: {e}")
        continue

    stacked = np.stack([image_dapi, image_tubulin, image_actin], axis=-1)  # shape: (H, W, 3)

    # Create subdirectory if needed
    sub_output_dir = os.path.join(OUTPUT_DIR, Image_PathName_DAPI)
    os.makedirs(sub_output_dir, exist_ok=True)

    output_path = os.path.join(sub_output_dir, Image_FileName_DAPI)  # Keep original file name
    tifffile.imwrite(output_path, stacked)
