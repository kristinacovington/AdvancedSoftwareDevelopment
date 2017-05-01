class output_bot:

    def list_reports(self, reports):
        print("\nPrinting all available reports:\n")
        reports = reports.decode('utf-8')
        print(reports)
        print("Done Printing")

    def print_content(self, content):
        print("\nPrinting content")
        print("-------------------------")
        content = content.decode('utf-8')
        print(content)
        print("-------------------------")
        print("Done Printing\n")