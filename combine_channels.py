import os
import numpy as np
import tifffile
from collections import defaultdict

DATA_PATH = "/net/afscra/people/plgjkosciukiewi/datasets/bray_unzipped"
OUTPUT_PATH = "/net/afscra/people/plgjkosciukiewi/datasets/bray_4_channel"

CHANNELS = ["Hoechst", "ERSyto", "Ph_golgi", "Mito"]

os.makedirs(OUTPUT_PATH, exist_ok=True)

def get_clean_id(filename):
    parts = filename.split("_")
    return "_".join(parts[:3]) if len(parts) >= 3 else None

plate_ids = set([d.split("-")[0] for d in os.listdir(DATA_PATH) if "-" in d])

for plate_id in plate_ids:
    print(f"Processing plate: {plate_id}")

    channel_dirs = {
        channel: os.path.join(DATA_PATH, f"{plate_id}-{channel}")
        for channel in CHANNELS
    }

    if not all(os.path.isdir(p) for p in channel_dirs.values()):
        print(f"Skipping plate {plate_id} due to missing channels.")
        continue

    image_maps = defaultdict(dict)
    for channel, dir_path in channel_dirs.items():
        for filename in os.listdir(dir_path):
            image_id = get_clean_id(filename)
            if image_id:
                image_maps[image_id][channel] = filename

    valid_ids = [img_id for img_id, ch_map in image_maps.items() if len(ch_map) == len(CHANNELS)]
    print(f"Found {len(valid_ids)} valid images for plate {plate_id}")

    for img_id in valid_ids:
        try:
            stacked_channels = []
            for channel in CHANNELS:
                filename = image_maps[img_id][channel]
                img_path = os.path.join(channel_dirs[channel], filename)
                img = tifffile.imread(img_path)

                stacked_channels.append(np.array(img))

            stacked = np.stack(stacked_channels, axis=-1)

            output_plate_dir = os.path.join(OUTPUT_PATH, plate_id)
            os.makedirs(output_plate_dir, exist_ok=True)

            out_filename = f"{img_id}.tiff"
            out_path = os.path.join(output_plate_dir, out_filename)

            tifffile.imwrite(out_path, stacked)

        except Exception as e:
            print(f"Failed to process {img_id} in plate {plate_id}: {e}")
