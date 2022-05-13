# Zsh Prompt

```sh
precmd() {
  local rc=$? eol=$'\n' _gitdir _kcxt _repo _prompt_color _prompt_line1 _prompt_line2
  local _git_icon=$'\uf407' _py_icon=$'\uf81f' _k8s_icon=$'\ufd31'
  local fg_Blue="%F{33}" fg_Cyan="%F{37}" fg_Violet="%F{61}" fg_Green="%F{64}" fg_Magenta="%F{125}" fg_Red="%F{160}"
  local fg_NoColor="%f" bold="%B" nobold="%b" fg_Reset="%b%f"

  _PYENV="" _GIT="" _KUBECTL="" _HOSTNAME="" _CWD="${bold}${fg_Blue}%(5~|%-1~/.../%1~|%~)${fg_Reset} "

  [[ -n $SSH_CONNECTION ]] && _HOSTNAME="${bold}${fg_Magenta}$(hostname -s)${fg_Reset} in "
  [[ -n $TMUX ]] && _CWD="${bold}${fg_Blue}%1~${fg_Reset} "
  [[ -n "$VIRTUAL_ENV" ]] && _PYENV="via ${fg_Cyan}${_py_icon} ${bold}$(python --version | awk '{print $2}')${fg_Reset} "

  if _kcxt="$(kubectl config current-context 2> /dev/null)"; then
    [[ $_kcxt =~ ^gke ]] && _kcxt="$(sed -rn 's|^gke_.*_.*_(.*)(-cluster)*$|\1|p' <<< $_kcxt)"
    _KUBECTL="using ${fg_Violet}${_k8s_icon} ${bold}${_kcxt}${fg_Reset} "
  fi

  if _gitdir="$(git rev-parse --git-common-dir 2> /dev/null)"; then
    _repo="$(basename $(git config --get remote.origin.url || git rev-parse --show-toplevel) | sed 's/\.git$//')"
    vcs_info; _GIT="on ${fg_Green}${_git_icon} ${bold}${_repo}/${fg_NoColor}${vcs_info_msg_0_}${nobold}"
  fi

  case "$rc" in
    0) _prompt_color="${fg_Green}"   ;;
    1) _prompt_color="${fg_Red}"     ;;
    *) _prompt_color="${fg_Magenta}" ;;
  esac

  _prompt_line1="${_HOSTNAME}${_CWD}${_KUBECTL}${_PYENV}${_GIT}"
  _prompt_line2="${bold}${_prompt_color}%#${fg_NoColor}${nobold} "

  PS1="${eol}${_prompt_line1}${eol}${_prompt_line2}"
}

function +vi-extended-git() {
  [[ -s $(git rev-parse --show-toplevel)/.git/refs/stash ]] && hook_com[staged]+="$"
  git status --porcelain | grep -q "^?? " 2> /dev/null && hook_com[staged]+="?"
}

zstyle ':vcs_info:git*' actionformats '%F{64}%b %F{136}%u%c%m%f|%F{136}%a%f'
zstyle ':vcs_info:git*' check-for-changes true
zstyle ':vcs_info:git*' formats '%F{64}%b%f %F{136}%u%c%m%f'
zstyle ':vcs_info:git*' stagedstr '+'
zstyle ':vcs_info:git*' unstagedstr '*'
zstyle ':vcs_info:git*+set-message:*' hooks extended-git
```

----

```sh
precmd() {
  local rc=$? eol=$'\n' _gitdir _kcxt _repo _prompt_color _pyver _columns="$(( COLUMNS - 1 ))"
  local _git_icon=$'\uf407' _py_icon=$'\uf81f' _k8s_icon=$'\ufd31' _hl=$'\u2015'
  local bold="%B" nobold="%b" fg_NoColor="%f" reset="%k%b%f"
  local fg_Blue="%F{33}" bg_Blue="%K{33}" \
        fg_Cyan="%F{37}" \
        fg_Violet="%F{61}" \
        fg_Green="%F{64}" \
        fg_Magenta="%F{125}" \
        fg_Red="%F{160}" \
        fg_White="%F{252}"
  declare -A _prompt_lines

  if [[ -n $SSH_CONNECTION ]]; then
    _HOSTNAME="${bold}${fg_Magenta}$(hostname -s)${reset} in "
  else
    _HOSTNAME=""
  fi

  if [[ -n $TMUX ]]; then
    _CWD="${bold}${fg_Blue}%1~${reset} "
  else
    _CWD="${bold}${fg_Blue}%(5~|%-1~/.../%1~|%~)${reset} "
  fi

  if _kcxt="$(kubectl config current-context 2> /dev/null)"; then
    [[ $_kcxt =~ ^gke ]] && _kcxt="$(sed -rn 's|^gke_.*_.*_(.*)(-cluster)*$|\1|p' <<< $_kcxt)"
    _KUBECTL="using ${fg_Violet}${_k8s_icon} ${bold}${_kcxt}${reset} "
  else
    _KUBECTL=""
  fi

  if [[ -n "$VIRTUAL_ENV" ]]; then
    _PYENV="via ${fg_Cyan}${_py_icon} ${bold}$(python --version | grep -Eo '3\.[0-9]+')${reset} "
  else
    _PYENV=""
  fi

  if _gitdir="$(git rev-parse --git-common-dir 2> /dev/null)"; then
    _repo="$(basename -s '.git' $(git config --get remote.origin.url || git rev-parse --show-toplevel))"
    vcs_info; _GIT="on ${fg_Green}${_git_icon} ${bold}${_repo}/${fg_NoColor}${vcs_info_msg_0_}${nobold}"
  else
    _GIT=""
  fi

  case "$rc" in
    0) _prompt_color="${fg_Green}"   ;;
    1) _prompt_color="${fg_Red}"     ;;
    *) _prompt_color="${fg_Magenta}" ;;
  esac

  _prompt_lines=(
    [1]="${eol}${fg_White}$(printf %.1s $_hl{1..$COLUMNS})${fg_NoColor}"
    [2]="${eol}${_HOSTNAME}${_CWD}${_KUBECTL}${_PYENV}${_GIT}"
    [3]="${eol}${bold}${_prompt_color}%#${fg_NoColor}${nobold} "
  )

  PS1="${_prompt_lines[1]}${_prompt_lines[2]}${_prompt_lines[3]}"
}

+vi-extended-git() {
  if [[ -s $(git rev-parse --show-toplevel)/.git/refs/stash ]]; then hook_com[staged]+="$"; fi
  if git status --porcelain | grep -q "^?? " 2> /dev/null; then hook_com[staged]+="?"; fi
}

zstyle ':vcs_info:git*' actionformats '%F{64}%b %F{136}%u%c%m%f|%F{136}%a%f'
zstyle ':vcs_info:git*' check-for-changes true
zstyle ':vcs_info:git*' formats '%F{64}%b%f %F{136}%u%c%m%f'
zstyle ':vcs_info:git*' stagedstr '+'
zstyle ':vcs_info:git*' unstagedstr '*'
zstyle ':vcs_info:git*+set-message:*' hooks extended-git
```sh
