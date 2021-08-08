import logging
from uuid import uuid4

import aiobotocore

from backend.config import settings

logger = logging.getLogger(__name__)


class S3Service:
    aws_access_key_id = settings.AWS_ACCESS_KEY
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    region = settings.AWS_REGION

    async def upload_file(self, fileobject, bucket, key):
        session = aiobotocore.get_session()
        async with session.create_client("s3", region_name=self.region, aws_secret_access_key=self.aws_secret_access_key, aws_access_key_id=self.aws_access_key_id) as client:
            file_upload_response = await client.put_object(ACL="public-read", Bucket=bucket, Key=key, Body=fileobject)

            if file_upload_response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                logger.info(f"File uploaded path : https://{bucket}.s3.{self.region}.amazonaws.com/{key}")
                return True
        return False


def generate_png_string():
    logger.info("Generating random string .png")
    return uuid4().hex[:6].upper().replace("0", "X").replace("O", "Y") + ".png"


s3_service = S3Service()
