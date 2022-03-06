#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Denis Meyer
#
# This file is part of ImageScaler.
#

"""Thread"""

import logging
import os
import json
import csv

from PIL import Image
from PyQt5.QtCore import QObject, QRunnable, pyqtSlot

from gui.signals.WorkerSignals import WorkerSignals


class ScalerThread(QRunnable):
    """Image scaler thread"""

    def __init__(self, images=[], width=None, height=None, outdir='', createpdf=True, scaled_image_suffix='-scaled'):
        """Initializes the thread

        :param images: The images
        :param width: The width
        :param height: The height
        :param createpdf: Flag whether to create a PDF file of all images
        """
        super().__init__()

        logging.debug('Initializing ScalerThread')

        self.images = images
        self.width = width
        self.height = height
        self.outdir = outdir
        self.createpdf = createpdf
        self.scaled_image_suffix = scaled_image_suffix

        self.pdf_name = 'AllImages'

        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """Runs the thread"""
        processed_img_cnt = 0
        try:
            list_img = []
            for img in self.images:
                logging.debug('Processing image "{}", {}x{} px (width x height)'.format(img, self.width, self.height))
                scaled_img_name = self._get_scaled_img_path(img)
                if scaled_img_name:
                    logging.debug('Scaled path of image "{}": "{}"'.format(img, scaled_img_name))
                    logging.debug('Writing to "{}"'.format(scaled_img_name))
                    try:
                        self._scale_image(input_image_path=img,
                                          output_image_path=scaled_img_name,
                                          width=self.width,
                                          height=self.height)
                    except Exception as e:
                        logging.debug(
                            'Exception while scaling: {}'.format(e))

                    processed_img_cnt += 1

                    try:
                        if self.createpdf:
                            if scaled_img_name.lower().endswith('.png'):
                                rgba = Image.open(scaled_img_name)
                                rgb = Image.new('RGB', rgba.size, (255, 255, 255))
                                rgb.paste(rgba, mask=rgba.split()[3])
                                list_img.append(rgb)
                            else:
                                list_img.append(Image.open(scaled_img_name))
                    except Exception as e:
                        logging.debug(
                            'Exception while converting rgba to rgb: {}'.format(e))

                    self.signals.scalingresult.emit(processed_img_cnt, len(self.images))
        except Exception as ex:
            logging.exception('Failed to process images.')
            self.signals.scalingerror.emit(ex)
        finally:
            if self.createpdf and list_img:
                pdf_name = self.outdir + '/' + self.pdf_name + '.pdf'
                logging.debug('Generating PDF file "{}"'.format(pdf_name))
                list_img[0].save(pdf_name, 'PDF', resolution=100.0, save_all=True, append_images=list_img[1:])
            self.signals.scalingfinished.emit(processed_img_cnt, len(self.images))

    def _get_scaled_img_path(self, path_img):
        """returns the image name of the scaled image

        :param path_img: The image path
        """
        try:
            with open(path_img) as f:
                fname = os.path.basename(f.name)
                lindex = fname.rfind('.')
                newname = fname[:lindex] + self.scaled_image_suffix
                suffix = fname[lindex:]
                logging.debug('Output image path: "{}"'.format(self.outdir + "/" + newname + suffix))

                return self.outdir + "/" + newname + suffix
        except Exception as e:
            logging.error('Error getting path for image "{}": {}'.format(path_img, e))
            return None

    def _scale_image(self,
                     input_image_path,
                     output_image_path,
                     width=None,
                     height=None):
        """Scales the image

        :param input_image_path: The input image path
        :param output_image_path: The output image path
        :param width: The width [optional if height set]
        :param height: The height [optional if width set]
        """
        original_image = Image.open(input_image_path)
        w, h = original_image.size
        logging.debug('The original image size is {wide} wide x {height} high'.format(wide=w, height=h))

        if width and height:
            max_size = (width, height)
        elif width:
            max_size = (width, h)
        elif height:
            max_size = (w, height)
        else:
            # No width or height specified
            raise RuntimeError('Width or height required!')

        original_image.thumbnail(max_size, Image.ANTIALIAS)
        original_image.save(output_image_path)

        scaled_image = Image.open(output_image_path)
        width, height = scaled_image.size
        logging.debug('The scaled image size is {wide} wide x {height} high'.format(wide=width, height=height))
