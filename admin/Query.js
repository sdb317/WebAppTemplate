// Get the table schema for a table from Postgres
// cscript //nologo admin\Query.js <database> <sql> <delimiter> <wrapper>
try
    {
    var adOpenStatic=3;
    var adLockUnspecified=-1;
    var adCmdText=1;
    var adPosEOF=-3;
    if (WScript.Arguments.length>0)
        {
        var Database=WScript.Arguments(0);
        var Connection=new ActiveXObject('ADODB.Connection');
        Connection.Open('Driver={PostgreSQL Unicode(x64)};Server=localhost;Port=5432;Database=' + Database + ';Uid=postgres;Pwd=postgres;');
        if (Connection.State)
            {
            var SQL='';
            if (WScript.Arguments.length>1)
                SQL=WScript.Arguments(1);
            var Delimiter='';
            if (WScript.Arguments.length>2)
                Delimiter=WScript.Arguments(2);
            var Wrapper='';
            if (WScript.Arguments.length>3)
                Wrapper=WScript.Arguments(3);
            if (SQL.length) {
                var Recordset=new ActiveXObject('ADODB.Recordset');
                Recordset.Open(SQL,Connection,adOpenStatic,adLockUnspecified,adCmdText);
                var i=0;
                while (!Recordset.EOF)
                    {
                    var Row='';
                    var j=0;
                    while (j < Recordset.Fields.Count)
                        {
                        if (j>0)
                            Row+='\t';
                        if (Recordset.Fields(j).Value!=undefined)
                            Row+=Recordset.Fields(j).Value.toString();
                        j++;
                        }
                    if (Delimiter.length)
                        {
                        if (Wrapper.length)
                            {
                            WScript.Echo(Wrapper.replace(/<body>/g,Row.replace(/\t/g,Delimiter)));
                            }
                        else
                            {
                            WScript.Echo(Row.replace(/\t/g,Delimiter));
                            }
                        }
                    else
                        {
                        WScript.Echo(Row);
                        }
                    Recordset.MoveNext();
                    i++;
                    }
                Recordset.Close();
                Recordset=null;
                }
            Connection.Close();
            Connection=null;
            }
        }
    else
        {
        WScript.Echo('No \'DB\' specified');
        }
    }
catch (e)
    {
    WScript.Echo('Error in script: ' + e.description);
    }
