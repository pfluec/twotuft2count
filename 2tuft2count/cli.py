# Updated cli.py with support for panel, threshold_json, and save_fcs
import click
from .combine import combine_channels
from .segment import segment_images
from .measure import measure_intensities
from .quantify import quantify_cells
from .visualize import launch_viewer
import os

@click.group()
def main():
    """CellQuant CLI: Process, analyze, and visualize multiplexed imaging data."""
    pass

@main.command()
@click.argument('input_dir')
@click.argument('output_dir')
def combine(input_dir, output_dir):
    """Combine separate channel TIFFs into multi-channel TIFFs."""
    combine_channels(input_dir, output_dir)

@main.command()
@click.argument('input_dir')
@click.argument('output_dir')
def segment(input_dir, output_dir):
    """Run InstanSeg segmentation on multi-channel TIFFs."""
    segment_images(input_dir, output_dir)

@main.command()
@click.argument('image_dir')
@click.argument('mask_dir')
@click.option('--csv-dir', default='csv', show_default=True, help='Folder to save per-image CSVs')
@click.option('--fcs-dir', default='fcs', show_default=True, help='Folder to save per-image FCS files')
@click.option('--combined-fcs', default='all_images_fcs/combined.fcs', show_default=True, help='Path to save merged FCS')
@click.option('--panel', default='panel.csv', help="Path to panel CSV mapping channels to markers.")
def measure(image_dir, mask_dir, csv_dir, fcs_dir, combined_fcs, panel):
    """Measure all image/mask pairs and export to CSV + FCS (individual + merged)."""
    measure_intensities(image_dir, mask_dir, csv_dir, fcs_dir, combined_fcs, panel)


@main.command()
@click.option('--csv-dir', default='csv', show_default=True, help="Directory containing per-cell CSVs from measure step.")
@click.option('--results-dir', default='results', show_default=True, help="Directory to save summary CSVs.")
@click.option('--panel', default='panel.csv', show_default=True, help="Path to panel CSV mapping channels to markers.")
@click.option('--use-manual-thresholds', is_flag=True, show_default=True, help="Use a manual thresholds JSON file from csv/*.json.")
@click.option('--threshold-source-image', default=None, help="Image base name used to locate the *_thresholds.json file to use thresholds from a specific image.")
def quantify(csv_dir, results_dir, panel, use_manual_thresholds, threshold_source_image):
    """Quantify marker-positive populations across per-cell CSV files."""
    quantify_cells(
        csv_dir=csv_dir,
        results_dir=results_dir,
        panel=panel,
        use_manual_thresholds=use_manual_thresholds,
        threshold_source_image=threshold_source_image
    )




@main.command()
@click.argument('image_base')
@click.option('--img-dir', default='img', show_default=True, help="Directory containing multi-channel TIFF images.")
@click.option('--mask-dir', default='masks', show_default=True, help="Directory containing mask label TIFFs.")
@click.option('--csv-dir', default='csv', show_default=True, help="Directory containing per-cell measurements.")
@click.option('--panel', default='panel.csv', show_default=True, help="Path to panel CSV mapping channels to markers.")
@click.option('--threshold-json-out', default=None, help="Path to save threshold JSON file from GUI.")
@click.option('--use-manual-thresholds', is_flag=True, help="Use manually saved thresholds.")
@click.option('--threshold-source-image', default=None, help="Base image name for threshold file (e.g., '1_1_1_s03').")
def visualize(image_base, img_dir, mask_dir, csv_dir, panel,
              threshold_json_out, use_manual_thresholds, threshold_source_image):
    """Launch Napari with interactive threshold widget using image base name."""
    image_path = os.path.join(img_dir, f"{image_base}.tiff")
    label_path = os.path.join(mask_dir, f"{image_base}.tiff")
    csv_path = os.path.join(csv_dir, f"{image_base}.csv")

    if threshold_json_out is None:
        threshold_json_out = os.path.join(csv_dir, f"{image_base}_thresholds.json")

    launch_viewer(image_path, label_path, csv_path, panel,
                  threshold_json_out=threshold_json_out,
                  use_manual_thresholds=use_manual_thresholds,
                  threshold_source_image=threshold_source_image)





