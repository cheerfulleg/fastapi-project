-- upgrade --
ALTER TABLE "user" ADD "email" VARCHAR(120) NOT NULL  DEFAULT 'def@email.com';
-- downgrade --
ALTER TABLE "user" DROP COLUMN "email";
