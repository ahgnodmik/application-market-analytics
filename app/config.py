"""
설정 관리 모듈 (기획서 16.1)
환경 변수 로딩 및 dev/prod 설정 분리
"""
import os
from typing import Optional
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# 환경 변수 로드 (.env, .env.local 순서대로)
load_dotenv()
load_dotenv('.env.local')


class Settings:
    """애플리케이션 설정"""
    
    # 환경
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # 데이터베이스
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # 서버
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    # 스케줄러
    SCHEDULER_ENABLED: bool = os.getenv("SCHEDULER_ENABLED", "true").lower() == "true"
    
    # Play Store 수집 설정
    PLAY_STORE_COUNTRY: str = os.getenv("PLAY_STORE_COUNTRY", "kr")
    PLAY_STORE_LANG: str = os.getenv("PLAY_STORE_LANG", "ko")
    PLAY_STORE_DEFAULT_LIMIT: int = int(os.getenv("PLAY_STORE_DEFAULT_LIMIT", "100"))
    
    @property
    def is_production(self) -> bool:
        """프로덕션 환경 여부"""
        return self.APP_ENV.lower() == "prod"
    
    @property
    def is_development(self) -> bool:
        """개발 환경 여부"""
        return self.APP_ENV.lower() == "dev"
    
    @property
    def database_url_sqlite(self) -> str:
        """SQLite 데이터베이스 URL (개발용)"""
        if self.DATABASE_URL and self.DATABASE_URL.startswith("postgresql"):
            return self.DATABASE_URL
        
        # SQLite 경로 설정
        db_path = os.getenv("SQLITE_PATH", "market_analytics.db")
        
        # 서버리스 환경 (/tmp 사용)
        if os.getenv("LAMBDA_TASK_ROOT") or os.getenv("NETLIFY"):
            db_path = "/tmp/market_analytics.db"
        
        return f"sqlite:///{db_path}"
    
    def validate(self):
        """설정 검증"""
        errors = []
        
        # 프로덕션 환경에서 필수 항목 확인
        if self.is_production:
            if not self.DATABASE_URL:
                errors.append("DATABASE_URL is required in production")
        
        # OpenAI API 키 확인 (선택사항이지만 GPT 기능 사용 시 필요)
        if not self.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not set. GPT analysis features will not work.")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
    
    def __repr__(self):
        return f"Settings(env={self.APP_ENV}, db={'configured' if self.DATABASE_URL else 'sqlite'})"


# 전역 설정 인스턴스
settings = Settings()

# 시작 시 설정 검증
try:
    settings.validate()
    logger.info(f"✅ Settings loaded: {settings}")
except ValueError as e:
    logger.error(f"❌ Configuration error: {e}")
