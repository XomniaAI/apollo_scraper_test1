#!/usr/bin/env python3

from bs4 import BeautifulSoup

def test_extraction_logic():
    """Test the new extraction logic with the example HTML file."""
    
    # Read the example HTML file
    with open("example_3_people.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Create soup
    soup = BeautifulSoup(html_content, 'html.parser')
    print("🍲 Created BeautifulSoup object from example HTML")
    
    # STEP 4: Extract person rows
    person_rows = soup.find_all('div', {'class': 'zp_Uiy0R', 'role': 'row'})
    print(f"🔍 Found {len(person_rows)} person rows")
    
    # Expected results
    expected_results = [
        ("Edwin Jansen", "Head of Digital Transformation", "ING BANK N.V."),
        ("Prakash Pattiath", "Digital Transformation Manager", "Unigas International B.V."),
        ("Felice Davies", "Manager Digital Transformation", "KPMG Nederland")
    ]
    
    print("\n" + "="*60)
    print("TESTING EXTRACTION LOGIC")
    print("="*60)
    
    for idx, person_row in enumerate(person_rows, 1):
        print(f"\n🔍 Processing person {idx}...")
        
        # Get all cells, but exclude the checkbox cell (has zp_xk8LG class)
        all_cells = person_row.find_all('div', {'role': 'cell', 'class': 'zp_egyXf'})
        data_cells = [cell for cell in all_cells if 'zp_xk8LG' not in cell.get('class', [])]
        
        print(f"  📊 Found {len(all_cells)} total cells, {len(data_cells)} data cells")
        
        if len(data_cells) < 3:
            print(f"  ⚠️  Person {idx}: Only {len(data_cells)} data cells found, skipping")
            continue
        
        # Extract data from the first 3 cells
        name_cell = data_cells[0]
        job_title_cell = data_cells[1] 
        company_cell = data_cells[2]
        
        # Extract name
        name_element = name_cell.select_one('div[data-testid="contact-name-cell"] a')
        name = name_element.get_text().strip() if name_element else "Unknown Name"
        
        # Extract job title
        title_element = job_title_cell.select_one('span.zp_FEm_X')
        job_title = title_element.get_text().strip() if title_element else "Unknown Title"
        
        # Extract company
        company_element = company_cell.select_one('span.zp_xvo3G')
        company = company_element.get_text().strip() if company_element else "Unknown Company"
        
        print(f"  ✅ EXTRACTED: {name} | {job_title} | {company}")
        
        # Check against expected results
        if idx <= len(expected_results):
            expected_name, expected_title, expected_company = expected_results[idx-1]
            print(f"  📋 EXPECTED:  {expected_name} | {expected_title} | {expected_company}")
            
            # Verify results
            name_match = name == expected_name
            title_match = job_title == expected_title
            company_match = company == expected_company
            
            print(f"  ✅ Name Match: {name_match}")
            print(f"  ✅ Title Match: {title_match}")
            print(f"  ✅ Company Match: {company_match}")
            
            if name_match and title_match and company_match:
                print(f"  🎉 Person {idx}: ALL MATCHES - PERFECT!")
            else:
                print(f"  ⚠️  Person {idx}: Some mismatches detected")
    
    print(f"\n🎉 EXTRACTION TEST COMPLETED!")

if __name__ == "__main__":
    test_extraction_logic() 