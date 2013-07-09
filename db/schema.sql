-- Describe USER_PREFS
-- usage-
--  >>> from flaskr import init_db
--  >>> init_db()
--
CREATE TABLE "user_prefs" (
    "key" TEXT unique,
    "val" TEXT
);

CREATE TABLE playlist (
    id INTEGER PRIMARY KEY, 
    name TEXT
);

CREATE TABLE playlist_item (
    id INTEGER PRIMARY KEY, 
    playlist_id NUMERIC, 
    path TEXT, 
    list_order NUMERIC
);

-- set up prefs
Insert into user_prefs values ('user_pass', 'password');
Insert into user_prefs values ('admin_pass', 'password');
Insert into user_prefs values ('lib_dir', 'default');