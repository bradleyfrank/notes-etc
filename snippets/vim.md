# Vim

Partial Vimscript to search files and insert a Markdown link.

```vim
function! MDInsert()
  let l:searchPath = FindGitRoot()

  let dict = fzf#wrap({ 'dir': l:searchPath, 'sink*': {line -> setreg('*', line)} })

"  let dict['orig'] = dict['sink*']
"  function! dict['sink*'](lines)
"    if get(a:lines, 0, '') == 'ctrl-y'
"      call setreg('*', join(a:lines[1:], "\n"))
"    else
"      call self.orig(a:lines)
"    endif
"  endfunction

  call fzf#run(dict)
  let l:args = '^#+\s(.*)$ --no-line-number --max-count=1 --replace="$1" '
  execute "r !rg" . shellescape(l:args) . getreg('*')
endfunction

function! FindGitRoot()
  let l:dir = system('git rev-parse --show-toplevel 2> /dev/null')[:-2]
  if v:shell_error != 0
    return expand('%:p:h')
  else
    return l:dir
endfunction

command! Link call fzf#run({'options': '--multi', 'sink*': {lines -> setreg('*', join(lines, "\n"))}})
"command! -bang -nargs=? -complete=dir Link call fzf#vim#files(s:find_git_root(), fzf#vim#with_preview('right:50%'), <bang>0)
command! -nargs=? -complete=dir MDInsert call MDInsert()
```
