#!/bin/bash

while true
do
    echo "python3 manage.py action_A99_wait_manual_verification"
    python3 manage.py action_A99_wait_manual_verification
    echo "sleep 120s"
    sleep 120s
done
