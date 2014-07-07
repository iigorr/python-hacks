def ok(message):
  print '\033[92m' + message + '\033[0m'

def warn(message):
  print '\033[93m' + message + '\033[0m'

def error(message):
  print '\033[91m' + message + '\033[0m'

def info(message):
  print '\033[96m' + message + '\033[0m'

# ESC [ 0 m       # reset all (colors and brightness)
# ESC [ 1 m       # bright
# ESC [ 2 m       # dim (looks same as normal brightness)
# ESC [ 22 m      # normal brightness

# # FOREGROUND:
# ESC [ 30 m      # black
# ESC [ 31 m      # red
# ESC [ 32 m      # green
# ESC [ 33 m      # yellow
# ESC [ 34 m      # blue
# ESC [ 35 m      # magenta
# ESC [ 36 m      # cyan
# ESC [ 37 m      # white
# ESC [ 39 m      # reset

# # BACKGROUND
# ESC [ 40 m      # black
# ESC [ 41 m      # red
# ESC [ 42 m      # green
# ESC [ 43 m      # yellow
# ESC [ 44 m      # blue
# ESC [ 45 m      # magenta
# ESC [ 46 m      # cyan
# ESC [ 47 m      # white
# ESC [ 49 m      # reset