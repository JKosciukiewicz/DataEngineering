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
    for dir in os.listdir(week_path):
        dir_path = os.path.join(week_path, dir)
        if os.path.isdir(dir_path):
            for image in os.listdir(dir_path):
                # Join with directory to get relative path
                rel_path = os.path.join(directory, image)
                image_paths.append(rel_path)
# Create DataFrame
df = pd.DataFrame(image_paths, columns=["image_path"])
df.to_csv(os.path.join(CSV_PATH,"bray_image_paths.csv"), index=False)