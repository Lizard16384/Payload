import pyperclip

from payload.compressor import compress

class CommandLengthError(Exception):
    def __init__(self, value, message):
        self.value = value
        self.message = message
        super().__init__(f"{self.message} (Length: {self.value})")

class CommandWireError(Exception):
    def __init__(self, value, message):
        self.value = value
        self.message = message
        super().__init__(f"{self.message} (Length: {self.value})")

def read_file_lines(file_name):
    file = open(file_name)
    file_lines = []
    for line in file:
        new = line.strip()
        if len(new) > 0 and new[0] != "#":
            file_lines.append(new)
    file.close()
    return file_lines

def finish(raw_final, output, file_name = "result.txt"):
    print("Parsing and compressing provided command...")
    final = compress.compile_command(raw_final)

    if len(final) > 32500:
        raise CommandLengthError(len(final), f"Payload character length exceeds 32500! Command cannot be pasted in one command!")
    elif False:  # TODO: check byte length not to exceed 65536 and check behavior - maybe command can still be run, packet just can't be sent back to client.
        raise CommandWireError(len(final), f"Payload byte length exceeds 65536! Command cannot be sent to server in one command!")
    else:
        print("Payload successfully compiled command.")
        print(f"Payload: {((len(final)/32500) * 100):.2f}%, {len(final)} used of 32500")
    
    if "clipboard" in output:
        pyperclip.copy(final)
    if "write" in output:
        result = open(file_name, "w", -1, "utf-8")
        result.write(final)
        result.close()
    if "clipboard" not in output and "write" not in output:
        raise Exception('Please specify output method. Options are "clipboard" and/or "write"')

    print(f"Result {f'wrote to file {file_name}' if "write" in output else ""}{" and " if "clipboard" in output and "write" in output else ""}{"copied to clipboard" if "clipboard" in output else ""}.")
