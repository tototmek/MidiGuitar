class _logcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def _log(control_char, message):
    print(control_char + message + _logcolors.ENDC)

def log_ok(message):
    _log(_logcolors.OKGREEN, message)

def log_info(message):
    print(message)

def log_debug(message):
    _log(_logcolors.OKCYAN, message)

def log_warn(message):
    _log(_logcolors.WARNING, message)

def log_error(message):
    _log(_logcolors.FAIL, message)


if __name__=="__main__":
    log_ok("Log OK")
    log_info("Log info")
    log_debug("Log debug")
    log_warn("Log warn")
    log_error("Log error")
    