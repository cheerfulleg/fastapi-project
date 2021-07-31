-- upgrade --
ALTER TABLE "user" ALTER COLUMN "email" DROP DEFAULT;
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "email" SET DEFAULT 'def@email.com';
