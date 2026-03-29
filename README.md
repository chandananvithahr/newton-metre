# Costimize MVP - AI Manufacturing Cost Estimator

Costimize is an AI-powered manufacturing cost estimation tool that analyzes CNC engineering drawings and provides instant cost estimates for turning operations. Built with Streamlit and Google Gemini Vision API.

## Features

- 🤖 **AI-Powered Drawing Analysis**: Upload CNC engineering drawings (PNG, JPG) and automatically extract:
  - Part type (turning/milling)
  - Dimensions (OD, ID, length, width, height)
  - Material specifications
  - Features (threads, holes, grooves, etc.)
  - Surface finish requirements
  - Tolerance specifications

- 💰 **Intelligent Cost Estimation**: 
  - Material cost calculation with wastage
  - Machining time estimation
  - Setup cost amortization
  - Overhead and profit margins
  - Detailed cost breakdown

- 📊 **Professional UI**: 
  - Clean, modern interface
  - Real-time analysis results
  - Expandable cost breakdowns
  - Manual dimension input fallback

## Project Structure

```
costimize-mvp/
├── app.py                 # Main Streamlit application
├── vision.py              # Gemini vision for drawing analysis
├── cost_engine.py         # Cost calculation logic
├── material_price_fetcher.py  # Web price fetching
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your API keys (not in git)
├── sample_data/
│   └── materials.json     # Material costs database
└── README.md              # This file
```

## Setup Instructions

### 1. Install Dependencies

Make sure you have Python 3.8+ installed, then install the required packages:

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web app framework
- `google-generativeai` - Google Gemini API client
- `python-dotenv` - Environment variable management
- `Pillow` - Image processing
- `requests` - HTTP requests for web price fetching
- `beautifulsoup4` - Web scraping

### 2. Configure API Key

The `.env` file already contains your API key. If you need to update it:

1. Edit `.env` and update your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

   **How to get a Gemini API key:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the key and paste it in your `.env` file

### 3. Verify Materials Database

The `sample_data/materials.json` file contains material prices and densities. You can edit this file to add or update materials with current market prices.

## How to Run

1. Navigate to the project directory:
   ```bash
   cd costimize-mvp
   ```

2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. The app will open in your default web browser at `http://localhost:8501`

## Usage

1. **Upload a Drawing**: Click "Choose a file" and select a PNG or JPG image of your CNC engineering drawing

2. **Set Parameters** (in sidebar):
   - **Quantity**: Number of pieces to manufacture (1-10,000)
   - **Material**: Select from dropdown or choose "Auto-detect from drawing"
   - **Machine Rate**: Optional override for custom shop rates
   - **Use live web prices**: Toggle to fetch current market prices
   - **Region**: Currently optimized for India (USA/Europe coming soon)

3. **Review Analysis**: The AI will extract:
   - Part type and dimensions
   - Material (if specified on drawing)
   - Features and tolerances
   - Confidence level

4. **Get Cost Estimate**: 
   - View cost per piece and total cost
   - Expand breakdown for detailed analysis
   - Use manual dimension input if AI extraction fails

5. **Manual Input Fallback**: If dimensions aren't extracted automatically, use the collapsible "Manual Dimension Input" section

## Cost Calculation Details

The cost estimator uses real Indian job shop economics:

- **Material Cost**: 
  - Bar stock calculation with 3mm diameter and 5mm length allowance
  - 15% material wastage for cutoff and chips
  - Prices from `materials.json` or live web prices (cached for 24 hours)

- **Machining Time**:
  - Base time formula: `(OD × length) / 5000`
  - Facing, roughing, finishing passes
  - Feature time (threads, grooves, etc.)
  - Parting off time

- **Machining Cost**:
  - Default: ₹800/hr for standard CNC lathe
  - 30% surcharge for tight tolerances (< ±0.05mm)
  - 30-minute setup time amortized over quantity

- **Overhead & Profit**:
  - 15% overhead
  - 20% profit margin

## Error Handling

The app includes robust error handling:

- **API Key Errors**: Clear message if Gemini API key is missing or invalid
- **API Failures**: Friendly error message with manual input fallback
- **Missing Dimensions**: Automatic prompt for manual dimension input
- **Invalid Materials**: Error message with list of available materials

## Notes

- ⚠️ **Accuracy**: This is an AI-assisted estimate. Actual costs may vary ±15-20% based on:
  - Shop-specific rates
  - Material availability
  - Specific manufacturing requirements
  - Market fluctuations

- 📄 **PDF Support**: PDF upload is detected but not yet fully implemented. Convert to PNG/JPG for best results.

- 🔄 **Session State**: The app remembers your last analysis, so you can adjust parameters without re-uploading.

## Future Enhancements

- [ ] Full PDF processing support
- [ ] Milling cost estimation
- [ ] Multi-region pricing (USA, Europe)
- [ ] PDF quote generation
- [ ] Material database management UI
- [ ] Cost history and comparison
- [ ] Export to Excel/CSV

## Troubleshooting

**"API key not found" error:**
- Check that `.env` file exists and contains `GOOGLE_API_KEY=your_key`
- Make sure you're in the correct directory when running the app

**"Failed to load materials" error:**
- Verify `sample_data/materials.json` exists and is valid JSON
- Check file permissions

**Image upload fails:**
- Ensure file is PNG, JPG, or JPEG format
- Check file size (Streamlit has upload limits)

**Cost calculation errors:**
- Verify dimensions are provided (either from AI or manual input)
- Check that selected material exists in `materials.json`
- Ensure quantity is greater than 0

## License

This is an MVP project for demonstration purposes.

## Support

For issues or questions, please check:
- Streamlit documentation: https://docs.streamlit.io
- Google Gemini API docs: https://ai.google.dev/docs

---

**Built with ❤️ for the manufacturing industry**
