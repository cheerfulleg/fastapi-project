-- upgrade --
ALTER TABLE "post" ADD "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE "post" ALTER COLUMN "created_at" DROP NOT NULL;
-- downgrade --
ALTER TABLE "post" DROP COLUMN "modified_at";
ALTER TABLE "post" ALTER COLUMN "created_at" SET NOT NULL;
