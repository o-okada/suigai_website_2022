import logging

logger = logging.getLogger('suigai_website')
info_log_list = []
warn_log_list = []
error_log_list = []

###############################################################################
### 関数名：
### 関数概要：ログを出力する。
###############################################################################
def print_log(log_message, log_type):
    print(log_message)
    if log_type == 'INFO':
        logger.info(log_message)
    elif log_type == 'WARN':
        logger.warn(log_message)
    elif log_type == 'ERROR':
        logger.error(log_message)
    else:
        logger.error(log_message)
        
    info_log_list.append(log_message)

def get_info_log():
    return info_log_list

def get_warn_log():
    return warn_log_list

def get_error_log():
    return error_log_list