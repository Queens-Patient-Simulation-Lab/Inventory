#!/bin/bash

# ARG_OPTIONAL_BOOLEAN([watch],[],[Watches for changes in frontend files])
# ARG_OPTIONAL_BOOLEAN([production],[],[production build])
# ARG_HELP([Builds the frontend])
# ARGBASH_GO()
# needed because of Argbash --> m4_ignore([
### START OF CODE GENERATED BY Argbash v2.8.1 one line above ###
# Argbash is a bash code generator used to get arguments parsing right.
# Argbash is FREE SOFTWARE, see https://argbash.io for more info
# Generated online by https://argbash.io/generate


die()
{
	local _ret=$2
	test -n "$_ret" || _ret=1
	test "$_PRINT_HELP" = yes && print_help >&2
	echo "$1" >&2
	exit ${_ret}
}


begins_with_short_option()
{
	local first_option all_short_options='h'
	first_option="${1:0:1}"
	test "$all_short_options" = "${all_short_options/$first_option/}" && return 1 || return 0
}

# THE DEFAULTS INITIALIZATION - OPTIONALS
_arg_watch="off"
_arg_production="off"


print_help()
{
	printf '%s\n' "Builds the frontend"
	printf 'Usage: %s [--watch] [--production] [-h|--help]\n' "$0"
	printf '\t%s\n' "--watch: Watches for changes in frontend files (off by default)"
	printf '\t%s\n' "--production: production build (debug by default)"
	printf '\t%s\n' "-h, --help: Prints help"
}


parse_commandline()
{
	while test $# -gt 0
	do
		_key="$1"
		case "$_key" in
			--watch)
				_arg_watch="on"
				test "${1:0:5}" = "--no-" && _arg_watch="off"
				;;
			--production)
				_arg_production="on"
				test "${1:0:5}" = "--no-" && _arg_production="off"
				;;
			-h|--help)
				print_help
				exit 0
				;;
			-h*)
				print_help
				exit 0
				;;
			*)
				_PRINT_HELP=yes die "FATAL ERROR: Got an unexpected argument '$1'" 1
				;;
		esac
		shift
	done
}

parse_commandline "$@"

# OTHER STUFF GENERATED BY Argbash

### END OF CODE GENERATED BY Argbash (sortof) ### ])
# [ <-- needed because of Argbash

webpack_options=""
if [ "$_arg_watch" == "on" ]; then
    trap 'jobs -p | xargs kill' EXIT
    ./build-email.sh --watch &
    webpack_options+="--watch "
else
    ./build-email.sh
fi

if [ "$_arg_production" == "on" ]; then
    webpack_options+="--mode=production"
fi
./node_modules/.bin/webpack $webpack_options --config webpack.config.js

# ] <-- needed because of Argbash
