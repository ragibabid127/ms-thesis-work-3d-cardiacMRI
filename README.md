# Project Title: 3D Cardiac MRI Segmentation Dataset Exploration

## Overview

This repository provides tools and scripts to systematically explore, validate, and log metadata and statistics for a labeled 3D cardiac MRI segmentation dataset. By following the steps below, you can ensure data integrity, understand dataset characteristics, and prepare a reproducible audit trail for modeling workflows.

## Repository Structure

```
├── raw/                        # Original NIfTI files (images and segmentations)
├── code/                       # Analysis and EDA scripts
│   ├── scan_inventory.py       # Inventory & integrity checks
│   ├── eda_stats.py            # Dataset-wide statistics and plots
│   └── utils.py                # Helper functions
├── config/                     # Configuration files
│   └── preprocessing.yaml      # Resampling & padding parameters
├── logs/                       # CSV logs and merged metadata
│   └── inventory.csv           # Per-case metadata and integrity flags
│   └── master_dataset.csv      # Joined clinical & technical metadata
├── reports/                    # Generated figures and snapshots
│   ├── snapshots/              # Sample slice montages
│   └── eda/                    # Histograms, bar charts, UMAP plots
├── .github/workflows/          # CI pipelines (data consistency)
│   └── inventory-check.yml     # Runs scan_inventory on push
└── README.md                   # Project overview and instructions
```

## Prerequisites

- Python 3.10+
- Install dependencies:
  ```bash
  pip install nibabel numpy pandas matplotlib seaborn torchio
  ```

## Getting Started

1. **Clone the repo**:
   ```bash
   git clone https://github.com/your-org/cardiac-eda.git
   cd cardiac-eda
   ```
2. **Set up environment**:
   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```
3. **Place data**: Copy your `.nii.gz` files into the `raw/` folder, preserving naming:
   - Images: `patientXXX_cropped_norm.nii.gz`
   - Masks:  `patientXXX_cropped_seg.nii.gz`

## Scripts & Usage

- **Inventory & Integrity**:
  ```bash
  python code/scan_inventory.py --input raw/ --output logs/inventory.csv
  ```
- **Quick Visual Check**:
  ```bash
  python code/eda_stats.py --mode snapshots --cases 10
  ```
- **Generate Dataset Statistics**:
  ```bash
  python code/eda_stats.py --mode full --outdir reports/eda/
  ```

## Configuration & Logs

- **preprocessing.yaml**: Defines target isotropic voxel spacing and tensor size.
- **logs/inventory.csv**: Contains per-patient fields:
  - `shape`, `spacing`, `intensity_{min,mean,max}`, `labels_present`, `integrity_flag`
- **logs/master\_dataset.csv**: Merged with clinical and technical metadata.

## Continuous Integration

A GitHub Action (`.github/workflows/inventory-check.yml`) re-runs `scan_inventory.py` on every push. The build fails if any new integrity issues are detected.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Run existing tests and add new ones if needed
4. Submit a pull request for review

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

