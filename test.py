import uiautomator2 as u2

d = u2.connect("192.168.31.232:40375")
print(d.info)
d.app_start("com.xmcy.hykb")