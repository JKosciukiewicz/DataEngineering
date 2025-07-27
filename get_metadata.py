import pandas as pd
import os

OUTPUT_PATH = "/net/afscra/people/plgjkosciukiewi/datasets/bray_4_channel"
CSV_PATH = "/net/afscra/people/plgjkosciukiewi/datasets"
# OUTPUT_PATH = "/Volumes/Samsung SSD 990 EVO Plus 4TB/Datasets/bray/bray_4_channel"
# CSV_PATH = "/Volumes/Samsung SSD 990 EVO Plus 4TB/Datasets/bray"

# List to hold image paths
image_paths = []

# Walk through subdirectories
for directory in sorted(os.listdir(OUTPUT_PATH)):
    dir_path = os.path.join(OUTPUT_PATH, directory)
    if os.path.isdir(dir_path):
        for image in os.listdir(dir_path):
            # Join with directory to get relative path
            rel_path = os.path.join(directory, image)
            image_paths.append(rel_path)

# Create DataFrame
df = pd.DataFrame(image_paths, columns=["image_path"])
df.to_csv(os.path.join(CSV_PATH,"bray_image_paths.csv"), index=False)