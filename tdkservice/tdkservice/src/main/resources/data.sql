-- data.sql
INSERT INTO user_role (id, name) VALUES (1, 'admin'), (2, 'tester')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO user_group (id, name) VALUES (1, 'usergroup1'), (2, 'usergroup2')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO user (username, password, user_role_id, user_group_id, email, created_date, updated_at, theme, display_name)
VALUES ('admin', 'test', 1, 1, 'admin@gmail.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'DARK', 'Admin User')
ON DUPLICATE KEY UPDATE
username = VALUES(username),
password = VALUES(password),
user_role_id = VALUES(user_role_id),
user_group_id = VALUES(user_group_id),
email = VALUES(email),
updated_at = VALUES(updated_at),
theme = VALUES(theme),
display_name = VALUES(display_name);