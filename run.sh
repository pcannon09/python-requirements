if [ $# -eq 0 ]; then
    python3 ./python/main.py --path ./tests/.requirements
else
    python3 ./python/main.py "$@"
fi

