"""
This converts images to ascii like strings
"""
import base64

with open('bin\\data\\img\\ui\\upndown.png', 'rb') as f:
    base64string = base64.b64encode(f.read()).decode('ascii')
    with open('tools\\img.txt','w') as fo:
        fo.write(base64string)
print(base64string)