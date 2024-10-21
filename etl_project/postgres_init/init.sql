CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS companies
(
    id varchar(155) PRIMARY KEY,
    company_name varchar(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS charges
(
    id varchar(255) DEFAULT uuid_generate_v4() PRIMARY KEY,
    company_id varchar(155),
    amount decimal(22,2) NOT NULL,
    status varchar(30) NOT NULL,
    created_at timestamp NOT NULL,
    paid_at timestamp NULL,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

-- CREATE VIEW total_amount_per_day AS
-- SELECT
--     DATE(c.created_at) AS transaction_date,
--     co.company_name,
--     SUM(c.amount) AS total_amount
-- FROM
--     charges c
-- JOIN
--     companies co ON c.company_id = co.id
-- GROUP BY
--     transaction_date, co.company_name
-- ORDER BY
--     transaction_date, co.company_name;

-- SELECT * FROM total_amount_per_day;
