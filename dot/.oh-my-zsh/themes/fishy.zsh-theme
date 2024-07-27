# ZSH Theme emulating the Fish shell's default prompt.

# 定义一个函数 _fishy_collapsed_wd，用于将当前工作目录（pwd）进行压缩显示。
_fishy_collapsed_wd() {
  echo $(pwd | perl -pe '
   BEGIN {
      binmode STDIN,  ":encoding(UTF-8)";
      binmode STDOUT, ":encoding(UTF-8)";
   }; s|^$ENV{HOME}|~|g; s|/([^/.])[^/]*(?=/)|/$1|g; s|/\.([^/])[^/]*(?=/)|/.$1|g
')
}

# Conda info
# 定义一个函数 conda_prompt_info，用于在提示符中显示当前 Conda 环境名称。如果激活了某个 Conda 环境，则显示该环境名称；否则显示 (base)。
conda_prompt_info() {
  if [ -n "$CONDA_DEFAULT_ENV" ]; then
    echo -n "($CONDA_DEFAULT_ENV) "
  else 
    echo -n "(base) "
  fi
}

# local PR_USER PR_USER_OP PR_PROMPT PR_HOST

# Check the UID
# 检查用户的 UID（用户 ID）。 对root用户和普通用户设置不同的颜色
if [[ $UID -ne 0 ]]; then # normal user
  PR_USER='%F{cyan}%n%f'
  PR_USER_OP='%F{cyan}@%f'
  PR_PROMPT='%f➤ %f'
else # root
  PR_USER='%F{red}%n%f'
  PR_USER_OP='%F{red}@%f'
  PR_PROMPT='%F{red}➤ %f'
fi


# Check if we are on SSH or not
# 检查是否通过 SSH 连接。 如果是通过 SSH 连接（存在 SSH_CLIENT 或 SSH2_CLIENT 环境变量），则：PR_HOST 设置为红色的主机名。否则（本地终端），则：PR_HOST 设置为青色的主机名。
if [[ -n "$SSH_CLIENT"  ||  -n "$SSH2_CLIENT" ]]; then
  PR_HOST='%F{red}%M%f' # SSH
else
  PR_HOST='%F{cyan}%M%f' # no SSH
fi

# 定义 PROMPT 变量，设置提示符的格式：
local user_color='green'; [ $UID -eq 0 ] && user_color='red'
PROMPT='${PR_USER}${PR_USER_OP}${PR_HOST} %{$fg[$user_color]%}$(_fishy_collapsed_wd)%{$reset_color%}%(!.#.>) '
#PROMPT2='%{$fg[red]%}\ %{$reset_color%}'

# local return_status="%{$fg_bold[red]%}%(?..%?)%{$reset_color%}"
#RPROMPT="${RPROMPT}"'${return_status}$(git_prompt_info)$(git_prompt_status)%{$reset_color%}'

#定义 RPROMPT 变量，设置右侧提示符的格式：
RPROMPT='${ret_status} %{$fg[blue]%}$(git_current_branch)%{$reset_color%}'

#定义 Git 提示符的前缀、后缀、未清空状态和清空状态，分别为空字符串。
ZSH_THEME_GIT_PROMPT_PREFIX=" "
ZSH_THEME_GIT_PROMPT_SUFFIX=""
ZSH_THEME_GIT_PROMPT_DIRTY=""
ZSH_THEME_GIT_PROMPT_CLEAN=""

#定义 Git 提示符中不同状态的符号和颜色：
ZSH_THEME_GIT_PROMPT_ADDED="%{$fg_bold[green]%}+"
ZSH_THEME_GIT_PROMPT_MODIFIED="%{$fg_bold[blue]%}!"
ZSH_THEME_GIT_PROMPT_DELETED="%{$fg_bold[red]%}-"
ZSH_THEME_GIT_PROMPT_RENAMED="%{$fg_bold[magenta]%}>"
ZSH_THEME_GIT_PROMPT_UNMERGED="%{$fg_bold[yellow]%}#"
ZSH_THEME_GIT_PROMPT_UNTRACKED="%{$fg_bold[cyan]%}?"
