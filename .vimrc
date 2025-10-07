call plug#begin()

Plug 'catppuccin/vim', { 'as': 'catppuccin' }
Plug 'preservim/nerdtree'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'jiangmiao/auto-pairs'
Plug 'sheerun/vim-polyglot'
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
Plug 'tpope/vim-fugitive'
Plug 'airblade/vim-gitgutter'
Plug 'dense-analysis/ale'
Plug 'tpope/vim-commentary'
Plug 'ap/vim-buftabline'
Plug 'neoclide/coc.nvim', {'branch': 'release'}

call plug#end()

" === Основные настройки ===

set relativenumber
set number
set tabstop=4
set shiftwidth=4
set expandtab
set mouse=a
syntax enable

set termguicolors
set background=dark
colorscheme catppuccin_mocha
let g:airline_theme = 'catppuccin_mocha'
let g:airline_powerline_fonts = 1

filetype plugin indent on
set encoding=utf-8
set nocompatible
set laststatus=2

" === NERDTree ===
nnoremap <C-b> :NERDTreeToggle<CR>
autocmd VimEnter * NERDTree | wincmd p

" === ALE ===
let g:ale_linters = {
\   'python': ['flake8', 'pylint', 'mypy'],
\   'javascript': ['eslint', 'tsserver'],
\   'typescript': ['eslint', 'tsserver'],
\   'go': ['golangci-lint', 'gofmt'],
\   'rust': ['analyzer'],
\   'cpp': ['clangtidy', 'cppcheck'],
\   'lua': ['luacheck'],
\   'sh': ['shellcheck'],
\   'vim': ['vint'],
\   'html': ['tidy'],
\   'css': ['stylelint'],
\   'json': ['jq'],
\}
let g:ale_fixers = {
\   '*': ['remove_trailing_lines', 'trim_whitespace'],
\   'python': ['black', 'isort'],
\   'javascript': ['prettier', 'eslint'],
\   'typescript': ['prettier', 'eslint'],
\   'go': ['gofmt', 'goimports'],
\   'html': ['prettier'],
\   'css': ['prettier'],
\   'json': ['jq', 'prettier'],
\   'yaml': ['prettier'],
\   'markdown': ['prettier'],
\}
let g:ale_fix_on_save = 1
let g:ale_linters_explicit = 1
let g:ale_sign_error = '✗'
let g:ale_sign_warning = '⚠'
let g:ale_sign_info = 'ℹ'
let g:ale_virtualtext_cursor = 1

" === Buftabline ===
let g:buftabline_show = 1

" === Coc.nvim ===
inoremap <silent><expr> <TAB> coc#pum#visible() ? coc#pum#next(1) :
      \ CheckBackspace() ? "\<Tab>" : coc#refresh()
inoremap <expr><S-TAB> coc#pum#visible() ? coc#pum#prev(1) : "\<C-h>"
inoremap <silent><expr> <CR> coc#pum#visible() ? coc#pum#confirm() : "\<C-g>u\<CR>"

function! CheckBackspace() abort
  let col = col('.') - 1
  return !col || getline('.')[col - 1] =~# '\s'
endfunction

nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gr <Plug>(coc-references)
nmap <silent> <leader>rn <Plug>(coc-rename)
nnoremap <silent> K :call ShowDocumentation()<CR>
function! ShowDocumentation()
  if CocAction('hasProvider', 'hover')
    call CocActionAsync('doHover')
  else
    call feedkeys('K', 'in')
  endif
endfunction

" === Catppuccin Mocha Purple (Dark Cosmic) ===
" ====== Прозрачный тёмный фон ======
highlight Normal        guibg=NONE guifg=#cdd6f4
highlight SignColumn    guibg=NONE
highlight EndOfBuffer   guibg=NONE
highlight LineNr        guibg=NONE guifg=#45475a
highlight CursorLine    guibg=#11111b
highlight ColorColumn   guibg=#11111b
highlight CursorLineNr  guibg=#1e1e2e guifg=#cba6f7

" ====== Popup / Float окна ======
highlight CocFloating      guibg=#11111b guifg=#cdd6f4
highlight CocErrorFloat    guifg=#f38ba8 guibg=#11111b
highlight CocWarningFloat  guifg=#f9e2af guibg=#11111b
highlight CocInfoFloat     guifg=#89b4fa guibg=#11111b
highlight CocHintFloat     guifg=#94e2d5 guibg=#11111b

" ====== Меню и подсветка ======
highlight CocMenuSel       guibg=#2a2a3f guifg=#cba6f7
highlight Search           guibg=#cba6f7 guifg=#11111b
highlight IncSearch        guibg=#b4befe guifg=#11111b
highlight Visual           guibg=#2a2a3f

" ====== Синтаксис с фиолетовым акцентом ======
highlight CocSymbolMethod   guifg=#cba6f7
highlight CocSymbolVariable guifg=#fab387
highlight Function          guifg=#cba6f7
highlight Keyword           guifg=#cba6f7
highlight Identifier        guifg=#b4befe
highlight Statement         guifg=#cba6f7
highlight String            guifg=#fab387
highlight Type              guifg=#b4befe
highlight Comment           guifg=#bac2de

" ====== Темнее Airline ======
highlight StatusLine   guibg=#181825 guifg=#cba6f7
highlight StatusLineNC guibg=#1e1e2e guifg=#6c7086
