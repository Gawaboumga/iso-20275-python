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
                if original_lines[i][5] == new_row[5] and original_lines[i][6] == new_row[6]:
                    local_abbreviations = original_lines[i][9].split(';')
                    for other_local_abbreviation in new_row[9].split(';'):
                        if other_local_abbreviation not in local_abbreviations:
                            local_abbreviations.append(other_local_abbreviation)
                    original_lines[i][9] = ';'.join(local_abbreviations).strip(';')

                    transliterated_abbreviations = original_lines[i][10].split(';')
                    for other_transliterated_abbreviation in new_row[10].split(';'):
                        if other_transliterated_abbreviation not in transliterated_abbreviations:
                            transliterated_abbreviations.append(other_transliterated_abbreviation)
                    original_lines[i][10] = ';'.join(transliterated_abbreviations).strip(';')
                else:
                    new_legal_forms.append(new_row)

    results = original_lines + new_legal_forms
    results.sort(key=lambda x: x[1])

    multiples = {}
    for result in results:
        key = result[0] + result[6]
        values = multiples.get(key, [])
        values.append(result)
        multiples[key] = values

    for key, values in multiples.items():
        if len(values) > 1:
            print(f'Error for {key}: {values}')

    return results


def write(filepath, elfs):
    with open(filepath, 'w', encoding='utf-8', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, lineterminator='\n', quoting=csv.QUOTE_ALL)
        spamwriter.writerows(elfs)


def main():

    current_directory = os.path.dirname(os.path.realpath(__file__))

    header_line, original_lines = read_iso_20275(os.path.join(current_directory, 'ISO-20275 - 2020-11-19.csv'))
    elf_histo = {}
    for original_line in original_lines:
        number_of_occurences = elf_histo.get(original_line[0], 0)
        elf_histo[original_line[0]] = number_of_occurences + 1
    count = 0
    for value in elf_histo.values():
        if value > 1:
            count += 1
    print(f'There are {count} ELF entries with at least one line.')

    header_line, original_lines = read_iso_20275(os.path.join(current_directory, 'Cleaned - ISO-20275 - 2020-11-19.csv'))
    new_legal_forms, completed_legal_forms = read_additional_legal_forms(os.path.join(current_directory, 'Additional legal forms.txt'))

    new_elfs = merge(original_lines, new_legal_forms, completed_legal_forms)
    write(os.path.join(current_directory, 'Cleaned - with additional - ISO-20275 - 2020-11-19.csv'), header_line + new_elfs)
    

if __name__ == '__main__':
    main()
