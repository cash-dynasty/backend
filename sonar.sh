#!/usr/bin/env bash
set -eo pipefail

CONTAINER_NAME='sonar-scanner'
SONARQUBE_HOST='http://localhost:9000'
SONARQUBE_TOKEN='squ_40432f810d96f113d9e67818924c49141066f329'

docker stop "${CONTAINER_NAME}"
docker rm "${CONTAINER_NAME}"
docker run --name "${CONTAINER_NAME}" \
    --network host \
    -v .:/usr/src \
    sonarsource/sonar-scanner-cli:5.0 \
    sonar-scanner \
        -Dsonar.host.url="${SONARQUBE_HOST}" \
        -Dsonar.token="${SONARQUBE_TOKEN}" \
        -Dsonar.projectKey=backend \
        -Dsonar.projectName="Cash Dynasty / backend" \
        -Dsonar.sources=app/ \
        -Dsonar.inclusions=**/*.py \
        -Dsonar.tests=tests/ \
        -Dsonar.plugins.downloadOnlyRequired=true \
        -Dsonar.sourceEncoding=UTF-8 \
        -Dsonar.python.version=3.10,3.11,3.12 \
        -Dsonar.python.coverage.reportPaths=coverage.xml
