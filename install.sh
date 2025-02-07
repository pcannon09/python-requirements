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

    rm -rf ./python/build
    rm -rf ./python/dist

    cd python

    pyinstaller --onefile $compileFilesStr

    mv ./dist/main ./dist/py-req

    cd ..

    mkdir -p bin

    mv ./python/dist/py-req ./bin/

elif [[ "$1" == "run" ]]; then
    ./python/dist/main/py-req "$2"
fi

