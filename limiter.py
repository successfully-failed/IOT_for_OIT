import resource


def poor_mode (seconds, maxsize):
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    softm, hardm = resource.getrlimit(resource.RLIMIT_AS)
    print("lowering resources")
    resource.setrlimit(resource.RLIMIT_CPU, (seconds, hard))
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hardm))
    print("resources taken way")

def rich_mode ():
    print("lowering resources")
    resource.RLIM_INFINITY 
    print("resources taken way")
