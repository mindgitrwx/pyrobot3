# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
  export ZSH="/home/jonghyeon/.oh-my-zsh"

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="robbyrussell"

# Set list of themes to load
# Setting this variable when ZSH_THEME=random
# cause zsh load theme from this variable instead of
# looking in ~/.oh-my-zsh/themes/
# An empty array have no effect
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
  git
)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
#
# ---------------------------------------------------------------------

# User setting


bindkey -v
bindkey '^R' history-incremental-search-backward

alias ohmyzsh="mate ~/.oh-my-zsh"
cd() {
    builtin cd "$@" && ls -lA
}

alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

alias sourcerc='source ~/.zshrc'
alias bashrc='vim ~/.bashrc'
alias zshrc='vim ~/.zshrc'
alias vimrc='vim ~/.vimrc'
alias nvimrc='nvim /home/jonghyeon/.config/nvim/init.vim'

alias Grep='grep'
alias gerp='grep'

alias copy='xclip -sel clip'
alias setclip="xclip -selection c"
alias getclip="xclip -selection c -o"
alias ..='cd ..'
alias ...='cd ../..'
alias down='cd ~/Downloads'

# FROM https://wiki.kldp.org/HOWTO/html/Adv-Bash-Scr-HOWTO/sample-bashrc.html
alias h='history'
alias r='rlogin'
alias which='type -all'
alias path='echo -e ${PATH//:/\\n}'
#alias print='/usr/bin/lp -o nobanner -d $LPDEST'   # LPDEST 가 정의되어 있다고 가정
#alias pjet='enscript -h -G -fCourier9 -d $LPDEST'  # enscript 로 예쁜 출력하기(Pretty-print)
#alias background='xv -root -quit -max -rmode 5' # 백그라운드 배경 그림
alias vi='vim'
alias du='du -h'
alias df='df -kh'

alias run='python3 /ROBOT/pyrobot/bin/pyrobot.py'
alias run2='python /ROBOT_DEFALT_2/pyrobot/bin/pyrobot.py'
# 'ls' 그룹(여러분이 GNU ls 를 쓴다고 가정)
alias ls='ls -hF --color' # 파일타입 인식을 위해 색깔을 추가
alias lx='ls -lXB' # 확장자별로 정렬
alias lk='ls -lSr' # 크기별로 정렬
alias la='ls -Al' # 숨겨진 파일 보기
alias lr='ls -lR' # 재귀적 ls
alias lt='ls -ltr' # 날짜별로 정렬
alias lm='ls -al |more' # 'more'로 파이프 걸기
alias tree='tree -Cs' # 'ls'의 멋진 대용품


function ff() { find . -name '*'$1'*' ; }                 # 파일 찾기
function fe() { find . -name '*'$1'*' -exec $2 {} \; ; }  # 파일을 찾아서 $2 의 인자로 실행

function fstr() # 여러 파일중에서 문자열 찾기
{
    if [ "$#" -gt 2 ]; then
        echo "Usage: fstr \"pattern\" [files] "
        return;
    fi
    SMSO=$(tput smso)
    RMSO=$(tput rmso)
    find . -type f -name "${2:-*}" -print | xargs grep -sin "$1" | \
sed "s/$1/$SMSO$1$RMSO/gI"
}

function cuttail() # 파일에서 끝의 n 줄을 잘라냄. 기본값은 10
{
    nlines=${2:-10}
    sed -n -e :a -e "1,${nlines}!{P;N;D;};N;ba" $1
}

