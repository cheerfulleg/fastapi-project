-- upgrade --
ALTER TABLE "profile" ADD "avatar_url" TEXT;
-- downgrade --
ALTER TABLE "profile" DROP COLUMN "avatar_url";
