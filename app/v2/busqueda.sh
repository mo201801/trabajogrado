#!/bin/bash
salida=$(pdfgrep -r  -ion "$1")
echo "$salida"
