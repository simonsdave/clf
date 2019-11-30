#!/usr/bin/env bash

#
# Usage Examples
#
#   Usual running of spiders
#
#       ./run-sample.sh xe_exchange_rates
#       ./run-sample.sh pypi "${PYPI_USERNAME}" "${PYPI_PASSWORD}"
#       ./run-sample.sh pythonwheels
#
#   Debugging
#
#       ./run-sample.sh --verbose xe_exchange_rates
#       ./run-sample.sh --debug xe_exchange_rates
#

copy_debug_files_from_container_to_host() {
    DOCKER_CONTAINER_NAME=${1:-}
    SPIDER_OUTPUT=${2:-}
    KEY=${3:-}
    SPIDER_OUTPUT_ARTIFACT_DIR=${4:-}
    HOST_FILENAME=${5:-}

    DEBUG_FILE_IN_CONTAINER=$(jq -r "._debug.${KEY}" "${SPIDER_OUTPUT}" | sed -e "s|null||g")
    if [ ! "${DEBUG_FILE_IN_CONTAINER}" == "" ]; then
        DEBUG_FILE_ON_HOST=${SPIDER_OUTPUT_ARTIFACT_DIR}/${HOST_FILENAME}

        docker container cp \
            "${DOCKER_CONTAINER_NAME}:${DEBUG_FILE_IN_CONTAINER}" \
            "${DEBUG_FILE_ON_HOST}"

        sed -i "" -e "s|${DEBUG_FILE_IN_CONTAINER}|${DEBUG_FILE_ON_HOST}|" "${SPIDER_OUTPUT}"
    fi

    return 0
}

usage() {
    echo "usage: $(basename "$0") [--verbose|--debug] <spider> [<arg1> <arg2> ... <argN>]" >&2
    return 0
}

VERBOSE=0
CLF_DEBUG=''

echo_if_verbose() {
    if [ "1" -eq "${VERBOSE:-0}" ]; then
        echo "$@"
    fi
    return 0
}

while true
do
    case "${1:-}" in
        --verbose)
            shift
            # can only use --verbose or --debug command line option
            if [ "1" -eq "${VERBOSE:-}" ]; then
                usage
                exit 1
            fi
            VERBOSE=1
            ;;
        --debug)
            shift
            # can only use --verbose or --debug command line option
            if [ "1" -eq "${VERBOSE:-}" ]; then
                usage
                exit 1
            fi
            VERBOSE=1
            CLF_DEBUG=DEBUG
            ;;
        --help)
            shift
            usage
            exit 0
            ;;
        *)
            break
            ;;
    esac
done

if [ $# -lt 1 ]; then
    usage
    exit 1
fi

SPIDER=${1:-}
shift

# export CLF_REMOTE_CHROMEDRIVER=http://host.docker.internal:9515
# https://docs.docker.com/docker-for-mac/networking/
NETWORK=bridge
if [ ! "${CLF_REMOTE_CHROMEDRIVER:-}" == "" ]; then NETWORK=host; fi

DOCKER_CONTAINER_NAME=$(python -c "import uuid; print uuid.uuid4().hex")

SPIDER_OUTPUT_ARTIFACT_DIR=$(mktemp -d 2> /dev/null || mktemp -d -t DAS)
echo_if_verbose "Spider output artifact directory @ '${SPIDER_OUTPUT_ARTIFACT_DIR}'"

SPIDER_OUTPUT=${SPIDER_OUTPUT_ARTIFACT_DIR}/spider-output.json

docker run \
    --name "${DOCKER_CONTAINER_NAME}" \
    --security-opt seccomp:unconfined \
    --volume "$(repo-root-dir.sh):/app" \
    -e "CLF_REMOTE_CHROMEDRIVER=${CLF_REMOTE_CHROMEDRIVER:-}" \
    -e "CLF_DEBUG=${CLF_DEBUG:-}" \
    "--network=${NETWORK}" \
    "${DEV_ENV_DOCKER_IMAGE}" \
    "/app/$(repo.sh -u)/samples/${SPIDER}.py" "$@" >& "${SPIDER_OUTPUT}"

copy_debug_files_from_container_to_host \
    "${DOCKER_CONTAINER_NAME}" \
    "${SPIDER_OUTPUT}" \
    'spiderLog' \
    "${SPIDER_OUTPUT_ARTIFACT_DIR}" \
    'spider-log.txt'

copy_debug_files_from_container_to_host \
    "${DOCKER_CONTAINER_NAME}" \
    "${SPIDER_OUTPUT}" \
    'chromeDriverLog' \
    "${SPIDER_OUTPUT_ARTIFACT_DIR}" \
    'chromedriver-log.txt'

docker container rm "${DOCKER_CONTAINER_NAME}" > /dev/null

cat "${SPIDER_OUTPUT}"

exit 0
