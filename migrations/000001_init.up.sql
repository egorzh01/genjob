CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS auth_codes (
    id UUID PRIMARY KEY,
    email TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    code_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS profile_contacts (
    profile_id UUID PRIMARY KEY REFERENCES profiles (id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    email TEXT,
    phone_number TEXT,
    country TEXT,
    city TEXT
);

CREATE TABLE IF NOT EXISTS profile_educations (
    id UUID PRIMARY KEY,
    profile_id UUID NOT NULL REFERENCES profiles (id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    place TEXT NOT NULL,
    location TEXT,
    end_date TIMESTAMP WITH TIME ZONE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS profile_experiences (
    id UUID PRIMARY KEY,
    profile_id UUID NOT NULL REFERENCES profiles (id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    place TEXT NOT NULL,
    start_date TIMESTAMP WITH TIME ZONE,
    end_date TIMESTAMP WITH TIME ZONE,
    location TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS web_sessions (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    refresh_token_hash TEXT NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX idx_profiles_user_id ON profiles (user_id);

CREATE INDEX idx_profile_educations_profile_id ON profile_educations (profile_id);

CREATE INDEX idx_profile_experiences_profile_id ON profile_experiences (profile_id);

CREATE INDEX idx_web_sessions_user_id ON web_sessions (user_id);

CREATE INDEX idx_auth_codes_email ON auth_codes (email);

CREATE INDEX idx_users_email ON users (email);
