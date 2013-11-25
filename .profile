# MacPorts Installer addition on 2013-06-10_at_13:31:17: adding an appropriate PATH variable for use with MacPorts.
export PATH=/opt/local/bin:/opt/local/sbin:/opt/local/Library/Frameworks/Python.framework/Versions/3.3/bin/:$PATH
# Finished adapting your PATH environment variable for use with MacPorts.
# Finished adapting PATH environment variable for Syntastic

# alias the vim binary path
# alias vim='/opt/local/bin/vim'
alias vim='/Applications/MacVim.app/Contents/MacOS/Vim'

# alias ptt
alias ptt='ssh bbsu@ptt.cc'

# alias ls
alias ls='ls -a'

# enable the vim mode in bash
set -o vi

# enable the bash ls commande color
export CLICOLOR=1

# define fuction __git_ps1()
__git_ps1 () 
{ 
    local b="$(git symbolic-ref HEAD 2>/dev/null)";
    if [ -n "$b" ]; then
        printf "%s " "${b##refs/heads/}";
    fi
}

# define colors
blue='\[\e[0;34m\]'
orange='\[\e[0;1;31m\]'
normal='\[\e[m\]'

# customize bash prompt message
#export PS1=''$blue'$(__git_ps1)'$orange'\w '$normal''
export PS1=''$orange'\w$ '$normal''

# alias mosek
alias mosek='~/mosek/7/tools/platform/osx64x86/bin/mosek -f'

# default directory
cd ~/Workspace/Homework/MS\ Homework\ 2013/Homework\ 1/pycode/
