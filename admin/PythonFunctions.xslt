<?xml version='1.0' encoding='UTF-8' ?><!--msxsl app\sql\%1.%2.xml admin\PythonFunctions.xslt app=%1 table=%2 >>app\python\%1\%2Query.py-->
<xsl:stylesheet version='1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
  <xsl:output method='text' encoding='utf-8' indent='yes'/><!--encoding='utf-8'-->
  <xsl:param name='app'/>
  <xsl:param name='table'/>
  <xsl:param name='parent_table'/> <!--For foreign key relationships-->
  <xsl:variable name='links' select='concat(translate(substring($table, 1, 1),"abcdefghijklmnopqrstuvwxyz","ABCDEFGHIJKLMNOPQRSTUVWXYZ"),substring($table,2,string-length($table)-1))'/> <!--Capitalise-->

  <xsl:template match='/column_list'>
    <xsl:text>            sqlStatement = ""&#xa;</xsl:text>
    <xsl:apply-templates select='column[./@column_name != concat($parent_table,"_id")]' mode='args'/>
    <xsl:text>            sqlStatement = u"select </xsl:text><xsl:value-of select='$app'/><xsl:text>_save_</xsl:text>
    <xsl:value-of select='$table'/>
    <xsl:text>(%s, %d, </xsl:text>
    <xsl:choose>
      <xsl:when test='string-length($parent_table) > 0'>
        <xsl:text>%d, </xsl:text>
      </xsl:when>
      <xsl:otherwise>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='string-length($links) > 0'>
        <xsl:text>%s, </xsl:text>
      </xsl:when>
      <xsl:otherwise>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:text>%s)"%(&#xa;</xsl:text>
    <xsl:text>                self.ParseValue(user),&#xa;</xsl:text>
    <xsl:text>                self.ParseValue(</xsl:text><xsl:value-of select='$table'/><xsl:text>_id),&#xa;</xsl:text>
    <xsl:choose>
      <xsl:when test='string-length($parent_table) > 0'>
        <xsl:text>                self.ParseValue(</xsl:text><xsl:value-of select='$parent_table'/><xsl:text>_id),&#xa;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='string-length($links) > 0'>
        <xsl:text>                links,&#xa;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:text>                sqlStatement&#xa;</xsl:text>
    <xsl:text>                )&#xa;&#xa;</xsl:text>
    <xsl:text>            sqlStatement = u"select </xsl:text><xsl:value-of select='$app'/><xsl:text>_remove_</xsl:text>
    <xsl:value-of select='$table'/>
    <xsl:text>(%s, %d)"%(&#xa;</xsl:text>
    <xsl:text>                self.ParseValue(user),&#xa;</xsl:text>
    <xsl:text>                self.ParseValue(</xsl:text><xsl:value-of select='$table'/><xsl:text>_id),&#xa;</xsl:text>
    <xsl:text>                )&#xa;&#xa;</xsl:text>
  </xsl:template>

  <xsl:template match='column[@column_name!="id" and @column_name!="uuid" and @column_name!="saved_by" and @column_name!="saved_on"]' mode='args'>
    <xsl:text>            sqlStatement += unicode(self.ParseValue(</xsl:text><xsl:value-of select='$table'/><xsl:text>[u'</xsl:text><xsl:value-of select='./@column_name'/><xsl:text>']))&#xa;</xsl:text>
    <xsl:choose>
      <xsl:when test='(following-sibling::*)'>
        <xsl:text>            sqlStatement += ", "&#xa;</xsl:text>
      </xsl:when>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>

