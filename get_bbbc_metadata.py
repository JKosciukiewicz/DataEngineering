import pandas as pd
import os

OUTPUT_PATH = "/net/tscratch/people/plgjkosciukiewi/bbbc021/OUT_BBC"
CSV_PATH = "/net/tscratch/people/plgjkosciukiewi/bbbc021/"
# OUTPUT_PATH = "/Volumes/Samsung SSD 990 EVO Plus 4TB/Datasets/bray/bray_4_channel"
# CSV_PATH = "/Volumes/Samsung SSD 990 EVO Plus 4TB/Datasets/bray"

# List to hold image paths
image_paths = []

# Walk through subdirectories
for week_directory in sorted(os.listdir(OUTPUT_PATH)):
    week_path = os.path.join(OUTPUT_PATH, week_directory)
    for directory in os.listdir(week_path):
        dir_path = os.path.join(week_path, directory)
        if os.path.isdir(dir_path):
            for image in os.listdir(dir_path):
                # Join with directory to get relative path
                rel_path = os.path.join(week_path, dir_path, image)
                image_paths.append(rel_path)
# Create DataFrame
df = pd.DataFrame(image_paths, columns=["Image_Name"])
df.to_csv(os.path.join(CSV_PATH,"bbbc_image_paths.csv"), index=False)