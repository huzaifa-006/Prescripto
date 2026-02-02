
import os

file_path = "templates/clinic/prescription_print.html"

with open(file_path, 'r') as f:
    content = f.read()

# Replace logo.jpg with logo.png
new_content = content.replace('logo.jpg', 'logo.png')

if content != new_content:
    with open(file_path, 'w') as f:
        f.write(new_content)
        f.flush()
        os.fsync(f.fileno())
    print("Updated logo to logo.png")
else:
    print("Logo already updated or not found.")
