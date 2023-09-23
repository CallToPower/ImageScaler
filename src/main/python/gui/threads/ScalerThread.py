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

from PIL import Image
from PyQt5.QtCore import QObject, QRunnable, pyqtSlot

from gui.signals.WorkerSignals import WorkerSignals

class ScalerThread(QRunnable):
    """Image scaler thread"""

    def __init__(self, images=[], width=None, height=None, outdir='', createpdf=True, scaled_image_suffix='-scaled', pdf_name='AllImages'):
        """Initializes the thread

        :param images: The images
        :param width: The width
        :param height: The height
        :param createpdf: Flag whether to create a PDF file of all images
        :param scaled_image_suffix: Scaled image suffix
        :param pdf_name: The PDF name
        """
        super().__init__()

        logging.debug('Initializing ScalerThread')

        self.images = images
        self.width = width
        self.height = height
        self.outdir = outdir
        self.createpdf = createpdf
        self.scaled_image_suffix = scaled_image_suffix

        self.pdf_name = pdf_name

        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """Runs the thread"""
        processed_img_cnt = 0
        try:
            list_img = []
            for img in self.images:
                logging.debug('Processing image "%s", %dx%d px (width x height)', img, self.width, self.height)
                scaled_img_name = self._get_scaled_img_path(img)
                if scaled_img_name:
                    logging.debug('Scaled path of image "%s": "%s"', img, scaled_img_name)
                    logging.debug('Writing to "%s"', scaled_img_name)
                    try:
                        self._scale_image(input_image_path=img,
                                          output_image_path=scaled_img_name,
                                          width=self.width,
                                          height=self.height)
                    except Exception as ex:
                        logging.warning('Exception while scaling: %s', ex)

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
                    except Exception as ex:
                        logging.warning('Exception while converting rgba to rgb: %s', ex)

                    self.signals.scalingresult.emit(processed_img_cnt, len(self.images))
        except Exception as ex:
            logging.exception('Failed to process images.')
            self.signals.scalingerror.emit(ex)
        finally:
            pdf_written = False
            if self.createpdf and list_img:
                pdf_written = True
                pdf_name = f'{self.outdir}/{self.pdf_name}.pdf'
                if os.path.exists(pdf_name):
                    try:
                        logging.debug('File "%s" exists, deleting', pdf_name)
                        os.remove(pdf_name)
                    except Exception as ex:
                        logging.debug('Exception while deleting existing PDF file: %s', ex)
                        pdf_written = False
                if pdf_written:
                    logging.debug('Generating PDF file "%s"', pdf_name)
                    list_img[0].save(pdf_name, 'PDF', resolution=100.0, save_all=True, append_images=list_img[1:])
            self.signals.scalingfinished.emit(processed_img_cnt, len(self.images), pdf_written)

    def _get_scaled_img_path(self, path_img):
        """returns the image name of the scaled image

        :param path_img: The image path
        """
        try:
            with open(path_img, encoding='utf-8') as f:
                fname = os.path.basename(f.name)
                lindex = fname.rfind('.')
                newname = fname[:lindex] + self.scaled_image_suffix
                suffix = fname[lindex:]
                out_path = f'{self.outdir}/{newname}{suffix}'
                logging.debug('Output image path: "%s"', out_path)

                return out_path
        except Exception as ex:
            logging.error('Error getting path for image "%s": %s', path_img, ex)
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
        orig_width, orig_height = original_image.size
        logging.debug('The original image size is %d wide x %d high', orig_width, orig_height)

        if width and height:
            max_size = (width, height)
        elif width:
            max_size = (width, orig_height)
        elif height:
            max_size = (orig_width, height)
        else:
            # No width or height specified
            raise RuntimeError('Width or height required!')

        original_image.thumbnail(max_size, Image.LANCZOS)
        original_image.save(output_image_path)

        scaled_image = Image.open(output_image_path)
        width, height = scaled_image.size
        logging.debug('The scaled image size is %d wide x %d high', width, height)
