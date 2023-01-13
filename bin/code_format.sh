if [ $# -lt 1 ];then
    echo "Usage : code_format.sh [folder/file]"
    exit
fi


isort --multi-line 7 --profile black $1
black --skip-string-normalization --line-length 200 $1
