CREATE TABLE order_request (
    id SERIAL PRIMARY KEY,
    order_request jsonb NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()),
    archived_at timestamp without time zone DEFAULT NULL
);