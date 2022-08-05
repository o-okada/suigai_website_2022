#!/bin/bash

### ./action_A01_upload_ippan.sh &
### ./action_A02_verify_ippan.sh &

./action_A03_verify_idb_by_diff_method.sh &
sleep 10s

./action_A04_prorate_idb.sh &
sleep 10s

./action_A05_verify_idb_by_reverse_method.sh &
sleep 10s

./action_A06_summarize_sdb.sh &
sleep 10s

./action_A07_verify_sdb_by_reverse_method.sh &
sleep 10s

./action_A99_wait_manual_verification.sh &
sleep 10s

### ./action_B01_upload_area.sh &

./action_N01_download_ippan_chosa.sh &
sleep 10s

./action_O01_download_ippan_city.sh &
sleep 10s

./action_P01_download_ippan_ken.sh &
sleep 10s
