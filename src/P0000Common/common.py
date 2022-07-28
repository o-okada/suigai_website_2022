import logging
import sys
from datetime import date, datetime, timedelta, timezone

logger = logging.getLogger('suigai_website')
info_log = []
warn_log = []
error_log = []
debug_log = []

###############################################################################
### 関数名：
### 関数概要：ログを出力する。
###############################################################################
def print_log(log_message, log_type):
    JST = timezone(timedelta(hours=9), 'JST')
    datetime_now_YmdHMS = datetime.now(JST).strftime('%Y/%m/%d %H:%M:%S')

    print('[' + datetime_now_YmdHMS + '] ' + log_message)
    
    if log_type == 'INFO':
        logger.info('[' + datetime_now_YmdHMS + '] ' + log_message)
    elif log_type == 'WARN':
        logger.warn('[' + datetime_now_YmdHMS + '] ' + log_message)
    elif log_type == 'ERROR':
        logger.error('[' + datetime_now_YmdHMS + '] ' + log_message)
    elif log_type == 'DEBUG':
        pass
    else:
        pass
        
    ### if log_type == 'INFO':
    ###     info_log.append('[' + datetime_now_YmdHMS + '] ' + log_message)
    ### elif log_type == 'WARN':
    ###     warn_log.append('[' + datetime_now_YmdHMS + '] ' + log_message)
    ### elif log_type == 'ERROR':
    ###     error_log.append('[' + datetime_now_YmdHMS + '] ' + log_message)
    ### elif log_type == 'DEBUG':
    ###     debug_log.append('[' + datetime_now_YmdHMS + '] ' + log_message)

    if log_type == 'INFO':
        info_log.append(log_message)
    elif log_type == 'WARN':
        warn_log.append(log_message)
    elif log_type == 'ERROR':
        error_log.append(log_message)
    elif log_type == 'DEBUG':
        debug_log.append(log_message)

###############################################################################
### 関数名：reset_log()
### 関数概要：ログをリセットする。
###############################################################################
def reset_log():
    global info_log
    global warn_log
    global error_log
    global debug_log
    
    info_log = []
    warn_log = []
    error_log = []
    debug_log = []

###############################################################################
### 関数名：get_info_log()
### 関数概要：ログを出力する。
###############################################################################
def get_info_log():
    return info_log

###############################################################################
### 関数名：get_warn_log()
### 関数概要：ログを出力する。
###############################################################################
def get_warn_log():
    return warn_log

###############################################################################
### 関数名：get_error_log()
### 関数概要：ログを出力する。
###############################################################################
def get_error_log():
    return error_log

###############################################################################
### 関数名：get_debug_log()
### 関数概要：ログを出力する。
###############################################################################
def get_debug_log():
    return debug_log
