#!/usr/bin/env bash
pushd () {
    command pushd "$@" > /dev/null
}

popd () {
    command popd "$@" > /dev/null
}

pushd ./app/
uvicorn main:app --reload
popd
