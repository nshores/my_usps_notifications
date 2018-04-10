#!/bin/bash
webhook_url=""
usps_username=""
usps_password=""



docker run -d \
    --name myusps_notifications \
    -e webhook_url="${webhook_url}" \
    -e usps_username="${usps_username}" \
    -e usps_password="${usps_password}" \
    nshores/my_usps_notifications