function lowercase()  # 파일이름을 소문자로 변경
{
    for file ; do
        filename=${file##*/}
        case "$filename" in
        */*) dirname==${file%/*} ;;
        *) dirname=.;;
        esac
        nf=$(echo $filename | tr A-Z a-z)
        newname="${dirname}/${nf}"
        if [ "$nf" != "$filename" ]; then
            mv "$file" "$newname"
            echo "lowercase: $file --> $newname"
        else
            echo "lowercase: $file not changed."
        fi
    done
}
function uppercase()  # 파일이름을 소문자로 변경
{
    for file ; do
        filename=${file##*/}
        case "$filename" in
        */*) dirname==${file%/*} ;;
        *) dirname=.;;
        esac
        nf=$(echo $filename | tr a-z A-Z)
        newname="${dirname}/${nf}"
        if [ "$nf" != "$filename" ]; then
            mv "$file" "$newname"
            echo "lowercase: $file --> $newname"
        else
            echo "lowercase: $file not changed."
        fi
    done
}
function swap()         # 파일이름 두개를 서로 바꿈
{
    local TMPFILE=tmp.$$
    mv $1 $TMPFILE
    mv $2 $1
    mv $TMPFILE $2
}


# end of kldp
#-----------------------------------
# 프로세스/시스템 관련 함수들:
#-----------------------------------

function my_ps() { ps $@ -u $USER -o pid,%cpu,%mem,bsdtime,command ; }
function pp() { my_ps f | awk '!/awk/ && $0~var' var=${1:-".*"} ; }

# 이 함수는 리눅스의 'killall' 스크립트와 거의 비슷하지만
# 솔라리스에는, 제가 아는 한, 이와 비슷한 것이 없습니다.
function killps()   # 프로세스 이름으로 kill
{
    local pid pname sig="-TERM"   # 기본 시그널
    if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then 
	echo "Usage: killps [-SIGNAL] pattern"
	return;
    fi
    if [ $# = 2 ]; then sig=$1 ; fi
    for pid in $(my_ps| awk '!/awk/ && $0~pat { print $1 }' pat=${!#} ) ; do
	pname=$(my_ps | awk '$1~var { print $5 }' var=$pid )
	if ask "Kill process $pid <$pname> with signal $sig?"
	    then kill $sig $pid
	fi
    done
}

function my_ip() # IP 주소 알아내기
{
    MY_IP=$(/sbin/ifconfig ppp0 | awk '/inet/ { print $2 } ' | sed -e s/addr://)
    MY_ISP=$(/sbin/ifconfig ppp0 | awk '/P-t-P/ { print $3 } ' | sed -e s/P-t-P://)
}

function ii()   # 현재 호스트 관련 정보들 알아내기
{
    echo -e "\nYou are logged on ${RED}$HOST"
    echo -e "\nAdditionnal information:$NC " ; uname -a
    echo -e "\n${RED}Users logged on:$NC " ; w -h
    echo -e "\n${RED}Current date :$NC " ; date
    echo -e "\n${RED}Machine stats :$NC " ; uptime
    echo -e "\n${RED}Memory stats :$NC " ; free
    my_ip 2>&- ;
    echo -e "\n${RED}Local IP Address :$NC" ; echo ${MY_IP:-"Not connected"}
    echo -e "\n${RED}ISP Address :$NC" ; echo ${MY_ISP:-"Not connected"}
    echo
}


# 기타 유틸리티:

function repeat()       # 명령어를 n 번 반복
{
    local i max
    max=$1; shift;
    for ((i=1; i <= max ; i++)); do  # --> C 형태의 문법
        eval "$@";
    done
}


function ask()
{
    echo -n "$@" '[y/n] ' ; read ans
    case "$ans" in
        y*|Y*) return 0 ;;
        *) return 1 ;;
    esac
}

set -o vi
set bind -m vi-insert "\C-l":clear-screen

export EDITOR=nvim

logger() {
    local message="$1"
    local mode="$2"
    case "$mode" in
        0)
            echo "$message"
            ;;
        1)
            echo "$message" > "$LOG_FILE_DIRECTORY_PATH$LOG_FILE_NAME"
            echo
            ;;
    esac
}

#how(){
#    howdoi "$0" | setclip;
#}
###
#python() {
#    python "$0" | setclip;
#}
###
cd() {
    builtin cd "$@" && ls -lA
}

getnews () {
  curl https://newsapi.org/v2/top-headlines -s -G \
    -d sources=$1 \
    -d apiKey=noapikeyforyou \
    | jq '.articles[] | .title'
}

startmyday () {
  echo "good morning, jonghyeon."
  echo "\nUpdating Homebrew..."
  brew update && brew upgrade
  echo "The weather right now:"
  ansiweather

  #echo "\nNews from the BBC:"
  #getnews bbc-news
  #echo "\nNews from the Washington Post:"
  #getnews the-washington-post
  #echo "\nNews from Hacker News:"
  #getnews hacker-news
}


