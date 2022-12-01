import functools
import signal
import os


def timeout(sec):
    """
    timeout decorator
    :param sec: function raise TimeoutError after ? seconds
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):

            def _handle_timeout(signum, frame):
                err_msg = f'Function {func.__name__} timed out after {sec} seconds'
                raise TimeoutError(err_msg)

            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(sec)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapped_func
    return decorator


@timeout(10)
def update_git_ai_travel():
    os.chdir("/content/ai-travel/")
    os.system("""git fetch --all""")
    os.system("""git reset --hard origin/tencent""")
    os.system("""git pull origin tencent""")
