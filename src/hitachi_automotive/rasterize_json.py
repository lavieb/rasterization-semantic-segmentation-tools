#!/usr/bin/env python

import logging
from argparse import ArgumentParser
import os
import json
import gdal

from .utils import rasterize_polygon

if __name__ == "__main__":
    parser = ArgumentParser(description="Generate a TIFF file from the JSON file provided")
    parser.add_argument('-i', '--input', help='JSON file produced by the software', required=True)
    parser.add_argument('-m', '--image', help='TIFF image considered for the mask', required=True)
    parser.add_argument('-o', '--output', help='TIFF output file containing the mask of the image', required=True)
    parser.add_argument('-d', '--debug', help='Enable debugger mode', action="store_true")

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(format='%(asctime)s [%(levelname)-8s] %(message)s')
    logger = logging.getLogger('my-logger')
    if args.debug:
        logger.setLevel(logging.DEBUG)

    # Initialisation
    json_path = args.input
    image_path = args.image
    output_path = args.output

    logger.debug('Creating the mask...')

    # Get the raster from the JSON file
    logger.debug('Rasterizing the polygon...')

    image_dst = gdal.Open(image_path, gdal.GA_ReadOnly)
    raster = rasterize_polygon(json_path, image_dst.RasterXSize, image_dst.RasterYSize)
    image_dst = None

    logger.debug('Finished rasterizing the polygon')

    # Produce the TIFF image
    logger.debug('Writing on the TIFF file...')

    outdriver = gdal.GetDriverByName("GTiff")
    outdata = outdriver.Create(output_path, raster.shape[1],
                               raster.shape[0], 1, gdal.GDT_Byte)
    outdata.GetRasterBand(1).WriteArray(raster)
    outdata = None

    logger.debug('Finished writing on the TIFF file')

    logger.debug('Finished creating the mask')
