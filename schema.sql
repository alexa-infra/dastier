DROP TABLE IF EXISTS "reader_link";
DROP TABLE IF EXISTS "reader_readlater";
CREATE TABLE "reader_link" (
    "id" integer NOT NULL PRIMARY KEY,
    "url" varchar(200) NOT NULL,
    "title" varchar(50) NOT NULL,
    "usage_count" integer NOT NULL,
    "last_access" datetime NOT NULL
)
;
CREATE TABLE "reader_readlater" (
    "id" integer NOT NULL PRIMARY KEY,
    "url" varchar(200) NOT NULL,
    "title" varchar(50) NOT NULL,
    "created" datetime NOT NULL,
    "readed" bool NOT NULL
)
;

