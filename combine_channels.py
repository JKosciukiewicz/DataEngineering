import os
import zipfile
import shutil
import numpy as np
import tifffile
from collections import defaultdict

DATA_PATH = "/net/afscra/people/plgjkosciukiewi/datasets/bray"
OUTPUT_PATH = "/net/afscra/people/plgjkosciukiewi/datasets/bray_4_channel"

CHANNELS = ["Hoechst", "ERSyto", "Ph_golgi", "Mito"]

os.makedirs(OUTPUT_PATH, exist_ok=True)

def get_clean_id(filename):
    parts = filename.split("_")
    return "_".join(parts[:3]) if len(parts) >= 3 else None

# Step 1: Get unique plate IDs from zip filenames
zip_files = [f for f in os.listdir(DATA_PATH) if f.endswith(".zip")]
plate_ids = set(f.split("-")[0] for f in zip_files if "-" in f)

for plate_id in plate_ids:
    print(f"\nProcessing plate: {plate_id}")

    # Step 2: Unzip only the necessary channel folders
    channel_dirs = {}
    for channel in CHANNELS:
        zip_name = f"{plate_id}-{channel}.zip"
        zip_path = os.path.join(DATA_PATH, zip_name)

        if not os.path.exists(zip_path):
            print(f"Missing zip file for channel {channel} in plate {plate_id}, skipping plate.")
            break

        # Unzip into a temporary directory inside DATA_PATH
        extract_path = os.path.join(DATA_PATH, f"{plate_id}-{channel}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        channel_dirs[channel] = extract_path
    else:
        # Step 3: Process images once all channels are extracted
        image_maps = defaultdict(dict)
        for channel, dir_path in channel_dirs.items():
            for filename in os.listdir(dir_path):
                image_id = get_clean_id(filename)
                if image_id:
                    image_maps[image_id][channel] = filename

        valid_ids = [img_id for img_id, ch_map in image_maps.items() if len(ch_map) == len(CHANNELS)]
        print(f"  Found {len(valid_ids)} valid images.")

        output_plate_dir = os.path.join(OUTPUT_PATH, plate_id)
        os.makedirs(output_plate_dir, exist_ok=True)

        for img_id in valid_ids:
            try:
                stacked_channels = []
                for channel in CHANNELS:
                    filename = image_maps[img_id][channel]
                    img_path = os.path.join(channel_dirs[channel], filename)
                    img = tifffile.imread(img_path)
                    stacked_channels.append(np.array(img))

                stacked = np.stack(stacked_channels, axis=-1)
                out_path = os.path.join(output_plate_dir, f"{img_id}.tiff")
                tifffile.imwrite(out_path, stacked)
            except Exception as e:
                print(f"  Failed to process {img_id}: {e}")

        # # Step 4: Clean up extracted directories
        # for dir_path in channel_dirs.values():
        #     shutil.rmtree(dir_path)
        # print(f"  Cleaned up temporary folders for plate {plate_id}")
