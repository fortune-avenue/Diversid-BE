-- Create users table
CREATE TABLE
    users (
        user_id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
        email VARCHAR(255) NOT NULL UNIQUE,
        mobile_no VARCHAR(255) UNIQUE,
        full_name VARCHAR(255) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        ktp_photo VARCHAR,
        slf_ktp_photo VARCHAR,
        email_verified BOOLEAN DEFAULT FALSE,
        phone_verified BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- Create voice_data table
CREATE TABLE
    voice_data (
        voice_data_id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
        user_id UUID NOT NULL,
        voice_file_1 VARCHAR,
        voice_file_2 VARCHAR,
        voice_file_3 VARCHAR,
        voice_file_4 VARCHAR,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    );

-- Create jwt_token table
CREATE TABLE
    jwt_token (
        user_id UUID PRIMARY KEY,
        access_token VARCHAR NOT NULL,
        token_type VARCHAR NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    );

-- Add indexes for performance (optional but recommended)
CREATE INDEX idx_users_email ON users (email);

CREATE INDEX idx_users_mobile_no ON users (mobile_no);

CREATE INDEX idx_voice_data_user_id ON voice_data (user_id);