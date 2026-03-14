import pandas as pd
import yaml
import os
import glob

# Configuration
CSV_FILE = 'inventory.csv'
OUTPUT_DIR = '_items'
# Path where your folders are: assets/images/inventory/av0001/, etc.
IMAGE_BASE_DIR = 'assets/images/'

df = pd.read_csv(CSV_FILE)
os.makedirs(OUTPUT_DIR, exist_ok=True)

for _, row in df.iterrows():
    uid = str(row['unique_id']).strip()
    item_folder = os.path.join(IMAGE_BASE_DIR, uid)
    
    # Look for any common image formats in that specific folder
    found_images = []
    if os.path.isdir(item_folder):
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.PNG']
        for ext in extensions:
            # Get paths relative to the site root for Jekyll
            for img_path in glob.glob(os.path.join(item_folder, ext)):
                found_images.append(f"/{img_path}")

    metadata = {
        'layout': 'item',
        'unique_id': uid,
        'title': str(row['title']).strip(),
        'format': row['format'],
        'quantity': int(row['quantity']) if pd.notnull(row['quantity']) else 1,
        'date_on_label': str(row['date_on_label']),
        'condition': str(row['condition']) if pd.notnull(row['condition']) else 'Not Assessed',
        'ephemera_count': int(row['ephemera_count']) if pd.notnull(row['ephemera_count']) else 0,
        # The first image is the "main" one, the rest are for the gallery
        'images': found_images 
    }
    
    with open(os.path.join(OUTPUT_DIR, f"{uid}.md"), 'w') as f:
        f.write('---\n' + yaml.dump(metadata, sort_keys=False) + '---\n\n')
        f.write(f"### Internal Notes\n{row['internal_note'] if pd.notnull(row['internal_note']) else 'N/A'}")

print(f"Processed {len(df)} items. Folders scanned in {IMAGE_BASE_DIR}.")