import subprocess

subprocess.call(["xdotool", "mousemove", "453", "453"])

subprocess.call(["xdotool", "key", "--clearmodifiers", "XF86MonBrightnessDown"])
