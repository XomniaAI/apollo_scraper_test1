# Apollo Lead Scraper

A comprehensive, production-ready web scraper for extracting contact information from Apollo.io with advanced anti-detection capabilities, job change acceptance, and email revelation features.

## 🎯 Overview

This Apollo scraper automates the extraction of professional contact data including names, job titles, companies, emails, and industries. It handles complex scenarios like job change suggestions, hidden email revelation, Cloudflare protection bypass, and multi-page navigation with human-like behavior simulation.

## ✨ Key Features

- **🛡️ Anti-Detection System**: Multiple Cloudflare bypass methods (stealth, undetected, advanced, basic)
- **🔄 Job Change Acceptance**: Automated handling of job/company change suggestions by clicking on it and further on all pop-ups windows
   - **🔧 Page Recovery**: Handles page reloads after job change acceptance
- **📧 Email Revelation**: Clicking on buttons to reveal all the emails
- **🏭 Industry Extraction**: Automated industry data collection from profile buttons. Only 1 value is extracted!
- **📄 Multi-Page Support**: Sequential page processing with mimic human behaviour with some random scrolls and random clicking on buttons to reveal email.
- **🤖 Human-Like Behavior**: Realistic delays, mouse movements, and typing patterns
- **📊 Data Export**: CSV output to your local machine with comprehensive contact information

## 📋 Prerequisites

- Python 3.8+
- Chrome browser (latest version recommended)
- ChromeDriver (will auto-download if compatible)
- Apollo.io account with valid credentials

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd apollo_scraper_test1
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install additional anti-detection libraries**
   ```bash
   pip install selenium-stealth undetected-chromedriver
   ```

## ⚙️ Configuration

Create a `.env` file in the project root with the following variables:

```env
# Apollo.io Credentials (REQUIRED)
APOLLO_EMAIL=your_apollo_email@example.com
APOLLO_PASSWORD=your_apollo_password

# Apollo Search URL (REQUIRED)
# Navigate to your desired search in Apollo.io and copy the full URL
APOLLO_URL=https://app.apollo.io/#/people?...

# Scraping Configuration
PAGES_TO_SCRAPE=5
```

### 🔗 Getting Your Apollo URL

1. Log into Apollo.io manually
2. Set up your search filters (location, industry, job titles, etc.). For this project, it is already provided by sales team
3. Copy the complete URL from your browser address bar
4. Paste it as the `APOLLO_URL` value in your `.env` file

## 🏃‍♂️ Usage

### Basic Usage
```bash
# Activate virtual environment
source venv/bin/activate
```
add the environments in .env file

```bash
# Run the scraper
python3 main_pov.py
```


### Output
- **CSV Files**: Generated in `extracted_data/data_YYYYMMDD_HHMMSS.csv`
- **Screenshots**: Debug screenshots saved in `extracted_data/`
- **Logs**: Comprehensive console output with step-by-step progress

## 🏗️ Architecture

### Core Process Flow (8 Steps)

The scraper follows a carefully designed 8-step process for each page:

```
1. LOGIN & NAVIGATE → 2. GET HTML → 3. CREATE SOUP → 4. EXTRACT ROWS → 
5. ACCEPT JOB CHANGES → 6. REVEAL EMAILS → 7. EXTRACT DATA → 8. SAVE & NAVIGATE
```

#### Step-by-Step Breakdown

1. **Steps 1-2: Authentication & Navigation**
   - Anti-detection login with human-like typing
   - Cloudflare challenge handling
   - Navigation to search results

2. **Step 3: HTML Acquisition**
   - Page load waiting (9 seconds for stability)
   - Raw HTML extraction
   - BeautifulSoup object creation

3. **Step 4: Person Row Extraction**
   - Identifies individual contact rows (`div.zp_Uiy0R[role="row"]`)
   - Filters out non-data elements

4. **Step 4.4: Job Change Acceptance** ⭐
   - Detects job/company change suggestions
   - Handles 3-step acceptance workflow:
     - Click "Accept update" button
     - Submit form in first popup
     - Confirm "Yes" in second popup
   - Manages page reload recovery

5. **Step 4.5-4.6: Email Revelation** ⭐
   - Batch detection of hidden email buttons
   - Sequential clicking with human-like delays
   - Page refresh after email revelation

6. **Step 5: Data Extraction**
   - **Name**: From contact name cell
   - **Job Title**: Prioritizes NEW titles when job changes exist
   - **Company**: Prioritizes NEW companies when changes exist
   - **Email**: Extracts revealed email addresses
   - **Industry**: First industry from profile buttons

7. **Step 6: Data Storage**
   - CSV file creation/appending
   - Structured data with all 5 fields

8. **Step 7: Page Navigation**
   - Multi-strategy next page clicking
   - Error handling and retry logic

### Anti-Detection System

The scraper employs multiple bypass methods:

1. **Stealth Method** (Primary)
   - `selenium-stealth` library
   - Browser fingerprint masking
   - Automation detection removal

2. **Undetected Method** (Fallback)
   - `undetected-chromedriver`
   - Modified ChromeDriver

3. **Advanced Method**
   - Comprehensive browser arguments
   - Custom preferences
   - JavaScript automation hiding

