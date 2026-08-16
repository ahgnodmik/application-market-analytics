"""
워커 프로세스 진입점 (기획서 16.2)
스케줄러/배치 작업을 별도 프로세스로 실행
Railway에서 worker 서비스로 사용 가능
"""
import asyncio
import logging
import sys
from app.config import settings
from app.tasks.scheduler import check_and_fetch_rankings

# 로깅 설정
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def main():
    """워커 메인 함수"""
    logger.info("=" * 60)
    logger.info("🚀 Application Market Analytics - Worker Process")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Scheduler Enabled: {settings.SCHEDULER_ENABLED}")
    logger.info("=" * 60)
    
    if not settings.SCHEDULER_ENABLED:
        logger.info("Scheduler is disabled. Exiting.")
        return
    
    try:
        # 초기 실행
        logger.info("Running initial scheduler check...")
        result = await check_and_fetch_rankings()
        if result:
            logger.info(f"Scheduler result: {result}")
        
        # 주기적으로 확인 (24시간마다)
        while True:
            logger.info("Waiting 24 hours before next check...")
            await asyncio.sleep(3600 * 24)  # 24시간
            
            logger.info("Running scheduled check...")
            result = await check_and_fetch_rankings()
            if result:
                logger.info(f"Scheduler result: {result}")
                
    except KeyboardInterrupt:
        logger.info("Worker process interrupted. Shutting down...")
    except Exception as e:
        logger.error(f"Worker process error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
