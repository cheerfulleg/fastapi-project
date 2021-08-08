-- upgrade --
CREATE TABLE "subscriptions" ("profile_id" INT NOT NULL REFERENCES "profile" ("id") ON DELETE CASCADE,"subscriber" INT NOT NULL REFERENCES "profile" ("id") ON DELETE CASCADE);
-- downgrade --
DROP TABLE IF EXISTS "subscriptions";
