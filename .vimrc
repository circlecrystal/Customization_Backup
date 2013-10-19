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
Bundle 'scrooloose/nerdtree'
Bundle 'sjl/gundo.vim'
Bundle 'majutsushi/tagbar'
Bundle 'scrooloose/syntastic'
Bundle 'msanders/snipmate.vim'
Bundle 'Shougo/vimshell.vim'

filetype plugin indent on     " required!
"
" Brief help
" :BundleList          - list configured bundles
" :BundleInstall(!)    - install(update) bundles
" :BundleSearch(!) foo - search(or refresh cache first) for foo
" :BundleClean(!)      - confirm(or auto-approve) removal of unused bundles
"
" see :h vundle for more details or wiki for FAQ
" NOTE: comments after Bundle command are not allowed..

" Plugin toggle function
function! ToggleTagbar()
    GundoHide
    NERDTreeClose
    TagbarToggle
endfunction

function! ToggleGundo()
    TagbarClose
    NERDTreeClose
    GundoToggle
endfunction

function! ToggleNERDTree()
    TagbarClose
    GundoHide
    NERDTreeToggle
endfunction

function! ToggleErrors()
    if empty(filter(tabpagebuflist(), 'getbufvar(v:val, "&buftype") is# "quickfix"'))
        " No location/quickfix list shown, open syntastic error location panel
        Errors
    else
        lclose
    endif
endfunction

" Map plugin toggles
nmap <F2> :call ToggleTagbar()<CR>
nmap <F3> :call ToggleGundo()<CR>
nmap <F4> :call ToggleNERDTree()<CR>
nmap <F6> :SyntasticToggleMode<CR>
nmap <F7> :call ToggleErrors()<CR>

" Powerline Setup
set laststatus=2
set noshowmode

" NERDTree Setup
autocmd VimEnter * if !argc() | NERDTree | endif
autocmd bufenter *
    \ if (winnr("$") == 1 && exists("b:NERDTreeType") 
    \ && b:NERDTreeType == "primary") | q | endif
let g:NERDTreeWinSize = 40
let g:NERDTreeWinPos = "right"

" Tagbar setup
" let g:tagbar_left = 1
let g:tagbar_autoclose = 1
let g:tagbar_width = 40

" Gundo setup
" let g:gundo_preview_bottom = 1
let g:gundo_width = 40
let g:gundo_preview_height = 15
let g:gundo_right = 1

" Syntastic setup
" let g:syntastic_check_on_open = 1
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



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" My rest config follows here:
syntax on
colorscheme lucius

let python_highlight_all=1

" set laststatus=2
" set statusline=%t%=[\ %l,%c\ ][\ %P\ ]

set cursorline

set number
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

autocmd BufWinLeave *.* mkview
autocmd BufWinEnter *.* silent loadview

nmap <F5> :wall \| !clear && echo "% is running..." && python3 %<CR>

" highlight characters past column 79
autocmd FileType python
    \ highlight overlength
    \ ctermbg=darkgrey ctermfg=white guibg=#592929
autocmd FileType python match overlength /\%80v.\+/
autocmd FileType python set nowrap
