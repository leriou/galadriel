import leancloud
import logging

leancloud.init("d3Ferur4FUri7vERAylGpome-gzGzoHsz", "uRGeMnmfAq6h88QavSUfpS3q")

logging.basicConfig(level=logging.DEBUG)

Visitors = leancloud.Object.extend("Visitors")

m = Visitors()

m.set("ioo","91001")
m.set("age","123456")
m.save()
