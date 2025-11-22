#!/bin/bash
set -e

echo "[NomaanOS Backup] Starting..."
tar -czf nomaanos_backup_$(date +%Y%m%d_%H%M).tar.gz src || echo "Source not found"
echo "[NomaanOS Backup] Done"
