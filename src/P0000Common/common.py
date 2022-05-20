import logging

logger = logging.getLogger('suigai_website')

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