:: %1 is app e.g. demo
:: %2 is table e.g. person
cscript //nologo admin\QuerySchema.js %DATABASE% %1 %2 >app\sql\%1.%2.xml
msxsl app\sql\%1.%2.xml admin\PostgresFunctions.xslt type=save app=%1 table=%2 >app\sql\%1.%2Save.sql
msxsl app\sql\%1.%2.xml admin\PostgresFunctions.xslt type=remove app=%1 table=%2 >app\sql\%1.%2Remove.sql
msxsl app\sql\%1.%2.xml admin\PythonFunctions.xslt app=%1 table=%2 >>app\python\%1\%2Query.py
