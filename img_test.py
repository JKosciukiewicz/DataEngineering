import tifffile

img = tifffile.imread("/Volumes/Samsung SSD 990 EVO Plus 4TB/Datasets/bray/bray_4_channel/24277/cdp2bioactives_g10_s5.tiff")
print(img.shape)