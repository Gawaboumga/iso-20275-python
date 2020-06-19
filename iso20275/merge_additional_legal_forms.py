import csv
import os


def read_additional_legal_forms(filepath):
    new_legal_forms = []
    completed_legal_forms = {}
    with open(filepath, encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if len(row) <= 1:
                continue
            elif len(row) != 10 and len(row) != 16:
                raise Exception('Unknown line')
            else:
                if len(row) == 10:
                    new_legal_forms.append(row)
                else:
                    rows = completed_legal_forms.get(row[0], [])
                    rows.append(row)
                    completed_legal_forms[row[0]] = rows
    return new_legal_forms, completed_legal_forms


def read_iso_20275(filepath):
    lines = []
    with open(filepath, encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            lines.append(row)
    return [lines[0]], lines[1:]


def merge(original_lines, new_legal_forms, completed_legal_forms):
    fake_elf = 1
    for i in range(len(new_legal_forms)):
        new_legal_forms[i] = [f"{fake_elf:04d}"] + new_legal_forms[i]
        fake_elf += 1

    for i in range(len(original_lines)):
        elf = original_lines[i][0]
        new_rows = completed_legal_forms.get(elf, None)
        if new_rows is not None:
            for new_row in new_rows:
                if original_lines[i][5] == new_row[5]:
                    original_lines[i] = new_row
                else:
                    new_legal_forms.append(new_row)

    results = original_lines + new_legal_forms
    results.sort(key=lambda x: x[1])

    return results


def write(filepath, elfs):
    with open(filepath, 'w', encoding='utf-8', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, lineterminator='\n', quoting=csv.QUOTE_ALL)
        spamwriter.writerows(elfs)


def main():

    current_directory = os.path.dirname(os.path.realpath(__file__))
    header_line, original_lines = read_iso_20275(os.path.join(current_directory, 'Cleaned - ISO-20275 - 2019-11-06.csv'))
    new_legal_forms, completed_legal_forms = read_additional_legal_forms(os.path.join(current_directory, 'Additional legal forms.txt'))

    new_elfs = merge(original_lines, new_legal_forms, completed_legal_forms)
    write(os.path.join(current_directory, 'Cleaned - with additional - ISO-20275 - 2019-11-06.csv'), header_line + new_elfs)
    

if __name__ == '__main__':
    main()
