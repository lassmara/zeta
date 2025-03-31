CREATE TABLE transaction_locks (
    account_id BIGINT PRIMARY KEY,
    lock_status BOOLEAN DEFAULT FALSE
);
