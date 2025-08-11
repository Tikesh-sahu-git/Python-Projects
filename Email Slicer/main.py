import re
import json
import csv
from datetime import datetime
from pathlib import Path

class EmailSlicer:
    def __init__(self):
        self.results = []
        self.stats = {
            'total_processed': 0,
            'valid_emails': 0,
            'invalid_emails': 0
        }

    def validate_email(self, email):
        """🔍 Validate email format using advanced regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def extract_tld(self, domain):
        """🌐 Extract top-level domain with improved accuracy"""
        tld_pattern = r'\.([a-zA-Z]{2,63})$'
        match = re.search(tld_pattern, domain)
        return match.group(1) if match else None

    def analyze_email(self, email):
        """🛠 Perform comprehensive email analysis"""
        if not self.validate_email(email):
            raise ValueError("❌ Invalid email format")
        
        username, domain = email.split("@", 1)
        tld = self.extract_tld(domain)
        domain_parts = domain.split(".")
        domain_name = ".".join(domain_parts[:-1]) if len(domain_parts) > 1 else domain
        
        return {
            "email": email,
            "username": username,
            "domain": domain,
            "domain_name": domain_name,
            "top_level_domain": tld,
            "is_valid": True,
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def process_emails(self, emails):
        """⚙️ Process multiple emails efficiently"""
        batch_results = []
        for email in emails:
            try:
                result = self.analyze_email(email)
                batch_results.append(result)
                self.stats['valid_emails'] += 1
            except ValueError as e:
                error_result = {
                    "email": email,
                    "error": str(e),
                    "is_valid": False,
                    "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                batch_results.append(error_result)
                self.stats['invalid_emails'] += 1
        
        self.stats['total_processed'] += len(emails)
        self.results.extend(batch_results)
        return batch_results

    def save_results(self, format='json', filename=None):
        """💾 Save results in multiple formats"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"email_results_{timestamp}"
        
        if format == 'json':
            filename += '.json'
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
        elif format == 'csv':
            filename += '.csv'
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                writer.writeheader()
                writer.writerows(self.results)
        
        return filename

    def display_stats(self):
        """📊 Display comprehensive statistics"""
        print("\n📈 Email Processing Statistics:")
        print(f"📨 Total Emails Processed: {self.stats['total_processed']}")
        print(f"✅ Valid Emails: {self.stats['valid_emails']}")
        print(f"❌ Invalid Emails: {self.stats['invalid_emails']}")
        if self.stats['total_processed'] > 0:
            validity_percentage = (self.stats['valid_emails'] / self.stats['total_processed']) * 100
            print(f"📊 Validity Rate: {validity_percentage:.2f}%")

    def display_batch_results(self, batch_results):
        """🖥 Display results for a batch of emails"""
        for result in batch_results:
            if result['is_valid']:
                print(f"\n📧 Email: {result['email']}")
                print(f"👤 Username: {result['username']}")
                print(f"🏢 Domain: {result['domain_name']}")
                print(f"🌐 TLD: .{result['top_level_domain']}")
            else:
                print(f"\n❌ Invalid Email: {result['email']}")
                print(f"⚠️ Error: {result['error']}")

def main():
    print("""
    📧▄︻デ═══ Email Slicer Pro ════デ︻▄📧
    🔍 Extract usernames, domains, and TLDs from emails
    💡 Supports multiple inputs, file processing, and exports
    """)
    
    slicer = EmailSlicer()
    
    while True:
        print("\n" + "="*50)
        print("🔹 MENU:")
        print("1. Enter email(s) manually")
        print("2. Process emails from a file")
        print("3. View statistics")
        print("4. Save results")
        print("5. Exit")
        print("="*50)
        
        choice = input("🛠 Choose an option (1-5): ").strip()
        
        if choice == '1':
            emails_input = input("\n✏️ Enter email(s) (comma separated): ").strip()
            emails = [e.strip() for e in emails_input.split(",") if e.strip()]
            batch_results = slicer.process_emails(emails)
            slicer.display_batch_results(batch_results)
            
        elif choice == '2':
            file_path = input("\n📂 Enter file path (txt/csv/json): ").strip()
            try:
                file_ext = Path(file_path).suffix.lower()
                if file_ext == '.txt':
                    with open(file_path, 'r') as f:
                        emails = [line.strip() for line in f if line.strip()]
                elif file_ext == '.csv':
                    with open(file_path, 'r') as f:
                        reader = csv.DictReader(f)
                        emails = [row['email'] for row in reader if 'email' in row]
                elif file_ext == '.json':
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        emails = [item['email'] for item in data if isinstance(item, dict) and 'email' in item]
                else:
                    print("⚠️ Unsupported file format. Please use txt, csv, or json.")
                    continue
                
                print(f"📄 Found {len(emails)} emails in file.")
                batch_results = slicer.process_emails(emails)
                slicer.display_batch_results(batch_results)
                
            except FileNotFoundError:
                print("⚠️ File not found. Please try again.")
            except Exception as e:
                print(f"⚠️ Error processing file: {e}")
                
        elif choice == '3':
            slicer.display_stats()
            
        elif choice == '4':
            if not slicer.results:
                print("⚠️ No results to save. Process some emails first.")
                continue
                
            print("\n💾 Save Options:")
            print("1. JSON format")
            print("2. CSV format")
            save_choice = input("Choose format (1-2): ").strip()
            
            if save_choice in ('1', '2'):
                format = 'json' if save_choice == '1' else 'csv'
                custom_name = input("Enter custom filename (leave blank for auto): ").strip() or None
                filename = slicer.save_results(format=format, filename=custom_name)
                print(f"✅ Results saved to {filename}")
            else:
                print("⚠️ Invalid choice. Please try again.")
                
        elif choice == '5':
            if slicer.results:
                save_option = input("\n💾 Save results before exiting? (y/n): ").lower()
                if save_option == 'y':
                    format = input("Choose format (json/csv): ").lower()
                    if format in ('json', 'csv'):
                        filename = slicer.save_results(format=format)
                        print(f"✅ Results saved to {filename}")
                    else:
                        print("⚠️ Invalid format. Results not saved.")
            print("\n👋 Thank you for using Email Slicer Pro! Goodbye! 🚀")
            break
            
        else:
            print("⚠️ Invalid option. Please choose 1-5.")

if __name__ == "__main__":
    main()
