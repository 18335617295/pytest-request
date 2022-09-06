import time
from _pytest import terminal
from conf.GlobalConfig import GlobalConfig


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''收集测试结果'''
    GlobalConfig.RESULT_DICT = {
        "total": terminalreporter._numcollected,
        "passed": len(terminalreporter.stats.get('passed', [])),
        "failed": len(terminalreporter.stats.get('failed', [])),
        "error": len(terminalreporter.stats.get('error', [])),
        "skipped": len(terminalreporter.stats.get('skipped', [])),
        "time": round(time.time() - terminalreporter._sessionstarttime, 2)
    }
