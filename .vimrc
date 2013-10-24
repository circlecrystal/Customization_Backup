set nocompatible               " be iMproved
filetype off                   " required!

set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

" let Vundle manage Vundle
" required!
Bundle 'gmarik/vundle'

" My Bundles here:
Bundle 'Lokaltog/powerline', {'rtp': 'powerline/bindings/vim/'}
Bundle 'davidhalter/jedi-vim'
Bundle 'majutsushi/tagbar'
Bundle 'sjl/gundo.vim'
Bundle 'scrooloose/syntastic'
Bundle 'msanders/snipmate.vim'

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


" Powerline Setup
set laststatus=2
set noshowmode

" Tagbar setup
" let g:tagbar_left = 1
let g:tagbar_autoclose = 0
let g:tagbar_width = 35

"  Gundo setup
" let g:gundo_preview_bottom = 1
let g:gundo_width = 35
let g:gundo_preview_height = 15
let g:gundo_right = 1

" Syntastic setup
let g:syntastic_python_checkers = ['pylint']
" let g:syntastic_mode_map =
"     \ {
"     \ 'mode': 'active',
"     \ 'active_filetypes': ['python'],
"     \ 'passive_filetypes': []
"     \ }
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

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
nmap <F4> :call ToggleErrors()<CR>
nmap <F6> :call ToggleSyntastic()<CR>


" My rest config follows here:
syntax on
colorscheme lucius

let python_highlight_all=1

" set laststatus=2
" set statusline=%t%=[\ %l,%c\ ][\ %P\ ]

set cursorline

set number
" set relativenumber
set numberwidth=2

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

autocmd BufWinLeave *.* mkview
autocmd BufWinEnter *.* silent loadview

nmap <F5> :wall \| !clear && echo "% is running..." && python3 %<CR>

" highlight characters past column 79
autocmd FileType python
    \ highlight overlength
    \ ctermbg=darkgrey ctermfg=white guibg=#592929
autocmd FileType python match overlength /\%80v.\+/
autocmd FileType python set nowrap
