-- upgrade --
ALTER TABLE "user" ADD "is_admin" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "user" DROP COLUMN "is_admin";
