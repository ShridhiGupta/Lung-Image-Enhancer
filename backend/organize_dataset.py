import os
import shutil
from pathlib import Path

def organize_lung_disease_dataset():
    print("🔄 Reorganizing Lung Disease Dataset...")
    
    # Paths
    source_root = Path("C:/Users/HP/.cache/kagglehub/datasets/omkarmanohardalvi/lungs-disease-dataset-4-types/versions/1/Lung Disease Dataset")
    hackathon_root = Path(__file__).parent.parent
    dataset_dir = hackathon_root / "dataset" / "lungs_disease"
    
    # Clear existing organization
    if dataset_dir.exists():
        shutil.rmtree(dataset_dir)
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    # Create proper directories
    categories = {
        "normal": "Normal",
        "bacterial_pneumonia": "Bacterial Pneumonia", 
        "viral_pneumonia": "Viral Pneumonia",
        "tuberculosis": "Tuberculosis",
        "corona_virus": "Corona Virus Disease"
    }
    
    for cat_key in categories.keys():
        (dataset_dir / cat_key).mkdir(exist_ok=True)
    
    # Process train, val, test splits
    splits = ["train", "val", "test"]
    total_images = 0
    
    for split in splits:
        split_path = source_root / split
        if not split_path.exists():
            continue
            
        print(f"\n📁 Processing {split} set...")
        
        for category_dir in split_path.iterdir():
            if not category_dir.is_dir():
                continue
                
            category_name = category_dir.name.lower()
            
            # Map category names
            if "normal" in category_name:
                target_cat = "normal"
            elif "bacterial" in category_name:
                target_cat = "bacterial_pneumonia"
            elif "viral" in category_name:
                target_cat = "viral_pneumonia"
            elif "tuberculosis" in category_name:
                target_cat = "tuberculosis"
            elif "corona" in category_name:
                target_cat = "corona_virus"
            else:
                continue
            
            target_dir = dataset_dir / target_cat
            image_count = 0
            
            for image_file in category_dir.glob("*"):
                if image_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
                    # Copy with split prefix to maintain organization
                    new_name = f"{split}_{image_count:06d}_{image_file.name}"
                    target_file = target_dir / new_name
                    shutil.copy2(image_file, target_file)
                    image_count += 1
                    total_images += 1
            
            print(f"  ✅ {category_name}: {image_count} images → {target_cat}")
    
    print(f"\n📊 Dataset Statistics:")
    for cat_key, cat_name in categories.items():
        cat_dir = dataset_dir / cat_key
        count = len(list(cat_dir.glob("*")))
        print(f"  {cat_name}: {count} images")
    
    print(f"\n🎉 Total images organized: {total_images}")
    
    # Create dataset info
    info_file = dataset_dir / "dataset_info.txt"
    with open(info_file, 'w') as f:
        f.write("Lung Disease Dataset - 5 Types\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Source: Kaggle - omkarmanohardalvi/lungs-disease-dataset-4-types\n")
        f.write(f"Organized in: {dataset_dir}\n")
        f.write(f"Total images: {total_images}\n\n")
        f.write("Categories:\n")
        for cat_key, cat_name in categories.items():
            cat_dir = dataset_dir / cat_key
            count = len(list(cat_dir.glob("*")))
            f.write(f"  {cat_name}: {count} images\n")
        f.write("\nSplits: train, val, test (preserved in filenames)\n")
    
    print(f"📝 Dataset info saved to: {info_file}")
    return str(dataset_dir)

if __name__ == "__main__":
    dataset_path = organize_lung_disease_dataset()
    if dataset_path:
        print(f"\n🎉 Dataset ready for training at: {dataset_path}")
    else:
        print("\n❌ Failed to organize dataset")
