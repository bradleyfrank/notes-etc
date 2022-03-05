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
