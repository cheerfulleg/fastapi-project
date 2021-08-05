-- upgrade --
CREATE TABLE IF NOT EXISTS "post" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(120) NOT NULL,
    "body" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "profile_id" INT NOT NULL REFERENCES "profile" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "post";
