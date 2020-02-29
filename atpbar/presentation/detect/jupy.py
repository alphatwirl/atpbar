
##__________________________________________________________________||
def is_jupyter_notebook():
    try:
        from IPython import get_ipython
        if 'IPKernelApp' in get_ipython().config:
            return True
    except:
        pass
    return False

##__________________________________________________________________||
