# 🏥 MediAssist - Kaggle Notebook Setup Guide

## Quick Start for Kaggle

This guide will help you run MediAssist in a Kaggle notebook with input files.

---

## **Step 1: Upload the Project to Kaggle**

### Option A: Upload as Dataset
1. Go to [Kaggle Datasets](https://www.kaggle.com/datasets)
2. Click **"Create New Dataset"**
3. Upload the entire `mediassist` folder (all files from GitHub)
4. Publish as a dataset

### Option B: Upload to GitHub First (Recommended)
1. Push this project to GitHub
2. In Kaggle notebook, clone the GitHub repo:
```python
!git clone https://github.com/YOUR-USERNAME/Medicare-Assistant.git
%cd Medicare-Assistant/mediassist
```

---

## **Step 2: Set Up Google Gemini API Key in Kaggle**

### Get Your API Key
1. Visit https://ai.google.dev/
2. Click **"Get API Key"**
3. Create a new API key in Google Cloud Console

### Add to Kaggle Secrets
1. In your Kaggle notebook, click **Settings** (⚙️ icon) in the sidebar
2. Go to **Secrets**
3. Add a new secret:
   - **Name**: `GOOGLE_API_KEY`
   - **Value**: Your actual API key from Google Gemini
4. Click **Save**

---

## **Step 3: Install Dependencies**

Run this cell in your Kaggle notebook:

```python
import os
import subprocess
import sys

# Install dependencies
subprocess.check_call([
    sys.executable, "-m", "pip", "install", "-q",
    "streamlit>=1.28.0",
    "pandas>=2.0.0",
    "plotly>=5.13.0",
    "numpy>=1.24.0",
    "python-dateutil>=2.8.2",
    "google-generativeai>=0.3.0",
    "Pillow>=10.0.0",
    "toml>=0.10.2"
])

print("✅ All dependencies installed successfully!")
```

---

## **Step 4: Load API Key from Kaggle Secrets**

```python
import os
from kaggle_secrets import UserSecretsClient

# Load API key from Kaggle secrets
user_secrets = UserSecretsClient()
api_key = user_secrets.get_secret("GOOGLE_API_KEY")

# Set as environment variable
os.environ['GOOGLE_API_KEY'] = api_key

print("✅ API key loaded from Kaggle secrets")
```

---

## **Step 5: Load Input Data**

### Option A: Use Sample Data (Provided)
```python
import pandas as pd
from PIL import Image

# Load CSV file
df = pd.read_csv('Input file/discharge_summaries.csv')
print("✅ CSV loaded successfully!")
print(df.head())

# Load image files
img1 = Image.open('Input file/John Discharge summary.png')
img2 = Image.open('Input file/Elizabeth Discharge summary.png')
print("✅ Images loaded successfully!")
```

### Option B: Upload Your Own Files
1. In Kaggle notebook, click the **Upload** button
2. Select your CSV and image files
3. Wait for upload to complete
4. Read files:
```python
import pandas as pd
from PIL import Image

# Read your uploaded files
df = pd.read_csv('your_file.csv')
img = Image.open('your_image.png')
```

---

## **Step 6: Run MediAssist Core Functions**

### Test Data Extraction
```python
import sys
sys.path.insert(0, '.')

from utils_ocr_email import extract_discharge_summary_from_image
from agent_analyzer import AnalyzerAgent
from patient_knowledge_graph import PatientKnowledgeGraph

# Test with an image
image_path = 'Input file/John Discharge summary.png'
with open(image_path, 'rb') as f:
    success, data = extract_discharge_summary_from_image(f, api_key)
    
if success:
    print("✅ OCR Extraction successful!")
    print(f"Patient: {data.get('patient_name', 'Unknown')}")
    print(f"Medications extracted: {len(data.get('medications', []))}")
else:
    print("❌ Extraction failed:", data.get('error'))
```

### Test Agent Pipeline
```python
from patient_knowledge_graph import PatientKnowledgeGraph, DischargeSummary, MedicationRecord
from agent_analyzer import AnalyzerAgent
from agent_pharmacist import PharmacistAgent

# Create knowledge graph
kg = PatientKnowledgeGraph()

# Initialize agents
analyzer = AnalyzerAgent(kg)
pharmacist = PharmacistAgent(kg)

# Sample patient data
patient_data = {
    'patient_id': 'P001',
    'name': 'John Doe',
    'admission_date': '2025-11-15',
    'discharge_date': '2025-11-20',
    'primary_diagnosis': 'Acute Myocardial Infarction',
    'medications': 'Aspirin 325mg daily, Metoprolol 50mg daily, Lisinopril 10mg daily',
    'follow_up': 'Cardiology in 1 week'
}

# Run analyzer
analysis = analyzer.analyze_discharge_summary(patient_data)
print("✅ Analyzer completed!")
print(f"Medications found: {len(kg.get_current_medications())}")

# Run pharmacist
pharm_analysis = pharmacist.check_medication_interactions()
print("✅ Pharmacist completed!")
print(f"Interactions detected: {len(kg.drug_interactions)}")
```

---

## **Step 7: Process Your Data**

### Process CSV Data
```python
import pandas as pd
from agent_analyzer import AnalyzerAgent
from patient_knowledge_graph import PatientKnowledgeGraph

# Load CSV
df = pd.read_csv('Input file/discharge_summaries.csv')

# Process each patient
for idx, row in df.iterrows():
    kg = PatientKnowledgeGraph()
    analyzer = AnalyzerAgent(kg)
    
    # Convert row to dictionary
    patient_data = row.to_dict()
    
    # Run analyzer
    analysis = analyzer.analyze_discharge_summary(patient_data)
    
    print(f"✅ Processed: {patient_data.get('name', f'Patient {idx}')}")
    print(f"   Medications: {len(kg.get_current_medications())}")
    print(f"   Interactions: {len(kg.drug_interactions)}")
    print()
```

### Process Image Data
```python
from utils_ocr_email import extract_discharge_summary_from_image
from agent_analyzer import AnalyzerAgent
from patient_knowledge_graph import PatientKnowledgeGraph
import os

# Set API key
api_key = os.environ.get('GOOGLE_API_KEY')

# List of image files
image_files = [
    'Input file/John Discharge summary.png',
    'Input file/Elizabeth Discharge summary.png'
]

for image_path in image_files:
    with open(image_path, 'rb') as f:
        # Extract from image
        success, extracted_data = extract_discharge_summary_from_image(f, api_key)
        
        if success:
            kg = PatientKnowledgeGraph()
            analyzer = AnalyzerAgent(kg)
            
            # Normalize and analyze
            analysis = analyzer.analyze_discharge_summary(extracted_data)
            
            print(f"✅ {image_path}")
            print(f"   Patient: {extracted_data.get('patient_name')}")
            print(f"   Medications: {len(kg.get_current_medications())}")
            print()
        else:
            print(f"❌ Failed to extract from {image_path}")
            print(f"   Error: {extracted_data.get('error')}")
```

---

## **Step 8: Export Results**

### Export to CSV
```python
import pandas as pd

# Create results dataframe
results = []
for med in kg.get_current_medications():
    results.append({
        'Medication': med.name,
        'Dosage': med.dosage,
        'Frequency': med.frequency,
        'Route': med.route,
        'Indication': med.indication
    })

results_df = pd.DataFrame(results)

# Save to CSV
results_df.to_csv('output_medications.csv', index=False)
print("✅ Results exported to output_medications.csv")
```

### Export to JSON
```python
import json

# Get knowledge graph data
kg_data = kg.to_json()

# Save to JSON
with open('output_patient_data.json', 'w') as f:
    f.write(kg_data)

print("✅ Results exported to output_patient_data.json")
```

---

## **Troubleshooting**

### "API Key not valid" Error
- **Solution**: Verify API key is correctly set in Kaggle Secrets
- Check: https://ai.google.dev/pricing to ensure API is enabled
- Try: `!curl -H "Authorization: Bearer $GOOGLE_API_KEY" https://generativelanguage.googleapis.com/v1beta/models`

### "Module not found" Error
- **Solution**: Reinstall dependencies
- Run: `!pip install --upgrade google-generativeai`

### "Image extraction failed" Error
- **Causes**: 
  - Image is too blurry or low quality
  - Image doesn't contain medical text
  - Image format not supported (use PNG/JPG)
- **Solution**: Try with a different image or use CSV data instead

### "Secrets not accessible" Error
- **Solution**: 
  1. Go to Notebook Settings
  2. Enable "Internet" (for API calls)
  3. Make sure Kaggle Secrets are saved
  4. Restart kernel

---

## **Complete End-to-End Example**

```python
# ============================================================================
# COMPLETE KAGGLE NOTEBOOK TEMPLATE
# ============================================================================

import os
import sys
import subprocess
import pandas as pd
from PIL import Image
import google.generativeai as genai

# Step 1: Install dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", 
    "streamlit", "pandas", "plotly", "google-generativeai", "Pillow", "toml"])

# Step 2: Load secrets
from kaggle_secrets import UserSecretsClient
api_key = UserSecretsClient().get_secret("GOOGLE_API_KEY")
os.environ['GOOGLE_API_KEY'] = api_key

# Step 3: Import MediAssist modules
sys.path.insert(0, '.')
from utils_ocr_email import extract_discharge_summary_from_image
from agent_analyzer import AnalyzerAgent
from agent_pharmacist import PharmacistAgent
from patient_knowledge_graph import PatientKnowledgeGraph

# Step 4: Process CSV data
print("=" * 70)
print("🏥 MediAssist - Processing Patient Data")
print("=" * 70)

df = pd.read_csv('Input file/discharge_summaries.csv')

for idx, row in df.iterrows():
    kg = PatientKnowledgeGraph()
    analyzer = AnalyzerAgent(kg)
    pharmacist = PharmacistAgent(kg)
    
    patient_data = row.to_dict()
    analysis = analyzer.analyze_discharge_summary(patient_data)
    pharm_analysis = pharmacist.check_medication_interactions()
    
    print(f"\n✅ Patient {idx + 1}: {patient_data.get('name')}")
    print(f"   Diagnosis: {patient_data.get('primary_diagnosis')}")
    print(f"   Medications: {len(kg.get_current_medications())}")
    print(f"   Interactions: {len(kg.drug_interactions)}")

print("\n" + "=" * 70)
print("✅ Processing complete!")
```

---

## **Project Files Reference**

| File | Purpose |
|------|---------|
| `medisync_app.py` | Main Streamlit application |
| `patient_knowledge_graph.py` | Shared state management |
| `agent_analyzer.py` | Document parsing agent |
| `agent_pharmacist.py` | Medication analysis agent |
| `agent_care_coordinator.py` | Patient guidance agent |
| `utils_ocr_email.py` | OCR extraction using Gemini Vision |
| `a2a_protocol.py` | Agent-to-agent communication |
| `mcp_server.py` | MCP server for tool management |
| `config_api_keys.py` | Secure API key management |
| `requirements.txt` | Python dependencies |
| `Input file/` | Sample CSV and image files |
| `Docs/` | Security and setup documentation |

---

## **Support & Documentation**

- 📖 Full README: `README.md`
- 🏗️ Architecture: `ARCHITECTURE.md`
- 🔐 Security: `Docs/SECURITY_FINAL_SUMMARY.md`
- ⚙️ Setup: `SETUP_GUIDE.md`

---

## **License**

This project is open source and available for educational and research purposes.

**Created**: November 2025  
**Author**: Dhana Govind  
**Repository**: https://github.com/dhana-govind/Medicare-Assistant
