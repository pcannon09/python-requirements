# NOTE: Make sure to have `pyinstaller` installed

if [[ "$1" == "" ]]; then
    compileFiles=(
        "main.py"
        "File.py"
        "Debug.py"
        "ReqInfo.py"
    )

    compileFilesStr=""

    for compileFilesIt in "${compileFiles[@]}"; do
        compileFilesStr+="${compileFilesIt} "
    done

    echo "Files to compile: $compileFilesStr"

    if [ -e "./python/build" ]; then
        rm -rf ./python/build
    fi

    if [ -e "./python/dist" ]; then
        rm -rf ./python/dist
    fi

    mkdir python

    cd python

    pyinstaller --onefile $compileFilesStr

    mv ./dist/main ./dist/py-req

    cd ..

    mkdir -p bin

    mv ./python/dist/py-req ./bin/

    rm -rf ./python/dist/ ./python/build/ ./python/main.spec
fi

