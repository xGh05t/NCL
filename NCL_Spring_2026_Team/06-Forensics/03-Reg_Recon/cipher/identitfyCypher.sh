for nv in \
  "Token:IAbqoNjPktNncGsuyWztR+gmwzno6BSrEMk1ydkaOEI=" \
  "SessionId:+vKsMxVwi7+pXMRz" \
  "Upload:z52WCARnmTq/urIdoGXYQxjscCyMZf0SpOzoNj9edVTiCw==" ; do
  n="${nv%%:*}"; b="${nv#*:}"
  s=$(echo -n "$b" | base64 -d | wc -c)
  echo "$n = $s bytes"
done
