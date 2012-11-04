# positions
AT_BEGINNING = "at_beginning"
AT_BEGINNING_LINE = "at_beginning_line"
AT_BEGINNING_STRING = "at_beginning_string"
AT_BOUNDARY = "at_boundary"
AT_NON_BOUNDARY = "at_non_boundary"
AT_END = "at_end"
AT_END_LINE = "at_end_line"
AT_END_STRING = "at_end_string"
AT_LOC_BOUNDARY = "at_loc_boundary"
AT_LOC_NON_BOUNDARY = "at_loc_non_boundary"
AT_UNI_BOUNDARY = "at_uni_boundary"
AT_UNI_NON_BOUNDARY = "at_uni_non_boundary"

ATCODES = [
    AT_BEGINNING, AT_BEGINNING_LINE, AT_BEGINNING_STRING, AT_BOUNDARY,
    AT_NON_BOUNDARY, AT_END, AT_END_LINE, AT_END_STRING,
    AT_LOC_BOUNDARY, AT_LOC_NON_BOUNDARY, AT_UNI_BOUNDARY,
    AT_UNI_NON_BOUNDARY
]

def makedict(list):
    d = {}
    i = 0
    for item in list:
        d[item] = i
        i = i + 1
    return d

ATCODES = makedict(ATCODES)
a = 1

