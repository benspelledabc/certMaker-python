import os


def move_keys_and_csrs(destination_dir):
    # if not os.path.isdir(destination_dir):
    #     os.makedirs(destination_dir)
    with open("output.sh", "a+") as fp:
        fp.writelines("mkdir {0}\n".format(destination_dir))
        fp.writelines("mv *.csr {0}{1}\n".format(destination_dir, os.path.sep))
        fp.writelines("mv *.key {0}{1}\n".format(destination_dir, os.path.sep))


def process_no_sans_needed(line):
    output_line = 'openssl req -new -newkey rsa:2048 -nodes -keyout {0}.key -subj "/C=US/ST=MD/O=Ben Spelled ' \
                  'ABC/OU=Sample, OU=SubOU, OU=Level3Sub/CN={0}" -out {0}.csr'.format(line)
    with open("output.sh", "a+") as fp:
        fp.writelines(output_line + "\n")


def process_sans_needed(line_items):
    starting_string = r'openssl req -new -newkey rsa:2048 -nodes -keyout {0}.key -subj "/C=US/ST=CA/O=Acme, ' \
                      r'Inc./OU=Sample, OU=SubOU, OU=Level3Sub/CN={0}" -reqexts SAN -config <(cat sans.cnf <(printf ' \
                      r'"\n[SAN]\nsubjectAltName='.format(line_items[0])
    dns_strings = ''

    for x in range(1, len(line_items)):
        dns_strings += "DNS:{0}".format(line_items[x])
        if x != (len(line_items) - 1):
            dns_strings += ","

    buff = starting_string + dns_strings
    tail = r'\n")) -out {0}.csr'.format(line_items[0])

    final = buff + tail

    with open("output.sh", "a+") as fp:
        fp.writelines(final + "\n")


def process_unfiltered_list(input_list):
    for line in input_list:
        items = line.split(" ")
        if len(items) > 1:
            process_sans_needed(items)
        else:
            process_no_sans_needed(items[0])


def get_content(input_file):
    count = 0
    output = []

    with open(input_file) as fp:
        for line in fp:
            stripped_line = line.strip()
            if len(stripped_line) > 2:
                output.append(line.strip())

    return output


# Cleanup before first run
if os.path.isfile("output.sh"):
    os.remove("output.sh")

# doWork()
content = get_content('hosts.txt')
process_unfiltered_list(content)
move_keys_and_csrs("output")