4. **Basic Method** (Last resort)
   - Minimal anti-detection

### Human-Like Behavior Simulation

- **Typing**: Character-by-character input with realistic delays
- **Mouse Movement**: Random cursor movements
- **Scrolling**: Natural page scrolling patterns
- **Delays**: Variable timing between actions (0.7-2 seconds)
- **Breaks**: Natural pauses every 5 email clicks

## 📊 Data Output Format

The scraper generates CSV files with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `Full Name` | Contact's full name | "John Smith" |
| `Job Title` | Current job title (NEW if changed) | "Data Science Manager" |
| `Company` | Current company (NEW if changed) | "Tech Corp Inc." |
| `Email` | Email address (revealed if hidden) | "john.smith@techcorp.com" |
| `Industry` | First industry from profile | "Information Technology" |

## ⚠️ Current Limitations

### Performance Limitations
- **Email Clicking**: ~50% success rate due to stale element references
- **Job Change Processing**: Only processes first successful change per page
- **Page Load Times**: Conservative 9-second waits for stability
- **Sequential Processing**: One contact at a time (not parallelized)

### Functional Limitations
- **Single Job Change**: Stops after first job change acceptance to avoid stale elements
- **Industry Extraction**: Only captures first visible industry
- **Email Types**: Only handles standard Apollo email reveal buttons
- **Page Recovery**: Basic validation after job changes

### Technical Limitations
- **Browser Dependency**: Requires Chrome/Chromium
- **Network Dependency**: No offline mode
- **Memory Usage**: Loads full page HTML into memory
- **Error Recovery**: Limited retry mechanisms

## 🤔 Design Considerations

### Architecture Decisions

Based on extensive development and testing, key design choices include:

#### 1. **Integrated vs. Split Workflow**
**Decision**: Single integrated workflow
**Rationale**: 
- Considered splitting job change acceptance and data scraping into separate tools
- Chose integration for efficiency and state management
- Avoids double page loads and manual coordination

#### 2. **Page Recovery Strategy**
**Decision**: Intelligent page state checking after job changes
**Rationale**:
- Apollo reloads pages after job change acceptance
- Implemented recovery system to detect and handle empty page states
- Prevents premature navigation to next page

#### 3. **Email Revelation Approach**
**Decision**: Batch clicking with stale element tolerance
**Rationale**:
- Initial sequential clicking caused extensive stale element errors
- Batch approach finds all buttons first, then clicks sequentially
- Accepts 50% failure rate as acceptable for production use

#### 4. **Anti-Detection Strategy**
**Decision**: Multiple fallback methods
**Rationale**:
- Cloudflare protection varies by session
- Cascade approach: stealth → undetected → advanced → basic
- Ensures maximum success rate across different scenarios

#### 5. **Human Behavior Simulation**
**Decision**: Conservative timing with realistic patterns
**Rationale**:
- Aggressive clicking triggered Apollo pop-ups and blocks
- Balanced speed vs. detection risk
- 0.2-1.2 second delays between email clicks optimal

#### 6. **Data Extraction Priority**
**Decision**: NEW job/company data over original
**Rationale**:
- Job change suggestions indicate more current information
- Prioritizes updated data when available
- Maintains fallback to original data

### Performance Trade-offs

#### Speed vs. Reliability
- **Chosen**: Reliability over speed
- **Impact**: 9-second page loads, conservative delays
- **Benefit**: Consistent operation without detection

#### Completeness vs. Efficiency  
- **Chosen**: Process all available data
- **Impact**: Longer execution times
- **Benefit**: Maximum data extraction per session

#### Complexity vs. Maintainability
- **Chosen**: Modular 8-step process
- **Impact**: More code complexity
- **Benefit**: Clear debugging and maintenance

## 🔧 Maintenance & Troubleshooting

### Common Issues

1. **ChromeDriver Version Mismatch**
   ```bash
   # Update ChromeDriver
   pip install --upgrade chromedriver-autoinstaller
   ```

2. **Cloudflare Blocking**
   - Try different bypass methods
   - Update user agents
   - Increase delays between requests

3. **Element Not Found Errors**
   - Apollo may have updated their HTML structure
   - Check CSS selectors in the code
   - Update selectors as needed

4. **High Stale Element Rate**
   - Normal for email clicking (expected ~50% failure)
   - Consider increasing delays if rate exceeds 70%

### Debugging

- **Screenshots**: Automatically saved in `extracted_data/`
- **Console Logs**: Comprehensive step-by-step output
- **Error Screenshots**: Captured on failures

## 📈 Future Improvements

### Performance Optimizations
- [ ] Parallel email button clicking
- [ ] Dynamic delay adjustment based on success rates
- [ ] Intelligent page load detection
- [ ] Resume capability for interrupted sessions

### Feature Enhancements
- [ ] Phone number extraction
- [ ] LinkedIn profile URL capture
- [ ] Advanced filtering options
- [ ] Real-time progress dashboard

### Technical Improvements
- [ ] Database storage option
- [ ] API integration capabilities
- [ ] Configuration web interface
- [ ] Advanced error recovery


