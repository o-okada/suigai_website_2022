#!/bin/bash

./action_A01_download_ippan_chosa.sh &
sleep 10s

### ./action_A02_upload_ippan.sh &
### ./action_A03_verify_ippan.sh &

./action_A04_verify_idb_by_diff_method.sh &
sleep 10s

./action_A05_prorate_idb.sh &
sleep 10s

./action_A06_verify_idb_by_reverse_method.sh &
sleep 10s

./action_A07_summarize_sdb.sh &
sleep 10s

./action_A08_verify_sdb_by_reverse_method.sh &
sleep 10s

./action_A99_wait_manual_verification.sh &
sleep 10s

### ./action_B01_upload_area.sh &

./action_C01_download_ippan_city.sh &
sleep 10s

./action_D01_download_ippan_ken.sh &
sleep 10s
