#!/bin/bash
SESSION_ID=$1
LINES=-100000

TARGET="$SESSION_ID:1.1"
OUTFILE="tmux_session_${SESSION_ID}_$(date +%Y%m%d_%H%M%S).log"

echo "Exporting session:$SESSION_ID -> pane:$TARGET → $OUTFILE ..."
tmux capture-pane -t "$TARGET" -S $LINES -p > "$OUTFILE"
echo "Done."

