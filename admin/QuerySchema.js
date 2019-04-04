// Get the table schema for a table from Postgres
// cscript //nologo admin\QuerySchema.js <database> <app> <table>
try
    {
    if (WScript.Arguments.length)
        {
        var Database=WScript.Arguments(0);
        var App=WScript.Arguments(1);
        var Table=WScript.Arguments(2);
        var adOpenStatic=3;
        var adLockUnspecified=-1;
        var adCmdText=1;
        var Connection=new ActiveXObject('ADODB.Connection');
        Connection.Open('Driver={PostgreSQL Unicode(x64)};Server=localhost;Port=5432;Database='+Database+';Uid=postgres;Pwd=postgres;');
        var Recordset=new ActiveXObject('ADODB.Recordset');
        var SQL="select xmlelement(name column_list, xmlagg(xmlelement(name column, xmlattributes(column_name,data_type,character_maximum_length)) order by column_name)) from information_schema.columns where table_name='"+App+"_"+Table+"' and column_name not in ('id','uuid','saved_on','saved_by')";
        Recordset.Open(SQL,Connection,adOpenStatic,adLockUnspecified,adCmdText);
        while (!Recordset.EOF) 
            {
            if (Recordset.Fields(0).Value != undefined) 
                {
                //WScript.Echo(Recordset.Fields(0).Value);
                var Writer=new ActiveXObject('Msxml2.MXXMLWriter.6.0');
                Writer.indent=true;
                Writer.encoding='utf-8';
                Writer.omitXMLDeclaration=true;
                var Reader=new ActiveXObject('Msxml2.SAXXMLReader.6.0');
                Reader.contentHandler=Writer
                Reader.parse(Recordset.Fields(0).Value);
                WScript.Echo('<?xml version="1.0" encoding="utf-8" standalone="no"?>\n'+Writer.output); // Add utf-8 to declaration
                }
            Recordset.MoveNext();
            }
        Recordset.Close();
        Recordset=null;
        Connection.Close();
        Connection=null;
        }
    }
catch (e)
    {
    WScript.Echo('Error in script: '+e.description);
    }
