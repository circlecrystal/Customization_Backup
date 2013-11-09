# MacPorts Installer addition on 2013-06-10_at_13:31:17: adding an appropriate PATH variable for use with MacPorts.
export PATH=/opt/local/bin:/opt/local/sbin:/opt/local/Library/Frameworks/Python.framework/Versions/3.3/bin/:$PATH
# Finished adapting your PATH environment variable for use with MacPorts.
# Finished adapting PATH environment variable for Syntastic

# alias the vim binary path
# alias vim='/opt/local/bin/vim'
alias vim='/Applications/MacVim.app/Contents/MacOS/Vim'

# alias ptt
alias ptt='ssh bbsu@ptt.cc'

# enable the vim mode in bash
set -o vi

# enable the bash ls commande color
export CLICOLOR=1

# customize bash prompt message
export PS1='\e[1;31m\W$\e[m '

# default directory
cd ~/Workspace/
