#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of pyunicorn.
# Copyright (C) 2008--2019 Jonathan F. Donges and pyunicorn authors
# URL: <http://www.pik-potsdam.de/members/donges/software>
# License: BSD (3-clause)

"""
Function for Event Coincidence Analysis.
"""

import numpy as np


def ECA(EventSeriesX, EventSeriesY, delT, tau=0, ts1=None, ts2=None):
        """
        Event coincidence analysis:
        Returns the precursor and trigger coincidence rates of two event series
        X and Y.

        :type EventSeriesX: 1D Numpy array
        :arg EventSeriesX: Event series containing '0's and '1's
        :type EventSeriesY: 1D Numpy array
        :arg EventSeriesY: Event series containing '0's and '1's
        :arg delT: coincidence interval width
        :arg int tau: lag parameter
        :rtype: list
        :return: [Precursor coincidence rate XY, Trigger coincidence rate XY,
                  Precursor coincidence rate YX, Trigger coincidence rate YX]
        """

        # Count events that cannot be coincided due to tau and delT
        if not (tau == 0 and delT == 0):
            # Start of EventSeriesX
            n11 = np.count_nonzero(EventSeriesX[:tau+delT])
            # End of EventSeriesX
            n12 = np.count_nonzero(EventSeriesX[-(tau+delT):])
            # Start of EventSeriesY
            n21 = np.count_nonzero(EventSeriesY[:tau+delT])
            # End of EventSeriesY
            n22 = np.count_nonzero(EventSeriesY[-(tau+delT):])
        else:
            # Instantaneous coincidence
            n11, n12, n21, n22 = 0, 0, 0, 0
        # Get time indices
        if ts1 is None:
            e1 = np.where(EventSeriesX)[0]
        else:
            e1 = ts1[EventSeriesX]
        if ts2 is None:
            e2 = np.where(EventSeriesY)[0]
        else:
            e2 = ts2[EventSeriesY]
        del EventSeriesX, EventSeriesY, ts1, ts2
        # Number of events
        l1 = len(e1)
        l2 = len(e2)
        # Array of all interevent distances
        dst = (np.array([e1]*l2).T - np.array([e2]*l1))
        # Count coincidences with array slicing
        prec12 = np.count_nonzero(np.any(((dst - tau >= 0)
                                          * (dst - tau <= delT))[n11:, :],
                                         axis=1))
        trig12 = np.count_nonzero(np.any(((dst - tau >= 0)
                                          * (dst - tau <= delT))
                                         [:, :dst.shape[1]-n22],
                                         axis=0))
        prec21 = np.count_nonzero(np.any(((-dst - tau >= 0)
                                          * (-dst - tau <= delT))[:, n21:],
                                         axis=0))
        trig21 = np.count_nonzero(np.any(((-dst - tau >= 0)
                                          * (-dst - tau <= delT))
                                         [:dst.shape[0]-n12, :],
                                         axis=1))
        # Normalisation and output
        return (np.float32(prec12)/(l1-n11), np.float32(trig12)/(l2-n22),
                np.float32(prec21)/(l2-n21), np.float32(trig21)/(l1-n12))
