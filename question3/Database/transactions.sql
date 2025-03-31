CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    account_id BIGINT,
    type VARCHAR(10), -- 'debit' or 'credit'
    amount DECIMAL(10, 2),
    status VARCHAR(10), -- 'pending', 'completed', 'failed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
