if [[ "$1" == "--ungen" ]]; then
    echo "[ WARN ] Are you sure that you want to remove every generated file and dir? (CTRL + C to cancel, return to continue)"

    read

    printf "[ DELETE ] Deleting dir \`.private\` "; rm -rf ./.private ; echo "[ DONE ]"
fi

printf "[ CREATE ] Creating \`.private/logs\` dir " ; mkdir -p .private/logs ; echo "[ DONE ]"
