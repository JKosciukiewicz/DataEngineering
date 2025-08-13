import pandas as pd
import numpy as np
import tifffile
from pathlib import Path

CSV_PATH = "/net/tscratch/people/plgjkosciukiewi/bbbc021/BBBC021_v1_image.csv"
DATA_DIR = "/net/tscratch/people/plgjkosciukiewi/bbbc021/extracted_bbbc021/"
OUTPUT_DIR = "/net/tscratch/people/plgjkosciukiewi/bbbc021/BBBC_5_CHANNEL_CLOOME"

def convert_bbbc021_to_5channel(metadata_df, base_path, output_dir):
    """Convert BBBC021 3-channel images to 5-channel format"""

    Path(output_dir).mkdir(exist_ok=True)
    output_paths = []

    for i, row in metadata_df.iterrows():
        try:
            # Load the 3 channels
            dapi_path = Path(base_path) / row['Image_PathName_DAPI'] / row['Image_FileName_DAPI']
            tubulin_path = Path(base_path) / row['Image_PathName_Tubulin'] / row['Image_FileName_Tubulin']
            actin_path = Path(base_path) / row['Image_PathName_Actin'] / row['Image_FileName_Actin']

            dapi = tifffile.imread(str(dapi_path))
            tubulin = tifffile.imread(str(tubulin_path))
            actin = tifffile.imread(str(actin_path))

            # Create 5-channel image (5, H, W)
            h, w = dapi.shape
            five_channel = np.zeros((5, h, w), dtype=dapi.dtype)

            # Map channels to ["Mito", "ERSyto", "ERSytoBleed", "Ph_golgi", "Hoechst"]
            # five_channel[0] = 0       # Mito (zeros)
            five_channel[1] = tubulin   # ERSyto (from Tubulin)
            # five_channel[2] = 0       # ERSytoBleed (zeros)
            five_channel[3] = actin     # Ph_golgi (from Actin)
            five_channel[4] = dapi      # Hoechst (from DAPI)

            # Save as 5-channel TIFF
            plate = row['Image_Metadata_Plate_DAPI']
            well = row['Image_Metadata_Well_DAPI']
            img_num = row['ImageNumber']

            output_file = f"{output_dir}/plate_{plate}_well_{well}_img_{img_num}.tiff"
            tifffile.imwrite(output_file, five_channel)
            output_paths.append(output_file)

            if i % 100 == 0:
                print(f"Processed {i} images...")

        except Exception as e:
            print(f"Failed on image {i}: {e}")
            output_paths.append(None)  # Keep index alignment
            continue

    # Save output paths to CSV
    output_df = pd.DataFrame({'Image_Name': output_paths})
    output_df.to_csv(f"{output_dir}/converted_images.csv", index=False)

    print(f"Done! Converted {len(metadata_df)} images")
    print(f"Saved image paths to {output_dir}/converted_images.csv"



# Usage:
metadata_df = pd.read_csv(CSV_PATH)
convert_bbbc021_to_5channel(metadata_df, DATA_DIR, OUTPUT_DIR)