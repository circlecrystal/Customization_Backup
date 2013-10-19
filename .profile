# MacPorts Installer addition on 2013-06-10_at_13:31:17: adding an appropriate PATH variable for use with MacPorts.
export PATH=/opt/local/bin:/opt/local/sbin:/opt/local/Library/Frameworks/Python.framework/Versions/3.3/bin/:$PATH
# Finished adapting your PATH environment variable for use with MacPorts.

# alias the vim binary path
# alias vim='/opt/local/bin/vim'
alias vim='/Applications/MacVim.app/Contents/MacOS/Vim'

# enable the vim mode in bash
set -o vi

# enable the bash ls commande color
export CLICOLOR=1

# default directory
cd ~/Workspace/
