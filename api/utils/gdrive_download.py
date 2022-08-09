import os
import gdown

def gdrive_download(url, filepath):
    if os.path.exists(filepath):
        print("model already exist")
    else:
        print("model downloading")
        gdown.download(url, filepath, quiet=False, proxy=False)
        print("done")
