# ZSH Theme emulating the Fish shell's default prompt.

_fishy_collapsed_wd() {
  echo $(pwd | perl -pe '
   BEGIN {
      binmode STDIN,  ":encoding(UTF-8)";
      binmode STDOUT, ":encoding(UTF-8)";
   }; s|^$ENV{HOME}|~|g; s|/([^/.])[^/]*(?=/)|/$1|g; s|/\.([^/])[^/]*(?=/)|/.$1|g
')
}

# Conda info
conda_prompt_info() {
  if [ -n "$CONDA_DEFAULT_ENV" ]; then
    echo -n "($CONDA_DEFAULT_ENV) "
  else 
    echo -n "(base) "
  fi
}


local user_color='green'; [ $UID -eq 0 ] && user_color='red'
PROMPT='%n@%m%{$fg[green]%}$(conda_prompt_info)%{$fg[$user_color]%}$(_fishy_collapsed_wd)%{$reset_color%}%(!.#.>) '
#PROMPT2='%{$fg[red]%}\ %{$reset_color%}'

local return_status="%{$fg_bold[red]%}%(?..%?)%{$reset_color%}"
#RPROMPT="${RPROMPT}"'${return_status}$(git_prompt_info)$(git_prompt_status)%{$reset_color%}'

RPROMPT='${ret_status} %{$fg[blue]%}$(git_current_branch)%{$reset_color%}'

ZSH_THEME_GIT_PROMPT_PREFIX=" "
ZSH_THEME_GIT_PROMPT_SUFFIX=""
ZSH_THEME_GIT_PROMPT_DIRTY=""
ZSH_THEME_GIT_PROMPT_CLEAN=""

ZSH_THEME_GIT_PROMPT_ADDED="%{$fg_bold[green]%}+"
ZSH_THEME_GIT_PROMPT_MODIFIED="%{$fg_bold[blue]%}!"
ZSH_THEME_GIT_PROMPT_DELETED="%{$fg_bold[red]%}-"
ZSH_THEME_GIT_PROMPT_RENAMED="%{$fg_bold[magenta]%}>"
ZSH_THEME_GIT_PROMPT_UNMERGED="%{$fg_bold[yellow]%}#"
ZSH_THEME_GIT_PROMPT_UNTRACKED="%{$fg_bold[cyan]%}?"
