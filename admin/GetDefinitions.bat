cscript//nologo admin\Query.js "%DATABASE%" "select category||label,numeric from public.%APP%__definition" "=" >app\python\%APP%\definitions.py
cscript//nologo admin\Query.js "%DATABASE%" "select category||label,numeric from public.%APP%__definition" "=" "export const <body>;" >app\js\definitions.js
