-- Describe USER_PREFS
-- usage-
--  >>> from flaskr import init_db
--  >>> init_db()
--
CREATE TABLE "user_prefs" (
    "key" TEXT unique NOT NULL,
    "val" TEXT  NOT NULL
);

CREATE TABLE playlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    name TEXT  NOT NULL
);

CREATE TABLE playlist_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    playlist_id NUMERIC NOT NULL,
    path TEXT NOT NULL,
    list_order NUMERIC  NOT NULL
);

CREATE TABLE "bookmark" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT NOT NULL,
    "path" TEXT NOT NULL,
    "list_order" INTEGER NOT NULL
);


-- set up prefs
Insert into user_prefs values ('user_pass', 'password');
Insert into user_prefs values ('admin_pass', 'password');
Insert into user_prefs values ('lib_dir', 'default');