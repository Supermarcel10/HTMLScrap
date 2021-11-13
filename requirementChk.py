def __main__():
    recognised_ver = {
        "selenium": ["3.141.0"],
        "cryptography": ["2.8", "35.0.0"],
        "pandas": ["1.3.1", "1.3.4"]
    }

    # SELENIUM

    try:
        from selenium import __version__ as selenium_ver
    except ModuleNotFoundError as err:
        raise ModuleNotFoundError(err)

    try:
        if selenium_ver in recognised_ver["selenium"]:
            print("Compatible selenium version detected.")
        else:
            print("Running an untested selenium version, which may not work!")
    except:
        raise ModuleNotFoundError()

    # CRYPTOGRAPHY

    try:
        from cryptography import __version__ as cryptography_ver
    except ModuleNotFoundError as err:
        raise ModuleNotFoundError(err)

    try:
        if cryptography_ver in recognised_ver["cryptography"]:
            print("Compatible cryptography version detected.")
        else:
            print("Running an untested cryptography version, which may not work!")
    except:
        raise ModuleNotFoundError()

    # STY

    try:
        import sty
    except ModuleNotFoundError as err:
        raise ModuleNotFoundError(err)

    # PANDAS

    try:
        from pandas import __version__ as pandas_ver
    except ModuleNotFoundError as err:
        raise ModuleNotFoundError(err)

    try:
        if pandas_ver in recognised_ver["pandas"]:
            print("Compatible pandas version detected.")
        else:
            print("Running an untested pandas version, which may not work!")
    except:
        raise ModuleNotFoundError()


if __name__ == "__main__":
    __main__()
