"""
LLM容错模块 - 降级策略、缓存、熔断器
"""
import time
import hashlib
import json
import httpx
from typing import Optional, Callable, List, Any
from functools import lru_cache


class LLMCircuitBreaker:
    """LLM调用熔断器"""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "closed"  # closed, open, half-open

    def record_success(self):
        """记录成功调用"""
        self.failure_count = 0
        self.state = "closed"

    def record_failure(self):
        """记录失败调用"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = "open"

    def is_open(self) -> bool:
        """检查熔断器是否打开"""
        if self.state == "open":
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = "half-open"
                return False
            return True
        return False

    def get_state(self) -> str:
        """获取当前状态"""
        return self.state


class MiniMaxLLMClient:
    """MiniMax LLM客户端"""

    def __init__(self, api_key: str, api_base: str = "https://api.minimax.chat/v1"):
        self.api_key = api_key
        self.api_base = api_base.rstrip("/")

    async def generate(
        self,
        prompt: str,
        model: str = "MiniMax-Text-01",
        temperature: float = 0.3,
        max_tokens: int = 500,
        timeout: int = 30
    ) -> str:
        """调用MiniMax API生成文本"""
        url = f"{self.api_base}/text/chatcompletion_v2"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()

            # MiniMax API响应格式
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            elif "text" in result:
                return result["text"]
            else:
                raise ValueError(f"Unexpected response format: {result}")


class LLMWithFallback:
    """带降级策略的LLM客户端"""

    def __init__(
        self,
        primary_model: str,
        fallback_models: List[str],
        redis_client=None,
        agent_name: str = "default"
    ):
        self.primary_model = primary_model
        self.fallback_models = fallback_models
        self.redis = redis_client
        self.circuit_breaker = LLMCircuitBreaker()
        self.agent_name = agent_name

        # 加载配置
        self._load_llm_config()

    def _load_llm_config(self):
        """加载LLM配置"""
        from pathlib import Path
        import yaml

        config_path = Path(__file__).parent.parent.parent / "config" / "llm_config.yaml"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                minimax_cfg = config.get("minimax", {})
                self.api_key = minimax_cfg.get("api_key", "")
                self.api_base = minimax_cfg.get("api_base", "https://api.minimax.chat/v1")

                # 获取Agent特定配置
                agent_cfg = minimax_cfg.get("agents", {}).get(self.agent_name, {})
                self.default_temperature = agent_cfg.get("temperature", 0.3)
                self.default_max_tokens = agent_cfg.get("max_tokens", 500)
                self.default_timeout = agent_cfg.get("timeout", 30)
        except Exception as e:
            print(f"Failed to load LLM config: {e}")
            self.api_key = ""
            self.api_base = "https://api.minimax.chat/v1"
            self.default_temperature = 0.3
            self.default_max_tokens = 500
            self.default_timeout = 30

        # 创建MiniMax客户端
        if self.api_key:
            self.llm_client = MiniMaxLLMClient(self.api_key, self.api_base)
        else:
            self.llm_client = None

    async def agenerate(self, prompts: List[str], **kwargs) -> Any:
        """生成文本（兼容LangChain接口）"""
        if not prompts:
            raise ValueError("Empty prompts")

        prompt = prompts[0]
        temperature = kwargs.get("temperature", self.default_temperature)
        max_tokens = kwargs.get("max_tokens", self.default_max_tokens)
        model = kwargs.get("model", self.primary_model)

        result = await self.generate(prompt, temperature=temperature, max_tokens=max_tokens)

        # 返回兼容格式
        class Generation:
            def __init__(self, text):
                self.text = text

        class ChatResult:
            def __init__(self, text):
                self.generations = [Generation(text)]

        return ChatResult(result)

    async def generate(
        self,
        prompt: str,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """生成文本，带缓存和降级策略"""
        if temperature is None:
            temperature = self.default_temperature
        if max_tokens is None:
            max_tokens = self.default_max_tokens

        # 1. 检查缓存
        cache_key = self._get_cache_key(prompt)
        cached = await self._get_from_cache(cache_key)
        if cached:
            return cached

        # 2. 检查熔断器
        if self.circuit_breaker.is_open():
            return await self._call_fallback(prompt, temperature, max_tokens)

        # 3. 调用主模型
        try:
            result = await self._call_primary(prompt, temperature, max_tokens)
            self.circuit_breaker.record_success()
            await self._save_to_cache(cache_key, result)
            return result
        except Exception as e:
            print(f"Primary model error: {e}")
            self.circuit_breaker.record_failure()
            return await self._call_fallback(prompt, temperature, max_tokens)

    async def _call_primary(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """调用主模型"""
        if not self.llm_client:
            raise ValueError("LLM client not configured")

        return await self.llm_client.generate(
            prompt=prompt,
            model=self.primary_model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=self.default_timeout
        )

    async def _call_fallback(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """调用降级模型"""
        for model_info in self.fallback_models:
            if isinstance(model_info, dict):
                model = model_info.get("model", "MiniMax-Text-01")
            else:
                model = str(model_info)

            try:
                if self.llm_client:
                    result = await self.llm_client.generate(
                        prompt=prompt,
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        timeout=self.default_timeout
                    )
                    return result
            except Exception as e:
                print(f"Fallback model {model} error: {e}")
                continue

        raise Exception("All fallback models failed")

    def _get_cache_key(self, prompt: str) -> str:
        """生成缓存键"""
        return hashlib.md5(prompt.encode()).hexdigest()

    async def _get_from_cache(self, key: str) -> Optional[str]:
        """从缓存获取"""
        if self.redis:
            try:
                return await self.redis.get(f"llm:cache:{key}")
            except Exception as e:
                print(f"Cache get error: {e}")
        return None

    async def _save_to_cache(
        self,
        key: str,
        value: str,
        ttl: int = 3600
    ):
        """保存到缓存"""
        if self.redis:
            try:
                await self.redis.setex(f"llm:cache:{key}", ttl, value)
            except Exception as e:
                print(f"Cache set error: {e}")


class LLMConfigLoader:
    """LLM配置加载器"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """加载配置文件"""
        import yaml
        from pathlib import Path
        config_path = Path(__file__).parent.parent.parent / "config" / "llm_config.yaml"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f)
        except FileNotFoundError:
            self._config = self._get_default_config()

    def _get_default_config(self) -> dict:
        """获取默认配置"""
        return {
            "minimax": {
                "agents": {
                    "event_classifier": {
                        "model": "MiniMax-Text-01",
                        "temperature": 0.3,
                        "max_tokens": 500,
                        "timeout": 10
                    }
                },
                "cache": {"enabled": True, "ttl": 3600},
                "circuit_breaker": {
                    "failure_threshold": 5,
                    "recovery_timeout": 60
                }
            }
        }

    def get_agent_config(self, agent_name: str) -> dict:
        """获取指定Agent配置"""
        return self._config.get("minimax", {}).get("agents", {}).get(agent_name, {})

    def get_embedding_config(self) -> dict:
        """获取Embedding配置"""
        return self._config.get("minimax", {}).get("embedding", {})

    def get_fallback_config(self) -> List[dict]:
        """获取降级配置"""
        return self._config.get("minimax", {}).get("fallback", {}).get("models", [])

    def is_cache_enabled(self) -> bool:
        """是否启用缓存"""
        return self._config.get("minimax", {}).get("cache", {}).get("enabled", True)

    def get_cache_ttl(self) -> int:
        """获取缓存TTL"""
        return self._config.get("minimax", {}).get("cache", {}).get("ttl", 3600)


def create_llm_client(agent_name: str = "default") -> LLMWithFallback:
    """创建LLM客户端"""
    config = get_llm_config()
    agent_cfg = config.get_agent_config(agent_name)
    fallback_cfg = config.get_fallback_config()

    primary_model = agent_cfg.get("model", "MiniMax-Text-01")

    return LLMWithFallback(
        primary_model=primary_model,
        fallback_models=fallback_cfg,
        agent_name=agent_name
    )


@lru_cache()
def get_llm_config() -> LLMConfigLoader:
    """获取LLM配置单例"""
    return LLMConfigLoader()
