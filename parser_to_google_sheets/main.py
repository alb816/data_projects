from parser import parse_data
from sheets_uploader import upload_to_sheets
from export_from_sheets import export_from_sheets
from analysis import analyze_data

def main():
    data = parse_data()
    upload_to_sheets(data)
    export_from_sheets()
    analyze_data()

if __name__ == "__main__":
    main()