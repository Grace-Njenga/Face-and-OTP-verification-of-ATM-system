ALTER TABLE account_info
ADD COLUMN otp_expiry BLOB;
UPDATE account_info SET balance = 0 WHERE balance IS NULL;



ALTER TABLE account_info ADD otp_expiry INT(11) DEFAULT NULL;