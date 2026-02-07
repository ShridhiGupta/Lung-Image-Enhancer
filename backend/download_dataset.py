import kagglehub
import os
import shutil
from pathlib import Path

def download_and_organize_dataset():
    print("📥 Downloading Lungs Disease Dataset from Kaggle...")
    
    try:
        # Download latest version
        path = kagglehub.dataset_download("omkarmanohardalvi/lungs-disease-dataset-4-types")
        print(f"✅ Dataset downloaded to: {path}")
        
        # Create dataset directory in hackathon folder
        hackathon_root = Path(__file__).parent.parent
        dataset_dir = hackathon_root / "dataset" / "lungs_disease"
        dataset_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Organizing dataset in: {dataset_dir}")
        
        # Copy dataset files to our organized structure
        source_path = Path(path)
        
        # Create subdirectories for different types
        categories = ["Normal", "Benign", "Malignant", "Non-Cancerous"]
        for category in categories:
            target_dir = dataset_dir / category.lower()
            target_dir.mkdir(exist_ok=True)
        
        # Find and organize image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        organized_count = 0
        
        # Walk through the downloaded dataset
        for root, dirs, files in os.walk(source_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    source_file = Path(root) / file
                    
                    # Try to determine category from folder name or filename
                    folder_name = Path(root).name.lower()
                    
                    # Determine target category based on folder structure
                    if 'normal' in folder_name or 'normal' in file.lower():
                        target_dir = dataset_dir / "normal"
                    elif 'benign' in folder_name or 'benign' in file.lower():
                        target_dir = dataset_dir / "benign"
                    elif 'malignant' in folder_name or 'malignant' in file.lower():
                        target_dir = dataset_dir / "malignant"
                    elif 'non-cancerous' in folder_name or 'noncancerous' in folder_name or 'non_cancerous' in folder_name:
                        target_dir = dataset_dir / "non-cancerous"
                    else:
                        # Default to normal if unclear
                        target_dir = dataset_dir / "normal"
                    
                    # Copy file to organized location
                    target_file = target_dir / f"{organized_count:06d}_{file}"
                    shutil.copy2(source_file, target_file)
                    organized_count += 1
                    
                    if organized_count % 100 == 0:
                        print(f"  📊 Organized {organized_count} images...")
        
        print(f"✅ Dataset organization complete!")
        print(f"📈 Total images organized: {organized_count}")
        
        # Print dataset statistics
        print("\n📊 Dataset Statistics:")
        for category in categories:
            category_dir = dataset_dir / category.lower()
            count = len(list(category_dir.glob("*")))
            print(f"  {category}: {count} images")
        
        # Create a dataset info file
        info_file = dataset_dir / "dataset_info.txt"
        with open(info_file, 'w') as f:
            f.write("Lungs Disease Dataset - 4 Types\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Source: Kaggle - omkarmanohardalvi/lungs-disease-dataset-4-types\n")
            f.write(f"Downloaded from: {path}\n")
            f.write(f"Organized in: {dataset_dir}\n")
            f.write(f"Total images: {organized_count}\n\n")
            f.write("Categories:\n")
            for category in categories:
                category_dir = dataset_dir / category.lower()
                count = len(list(category_dir.glob("*")))
                f.write(f"  {category}: {count} images\n")
        
        print(f"📝 Dataset info saved to: {info_file}")
        
        return str(dataset_dir)
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {str(e)}")
        return None

if __name__ == "__main__":
    dataset_path = download_and_organize_dataset()
    if dataset_path:
        print(f"\n🎉 Dataset ready for training at: {dataset_path}")
    else:
        print("\n❌ Failed to download dataset")
