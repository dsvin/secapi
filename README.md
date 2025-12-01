# secapi

`secapi` is a Python package for retrieving SEC company filings, extracting financial metrics, and intelligently mapping financial statement items using AI embeddings powered by Sentence Transformers.

This package simplifies working with SEC XBRL data by:

- Fetching raw company facts from the SEC API  
- Transforming raw XBRL JSON into structured Pandas DataFrames  
- Automatically grouping financial metrics into  
  - **Income Statement**  
  - **Balance Sheet**  
  - **Cash Flow Statement**  
- Using semantic similarity to match metric names to canonical financial metrics  
- Providing a clean, object-oriented API through the `Ticker` class  

---

## 🔧 Features

- Retrieve SEC financial data (10-K and 10-Q)
- Convert and normalize XBRL data into clean Pandas DataFrames
- AI-powered metric matching using Sentence Transformers
- Annual and quarterly financial statement creation
- Customizable dictionaries for metric names and synonyms
- Modular and extendable architecture

---

## 📦 Installation (Local Development Mode)

Since this package is **not yet on PyPI**, you must install it directly from source:

```bash
git clone https://github.com/YOUR_USERNAME/secapi.git
cd secapi
pip install -e .
```

This installs the package in *editable mode*, allowing you to modify the source code and immediately see changes.

---

## 🚀 Usage Example

```python
from secapi import Ticker, UserSettings

# Required SEC user agent email
user = UserSettings("example@example.com")

# Create a Ticker instance
aapl = Ticker("AAPL", user)

# Income Statement (annual)
df_is = aapl.income_statement()
print(df_is)

# Balance Sheet (quarterly)
df_bs = aapl.balance_sheet(yearly=False)

# Cash Flow Statement (annual)
df_cf = aapl.cash_flow_statement()
```

---

## 📁 Project Structure

```
secapi/
    __init__.py
    ticker.py
    metric_matching.py
    metrics.py

README.md
LICENSE
requirements.txt
setup.py
```

---

## 🤖 AI Metric Matching

The `metric_matching.py` module uses a pretrained Sentence Transformer model  
**`all-MiniLM-L6-v2`** to match DataFrame column names to financial metrics.

### How it works:

1. Embed DataFrame column names  
2. Embed synonyms defined in `metrics.py`  
3. Compute cosine similarity using Sentence Transformers  
4. Match each metric to its canonical financial concept  
5. Assign results to:
   - Income Statement  
   - Balance Sheet  
   - Cash Flow Statement  

A similarity threshold of **0.80** ensures high-quality matches.

---

## 🧩 Customization

You may customize the behavior by editing:

### `metrics.py`
- Contains canonical financial metric mappings
- Defines which metrics belong to which statement

### `key_metric_synonyms`
- Lists synonyms and alternate naming conventions for metrics
- Helps the AI model recognize variations in naming

This flexibility allows adaptation to unique datasets and custom accounting terminology.

---

## 🛠 Development

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the package in editable mode:

```bash
pip install -e .
```

Restart your Jupyter kernel if you're developing in notebooks.

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [`LICENSE`](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome!

You may:

- Open issues (There are still some issues that need to fixed including null values that are because of the JSON files from the SEC EDGAR)
- Suggest new features  
- Submit pull requests  
- Help refine financial metric matching logic  

---

## 🔗 Useful Links

- **SEC API Documentation:**  
  https://www.sec.gov/edgar/sec-api-documentation

- **Sentence Transformers:**  
  https://www.sbert.net/

- **GitHub Repository:**  
  https://github.com/dsvin/secapi
