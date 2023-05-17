# autoSaver

[![QGIS.org](https://img.shields.io/badge/QGIS.org-published-green)](https://plugins.qgis.org/plugins/autoSaver/)

## Features

The plugin allows the automatic saving of the project and layers in edit mode at a user-defined interval.

## PyQGIS

For PyQGIS plugin developers, the plugin will change the
[QgsProject filename](https://api.qgis.org/api/classQgsProject.html#a49c729d8fac976c0a91df3573002bfa0) in the
background **temporary**.
So QGIS will trigger the signal `fileNameChanged`.

If your plugin or script is listening to this signal, it's somehow a false positive because the user
didn't change the filename on purpose and the plugin will set back the normal filename after the backup is made.

For this reason, when the `fileNameChanged` is emitted, you can check if the environment variable
`QGIS_PLUGIN_AUTO_SAVING` is present.
If yes, it means it has been the plugin doing the backup file.
