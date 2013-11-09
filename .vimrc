set nocompatible               " be iMproved
filetype off                   " required!

set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

" let Vundle manage Vundle
" required!
Bundle 'gmarik/vundle'

" My Bundles here:
Bundle 'davidhalter/jedi-vim'
Bundle 'majutsushi/tagbar'
Bundle 'sjl/gundo.vim'
Bundle 'scrooloose/syntastic'
Bundle 'msanders/snipmate.vim'
Bundle 'altercation/vim-colors-solarized'
Bundle 'Shougo/unite.vim'
Bundle 'Shougo/vimproc.vim'
Bundle 'Lokaltog/powerline', {'rtp': 'powerline/bindings/vim/'}

filetype plugin indent on  " required!
"
" Brief help
" :BundleList          - list configured bundles
" :BundleInstall(!)    - install(update) bundles
" :BundleSearch(!) foo - search(or refresh cache first) for foo
" :BundleClean(!)      - confirm(or auto-approve) removal of unused bundles
"
" see :h vundle for more details or wiki for FAQ
" NOTE: comments after Bundle command are not allowed..


" Tagbar setup
"let g:tagbar_left = 1
let g:tagbar_autoclose = 1
let g:tagbar_width = 40

"  Gundo setup
"let g:gundo_preview_bottom = 1
let g:gundo_width = 37
let g:gundo_preview_height = 15
let g:gundo_right = 1

" Syntastic setup
let g:syntastic_python_checkers = ['pylint']
let g:syntastic_mode_map =
        \ {
        \ 'mode': 'passive',
        \ 'active_filetypes': [],
        \ 'passive_filetypes': []
        \ }
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

" Solarized setup
syntax on
set background=dark
colorscheme solarized
set number
set numberwidth=2
set cursorline
hi CursorLineNr ctermfg=10 ctermbg=0 guifg=Yellow

" Unite setup
nmap <space><space> :Unite -toggle file_rec/async<CR>
nmap <space>, :Unite -toggle file_mru<CR>
nmap <space>/ :Unite -toggle grep:$buffers<CR>
nmap <space>. :Unite -toggle grep:.<CR>

let g:unite_source_grep_max_candidates = 200

if executable('ag')
  " Use ag in unite grep source.
  let g:unite_source_grep_command = 'ag'
  let g:unite_source_grep_default_opts =
        \ '--line-numbers --nocolor --nogroup --hidden --ignore ' .
        \  '''.hg'' --ignore ''.svn'' --ignore ''.git'' --ignore ''.bzr'''
  let g:unite_source_grep_recursive_opt = ''
elseif executable('ack-grep')
  " Use ack in unite grep source.
  let g:unite_source_grep_command = 'ack-grep'
  let g:unite_source_grep_default_opts =
        \ '--no-heading --no-color -a -H'
  let g:unite_source_grep_recursive_opt = ''
endif

" Powerline setup
set noshowmode

"" Airline setup
"set noshowmode
"let g:airline_powerline_fonts = 1
"let g:airline#extensions#default#section_truncate_width = {}

" Plugin toggle function
function ToggleTagbar()
    GundoHide
    call ErrorsClose()
    TagbarToggle
endfunction

function ToggleGundo()
    TagbarClose
    call ErrorsClose()
    GundoToggle
endfunction

function ErrorsToggle()
    if empty(filter(tabpagebuflist(), 'getbufvar(v:val, "&buftype")
                                                \ is# "quickfix"'))
        Errors
    else
        lclose
    endif
endfunction

function ErrorsClose()
    if empty(filter(tabpagebuflist(), 'getbufvar(v:val, "&buftype")
                                                \ is# "quickfix"'))
    else
        lclose
    endif
endfunction

function ToggleErrors()
    TagbarClose
    GundoHide
    call ErrorsToggle()
endfunction

function ToggleSyntastic()
    TagbarClose
    GundoHide
    SyntasticToggleMode
endfunction

" Map plugin toggles
nmap <F2> :call ToggleTagbar()<CR>
nmap <F3> :call ToggleGundo()<CR>
nmap <F6> :call ToggleSyntastic()<CR>
nmap <F7> :call ToggleErrors()<CR>


" My rest config follows here:
"syntax on
let python_highlight_all=1

set laststatus=2
"set statusline=%t%=[\ %l,%c\ ][\ %P\ ]

"set number
"set numberwidth=2
"set cursorline

set foldmethod=indent
set foldlevel=99

set smartindent
set tabstop=4
set shiftwidth=4
set expandtab
set softtabstop=4

set backspace=indent,eol,start

set undofile
set undodir=~/.vim/undo
set undolevels=1000
set undoreload=10000

set wildmenu
set mouse=a

set timeoutlen=1000 ttimeoutlen=0

autocmd BufWinLeave *.* mkview
autocmd BufWinEnter *.* silent loadview

nmap <F5> :wall \| !clear && echo "% is running..." && python3 %<CR>

" highlight characters past column 79
autocmd FileType python
        \ highlight overlength
        \ ctermbg=darkgrey ctermfg=white guibg=#592929
autocmd FileType python match overlength /\%80v.\+/
autocmd FileType python set nowrap
