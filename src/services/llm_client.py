"""
LLM客户端 - 调用MiniMax API生成分析
"""
import aiohttp
import asyncio
import yaml
from typing import List, Dict, Optional
import os


class LLMClient:
    """MiniMax LLM客户端"""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "config",
                "llm_config.yaml"
            )

        self.config = self._load_config(config_path)
        self.api_key = self.config.get("minimax", {}).get("api_key", "")
        self.api_base = self.config.get("minimax", {}).get("api_base", "https://api.minimax.chat/v1")

        self.default_model = "MiniMax-Text-01"
        self.timeout = 30
        
        # 获取Agent配置
        agents_config = self.config.get("minimax", {}).get("agents", {})
        self.event_classifier_config = agents_config.get("event_classifier", {})
        self.scene_inference_config = agents_config.get("scene_inference", {})

    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        try:
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"加载LLM配置失败: {e}")
        return {}

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 500
    ) -> Dict:
        """
        调用LLM生成对话

        Args:
            messages: 对话消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数

        Returns:
            包含content的响应字典
        """
        if not self.api_key or self.api_key == "your-api-key-here":
            print("🤖 LLM调用: 使用Mock响应（未配置API Key）")
            return await self._mock_response(messages)

        model = model or self.default_model
        url = f"{self.api_base}/text/chatcompletion_v2"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        print(f"🤖 LLM调用中... URL: {url}, Model: {model}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        choices = result.get("choices", [])
                        if choices:
                            content = choices[0].get("message", {}).get("content", "")
                            print(f"🤖 LLM调用成功! 响应长度: {len(content)} 字符")
                            return {"content": content}
                        else:
                            print(f"🤖 LLM响应格式异常: {result}")
                    else:
                        error_text = await response.text()
                        print(f"❌ LLM API错误: {response.status} - {error_text[:200]}")
                        return await self._mock_response(messages)

        except asyncio.TimeoutError:
            print(f"❌ LLM API超时")
            return await self._mock_response(messages)
        except Exception as e:
            print(f"❌ LLM API调用失败: {e}")
            return await self._mock_response(messages)

        return await self._mock_response(messages)

    async def agenerate(self, prompts: List[str], agent_type: str = "event_classifier") -> Dict:
        """
        异步生成响应（Agent调用接口）

        Args:
            prompts: 提示列表
            agent_type: Agent类型，用于获取对应配置

        Returns:
            包含content的响应字典
        """
        if not prompts or len(prompts) == 0:
            return {"content": ""}
        
        # 将提示转换为消息格式
        user_content = prompts[0]
        messages = [{"role": "user", "content": user_content}]
        
        # 根据Agent类型获取配置
        if agent_type == "event_classifier":
            config = self.event_classifier_config
        elif agent_type == "scene_inference":
            config = self.scene_inference_config
        else:
            config = {}
        
        # 调用chat方法
        return await self.chat(
            messages=messages,
            model=config.get("model", self.default_model),
            temperature=config.get("temperature", 0.3),
            max_tokens=config.get("max_tokens", 500)
        )

    async def _mock_response(self, messages: List[Dict[str, str]]) -> Dict:
        """
        模拟LLM响应（当API不可用时）

        Args:
            messages: 用户消息

        Returns:
            模拟的响应
        """
        await asyncio.sleep(0.5)

        user_message = ""
        for msg in messages:
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        if "商家" in user_message and "分析" in user_message:
            mock_content = """基于数据分析，本周期夜宵消费呈现以下趋势：

1. **趋势分析**：啤酒类商品需求预计增长30%以上，卤味零食紧随其后。建议重点备货青岛啤酒、百威啤酒和周黑鸭系列。

2. **补货优先级**：TOP3爆品补货量应增加50%，其中青岛啤酒330ml建议备货200件以上，避免高峰时段缺货。

3. **定价策略**：建议对啤酒类爆品采取微幅降价策略（5%-8%），可有效提升销量15%-20%。"""

            return {"content": mock_content}

        return {
            "content": "基于数据分析，系统建议关注热门商品的备货和定价策略。"
        }


_llm_client = None


def get_llm_client() -> LLMClient:
    """获取LLM客户端实例"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
