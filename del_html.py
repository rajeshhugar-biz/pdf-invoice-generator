import os

for root, dirs, files in os.walk("output"):
    for file in files:
        if file.endswith(".html"):
            os.remove(os.path.join(root, file))
            print("Deleted:", os.path.join(root, file))