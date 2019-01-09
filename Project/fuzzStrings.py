import os

# set 0 is a general set
# set 1 is exhaustive mysql
# set 2 is xss
# set 3 is OS command injection
# set 4 is common passwords
# set 5 is buffer overflows

fuzzSets = [ \
            ["quick_fuzz.txt", "overflow.txt"], \
            ["basic_fuzz.txt", "sqli-union-select.txt", "sqli-error-based.txt", \
            "sqli_escape_chars.txt", "sqli-time-based.txt"], \
            ["xss_escape_chars.txt", "xss_find_inject.txt", "xss_grep.txt", "xss_payloads_quick.txt", \
            "xss_remote_payloads-http.txt", "xss_swf_fuzz.txt"], \
            ["command_exec.txt", "traversal.txt", "traversal-short.txt"], \
            ["passwords_long.txt"], \
            ["numbers.txt"]
            ]

class Flicker:
    def __init__(self, phaseLength):
        self.phaseLength = phaseLength
        self.count = 0
        self.show = '/'

    def update(self):
        self.count += 1
        if self.count == self.phaseLength:
            self.count = 0
            if self.show == '/':
                self.show = '-'
            elif self.show == '-':
                self.show = '\\'
            elif self.show == '\\':
                self.show = '|'
            elif self.show == '|':
                self.show = '/'
        return self.show


def pullFuzzFromFiles(file):
    f = open(file, "r")
    ret = []
    for line in f:
        if not line.startswith("####"):
            ret.append(line.rstrip())
    return ret

def getFuzzFromSet(choice):
    paths = [os.getcwd() + "/IntruderPayloads/FuzzLists/" + p for p in fuzzSets[choice]]
    ret = []
    for file in paths:
        f = open(file, 'r')
        for line in f:
            if not line.startswith("####"):
                ret.append(line.rstrip())
        f.close()
    return ret


def quickFuzz():
    file = os.getcwd() + "/IntruderPayloads/FuzzLists/quick_fuzz.txt"
    return pullFuzzFromFiles(file)

def sql_quick():
    file = os.getcwd() + "/IntruderPayloads/FuzzLists/sql_quick.txt"
    return pullFuzzFromFiles(file)