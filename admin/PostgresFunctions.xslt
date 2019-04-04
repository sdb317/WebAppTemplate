<?xml version='1.0' encoding='UTF-8' ?>
<!--msxsl app\sql\%1.%2.xml admin\PostgresFunctions.xslt type=save app=%1 table=%2 >app\sql\%1.%2Save.sql-->
<xsl:stylesheet version='1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
  <xsl:output method='text' encoding='utf-8' indent='yes'/><!--encoding='utf-8'-->
  <xsl:param name='type'/>
  <xsl:param name='app'/>
  <xsl:param name='table'/>
  <xsl:param name='parent_table'/> <!--For foreign key relationships-->
  <xsl:variable name='links' select='concat(translate(substring($table, 1, 1),"abcdefghijklmnopqrstuvwxyz","ABCDEFGHIJKLMNOPQRSTUVWXYZ"),substring($table,2,string-length($table)-1))'/> <!--Capitalise-->

  <xsl:template match='/column_list'>
    <xsl:text>create or replace function&#xd;&#xa;</xsl:text>
    <xsl:choose>
      <xsl:when test='$type="save"'>
        <xsl:value-of select='$app'/>
        <xsl:text>_save_</xsl:text>
        <xsl:value-of select='$table'/>
        <xsl:text>&#xd;&#xa;</xsl:text>
        <xsl:text>    (&#xd;&#xa;</xsl:text>
        <xsl:text>    _saved_by varchar(256),&#xd;&#xa;</xsl:text>
        <xsl:text>    _id int,&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($parent_table) > 0'>
            <xsl:text>    _</xsl:text><xsl:value-of select='$parent_table'/><xsl:text>_id int,&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:choose>
          <xsl:when test='string-length($links) > 0'>
            <xsl:text>    _links </xsl:text><xsl:value-of select='$app'/><xsl:text>_link_type[],&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select='column[./@column_name != concat($parent_table,"_id")]' mode='arguments'/>
        <xsl:text>    )&#xd;&#xa;</xsl:text>
        <xsl:text>returns int as&#xd;&#xa;</xsl:text>
        <xsl:text>$$&#xd;&#xa;</xsl:text>
        <xsl:text>begin&#xd;&#xa;</xsl:text>
        <xsl:text>    if _id=0 then /* If it is new */&#xd;&#xa;</xsl:text>
        <xsl:text>        insert into&#xd;&#xa;</xsl:text>
        <xsl:text>            public.</xsl:text><xsl:value-of select='$app'/><xsl:text>_</xsl:text><xsl:value-of select='$table'/><xsl:text>&#xd;&#xa;</xsl:text>
        <xsl:text>                (&#xd;&#xa;</xsl:text>
        <xsl:text>                uuid,&#xd;&#xa;</xsl:text>
        <xsl:text>                saved_on,&#xd;&#xa;</xsl:text>
        <xsl:text>                saved_by,&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($parent_table) > 0'>
            <xsl:text>                </xsl:text><xsl:value-of select='$parent_table'/><xsl:text>_id,&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select='column[./@column_name != concat($parent_table,"_id")]' mode='insertColumns'/>
        <xsl:text>                )&#xd;&#xa;</xsl:text>
        <xsl:text>            values&#xd;&#xa;</xsl:text>
        <xsl:text>                (&#xd;&#xa;</xsl:text>
        <xsl:text>                (select md5(random()::text || clock_timestamp()::text)::uuid),&#xd;&#xa;</xsl:text>
        <xsl:text>                now(),&#xd;&#xa;</xsl:text>
        <xsl:text>                _saved_by,&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($parent_table) > 0'>
            <xsl:text>                _</xsl:text><xsl:value-of select='$parent_table'/><xsl:text>_id,&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select='column[./@column_name != concat($parent_table,"_id")]' mode='insertValues'/>
        <xsl:text>                );&#xd;&#xa;</xsl:text>
        <xsl:text>        _id=currval(pg_get_serial_sequence('</xsl:text><xsl:value-of select='$app'/><xsl:text>_</xsl:text><xsl:value-of select='$table'/><xsl:text>','id')); /* Get the new identity value */&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($links) > 0'>
            <xsl:text>        insert into /* Add new links */&#xd;&#xa;</xsl:text>
            <xsl:text>            public.</xsl:text><xsl:value-of select='$app'/><xsl:text>__link&#xd;&#xa;</xsl:text>
            <xsl:text>                (&#xd;&#xa;</xsl:text>
            <xsl:text>                entity_type,&#xd;&#xa;</xsl:text>
            <xsl:text>                entity_id,&#xd;&#xa;</xsl:text>
            <xsl:text>                link_type,&#xd;&#xa;</xsl:text>
            <xsl:text>                link_id&#xd;&#xa;</xsl:text>
            <xsl:text>                )&#xd;&#xa;</xsl:text>
            <xsl:text>            select&#xd;&#xa;</xsl:text>
            <xsl:text>                (select numeric from public.</xsl:text><xsl:value-of select='$app'/><xsl:text>__definition where category='EntityType' and label='</xsl:text><xsl:value-of select='$links'/><xsl:text>'),&#xd;&#xa;</xsl:text>
            <xsl:text>                _id, /* Override the value in the array argument, which will be 0 */&#xd;&#xa;</xsl:text>
            <xsl:text>                new_link.link_type,&#xd;&#xa;</xsl:text>
            <xsl:text>                new_link.link_id&#xd;&#xa;</xsl:text>
            <xsl:text>            from&#xd;&#xa;</xsl:text>
            <xsl:text>                unnest(_links) new_link;&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:text>    else&#xd;&#xa;</xsl:text>
        <xsl:text>        insert into&#xd;&#xa;</xsl:text>
        <xsl:text>            public.</xsl:text><xsl:value-of select='$app'/><xsl:text>_</xsl:text><xsl:value-of select='$table'/><xsl:text>_audit&#xd;&#xa;</xsl:text>
        <xsl:text>                (&#xd;&#xa;</xsl:text>
        <xsl:text>                uuid,&#xd;&#xa;</xsl:text>
        <xsl:text>                saved_on,&#xd;&#xa;</xsl:text>
        <xsl:text>                saved_by,&#xd;&#xa;</xsl:text>
        <xsl:text>                </xsl:text><xsl:value-of select='$table'/><xsl:text>_id,&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($parent_table) > 0'>
            <xsl:text>                </xsl:text><xsl:value-of select='$parent_table'/><xsl:text>_id,&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select='column[./@column_name != concat($parent_table,"_id")]' mode='insertColumns'/>
        <xsl:text>                )&#xd;&#xa;</xsl:text>
        <xsl:text>            select&#xd;&#xa;</xsl:text>
        <xsl:text>                uuid,&#xd;&#xa;</xsl:text>
        <xsl:text>                saved_on,&#xd;&#xa;</xsl:text>
        <xsl:text>                saved_by,&#xd;&#xa;</xsl:text>
        <xsl:text>                id,&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($parent_table) > 0'>
            <xsl:text>                </xsl:text><xsl:value-of select='$parent_table'/><xsl:text>_id,&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select='column[./@column_name != concat($parent_table,"_id")]' mode='insertColumns'/>
        <xsl:text>            from&#xd;&#xa;</xsl:text>
        <xsl:text>                public.</xsl:text><xsl:value-of select='$app'/><xsl:text>_</xsl:text><xsl:value-of select='$table'/><xsl:text>&#xd;&#xa;</xsl:text>
        <xsl:text>            where&#xd;&#xa;</xsl:text>
        <xsl:text>                id=_id;&#xd;&#xa;</xsl:text>
        <xsl:text>        update&#xd;&#xa;</xsl:text>
        <xsl:text>            public.</xsl:text><xsl:value-of select='$app'/><xsl:text>_</xsl:text><xsl:value-of select='$table'/><xsl:text>&#xd;&#xa;</xsl:text>
        <xsl:text>                set&#xd;&#xa;</xsl:text>
        <xsl:text>                    saved_on=now(),&#xd;&#xa;</xsl:text>
        <xsl:text>                    saved_by=_saved_by,&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($parent_table) > 0'>
            <xsl:text>                    </xsl:text><xsl:value-of select='$parent_table'/><xsl:text>_id=_</xsl:text><xsl:value-of select='$parent_table'/><xsl:text>_id,&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select='column[./@column_name != concat($parent_table,"_id")]' mode='updateColumns'/>
        <xsl:text>                where&#xd;&#xa;</xsl:text>
        <xsl:text>                    id=_id;&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($links) > 0'>
            <xsl:text>        insert into /* Add new links */&#xd;&#xa;</xsl:text>
            <xsl:text>            public.</xsl:text><xsl:value-of select='$app'/><xsl:text>__link&#xd;&#xa;</xsl:text>
            <xsl:text>                (&#xd;&#xa;</xsl:text>
            <xsl:text>                entity_type,&#xd;&#xa;</xsl:text>
            <xsl:text>                entity_id,&#xd;&#xa;</xsl:text>
            <xsl:text>                link_type,&#xd;&#xa;</xsl:text>
            <xsl:text>                link_id&#xd;&#xa;</xsl:text>
            <xsl:text>                )&#xd;&#xa;</xsl:text>
            <xsl:text>            select&#xd;&#xa;</xsl:text>
            <xsl:text>                (select numeric from public.</xsl:text><xsl:value-of select='$app'/><xsl:text>__definition where category='EntityType' and label='</xsl:text><xsl:value-of select='$links'/><xsl:text>'),&#xd;&#xa;</xsl:text>
            <xsl:text>                _id, /* Override the value in the array argument, which will be 0 */&#xd;&#xa;</xsl:text>
            <xsl:text>                new_link.link_type,&#xd;&#xa;</xsl:text>
            <xsl:text>                new_link.link_id&#xd;&#xa;</xsl:text>
            <xsl:text>            from&#xd;&#xa;</xsl:text>
            <xsl:text>                unnest(_links) new_link&#xd;&#xa;</xsl:text>
            <xsl:text>                left outer join </xsl:text><xsl:value-of select='$app'/><xsl:text>__link old_link&#xd;&#xa;</xsl:text>
            <xsl:text>                    on&#xd;&#xa;</xsl:text>
            <xsl:text>                        old_link.entity_type=(select numeric from public.</xsl:text><xsl:value-of select='$app'/><xsl:text>__definition where category='EntityType' and label='</xsl:text><xsl:value-of select='$links'/><xsl:text>')&#xd;&#xa;</xsl:text>
            <xsl:text>                        and&#xd;&#xa;</xsl:text>
            <xsl:text>                        old_link.entity_id=new_link.entity_id&#xd;&#xa;</xsl:text>
            <xsl:text>                        and&#xd;&#xa;</xsl:text>
            <xsl:text>                        old_link.link_type=new_link.link_type&#xd;&#xa;</xsl:text>
            <xsl:text>                        and&#xd;&#xa;</xsl:text>
            <xsl:text>                        old_link.link_id=new_link.link_id&#xd;&#xa;</xsl:text>
            <xsl:text>            where&#xd;&#xa;</xsl:text>
            <xsl:text>                old_link.entity_id is null; /* I.e. not in old list */&#xd;&#xa;</xsl:text>
            <xsl:text>        delete from /* Remove old ones */&#xd;&#xa;</xsl:text>
            <xsl:text>            public.</xsl:text><xsl:value-of select='$app'/><xsl:text>__link&#xd;&#xa;</xsl:text>
            <xsl:text>            where&#xd;&#xa;</xsl:text>
            <xsl:text>                id&#xd;&#xa;</xsl:text>
            <xsl:text>                in&#xd;&#xa;</xsl:text>
            <xsl:text>                (&#xd;&#xa;</xsl:text>
            <xsl:text>                select&#xd;&#xa;</xsl:text>
            <xsl:text>                    old_link.id&#xd;&#xa;</xsl:text>
            <xsl:text>                from&#xd;&#xa;</xsl:text>
            <xsl:text>                    </xsl:text><xsl:value-of select='$app'/><xsl:text>__link old_link&#xd;&#xa;</xsl:text>
            <xsl:text>                    left outer join unnest(_links) new_link&#xd;&#xa;</xsl:text>
            <xsl:text>                        on&#xd;&#xa;</xsl:text>
            <xsl:text>                            new_link.entity_id=old_link.entity_id&#xd;&#xa;</xsl:text>
            <xsl:text>                            and&#xd;&#xa;</xsl:text>
            <xsl:text>                            new_link.link_type=old_link.link_type&#xd;&#xa;</xsl:text>
            <xsl:text>                            and&#xd;&#xa;</xsl:text>
            <xsl:text>                            new_link.link_id=old_link.link_id&#xd;&#xa;</xsl:text>
            <xsl:text>                where&#xd;&#xa;</xsl:text>
            <xsl:text>                    old_link.entity_type=(select numeric from public.</xsl:text><xsl:value-of select='$app'/><xsl:text>__definition where category='EntityType' and label='</xsl:text><xsl:value-of select='$links'/><xsl:text>')&#xd;&#xa;</xsl:text>
            <xsl:text>                    and&#xd;&#xa;</xsl:text>
            <xsl:text>                    old_link.entity_id=_id&#xd;&#xa;</xsl:text>
            <xsl:text>                    and&#xd;&#xa;</xsl:text>
            <xsl:text>                    new_link.entity_id is null /* I.e. not in new list */&#xd;&#xa;</xsl:text>
            <xsl:text>                );&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:text>    end if;&#xd;&#xa;</xsl:text>
        <xsl:text>    return _id;&#xd;&#xa;</xsl:text>
        <xsl:text>end;&#xd;&#xa;</xsl:text>
        <xsl:text>$$ language plpgsql;&#xd;&#xa;</xsl:text>
        <xsl:text>&#xd;&#xa;</xsl:text>
        <xsl:text>/*&#xd;&#xa;</xsl:text>
        <xsl:text>select&#xd;&#xa;</xsl:text>
        <xsl:text>    </xsl:text><xsl:value-of select='$app'/><xsl:text>_save_</xsl:text><xsl:value-of select='$table'/><xsl:text>&#xd;&#xa;</xsl:text>
        <xsl:text>        (&#xd;&#xa;</xsl:text>
        <xsl:text>        '', -- _saved_by varchar(256),&#xd;&#xa;</xsl:text>
        <xsl:text>        0, -- _id int,&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($parent_table) > 0'>
            <xsl:text>        0, -- _</xsl:text><xsl:value-of select='$parent_table'/><xsl:text>_id int,&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:choose>
          <xsl:when test='string-length($links) > 0'>
            <xsl:text>        array[row(0,0,0),]::</xsl:text><xsl:value-of select='$app'/><xsl:text>_link_type[], -- _links </xsl:text><xsl:value-of select='$app'/><xsl:text>_link_type[],&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select='column[./@column_name != concat($parent_table,"_id")]' mode='argumentsForTesting'/>
        <xsl:text>        )&#xd;&#xa;</xsl:text>
        <xsl:text>*/&#xd;&#xa;</xsl:text>
        <xsl:text>&#xd;&#xa;</xsl:text>
      </xsl:when>
      <xsl:when test='$type="remove"'>
        <xsl:text></xsl:text><xsl:value-of select='$app'/><xsl:text>_remove_</xsl:text>
        <xsl:value-of select='$table'/>
        <xsl:text>&#xd;&#xa;</xsl:text>
        <xsl:text>    (&#xd;&#xa;</xsl:text>
        <xsl:text>    _saved_by varchar(256),&#xd;&#xa;</xsl:text>
        <xsl:text>    _id int&#xd;&#xa;</xsl:text>
        <xsl:text>    )&#xd;&#xa;</xsl:text>
        <xsl:text>returns int as&#xd;&#xa;</xsl:text>
        <xsl:text>$$&#xd;&#xa;</xsl:text>
        <xsl:text>begin&#xd;&#xa;</xsl:text>
        <xsl:text>    if not _id=0 then /* If it is valid */&#xd;&#xa;</xsl:text>
        <xsl:text>        insert into /* Audit current item */&#xd;&#xa;</xsl:text>
        <xsl:text>            public.</xsl:text><xsl:value-of select='$app'/><xsl:text>_</xsl:text><xsl:value-of select='$table'/><xsl:text>_audit&#xd;&#xa;</xsl:text>
        <xsl:text>                (&#xd;&#xa;</xsl:text>
        <xsl:text>                uuid,&#xd;&#xa;</xsl:text>
        <xsl:text>                saved_on,&#xd;&#xa;</xsl:text>
        <xsl:text>                saved_by,&#xd;&#xa;</xsl:text>
        <xsl:text>                </xsl:text><xsl:value-of select='$table'/><xsl:text>_id,&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($parent_table) > 0'>
            <xsl:text>                </xsl:text><xsl:value-of select='$parent_table'/><xsl:text>_id,&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select='column[./@column_name != concat($parent_table,"_id")]' mode='insertColumns'/>
        <xsl:text>                )&#xd;&#xa;</xsl:text>
        <xsl:text>            select&#xd;&#xa;</xsl:text>
        <xsl:text>                uuid,&#xd;&#xa;</xsl:text>
        <xsl:text>                saved_on,&#xd;&#xa;</xsl:text>
        <xsl:text>                saved_by,&#xd;&#xa;</xsl:text>
        <xsl:text>                id,&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($parent_table) > 0'>
            <xsl:text>                </xsl:text><xsl:value-of select='$parent_table'/><xsl:text>_id,&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select='column[./@column_name != concat($parent_table,"_id")]' mode='insertColumns'/>
        <xsl:text>            from&#xd;&#xa;</xsl:text>
        <xsl:text>                public.</xsl:text><xsl:value-of select='$app'/><xsl:text>_</xsl:text><xsl:value-of select='$table'/><xsl:text>&#xd;&#xa;</xsl:text>
        <xsl:text>            where&#xd;&#xa;</xsl:text>
        <xsl:text>                id=_id;&#xd;&#xa;</xsl:text>
        <xsl:text>        insert into /* Audit deletion */&#xd;&#xa;</xsl:text>
        <xsl:text>            public.</xsl:text><xsl:value-of select='$app'/><xsl:text>_</xsl:text><xsl:value-of select='$table'/><xsl:text>_audit&#xd;&#xa;</xsl:text>
        <xsl:text>                (&#xd;&#xa;</xsl:text>
        <xsl:text>                uuid,&#xd;&#xa;</xsl:text>
        <xsl:text>                saved_on,&#xd;&#xa;</xsl:text>
        <xsl:text>                saved_by,&#xd;&#xa;</xsl:text>
        <xsl:text>                </xsl:text><xsl:value-of select='$table'/><xsl:text>_id,&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($parent_table) > 0'>
            <xsl:text>                </xsl:text><xsl:value-of select='$parent_table'/><xsl:text>_id,&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select='column[./@column_name != concat($parent_table,"_id")]' mode='insertColumns'/>
        <xsl:text>                )&#xd;&#xa;</xsl:text>
        <xsl:text>            select&#xd;&#xa;</xsl:text>
        <xsl:text>                uuid,&#xd;&#xa;</xsl:text>
        <xsl:text>                now(),&#xd;&#xa;</xsl:text>
        <xsl:text>                _saved_by,&#xd;&#xa;</xsl:text>
        <xsl:text>                id,&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($parent_table) > 0'>
            <xsl:text>                </xsl:text><xsl:value-of select='$parent_table'/><xsl:text>_id,&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select='column[./@column_name != concat($parent_table,"_id")]' mode='insertColumns'/>
        <xsl:text>            from&#xd;&#xa;</xsl:text>
        <xsl:text>                public.</xsl:text><xsl:value-of select='$app'/><xsl:text>_</xsl:text><xsl:value-of select='$table'/><xsl:text>&#xd;&#xa;</xsl:text>
        <xsl:text>            where&#xd;&#xa;</xsl:text>
        <xsl:text>                id=_id;&#xd;&#xa;</xsl:text>
        <xsl:choose>
          <xsl:when test='string-length($links) > 0'>
            <xsl:text>        delete from&#xd;&#xa;</xsl:text>
            <xsl:text>            public.</xsl:text><xsl:value-of select='$app'/><xsl:text>__link&#xd;&#xa;</xsl:text>
            <xsl:text>                where&#xd;&#xa;</xsl:text>
            <xsl:text>                    entity_id=_id&#xd;&#xa;</xsl:text>
            <xsl:text>                    and&#xd;&#xa;</xsl:text>
            <xsl:text>                    entity_type=(select numeric from public.</xsl:text><xsl:value-of select='$app'/><xsl:text>__definition where category='EntityType' and label='</xsl:text><xsl:value-of select='$links'/><xsl:text>');&#xd;&#xa;</xsl:text>
          </xsl:when>
          <xsl:otherwise>
          </xsl:otherwise>
        </xsl:choose>
        <xsl:text>        delete from&#xd;&#xa;</xsl:text>
        <xsl:text>            public.</xsl:text><xsl:value-of select='$app'/><xsl:text>_</xsl:text><xsl:value-of select='$table'/><xsl:text>&#xd;&#xa;</xsl:text>
        <xsl:text>                where&#xd;&#xa;</xsl:text>
        <xsl:text>                    id=_id;&#xd;&#xa;</xsl:text>
        <xsl:text>    end if;&#xd;&#xa;</xsl:text>
        <xsl:text>    return _id;&#xd;&#xa;</xsl:text>
        <xsl:text>end;&#xd;&#xa;</xsl:text>
        <xsl:text>$$ language plpgsql;&#xd;&#xa;</xsl:text>
        <xsl:text>&#xd;&#xa;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match='column[@column_name!="id" and @column_name!="uuid" and @column_name!="saved_by" and @column_name!="saved_on"]' mode='arguments'>
    <xsl:text>    _</xsl:text>
    <xsl:value-of select='@column_name'/>
    <xsl:text> </xsl:text>
    <xsl:choose>
      <xsl:when test='@data_type="integer"'>
        <xsl:text>int</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="boolean"'>
        <xsl:text>boolean</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="uuid"'>
        <xsl:text>int</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="timestamp with time zone"'>
        <xsl:text>varchar(10)</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="time without time zone"'>
        <xsl:text>varchar(10)</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="date"'>
        <xsl:text>varchar(10)</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="character varying"'>
        <xsl:text>varchar</xsl:text>
        <xsl:text>(</xsl:text>
        <xsl:value-of select='@character_maximum_length'/>
        <xsl:text>)</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="text"'>
        <xsl:text>text</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>ERROR</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='(following-sibling::*)'>
        <xsl:text>,&#xd;&#xa;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>&#xd;&#xa;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match='column[@column_name!="id" and @column_name!="uuid" and @column_name!="saved_on"]' mode='insertColumns'>
    <xsl:text>                </xsl:text>
    <xsl:value-of select='@column_name'/>
    <xsl:choose>
      <xsl:when test='(following-sibling::*)'>
        <xsl:text>,&#xd;&#xa;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>&#xd;&#xa;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match='column[@column_name!="id" and @column_name!="uuid" and @column_name!="saved_on"]' mode='insertValues'>
    <xsl:text>                </xsl:text>
    <xsl:choose>
      <xsl:when test='@data_type="timestamp with time zone"'>
        <xsl:text>to_date(replace(_</xsl:text>
        <xsl:value-of select='@column_name'/>
        <xsl:text>,'-',''),'YYYYMMDD')::date</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="time without time zone"'>
        <xsl:text>to_timestamp(replace(_</xsl:text>
        <xsl:value-of select='@column_name'/>
        <xsl:text>,':',''),'HH24MISS')::time</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="date"'>
        <xsl:text>to_date(replace(_</xsl:text>
        <xsl:value-of select='@column_name'/>
        <xsl:text>,'-',''),'YYYYMMDD')::date</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>_</xsl:text><xsl:value-of select='@column_name'/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='(following-sibling::*)'>
        <xsl:text>,&#xd;&#xa;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>&#xd;&#xa;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match='column[@column_name!="id" and @column_name!="uuid" and @column_name!="saved_on"]' mode='updateColumns'>
    <xsl:text>                    </xsl:text>
    <xsl:value-of select='@column_name'/>
    <xsl:text>=</xsl:text>
    <xsl:choose>
      <xsl:when test='@data_type="timestamp with time zone"'>
        <xsl:text>to_date(replace(_</xsl:text>
        <xsl:value-of select='@column_name'/>
        <xsl:text>,'-',''),'YYYYMMDD')::date</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="time without time zone"'>
        <xsl:text>to_timestamp(replace(_</xsl:text>
        <xsl:value-of select='@column_name'/>
        <xsl:text>,':',''),'HH24MISS')::time</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="date"'>
        <xsl:text>to_date(replace(_</xsl:text>
        <xsl:value-of select='@column_name'/>
        <xsl:text>,'-',''),'YYYYMMDD')::date</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>_</xsl:text>
        <xsl:value-of select='@column_name'/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='(following-sibling::*)'>
        <xsl:text>,&#xd;&#xa;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>&#xd;&#xa;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match='column[@column_name!="id" and @column_name!="uuid" and @column_name!="saved_on"]' mode='argumentsForTesting'>
    <xsl:text>        </xsl:text>
    <xsl:choose>
      <xsl:when test='@data_type="integer"'>
        <xsl:text>0</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="boolean"'>
        <xsl:text>false</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>''</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='(following-sibling::*)'>
        <xsl:text>, -- _</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text> -- _</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:value-of select='@column_name'/>
    <xsl:text> </xsl:text>
    <xsl:choose>
      <xsl:when test='@data_type="integer"'>
        <xsl:text>int</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="boolean"'>
        <xsl:text>boolean</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="uuid"'>
        <xsl:text>int</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="timestamp with time zone"'>
        <xsl:text>varchar(10)</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="time without time zone"'>
        <xsl:text>varchar(10)</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="date"'>
        <xsl:text>varchar(10)</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="character varying"'>
        <xsl:text>varchar</xsl:text>
        <xsl:text>(</xsl:text>
        <xsl:value-of select='@character_maximum_length'/>
        <xsl:text>)</xsl:text>
      </xsl:when>
      <xsl:when test='@data_type="text"'>
        <xsl:text>text</xsl:text>
      </xsl:when>
      <xsl:otherwise>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:choose>
      <xsl:when test='(following-sibling::*)'>
        <xsl:text>,&#xd;&#xa;</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>&#xd;&#xa;</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>

