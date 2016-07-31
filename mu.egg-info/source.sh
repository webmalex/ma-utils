_mu_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _MU_COMPLETE=complete $1 ) )
    return 0
}

complete -F _mu_completion -o default mu;
