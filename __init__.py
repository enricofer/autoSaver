"""
/***************************************************************************
 autoSaver
                                 A QGIS plugin
 auto save current project
                             -------------------
        begin                : 2014-06-16
        copyright            : (C) 2014 by Enrico Ferreguti
        email                : enricofer@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load autoSaver class from file autoSaver.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .autosave import autoSaver
    return autoSaver(iface)
