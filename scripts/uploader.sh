#!/usr/bin/env bash


# INIT GLOBAL VARIABLES:
_VERSION="0.1.0"
_PACKGMGR="apt yum"
_SCRIPT_NAME="$0"
_CMD="curl"
_FILE=""
_TOKEN=""
_URL=""


# Colorize output
# Usage - $(colorize CYAN "Hello, friend!")
colorize() {
	local RED="\033[0;31m"
	local GREEN="\033[0;32m"  # <-- [0 means not bold
	local YELLOW="\033[1;33m" # <-- [1 means bold
	local BLUE="\033[0;34m"
	local MAGNETA="\033[0;35"
	local CYAN="\033[1;36m"
	# ... Add more colors if you like

	local NC="\033[0m" # No Color

	# printf "${(P)1}${2} ${NC}\n" # <-- zsh
	# printf "${!1}${2} ${NC}\n"   # <-- bash
	echo -e "${!1}${2}${NC}"       # <-- all-purpose
}


# checks whether the utility is installed
# takes the util name as input $_CMD
check_util_exists() {
	local request_util=$1
	if ! command -v $request_util >/dev/null; then
		return 1
	fi
}


# Print help message how used it script
help() {
	local script=$(colorize GREEN "$_SCRIPT_NAME")
	local required=$(colorize RED "required")
	printf "Usage: $script [options [parameters]]\n"
	printf "\n"
	printf "Options:\n"
	printf "\n"
	printf " -f | --file     full path to upload file $required\n"
	printf " -t | --token    access token             $required\n"
	printf " -u | --url      target url               $required\n"
	printf " -v | --version  print version\n"
	printf " -h | --help     print help\n"
}


# parse user arguments
argparser() {
	# count user-passed arguments:
	local count_arguments=$#
	# run help if empty and exit:
	if [[ count_arguments -eq 0 ]]; then
		help
		exit 2
	fi
	# parse args:
	while [ ! -z "$1" ]; do
		case "$1" in
			--file|-f)
				shift
				_FILE="$1"
				;;
			--token|-t)
				shift
				_TOKEN="$1"
				;;
			--url|-u)
				shift
				_URL="$1"
				;;
			--help|-h)
				help
				exit 0
				;;
			--version|-v)
				printf "$_VERSION\n"
				exit 0
				;;
			*)
				help
				exit 2
				;;
		esac
	shift
	done
}


# check curl is exists:
curl_is_exists() {
	if ! check_util_exists $_CMD; then
		local error_cmd=$(colorize RED "$_CMD")
		printf  "$(colorize RED "ERROR"): upload util doesn't exist, "
		printf	"please install $error_cmd before run $_SCRIPT_NAME\n"
		# Print how install curl (support only apt/yum):
		for pkgmgr in $_PACKGMGR; do
			if check_util_exists $pkgmgr; then
				printf "$(colorize GREEN "RUN"): $pkgmgr install $error_cmd"
			fi
		done
		exit 1
	fi
}


validate_args() {
	if [[ -z $_URL ]]; then
		printf "$(colorize RED "ERROR"): -u | --url argument is required\n"
		exit 1
	fi
	if [[ -z $_FILE ]]; then
		printf "$(colorize RED "ERROR"): -f | --file argument is required\n"
		exit 1
	fi
	if [[ -z $_TOKEN ]]; then
		printf "$(colorize RED "ERROR"): -t | --token argument is required\n"
		exit 1
	fi
}


# Upload file used curl
# get $_URL $_FILE $_TOKEN
upload() {
	local url=$1
	local file=$2
	local token=$3
	# run:
	curl --progress-bar -X 'POST' \
		"${url}" \
		-H 'accept: application/json' \
		-H "Upload-Token: ${token} " \
		-H 'Content-Type: multipart/form-data' \
		-F "file=@${file}" | cat  # cat required to show progress bar
}


main () {
	argparser $@
	curl_is_exists
	validate_args
	upload $_URL $_FILE $_TOKEN	
}


# RUN IT:
main $@
