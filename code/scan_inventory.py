#!/usr/bin/env python3
"""
scan_inventory.py

Scans a dataset directory for image/mask pairs and logs their properties to a CSV file.
"""

import os
import glob
import argparse
import nibabel as nib
import numpy as np
import pandas as pd

def scan_directory(input_dir):
    """
    Find all *_cropped_norm.nii.gz images in input_dir, match them with
    *_cropped_seg.nii.gz masks, and collect key stats.
    """
    image_pattern = os.path.join(input_dir, "*_cropped_norm.nii.gz")
    image_files = sorted(glob.glob(image_pattern))
    records = []

    for img_path in image_files:
        base = os.path.basename(img_path)
        patient_id = base.split("_")[0]

        # expected mask filename
        mask_path = img_path.replace("_cropped_norm.nii.gz", "_cropped_seg.nii.gz")
        if not os.path.exists(mask_path):
            print(f"[WARNING] No mask found for image: {img_path}")
            continue

        # load image & mask
        img = nib.load(img_path)
        img_data = img.get_fdata()
        mask = nib.load(mask_path)
        mask_data = mask.get_fdata()

        # basic integrity checks & stats
        shape_match = img_data.shape == mask_data.shape
        spacing = img.header.get_zooms()
        mask_spacing = mask.header.get_zooms()
        spacing_match= ((spacing[0]==mask_spacing[0]) and (spacing[1]==mask_spacing[1]) and (spacing[2]==mask_spacing[2]))
        min_intensity = float(np.min(img_data))
        mean_intensity = float(np.mean(img_data))
        max_intensity = float(np.max(img_data))
        unique_labels = np.unique(mask_data).tolist()

        records.append({
            "patient_id":        patient_id,
            "image_path":        img_path,
            "mask_path":         mask_path,
            "shape":             img_data.shape,
            "spacing_x":         spacing[0],
            "spacing_y":         spacing[1] if len(spacing) > 1 else np.nan,
            "spacing_z":         spacing[2] if len(spacing) > 2 else np.nan,
            "mask_spacing_x":    mask_spacing[0],
            "mask_spacing_y":    mask_spacing[1] if len(spacing) > 1 else np.nan,
            "mask_spacing_z":    mask_spacing[2] if len(spacing) > 2 else np.nan,
            "min_intensity":     min_intensity,
            "mean_intensity":    mean_intensity,
            "max_intensity":     max_intensity,
            "shape_match":       shape_match,
            "spacing_match":     spacing_match
        })

    return records

def main():
    p = argparse.ArgumentParser(description="Scan 3D MRI dataset and inventory image/mask stats.")
    p.add_argument(
        "--input_dir",
        type=str,
        default="/home/ragibabdi127/ms_thesis/cropped_norm/cropped_norm",
        help="Directory containing the NIfTI files (images & masks)."
    )
    p.add_argument(
        "--output_csv_path",
        type=str,
        default="logs/inventory.csv",
        help="Path to write the inventory CSV."
    )
    args = p.parse_args()

    # ensure output folder exists
    os.makedirs(os.path.dirname(args.output_csv_path), exist_ok=True)

    # run scan
    records = scan_directory(args.input_dir)
    if not records:
        print("No records found. Please check your input_dir and filename patterns.")
        return

    # build DataFrame
    df = pd.DataFrame(records)
    # serialize tuples & lists
    df["shape"] = df["shape"].apply(lambda t: "x".join(map(str, t)))

    # save CSV
    df.to_csv(args.output_csv_path, index=False)
    total = len(df)
    mismatches = int((~df["shape_match"]).sum())
    print(f"Scanned {total} cases, found {mismatches} shape mismatches.")

if __name__ == "__main__":
    main()
