# config-storcli.py
# Command strings to generate storcli reports


# Command to generate detailed disk information
cmd_detail = [
    "/opt/MegaRAID/storcli/storcli64",
    "/c0/dALL",
    "show",
    "all" ]
# for debugging
#cmd_detail = [ "/bin/cat", "raid.current.txt" ]


# Command to generate predictive failures
cmd_predict = [
    "/opt/MegaRAID/storcli/storcli64",
    "/c0/eALL/sALL",
    "show",
    "all" ]
# for debugging
#cmd_predict = [ "/bin/cat", "/dev/null" ]

