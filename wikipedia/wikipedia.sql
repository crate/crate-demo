-- dbext:type=CRATE:host=nuc1.p.fir.io:port=4200

create analyzer "wiki" extends snowball with (language = 'English');

create table wikipedia (
    "pageId" int primary key,
    namespace string,
    title string,
    redirect_title string,
    revision object (strict) as (
        id int,
        parentid int,
        minor boolean,
        comment string
    ),
    modified_at timestamp,
    contributor object (strict) as (
        id int,
        username string,
        "ip" ip
    ),
    text string index off,
    text_sha1 string,
    model string,
    format string,
    categories string,
    links string,
    files string,
    index ft using fulltext (title, redirect_title, text) with (analyzer='wiki')
) clustered into 32 shards with (number_of_replicas='0');
