import os
from barcode import Code128
from barcode.writer import ImageWriter

# Define your 12 items: 
# key = label (as string), value = item name
items = {
    "1000000001": "Apple",
    "1000000002": "Water",
    "1000000003": "Butter",
    "1000000004": "Milk",
    "1000000005": "Eggs",
    "1000000006": "Oil",
    "1000000007": "Salmon",
    "1000000008": "Honey",
    "1000000009": "IceCream",
    "1000000010": "Beer",
    "1000000011": "Wine",
    "1000000012": "Bread",
}

# Create an output directory for PNGs
output_dir = "barcodes_PNG"
os.makedirs(output_dir, exist_ok=True)

# Loop and generate each barcode PNG
for number, name in items.items():
    # Code128 barcode object with embedded checksum
    barcode = Code128(number, writer=ImageWriter())
    
    # standardised filename
    save_name = name.replace(" ", "_")
    filename = os.path.join(output_dir, f"{number}_{save_name}")
    
    # save() writes out <filename>.png by default
    barcode.save(filename, options={
        "write_text": not True,      # draw the numeric code below bars
        "text_distance": 1,      # gap between bars and text
        "font_size": 14,
        "module_width": 0.2,     # bar thickness
        "module_height": 5      # bar height
    })
    print(f"→ Generated {filename}.png")
