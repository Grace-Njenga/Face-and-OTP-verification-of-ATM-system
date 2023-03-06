ALTER TABLE account_info ADD COLUMN Withdraw_time DATETIME;
ALTER TABLE account_info ADD COLUMN deposit_time DATETIME;

ALTER TABLE account_info
DROP COLUMN faces;

-- Change the data type of the column and set the NOT NULL constraint
ALTER TABLE account_info ADD COLUMN balance INT NOT NULL DEFAULT 0;

-- Set the default value of the column to 0 for all existing records
UPDATE account_info SET balance = 0;

--moify to not NULL
ALTER TABLE account_info MODIFY COLUMN otp_expiry DATETIME NOT NULL;

---face recognition database
CREATE TABLE face_data (
  account_number INT NOT NULL,
  faces LONGBLOB NOT NULL);

--create a login_time field
ALTER TABLE account_info MODIFY COLUMN login_time DATETIME AFTER national_ID;

ALTER TABLE transaction_history ADD login_time DATETIME AFTER transaction_amount;

ALTER TABLE transaction_history MODIFY login_time TIME;


CREATE TABLE transaction_history (
  transaction_id INT NOT NULL,
  transaction_date DATE NOT NULL,
  transaction_type VARCHAR(255) NOT NULL,
  transaction_amount FLOAT NOT NULL,
  account_number INT NOT NULL,
  PRIMARY KEY (transaction_id),
  FOREIGN KEY (account_number) REFERENCES account_info(account_number)
);
