import os
import subprocess

def convert_to_pdfa(input_pdf, output_pdfa, ghostscript_path='gs'):
    try:
        # Ghostscript-Befehl für PDF/A-3b
        command = [
            ghostscript_path,
            '-dPDFA=3',
            '-dBATCH',
            '-dNOPAUSE',
            '-dNOOUTERSAVE',
            '-sColorConversionStrategy=UseDeviceIndependentColor',
            '-sOutputFile=' + output_pdfa,
            '-sDEVICE=pdfwrite',
            '-dPDFACompatibilityPolicy=1',
            input_pdf
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            print(f'Konvertierung erfolgreich: {output_pdfa}')
        else:
            print(f'Fehler bei der Konvertierung:\n{result.stderr.decode()}')
    
    except Exception as e:
        print(f'Fehler: {str(e)}')

def inject_xml(output_pdfa, input_xml, zugpferd_pdf):
    try:
        #factur-x befehl zur Einbettung
        command = [
            'facturx-pdfgen',
            output_pdfa,
            input_xml,
            zugpferd_pdf
        ]
        
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            print(f'Injezierung erfolgreich: {zugpferd_pdf}')
        else:
            print(f'Fehler bei der Konvertierung:\n{result.stderr.decode()}')
    
    except Exception as e:
        print(f'Fehler: {str(e)}')

def main():
    for file_name in os.listdir():
        print(file_name) #Test file finder
        if file_name.lower().endswith('.pdf'):
            input_pdf = file_name
            output_pdfa = f'PDF_A3_{file_name}'
            for file_name2 in os.listdir():
                if file_name2.lower().endswith('.xml'):
                    input_xml = file_name2
            zugferd_pdf = f'Zugferd_{file_name}'
            print(f'Konvertiere {input_pdf} nach PDF/A-3...')
            convert_to_pdfa(input_pdf, output_pdfa)
            print(f'Injiziere {input_xml} in {output_pdfa} ...')
            inject_xml(output_pdfa, input_xml, zugferd_pdf)
            os.remove(output_pdfa)
            break

if __name__ == '__main__':
    main()
