cscript//nologo admin\Query.js "%1" "select category||label,numeric from public.demo__definition" "=" >app\python\definitions.py
cscript//nologo admin\Query.js "%1" "select category||label,numeric from public.demo__definition" "=" "export const <body>;" >app\js\definitions.js
